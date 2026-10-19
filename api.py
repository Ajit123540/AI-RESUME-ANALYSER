from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import os
import shutil
from datetime import datetime

from src.analyzer import ResumeAnalyzer

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = ResumeAnalyzer(use_ai=True)

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Resume Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/analyze": "Analyze a single resume",
            "POST /api/batch": "Analyze multiple resumes",
            "POST /api/improve": "Get improvement suggestions",
            "POST /api/rewrite-bullets": "Rewrite supported resume bullets for a target job",
            "POST /api/compare": "Compare two resumes",
            "GET /api/health": "Health check"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_enabled": analyzer.use_ai
    }


@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(""),
    required_skills: Optional[str] = Form(""),
    analysis_mode: str = Form("ai")
):
    """
    Analyze a single resume file.
    
    - **file**: Resume file (PDF, DOCX, or TXT)
    - **job_description**: Optional job description for matching
    - **required_skills**: Optional comma-separated list of required skills
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        # Read file content
        file_content = await file.read()
        
        # Parse required skills if provided
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(",")]
        
        # Analyze the resume
        result = analyzer.analyze_uploaded_file(
            file_content,
            file.filename,
            job_description,
            skills_list,
            analysis_mode
        )
        
        if not result.get('parse_success'):
            raise HTTPException(status_code=400, detail=result.get('error'))
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch")
async def batch_analyze(
    files: List[UploadFile] = File(...),
    job_description: str = Form(""),
    required_skills: Optional[str] = Form(""),
    analysis_mode: str = Form("ai")
):
    """
    Analyze multiple resume files.
    
    - **files**: Multiple resume files (PDF, DOCX, or TXT)
    - **job_description**: Optional job description for matching
    - **required_skills**: Optional comma-separated list of required skills
    """
    try:
        # Save uploaded files temporarily
        file_paths = []
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)
        
        # Parse required skills if provided
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(",")]
        
        # Batch analyze
        results = analyzer.batch_analyze(
            file_paths, job_description, skills_list, analysis_mode
        )
        
        # Clean up temporary files
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return JSONResponse(content={
            "total_files": len(files),
            "successful_analyses": sum(1 for r in results if r.get('parse_success')),
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/improve")
async def get_improvement_suggestions(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    analysis_mode: str = Form("ai")
):
    """
    Get AI-powered improvement suggestions for a resume.
    
    - **file**: Resume file (PDF, DOCX, or TXT)
    - **job_description**: Job description for comparison
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Parse resume
        resume_text = analyzer.parser.parse_uploaded_file(file_content, file.filename)
        
        # Get improvement suggestions
        suggestions = analyzer.get_improvement_suggestions(
            resume_text, job_description, analysis_mode
        )
        
        return JSONResponse(content=suggestions)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rewrite-bullets")
async def rewrite_resume_bullets(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    analysis_mode: str = Form("ai")
):
    """Rewrite resume bullets for a target job using only resume-supported facts."""
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No file selected")

    allowed_extensions = {".pdf", ".docx", ".doc", ".txt"}
    extension = os.path.splitext(filename)[1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: pdf, docx, doc, txt"
        )
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")
    if analysis_mode != "ai":
        raise HTTPException(
            status_code=503,
            detail="Resume bullet rewrites require an AI model and are unavailable in local mode."
        )

    try:
        file_content = await file.read()
        resume_text = analyzer.parser.parse_uploaded_file(file_content, filename)
        result = analyzer.ai_scorer.rewrite_resume_bullets(resume_text, job_description)
        if result.get("error"):
            raise HTTPException(status_code=503, detail=result["error"])
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare")
async def compare_resumes(
    resume1: UploadFile = File(...),
    resume2: UploadFile = File(...),
    job_description: str = Form(...),
    analysis_mode: str = Form("ai")
):
    """
    Compare two resumes using AI.
    
    - **resume1**: First resume file
    - **resume2**: Second resume file
    - **job_description**: Job description for comparison
    """
    try:
        if analysis_mode != "ai":
            raise HTTPException(
                status_code=503,
                detail="AI resume comparison is unavailable in local mode. Use batch ranking for local comparisons."
            )
        if not analyzer.use_ai:
            raise HTTPException(
                status_code=400,
                detail="AI features not enabled. Set OPENAI_API_KEY environment variable."
            )
        
        # Save files temporarily
        resume1_path = os.path.join(UPLOAD_DIR, resume1.filename)
        resume2_path = os.path.join(UPLOAD_DIR, resume2.filename)
        
        with open(resume1_path, "wb") as buffer:
            shutil.copyfileobj(resume1.file, buffer)
        with open(resume2_path, "wb") as buffer:
            shutil.copyfileobj(resume2.file, buffer)
        
        # Compare resumes
        comparison = analyzer.compare_resumes(resume1_path, resume2_path, job_description)
        
        # Clean up
        for path in [resume1_path, resume2_path]:
            if os.path.exists(path):
                os.remove(path)
        
        return JSONResponse(content=comparison)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-text")
async def analyze_text(
    resume_text: str = Form(...),
    job_description: str = Form(""),
    required_skills: Optional[str] = Form(""),
    analysis_mode: str = Form("ai")
):
    """
    Analyze resume text directly (without file upload).
    
    - **resume_text**: Resume text content
    - **job_description**: Optional job description for matching
    - **required_skills**: Optional comma-separated list of required skills
    """
    try:
        # Parse required skills if provided
        skills_list = None
        if required_skills:
            skills_list = [skill.strip() for skill in required_skills.split(",")]
        
        # Analyze the resume text
        result = analyzer.analyze_resume(
            resume_text, job_description, skills_list, analysis_mode
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
