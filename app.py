from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from datetime import datetime

from src.analyzer import ResumeAnalyzer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize analyzer
analyzer = ResumeAnalyzer(use_ai=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main web interface."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login page."""
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Render the signup page."""
    return render_template('signup.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze a single resume file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: pdf, docx, doc, txt'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Get form data
                job_description = request.form.get('job_description', '')
                required_skills_str = request.form.get('required_skills', '')
                required_skills = [s.strip() for s in required_skills_str.split(',')] if required_skills_str else None
                
                # Analyze the resume
                analysis_mode = request.form.get('analysis_mode', 'ai')
                result = analyzer.analyze_file(
                    filepath, job_description, required_skills, analysis_mode
                )
                
                # Clean up
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                return jsonify(result)
                
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    """Analyze multiple resume files."""
    try:
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files provided'}), 400
        
        # Filter valid files
        valid_files = [f for f in files if f.filename and allowed_file(f.filename)]
        if not valid_files:
            return jsonify({'error': 'No valid files provided'}), 400
        
        # Save files temporarily
        file_paths = []
        for file in valid_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_paths.append(filepath)
        
        try:
            # Get form data
            job_description = request.form.get('job_description', '')
            required_skills_str = request.form.get('required_skills', '')
            required_skills = [s.strip() for s in required_skills_str.split(',')] if required_skills_str else None
            
            # Batch analyze
            analysis_mode = request.form.get('analysis_mode', 'ai')
            results = analyzer.batch_analyze(
                file_paths, job_description, required_skills, analysis_mode
            )
            
            # Clean up
            for filepath in file_paths:
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            return jsonify({
                'total_files': len(valid_files),
                'successful_analyses': sum(1 for r in results if r.get('parse_success')),
                'results': results
            })
            
        except Exception as e:
            # Clean up on error
            for filepath in file_paths:
                if os.path.exists(filepath):
                    os.remove(filepath)
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/improve', methods=['POST'])
def get_improvement_suggestions():
    """Get improvement suggestions (AI-powered or rule-based)."""
    try:
        # Allow suggestions even without AI - will use rule-based fallback
        if not analyzer.ai_scorer:
            return jsonify({'error': 'AI scorer not initialized'}), 500
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        job_description = request.form.get('job_description', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Parse resume
                resume_text = analyzer.parser.parse_file(filepath)
                
                # Get suggestions
                analysis_mode = request.form.get('analysis_mode', 'ai')
                suggestions = analyzer.get_improvement_suggestions(
                    resume_text, job_description, analysis_mode
                )
                
                # Clean up
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                return jsonify(suggestions)
                
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rewrite-bullets', methods=['POST'])
def rewrite_resume_bullets():
    """Rewrite supported resume statements to better fit a target job."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: pdf, docx, doc, txt'}), 400

    job_description = request.form.get('job_description', '').strip()
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400

    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1]
    filepath = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=app.config['UPLOAD_FOLDER'],
            prefix='resume-rewrite-',
            suffix=extension,
            delete=False
        ) as temp_file:
            filepath = temp_file.name

        file.save(filepath)
        resume_text = analyzer.parser.parse_file(filepath)
        analysis_mode = request.form.get('analysis_mode', 'ai')
        result = analyzer.ai_scorer.rewrite_resume_bullets(
            resume_text, job_description, use_ai=(analysis_mode == 'ai')
        )
        if result.get('error') and not result.get('rewrites'):
            return jsonify(result), 500
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze resume text directly."""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        required_skills = data.get('required_skills', [])
        
        if isinstance(required_skills, str):
            required_skills = [s.strip() for s in required_skills.split(',') if s.strip()]
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        result = analyzer.analyze_resume(
            resume_text, job_description, required_skills,
            (request.get_json() or {}).get('analysis_mode', 'ai')
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intelligence/fairness-audit', methods=['POST'])
def fairness_audit():
    """Audit screening model fairness across demographic variations."""
    try:
        data = request.get_json() or {}
        resume_text = data.get('resume_text', '')
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        from src.intelligence.fairness_audit import FairnessAuditor
        def dummy_score(txt):
            return 84.0
        
        audit_result = FairnessAuditor.audit_fairness(resume_text, dummy_score)
        return jsonify(audit_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intelligence/recruiter-sim', methods=['POST'])
def recruiter_simulation():
    """Simulate evaluation across 3 recruiter lenses."""
    try:
        data = request.get_json() or {}
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
            
        analysis = analyzer.analyze_resume(
            resume_text, job_description,
            analysis_mode=data.get('analysis_mode', 'ai')
        )
        platform_data = analysis.get('intelligence_platform', {})
        return jsonify(platform_data.get('recruiter_simulations', {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intelligence/version-compare', methods=['POST'])
def compare_resume_versions():
    """Compare two versions of a candidate's resume."""
    try:
        data = request.get_json() or {}
        v1_text = data.get('version1_text', '')
        v2_text = data.get('version2_text', '')
        label1 = data.get('label1', 'Version 1')
        label2 = data.get('label2', 'Version 2')
        
        if not v1_text or not v2_text:
            return jsonify({'error': 'Both version1_text and version2_text are required'}), 400
            
        from src.intelligence.version_compare import VersionIntelligence
        diff_result = VersionIntelligence.compare_versions(v1_text, v2_text, label1, label2)
        return jsonify(diff_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_enabled': analyzer.use_ai,
        'platform_version': '3.0-SaaS-Intelligence'
    })


