# AI Resume Analyzer - Project Notes

## Project Overview
This is an AI-based resume analyzer that provides comprehensive analysis through multiple interfaces (web, CLI, API).

## Key Technologies
- **Backend**: Flask (web), FastAPI (REST API)
- **AI/ML**: OpenAI GPT models, spaCy for NLP
- **File Processing**: PyPDF2, python-docx
- **CLI**: Click framework

## Development Notes

### Environment Setup
- Python 3.8+ required
- Virtual environment recommended
- OpenAI API key required for AI features
- spaCy model `en_core_web_sm` for advanced NLP

### File Structure
- `src/` - Core analysis modules
- `templates/` - HTML templates for web interface
- `uploads/` - Temporary file storage (gitignored)

### Key Components
1. **ResumeParser** - Handles PDF/DOCX/TXT parsing
2. **KeywordMatcher** - Keyword and phrase matching
3. **SkillsExtractor** - NLP-based skill extraction and categorization
4. **AIScorer** - OpenAI integration for scoring and ranking
5. **ResumeAnalyzer** - Main orchestration class

### API Endpoints
- Flask runs on port 5000
- FastAPI runs on port 8000
- Both provide similar functionality

### Testing
- No formal test suite currently implemented
- Manual testing through web interface and CLI
- Test with various resume formats (PDF, DOCX, TXT)

### Known Limitations
- AI features require OpenAI API key and credits
- spaCy model download required for full NLP features
- File size limited to 16MB for web uploads
- Some resume formats may not parse correctly

### Future Enhancements
- Add formal test suite
- Support more file formats (RTF, ODT)
- Add database support for storing analyses
- Implement user authentication
- Add export to multiple formats (PDF, Excel)
- Create Docker container for easy deployment
- Add more sophisticated AI models
- Implement resume templates
- Add ATS (Applicant Tracking System) compatibility checks

### Build/Run Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run web interface
python app.py

# Run API server
python -m uvicorn api:app --reload

# Run CLI
python cli.py --help
```

### Environment Variables
- `OPENAI_API_KEY` - Required for AI features
- Set in `.env` file in project root

### Debugging
- Flask runs in debug mode by default
- FastAPI runs with --reload flag for development
- Check console output for parsing errors
- Verify file permissions for upload directory
