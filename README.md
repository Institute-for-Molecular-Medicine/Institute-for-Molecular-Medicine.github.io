# 고려대학교 분자의학연구소 홈페이지

GitHub Pages(Jekyll)로 운영하는 정적 홈페이지입니다. 별도 서버가 필요 없습니다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `_config.yml` | 연구소명, 영문명, 주소, 전화, 이메일 (전체 사이트에 반영) |
| `_data/nav.yml` | 상단 메뉴 |
| `_data/quicklinks.yml` | 메인 QUICK MENU 링크 |
| `_notices/` | 공지사항 게시물 (파일 1개 = 글 1개) |
| `_seminars/` | 연구소 일정 (세미나) 게시물 |
| `about/`, `research/` | 소개, 연구업적 페이지 |
| `assets/img/` | 로고, 메인 이미지, 소장 사진 |
| `assets/uploads/` | 게시물 첨부파일, 포스터 |
| `.pages.yml` | Pages CMS 관리자 화면 설정 |

## 게시물 올리기

### 방법 A: Pages CMS (추천)

1. https://app.pagescms.org 에서 GitHub 계정으로 로그인합니다.
2. 연구소 저장소를 선택하면 `공지사항`, `연구소 일정` 메뉴가 나타납니다.
3. `Add an entry` 로 제목, 날짜, 본문을 입력하고 저장하면 1~2분 뒤 홈페이지에 반영됩니다.
4. 직원 계정은 GitHub Organization에 멤버로 초대하면 같은 방식으로 쓸 수 있습니다.

### 방법 B: GitHub 웹에서 직접

`_notices/` 폴더에서 Add file > Create new file 을 눌러 아래 형식으로 저장합니다.
파일명은 `2026-10-05-notice-xxx.md` 처럼 날짜로 시작해야 합니다 (영문, 숫자, 하이픈 권장).

```markdown
---
title: 2027년 연구원 모집 안내
date: 2026-10-05
---
본문을 여기에 씁니다.
```

세미나는 `_seminars/` 에 아래 형식으로 씁니다.

```markdown
---
title: "연구소 초청 세미나 (11월 3일) 홍길동 교수"
date: 2026-10-20
event_date: 2026-11-03
time: 오후 5시
speaker: 홍길동 교수
affiliation: OO대학교 의과대학
venue: 문숙의학관 3층 세미나실
attachment: /assets/uploads/poster.pdf
---
세미나 내용을 적습니다.
```

글을 지우려면 해당 파일을 삭제하면 됩니다.

## 학교 도메인 연결

1. 학교 전산팀에 아래 레코드를 요청합니다.
   - CNAME: `<연구소 도메인>` 을 `institute-of-molecular-medicine-at-ku.github.io` 로
   - TXT: GitHub Organization Settings > Pages > Verified domains 에서 안내하는 값
   - CAA 레코드가 있다면 `letsencrypt.org` 허용
2. 저장소 Settings > Pages > Custom domain에 도메인 입력
3. `_config.yml` 의 `url` 에 `https://<연구소 도메인>` 을 적고, 정식 공개 시 `noindex` 를 `false` 로 바꿉니다.
4. 인증서가 발급되면 Enforce HTTPS를 켭니다.

## 교체가 필요한 항목

- `assets/img/logo.svg`, `logo-white.svg`: 임시 로고입니다. 학교 CI 규정에 따라 공식 엠블럼으로 교체하세요.
- `assets/img/hero1~3.svg`: 메인 이미지. 사진(jpg)을 넣고 `index.html` 의 파일명을 바꾸면 됩니다.
- `assets/img/director.svg`: 소장 사진. `director.jpg` 로 넣고 `about/greeting.md` 의 경로를 바꾸세요.
- `about/intro.md` 의 조직도와 내규, `about/history.md` 의 역대 소장 재임 기간은 확인 후 수정이 필요합니다.