@app.route('/api/cover-letter', methods=['POST'])
def cover_letter():
    """Generate a cover letter based on resume and job description."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        job_description = request.form.get('job_description', '')
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resume_text = analyzer.parser.parse_file(filepath)
            os.remove(filepath)
            analysis_mode = request.form.get('analysis_mode', 'ai')
            result = analyzer.ai_scorer.generate_cover_letter(
                resume_text, job_description, use_ai=analysis_mode == 'ai'
            )
            return jsonify(result)
        return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview-chat', methods=['POST'])
def interview_chat():
    """Mock interview chat endpoint."""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        history = data.get('history', [])
        
        if not resume_text:
            return jsonify({'error': 'Resume text required'}), 400
        use_ai = (data.get('analysis_mode', 'ai') == 'ai')
        result = analyzer.ai_scorer.mock_interview_response(
            resume_text, job_description, history, use_ai=use_ai
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/assistant-chat', methods=['POST'])
def assistant_chat():
    """AI Copilot / Assistant chat endpoint supporting local mode and AI mode."""
    try:
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        history = data.get('history', [])
        resume_context = data.get('resume_context', '')
        analysis_mode = data.get('analysis_mode', 'local')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        use_ai = (analysis_mode == 'ai')
        result = analyzer.ai_scorer.assistant_chat_response(
            message=message,
            conversation_history=history,
            resume_context=resume_context,
            use_ai=use_ai
        )
        result['mode'] = 'local' if result.get('generation_mode') != 'ai_assistant' else 'ai'
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ats-simulator', methods=['POST'])
def ats_simulator():
    """Simulate ATS raw parsing."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resume_text = analyzer.parser.parse_file(filepath)
            os.remove(filepath)
            return jsonify({"raw_text": resume_text})
        return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/career-paths', methods=['POST'])
def career_paths():
    """Generate AI career path recommendations."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        job_description = request.form.get('job_description', '')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resume_text = analyzer.parser.parse_file(filepath)
            os.remove(filepath)
            analysis_mode = request.form.get('analysis_mode', 'ai')
            result = analyzer.ai_scorer.career_path_recommendations(
                resume_text, job_description, use_ai=(analysis_mode == 'ai')
            )
            return jsonify(result)
        return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/salary-estimate', methods=['POST'])
def salary_estimate():
    """Estimate salary based on resume and job description."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        job_description = request.form.get('job_description', '')

        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resume_text = analyzer.parser.parse_file(filepath)
            os.remove(filepath)
            analysis_mode = request.form.get('analysis_mode', 'ai')
            result = analyzer.ai_scorer.salary_estimate(
                resume_text, job_description, use_ai=(analysis_mode == 'ai')
            )
            return jsonify(result)
        return jsonify({'error': 'Invalid file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/github-verify', methods=['POST'])
def github_verify():
    """Verify candidate code evidence by cross-referencing public GitHub repositories."""
    try:
        # Support JSON payload or Form data (with optional file upload)
        if request.is_json:
            data = request.get_json() or {}
            username = data.get('username', '').strip()
            resume_text = data.get('resume_text', '').strip()
        else:
            username = request.form.get('username', '').strip()
            resume_text = request.form.get('resume_text', '').strip()
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    resume_text = analyzer.parser.parse_file(filepath)
                    os.remove(filepath)

        if not username:
            return jsonify({'error': 'GitHub username or profile URL is required'}), 400

        result = analyzer.verify_github_evidence(username, resume_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ats-rebuild-resume', methods=['POST'])
def ats_rebuild_resume():
    """Audit resume errors and rebuild a complete, 100% ATS-friendly resume."""
    try:
        if request.is_json:
            data = request.get_json() or {}
            resume_text = data.get('resume_text', '').strip()
            job_description = data.get('job_description', '').strip()
            analysis_mode = data.get('analysis_mode', 'local')
        else:
            resume_text = request.form.get('resume_text', '').strip()
            job_description = request.form.get('job_description', '').strip()
            analysis_mode = request.form.get('analysis_mode', 'local')
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    resume_text = analyzer.parser.parse_file(filepath)
                    os.remove(filepath)

        if not resume_text:
            return jsonify({'error': 'Resume text or file is required'}), 400

        use_ai = (analysis_mode == 'ai')
        result = analyzer.rebuild_ats_friendly_resume(
            resume_text=resume_text,
            job_description=job_description,
            use_ai=use_ai
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


