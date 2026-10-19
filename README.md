# AI-Based Resume Analyzer

A comprehensive AI-powered resume analysis system that parses resumes, extracts skills, matches keywords, and provides AI-based scoring and ranking.

## Features

- **Resume Parsing**: Extract text from PDF and Word documents
- **Keyword Matching**: Match resume keywords against job descriptions
- **Skills Extraction**: Identify and extract skills from resumes using NLP
- **AI Scoring/Ranking**: Use OpenAI API to score and rank resumes
- **Local Scoring/Ranking**: Parse, keyword-match, calculate TF-IDF similarity, score, and rank resumes without an LLM or API charges
- **Multiple Interfaces**: Web application, CLI tool, and REST API
- **Batch Processing**: Analyze multiple resumes at once
- **Improvement Suggestions**: Get AI-powered tips to improve your resume
- **Fact-grounded Bullet Rewrites**: Tailor resume bullets to a job description without adding unsupported claims
- **Cover Letter Drafts**: Generate with AI when configured, or use a resume-grounded local template without an API key

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Download spaCy model (for advanced NLP features):
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Web Application (Flask)
```bash
python app.py
```
Visit http://localhost:5000 to access the web interface.

The web interface provides:
- Single resume analysis with file upload
- Batch analysis for multiple resumes
- Text-based analysis (paste resume text directly)
- AI-powered improvement suggestions
- Job-tailored resume bullet rewrites with original text shown for review
- Cover letter generation, with a clearly labeled local template fallback when AI is not configured
- A site-wide analysis mode selector. Local mode is selected by default and does not call an LLM for analysis/ranking; AI-assisted mode explicitly opts into OpenAI API usage.

In local mode, resume fit scores combine keyword overlap with TF-IDF cosine similarity, and include target-skill overlap when target skills are available. AI-authored bullet rewrites, interview chat, career paths, and salary estimates remain unavailable in local mode; cover letters use a resume-grounded local template and improvement suggestions use rule-based guidance.

The FastAPI `POST /api/analyze`, `/api/batch`, `/api/analyze-text`, and `/api/improve` endpoints accept an optional `analysis_mode` form field (`local` or `ai`). The default is `ai` for API compatibility. Send `analysis_mode=local` to disable paid-model calls; `/api/rewrite-bullets` and `/api/compare` return an unavailable response in that mode.

### CLI Tool

#### Analyze a single resume:
```bash
python cli.py analyze --resume path/to/resume.pdf --job-description "Senior Python Developer position" --required-skills "Python, Django, AWS, PostgreSQL"
```

#### Batch analyze resumes in a directory:
```bash
python cli.py batch --directory ./resumes --job-description "Data Scientist role" --extension pdf
```

#### Get improvement suggestions:
```bash
python cli.py improve --resume path/to/resume.pdf --job-description "Target job description"
```

#### Compare two resumes:
```bash
python cli.py compare --resume1 resume1.pdf --resume2 resume2.pdf --job-description "Job description"
```

#### Analyze resume text directly:
```bash
python cli.py analyze-text --text "Your resume text here" --job-description "Job description"
```

### REST API (FastAPI)

Start the API server:
```bash
python -m uvicorn api:app --reload
```

API endpoints:
- `POST /api/analyze` - Analyze a single resume
- `POST /api/batch` - Batch analyze multiple resumes
- `POST /api/improve` - Get AI-powered improvement suggestions
- `POST /api/rewrite-bullets` - Rewrite supported resume bullets for a target job
- `POST /api/compare` - Compare two resumes
- `POST /api/analyze-text` - Analyze resume text directly
- `GET /api/health` - Health check

#### Example API usage with curl:

**Analyze a resume:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@resume.pdf" \
  -F "job_description=Senior Python Developer" \
  -F "required_skills=Python,Django,AWS"
```

**Batch analyze:**
```bash
curl -X POST "http://localhost:8000/api/batch" \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.pdf" \
  -F "job_description=Data Scientist"
```

**Get improvement suggestions:**
```bash
curl -X POST "http://localhost:8000/api/improve" \
  -F "file=@resume.pdf" \
  -F "job_description=Target job description"
```

**Rewrite resume bullets for a job:**
```bash
curl -X POST "http://localhost:8000/api/rewrite-bullets" \
  -F "file=@resume.pdf" \
  -F "job_description=Target job description"
```

## Project Structure

```
.
├── app.py                 # Flask web application
├── api.py                 # FastAPI REST API
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md             # This file
├── src/
│   ├── __init__.py
│   ├── parser.py         # Resume parsing (PDF/Word)
│   ├── keyword_matcher.py # Keyword matching
│   ├── skills_extractor.py # Skills extraction using NLP
│   ├── ai_scorer.py      # OpenAI-based scoring and optional AI features
│   ├── local_scorer.py   # Local TF-IDF and deterministic scoring
│   └── analyzer.py       # Main analyzer orchestration
├── templates/
│   └── index.html        # Web interface
└── uploads/              # Temporary upload directory
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Supported File Formats

- PDF (`.pdf`)
- Word documents (`.docx`, `.doc`)
- Plain text (`.txt`)

## Features in Detail

### Resume Parsing
- Extracts text from PDF and Word documents
- Handles uploaded files and local file paths
- Supports batch processing

### Keyword Matching
- Extracts keywords from resumes and job descriptions
- Calculates match scores (keyword and phrase matching)
- Identifies missing keywords
- Provides frequency analysis

### Skills Extraction
- Uses NLP (spaCy) for intelligent skill extraction
- Categorizes skills (Programming, Web, Cloud, Data, etc.)
- Matches against comprehensive skill database
- Compares with required skills

### Scoring and Ranking
- Uses OpenAI GPT models for intelligent analysis
- Provides overall scores (0-100)
- Generates strengths and weaknesses
- Offers recommendations (Strong Recommend, Recommend, Consider, Do Not Recommend)
- Includes detailed summaries
- Local mode computes a deterministic score from keyword overlap and TF-IDF similarity, plus required-skill overlap where available; batch candidates are ranked by this score without sending resume text to an LLM.

### Batch Processing
- Analyze multiple resumes simultaneously
- AI-powered ranking of candidates
- Comparative analysis across applicants
- Export results to JSON

## Example Output

The analyzer provides comprehensive results including:

```json
{
  "skills_analysis": {
    "all_skills": ["Python", "Django", "AWS", "PostgreSQL"],
    "categorized": {
      "Programming Languages": ["Python"],
      "Web Technologies": ["Django"],
      "Cloud & DevOps": ["AWS"]
    },
    "skill_count": 4
  },
  "keyword_matching": {
    "combined_score": 85.5,
    "matched_keywords": ["python", "django", "aws"],
    "missing_keywords": ["kubernetes"]
  },
  "ai_analysis": {
    "overall_score": 87,
    "recommendation": "Recommend",
    "strengths": ["Strong technical background", "Relevant experience"],
    "summary": "Strong candidate with good technical skills"
  },
  "overall_assessment": {
    "recommendation": "Recommend",
    "confidence_score": 87,
    "strengths": ["Excellent keyword match (85.5%)"],
    "weaknesses": ["Missing some cloud skills"]
  }
}
```

## Troubleshooting

### spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### OpenAI API errors
- Ensure your API key is correctly set in `.env`
- Check your OpenAI account has available credits
- Verify the API key has the necessary permissions

### File parsing errors
- Ensure files are not corrupted
- Check that file formats are supported
- Verify file permissions

## Requirements

- Python 3.8+
- OpenAI API key (only for AI-assisted features)
- Internet connection (only for OpenAI API features)

## License

This project is provided as-is for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
