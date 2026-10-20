"""PubMed에서 연구소 논문 목록을 받아 _data/publications.json 으로 저장합니다.

검색 조건은 아래 SEARCH_TERM 과 YEARS 를 고치면 됩니다.
PubMed 검색은 저자 소속을 논문 전체에서 찾기 때문에, 서로 다른 저자의 소속이
섞여 걸리는 경우가 있습니다. 그래서 받아온 뒤 '한 저자의 소속 한 줄' 안에
REQUIRED 의 단어가 모두 들어 있는 논문만 남깁니다.
"""
import datetime
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SEARCH_TERM = '("Korea University"[Affiliation]) AND ("Department of Biochemistry and Molecular Biology"[Affiliation])'
YEARS = 5
REQUIRED = ["korea university", "biochemistry and molecular biology"]
EXCLUDE_FILE = ".github/pubmed_exclude.txt"   # 빼고 싶은 PMID를 한 줄에 하나씩
OUT = "_data/publications.json"

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = {"tool": "imm-korea-homepage", "email": "yyb77@korea.ac.kr"}
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def call(endpoint, params):
    data = urllib.parse.urlencode({**params, **TOOL}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(BASE + endpoint, data=data)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # 일시적 오류는 재시도
            print("retry", endpoint, e)
            time.sleep(2 + attempt * 3)
    raise RuntimeError("PubMed request failed: " + endpoint)


def text(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""


def norm(s):
    return s.lower().replace("&", "and")


def parse_date(art):
    y, m, d = 0, 0, 0
    ad = art.find(".//Article/ArticleDate")
    pd = art.find(".//Article/Journal/JournalIssue/PubDate")
    src = ad if ad is not None else pd
    if src is not None:
        y = src.findtext("Year") or ""
        if not y:
            md = src.findtext("MedlineDate") or ""
            y = md[:4]
        mo = (src.findtext("Month") or "").strip().lower()
        m = int(mo) if mo.isdigit() else MONTHS.get(mo[:3], 0)
        dd = src.findtext("Day") or "0"
        d = int(dd) if dd.isdigit() else 0
    try:
        y = int(y)
    except ValueError:
        y = 0
    return y, m, d


def main():
    today = datetime.date.today()
    start = today.replace(year=today.year - YEARS)
    res = json.loads(call("esearch.fcgi", {
        "db": "pubmed", "term": SEARCH_TERM, "retmode": "json", "retmax": 10000,
        "datetype": "pdat", "mindate": start.strftime("%Y/%m/%d"), "maxdate": "3000",
    }))
    ids = res["esearchresult"]["idlist"]
    print("esearch hits:", len(ids))

    exclude = set()
    if os.path.exists(EXCLUDE_FILE):
        exclude = {l.strip() for l in open(EXCLUDE_FILE) if l.strip() and not l.startswith("#")}

    items = []
    for i in range(0, len(ids), 200):
        chunk = ids[i:i + 200]
        root = ET.fromstring(call("efetch.fcgi", {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"}))
        for art in root.findall("PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID")
            if pmid in exclude:
                continue
            authors, lab_hit = [], False
            for a in art.findall(".//Article/AuthorList/Author"):
                affs = [norm(text(x)) for x in a.findall("AffiliationInfo/Affiliation")]
                mine = any(all(k in aff for k in REQUIRED) for aff in affs)
                lab_hit = lab_hit or mine
                name = (a.findtext("LastName") or "") + (" " + a.findtext("Initials") if a.findtext("Initials") else "")
                if not name.strip():
                    name = a.findtext("CollectiveName") or ""
                if name.strip():
                    authors.append({"n": name.strip(), "m": mine})
            if not lab_hit:
                continue
            y, m, d = parse_date(art)
            doi = ""
            for aid in art.findall(".//PubmedData/ArticleIdList/ArticleId"):
                if aid.get("IdType") == "doi":
                    doi = (aid.text or "").strip()
            journal = art.findtext(".//Article/Journal/ISOAbbreviation") or art.findtext(".//Article/Journal/Title") or ""
            items.append({
                "pmid": pmid,
                "title": text(art.find(".//Article/ArticleTitle")).rstrip("."),
                "journal": journal,
                "year": y,
                "sort": "%04d%02d%02d" % (y, m, d),
                "doi": doi,
                "authors": authors,
            })
        time.sleep(0.5)

    items.sort(key=lambda x: x["sort"], reverse=True)
    out = {
        "updated": today.isoformat(),
        "from_year": start.year,
        "count": len(items),
        "items": items,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("saved", len(items), "papers")


if __name__ == "__main__":
    main()
