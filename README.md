# AI Resume Analyzer

Prepared by Ali Raza | Version 1.0

## 1. Project Overview

AI Resume Analyzer is a web application where a user uploads a CV (PDF or DOCX) and receives an instant score out of 100, a section-by-section breakdown, a keyword match against a target job description, and clear tips to improve the CV. The system combines text extraction, Natural Language Processing (NLP) and rule-based scoring to give feedback similar to an Applicant Tracking System (ATS).

## 2. Problem Statement

Most job seekers, especially fresh graduates, do not know why their CV gets rejected. Many CVs fail ATS filters because of poor formatting, missing keywords, weak descriptions or missing sections. Hiring a career consultant is expensive. This project gives every candidate free, instant and objective feedback.

## 3. Objectives

- Extract text and structure from uploaded CV files.
- Detect key sections: contact details, summary, education, experience, skills, projects.
- Calculate an overall ATS-friendliness score with a breakdown.
- Compare the CV with a job description and show matched and missing keywords.
- Suggest specific, actionable improvements.
- Store analysis history for each user.

## 4. Scope

In scope: CV upload, text extraction, scoring, keyword matching, improvement tips, user accounts, history, downloadable report.

Out of scope (future work): automatic CV rewriting, LinkedIn import, multi-language CVs, recruiter-side tools, scanned-PDF OCR.

## 5. Features

### 5.1 User features

- Sign up and login (JWT based).
- Drag-and-drop CV upload (PDF, DOCX, max 5 MB).
- Optional job description paste for targeted analysis.
- Overall score and category scores shown with charts.
- Matched and missing skills list.
- Improvement tips grouped by priority (High, Medium, Low).
- History of previous analyses and score comparison.
- Download report as PDF.

### 5.2 Admin features

- View total users and analyses.
- Manage the skills dictionary (add, edit, remove skills).
- View usage statistics.

## 6. Languages and Technologies Used

### 6.1 Programming and markup languages

| Language | Where it is used |
|---|---|
| Python | Backend, CV parsing, NLP and scoring engine |
| TypeScript | Frontend (React) and shared type definitions |
| JavaScript | Build configuration and small helper scripts |
| HTML5 | Page structure through React JSX |
| CSS3 / Tailwind CSS | Styling, layout, responsive design, dark mode |
| SQL | Database queries (PostgreSQL) |
| JSON | API requests and responses, configuration |
| Markdown | README and documentation |

### 6.2 Frameworks and libraries

| Layer | Technology |
|---|---|
| Frontend | React, Vite, React Router, Tailwind CSS, Recharts (charts), Axios |
| Backend API | FastAPI (Python), Uvicorn, Pydantic |
| File parsing | pdfplumber (PDF), python-docx (DOCX) |
| NLP | spaCy (entity and phrase extraction), NLTK (stop words, tokenizing) |
| Matching | scikit-learn (TF-IDF, cosine similarity); optional Sentence-Transformers for semantic matching |
| Database | PostgreSQL with SQLAlchemy ORM (or MongoDB as an alternative) |
| Authentication | JWT, bcrypt |
| Report generation | ReportLab or WeasyPrint (PDF export) |
| Testing | Pytest (backend), Vitest and React Testing Library (frontend) |
| Tools | Git, GitHub, Postman, VS Code, Docker |
| Deployment | Vercel (frontend), Render or Railway (backend), Neon or Supabase (database) |

## 7. System Architecture

Client-server architecture with a separate AI processing module:

1. Client (React): user uploads the CV and optional job description.
2. API (FastAPI): validates the file, authenticates the user and passes the file to the parser.
3. Parser module: extracts raw text from PDF or DOCX and cleans it.
4. NLP module: detects sections, skills, dates, education and contact details.
5. Scoring engine: applies rules and similarity measures to produce scores and tips.
6. Database (PostgreSQL): stores users, CV metadata and analysis results.
7. Response: the API returns the result as JSON and the client displays it with charts.

Flow summary: Upload, then Extract, then Analyze, then Score, then Suggest, then Display and Save.

## 8. Analysis and Scoring Logic

The overall score is out of 100 and is a weighted sum:

| Category | Weight | What is checked |
|---|---|---|
| Contact information | 10 | Email, phone, LinkedIn or GitHub link present and valid |
| Structure and sections | 20 | Presence and order of Summary, Education, Experience, Skills, Projects |
| Skills and keywords | 25 | Number and relevance of skills, match with job description |
| Experience quality | 20 | Action verbs, measurable results (numbers, percentages), clear dates |
| Formatting and ATS readability | 15 | Readable text, no tables or images hiding content, reasonable length |
| Language and grammar | 10 | Spelling, sentence length, repeated words, tone |

### 8.1 Keyword matching

1. Clean the CV text and the job description (lowercase, remove stop words).
2. Extract skills using a skills dictionary and spaCy phrase matcher.
3. Compute TF-IDF vectors and cosine similarity between CV and job description.
4. Report matched skills, missing skills and a match percentage.

### 8.2 Improvement tips

Tips are generated from rules, for example:

- No measurable result found: add numbers such as "improved load time by 40%".
- Summary section missing: add a 3 to 4 line professional summary.
- Skill from the job description is missing: add it if you have the experience.
- CV is longer than two pages: shorten it to the most relevant content.

## 9. Database Design

- **users:** id (primary key), name, email (unique), password_hash, role, created_at
- **resumes:** id (primary key), user_id (foreign key), file_name, file_type, extracted_text, uploaded_at
- **analyses:** id (primary key), resume_id (foreign key), job_description (optional), overall_score, category_scores (JSON), matched_skills (JSON), missing_skills (JSON), tips (JSON), created_at
- **skills:** id (primary key), name, category (for example Programming, Database, Soft skill)

