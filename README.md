# Project Charter: SnapFridge

| Field | Details |
|---|---|
| Course | ISE304E – Software Engineering (2026–2027 Fall) |
| Group | SnapFridge – Group 2 |
| Customer / Instructor | Res. Asst. Dr. Abdullah Cihan AK |
| Repository | https://github.com/iemiral-spec/SnapFridge |
| Document version / date | 2.0 – 2026-11-03 |

## 1. Project Description

SnapFridge is a web application that helps users decide what to cook with the ingredients they already have. The user uploads a photo of their fridge or kitchen counter, an AI vision service marks the ingredients it recognizes on a list of common ingredients, the user corrects the selection or picks ingredients manually, and the system suggests recipes from a recipe database. The domain is food and lifestyle; the main users are students, employees and home cooks.

## 2. Objectives and Outcomes

**Objectives**

- Turn a fridge photo into an editable ingredient list in under 30 seconds.
- Suggest recipes ranked by how many of their ingredients the user already has, and show the missing ones.
- Deliver a cloud-hosted, tested web application that meets the course's technical requirements.

**Outcomes (in scope)**

- Registration, login and role-based authorization (User / Admin)
- Photo upload and AI-based ingredient recognition: one AI call per photo, results split into "sure" and "not sure"
- Ingredient selection screen with about 50 common ingredients and a search box; works with or without a photo
- Recipe dataset (TheMealDB; Kaggle as fallback) imported into PostgreSQL
- Ingredient-based recipe suggestions with recipe details and missing ingredients
- Favorite recipes
- Admin recipe management (add, edit, delete)

**Optional (only if core work is finished):** analysis history, recipe categories, keyword search, AI-generated recipes.

**Out of scope:** native mobile app, grocery ordering or payment, social features, calorie/diet tracking, training our own AI model.

**Technology:** Python FastAPI (REST API), PostgreSQL, JWT authentication, React + Tailwind CSS, Render (cloud hosting), GitHub Actions (CI), a vision-capable LLM API. AI coding assistants (Claude Code / GitHub Copilot) may be used; their work, effort, human review effort and the errors they introduce will be reported.

## 3. Project Manager and Staff

| Member | Student ID | Role |
|---|---|---|
| Biray Dağlı | 150210215 | Project Manager + Backend Developer |
| Ahmet İlker Yıldızlı | 150210211 | Configuration Manager + Frontend Developer |
| Umut Uğurlu | 150230213 | Test Manager + Backend Developer |
| Talha Arpacık | 150220213 | Documentation Lead + AI Integration Developer |
| İdil Emiral | 150230223 | Communication Lead + Database Developer |

## 4. Summary Milestone Schedule

Dates follow the course's 13-week project outline (Wednesday classes, no class on 18 November). Report deadlines are 23:59 on the date shown; the exact time of each submission should be checked on Ninova.

| Week | Date (2026) | Deliverable | Customer meeting / peer scoring |
|---|---|---|---|
| 3 | 13 Oct | Project Charter | – |
| 4 | 21 Oct | – | Meeting 1 on Project Plan |
| 5 | 28 Oct | Project Plan (submitted 3 Nov) | – |
| 6 | 4 Nov | – | Meeting 2 on Requirements |
| 7 | 10 Nov | Requirements Specification Report | Peer Scoring 1 (11 Nov) |
| 8 | 24 Nov | Requirements Analysis Report | Midterm (25 Nov) |
| 9 | 2 Dec | – | Peer Scoring 2 |
| 10 | 8 Dec | Software Design Report | Meeting 3 on Design (9 Dec) |
| 12 | 22 Dec | Software Test Report, Code Freeze | Meeting 4 on Tests (23 Dec) |
| – | 27 Dec | Codebase | – |
| 13 | 30 Dec, 12:30 | Final Demo and Presentation | Peer Scoring 3 |

## 5. Preliminary Cost Estimation

- **Effort:** about 170 person-hours of development work (5 members × ~10 hours/week over 9 weeks for project activities), plus time for reports and meetings.
- **Money:** no budget. We use free tiers and student offers: GitHub (Student Pack), Render free tier, PostgreSQL on Render, TheMealDB. The vision API is pay-per-use; we will pick a provider with a free tier or student credits and limit calls during development.

## 6. Preliminary Risks

| Risk | Impact | Response |
|---|---|---|
| AI recognizes ingredients wrongly | Wrong recipe suggestions | AI chooses only from the common list; uncertain items shown separately; user always confirms |
| Vision API cost, quota or downtime | Main flow stops | One call per photo; users can still pick ingredients from the list without the AI |
| Recipe dataset licence or coverage is not adequate | Few or no matches | Switch to a Kaggle dataset or a smaller hand-picked set |
| Exams and other courses slow the team | Missed deadlines | Small core scope, weekly check-in, optional features dropped first |
| Scope grows after customer meetings | Schedule slips | New requests go to the optional list unless the customer approves a trade-off |
| Free hosting limits (sleep, storage) | Demo problems | Rehearse deployment early; keep a recorded demo as backup |