Relationships: one user has many resumes; one resume has many analyses.

## 10. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/register | Create an account |
| POST | /api/auth/login | Login and receive a JWT |
| POST | /api/resumes/analyze | Upload CV (and optional job description) and get analysis |
| GET | /api/analyses | List the user's past analyses |
| GET | /api/analyses/{id} | Get one analysis in detail |
| GET | /api/analyses/{id}/report | Download the PDF report |
| DELETE | /api/analyses/{id} | Delete an analysis |
| GET | /api/admin/stats | Admin statistics |
| POST | /api/admin/skills | Add a skill to the dictionary |

## 11. Folder Structure

```
ai-resume-analyzer/
  frontend/
    src/
      components/   (UploadBox, ScoreCard, SkillsList, TipsList, Navbar, CategoryChart)
      pages/        (Home, Login, Register, Analyze, Result, History, Admin)
      hooks/        (useAuth, useAnalysis)
      services/     (api.ts)
      context/      (AuthContext)
  backend/
    app/
      main.py
      routers/      (auth.py, resumes.py, admin.py)
      services/     (parser.py, nlp.py, scoring.py, report.py)
      models/       (models.py)
      schemas/      (schemas.py)
      data/         (skills.json)
    tests/
  README.md
```

## 12. User Interface Pages

- Home: project introduction and Upload button.
- Login / Register: simple authentication forms.
- Analyze: drag-and-drop upload and job description box.
- Result: score gauge, category bar chart, matched and missing skills, tips list.
- History: table of past analyses with date and score.
- Admin: statistics and skills management.

## 13. Security Considerations

- Allow only PDF and DOCX files and limit the size to 5 MB.
- Hash passwords with bcrypt and protect routes with JWT.
- Validate all input with Pydantic.
- Enable CORS only for the frontend domain.
- Store files securely and allow users to delete their data.
- Use environment variables for secrets.

## 14. Testing Plan

- Unit tests: parser, scoring functions and keyword matching (Pytest).
- API tests: all endpoints using Postman and Pytest.
- UI tests: upload flow and result page (Vitest, React Testing Library).
- Sample data: at least 20 CVs of different formats to test accuracy.

## 15. Setup Guide

### Backend

1. Install Python 3.11 or later.
2. Create a virtual environment and install packages: `pip install -r backend/requirements.txt` (fastapi, uvicorn, pdfplumber, python-docx, scikit-learn, sqlalchemy, bcrypt, PyJWT).
3. Download the spaCy model if you want spaCy matching: `python -m spacy download en_core_web_sm` (see Demo notes — not required for the current build).
4. Create a `.env` file (see `backend/.env.example`) with `DATABASE_URL` and `SECRET_KEY`.
5. Run: `uvicorn app.main:app --reload` from the `backend/` folder.

### Frontend

1. Install Node.js 20 or later.
2. Run `npm install` inside the `frontend/` folder.
3. Set `VITE_API_URL` in the `.env` file (see `frontend/.env.example`).
4. Run `npm run dev` (development) or `npm run build` (production).

## 16. Deployment

- Frontend on Vercel.
- Backend on Render or Railway using a Dockerfile.
- PostgreSQL on Neon or Supabase.
- Add the live links to the README, GitHub and CV.

## 17. Development Timeline

| Week | Task |
|---|---|
| 1 | Requirements, UI design, project setup |
| 2 | CV parsing (PDF and DOCX) and text cleaning |
| 3 | NLP, section and skill detection |
| 4 | Scoring engine and tips |
| 5 | React frontend and charts |
| 6 | Authentication, history, PDF report |
| 7 | Testing and bug fixing |
| 8 | Deployment and documentation |

## 18. Limitations

- Scoring is rule-based and may not match every real ATS exactly.
- Scanned (image-only) PDFs need OCR, which is not included in version 1.
- Only English CVs are supported.

## 19. Future Improvements

- OCR support using Tesseract for scanned CVs.
- Large Language Model (LLM) feedback for rewriting weak bullet points.
- Urdu and Arabic CV support.
- Cover letter generator.
- Job recommendations based on the CV.
- Recruiter dashboard to rank multiple CVs.

## 20. Conclusion

AI Resume Analyzer solves a real problem for job seekers by giving fast, objective and actionable CV feedback. It demonstrates full-stack development (React, TypeScript, FastAPI), NLP (spaCy, scikit-learn), database design and deployment, which makes it a strong project for university evaluation, a portfolio and interviews.

---

## Demo notes (honest, read before showing this to anyone)

- **Database fallback:** PostgreSQL is used when `DATABASE_URL` is set (Neon/Supabase for production). Locally, without `DATABASE_URL`, the same SQLAlchemy models run on SQLite (`resumes.db`, gitignored). Live Postgres was NOT tested in this build.
- **spaCy fallback:** the spaCy model was NOT downloaded here (heavy download, not available in this environment), so `nlp.py` uses a documented regex/tokenizer fallback with the same outputs. TF-IDF + cosine similarity via scikit-learn DID run in tests. Do not claim spaCy ran until the model is installed.
- **Charts:** Recharts is installed in `package.json`, but the Result page currently uses simple CSS bar charts (`CategoryChart.tsx`) for reliability — visually equivalent for this demo.
- **No demo admin seeded:** no real or demo user account is created by default. Register a new account via `/register` to test; the test account used during development was a throwaway local test user, not a real person.
- **No real users or data:** do not add contact details, photos or personal data to this project.
- **Not verified:** live Postgres, live deployment (Vercel/Render), frontend Vitest/React Testing Library tests, and browser UI click-through. Backend Pytest, frontend build, and the full API smoke test below WERE verified.
