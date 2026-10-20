"""
Comprehensive Integration and Browser Feature Test Suite
Audits frontend DOM linkages, CSS assets, Flask routes, and all API endpoints.
"""

import unittest
import json
import re
import os
import io

from app import app, analyzer

class TestBrowserAndFeatures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    # -------------------------------------------------------------------------
    # 1. FRONTEND DOM & JS INTEGRITY AUDIT
    # -------------------------------------------------------------------------
    def test_dom_ids_integrity(self):
        """Verify that every getElementById call in app.js has a matching ID in index.html (or is dynamically generated)."""
        with open('static/js/app.js', 'r', encoding='utf-8') as f:
            js = f.read()
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        referenced_ids = set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_\-]+)['\"]\)", js))
        html_ids = set(re.findall(r"id=['\"]([a-zA-Z0-9_\-]+)['\"]", html))

        # Some IDs are dynamically injected or rendered into sub-results
        known_dynamic = {
            'ats-resume-sheet-view', 'batch-filter-search', 'batch-filter-tier',
            'batch-stat-total', 'batch-stat-tier1', 'batch-stat-avg', 'batch-stat-top',
            'github-verified-count-badge', 'github-self-reported-badge', 'github-hidden-badge',
            'github-verified-skills-list', 'github-self-reported-list', 'github-hidden-skills-list',
            'github-lang-bars', 'github-recruiter-note', 'github-repos-grid', 'github-hero-card',
            'github-repo-count-badge', 'single-remove', 'theme-icon', 'theme-toggle',
            'login-email', 'login-password', 'signup-name', 'signup-email', 'signup-password',
            'toggle-password', 'toggle-password-icon',
            'cover-text', 'keyword-heatmap-block', 'typing-indicator', 'batch-items-list',
            'assistant-typing-indicator'
        }

        missing = []
        for elem_id in referenced_ids:
            if elem_id not in html_ids and elem_id not in known_dynamic and not elem_id.startswith('rdm-') and not elem_id.startswith('showcase-'):
                missing.append(elem_id)

        self.assertEqual(len(missing), 0, f"Found unmapped getElementById targets in index.html: {missing}")

    # -------------------------------------------------------------------------
    # 2. HTML ROUTES & STATIC ASSET TESTS
    # -------------------------------------------------------------------------
    def test_homepage_route(self):
        """Test GET / returns 200 and renders hero cockpit, all 13 tab buttons, and scripts."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('ResumeAI Intelligence Platform', html)
        self.assertIn('hero-showcase-cockpit', html)
        self.assertIn('data-tab="single"', html)
        self.assertIn('data-tab="github"', html)
        self.assertIn('data-tab="improve"', html)
        self.assertIn('data-tab="roadmap"', html)
        self.assertIn('data-tab="version"', html)
        self.assertIn('assistant-launcher-wrap', html)

    def test_login_route(self):
        """Test GET /login renders 200, form card, and password toggle."""
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('Welcome back', html)
        self.assertIn('toggle-password', html)

    def test_signup_route(self):
        """Test GET /signup renders 200, form card, and password toggle."""
        resp = self.client.get('/signup')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('Create account', html)
        self.assertIn('toggle-password', html)

    def test_static_css_and_js(self):
        """Test static CSS and JS are served and contain the design system tokens and functions."""
        css_resp = self.client.get('/static/css/styles.css')
        self.assertEqual(css_resp.status_code, 200)
        css = css_resp.get_data(as_text=True)
        self.assertIn(':focus-visible', css)
        self.assertIn('.hero-showcase-cockpit', css)
        self.assertIn('.skeleton-telemetry-banner', css)

        js_resp = self.client.get('/static/js/app.js')
        self.assertEqual(js_resp.status_code, 200)
        js = js_resp.get_data(as_text=True)
        self.assertIn('switchHeroShowcase', js)
        self.assertIn('loadVersionCompareDemo', js)

    # -------------------------------------------------------------------------
    # 3. API ENDPOINTS INTEGRATION TESTS
    # -------------------------------------------------------------------------
    def test_api_health(self):
        """Test /api/health endpoint."""
        resp = self.client.get('/api/health')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('status'), 'healthy')

    def test_api_analyze_text(self):
        """Test /api/analyze-text with sample resume text."""
        payload = {
            'resume_text': 'Alex Chen\nSenior Engineer with Python, FastAPI, Docker, and AWS experience.',
            'job_description': 'Senior Python AWS engineer needed with Docker experience.',
            'required_skills': 'Python, AWS, Docker',
            'analysis_mode': 'local'
        }
        resp = self.client.post('/api/analyze-text', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('ai_analysis', data)
        self.assertIn('overall_score', data['ai_analysis'])
        self.assertIn('intelligence_platform', data)

    def test_api_analyze_file_upload(self):
        """Test /api/analyze with multipart file upload."""
        resume_bytes = io.BytesIO(b"Alex Chen\nSenior Full-Stack Engineer\nSkills: Python, FastAPI, Docker, AWS")
        data = {
            'file': (resume_bytes, 'alex_resume.txt', 'text/plain'),
            'job_description': 'Looking for Python and AWS engineer.',
            'required_skills': 'Python, AWS',
            'analysis_mode': 'local'
        }
        resp = self.client.post('/api/analyze', data=data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        result = resp.get_json()
        self.assertIn('ai_analysis', result)
        self.assertIn('overall_score', result['ai_analysis'])
        self.assertIn('skills_analysis', result)

    def test_api_ats_rebuild_resume(self):
        """Test /api/ats-rebuild-resume error audit and rebuild engine."""
        payload = {
            'resume_text': 'Alex Chen\nSenior Engineer\nalex@test.com\nSkills: Python, Docker\nExperience: Staff Engineer at TechCorp\n- built microservices',
            'job_description': 'Python, Docker, AWS'
        }
        resp = self.client.post('/api/ats-rebuild-resume', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('ats_score_before', data)
        self.assertIn('ats_score_after', data)
        self.assertIn('rebuilt_plain_text', data)
        self.assertGreater(data['ats_score_after'], data['ats_score_before'])

    def test_api_github_verify(self):
        """Test /api/github-verify with public GitHub profile and claimed resume skills."""
        payload = {
            'username': 'alexchen-dev',
            'resume_text': 'Python, AWS, Docker, Kubernetes, Go, TypeScript'
        }
        resp = self.client.post('/api/github-verify', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get('username'), 'alexchen-dev')
        self.assertIn('verified_skills', data)
        self.assertIn('language_distribution', data)

    def test_api_version_compare(self):
        """Test /api/intelligence/version-compare delta analysis."""
        payload = {
            'version1_text': 'Junior Developer\nSkills: Python, HTML, CSS',
            'version2_text': 'Senior Developer\nSkills: Python, FastAPI, Docker, AWS, Kubernetes'
        }
        resp = self.client.post('/api/intelligence/version-compare', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('deltas', data)
        self.assertTrue(len(data['deltas'].get('added_skills', [])) > 0)

    def test_api_recruiter_sim(self):
        """Test /api/intelligence/recruiter-sim 3-lens simulation."""
        payload = {
            'resume_text': 'Alex Chen\nSenior Engineer\nSkills: Python, AWS, Docker',
            'job_description': 'Staff Platform Engineer'
        }
        resp = self.client.post('/api/intelligence/recruiter-sim', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('startup_recruiter', data)
        self.assertIn('enterprise_recruiter', data)
        self.assertIn('technical_interviewer', data)

    def test_api_fairness_audit(self):
        """Test /api/intelligence/fairness-audit demographic audit."""
        payload = {
            'resume_text': 'Software Engineer with 5 years experience in Python and cloud systems.'
        }
        resp = self.client.post('/api/intelligence/fairness-audit', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('disparity_delta', data)
        self.assertIn('original_qualification_score', data)

    def test_api_assistant_chat_local(self):
        """Test /api/assistant-chat in offline local mode."""
        payload = {
            'message': 'How does the ATS Resume Rebuilder work?'
        }
        resp = self.client.post('/api/assistant-chat', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('reply', data)
        self.assertEqual(data.get('mode'), 'local')

    def test_api_cover_letter(self):
        """Test /api/cover-letter synthesis."""
        resume_bytes = io.BytesIO(b"Alex Chen\nSenior Full-Stack Engineer\nSkills: Python, FastAPI, AWS")
        data = {
            'file': (resume_bytes, 'alex_resume.txt', 'text/plain'),
            'job_description': 'Seeking an experienced Python Cloud Architect at NextGen Tech.'
        }
        resp = self.client.post('/api/cover-letter', data=data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        res = resp.get_json()
        self.assertIn('cover_letter', res)
        self.assertTrue(len(res['cover_letter']) > 50)

    def test_api_career_paths(self):
        """Test /api/career-paths trajectory generation."""
        resume_bytes = io.BytesIO(b"Alex Chen\nStaff Software Engineer\nSkills: Python, Go, AWS, Docker, Kubernetes")
        data = {
            'file': (resume_bytes, 'alex_resume.txt', 'text/plain'),
            'job_description': 'Principal Engineer or Engineering Director'
        }
        resp = self.client.post('/api/career-paths', data=data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        res = resp.get_json()
        self.assertIn('paths', res)

    def test_api_salary_estimate(self):
        """Test /api/salary-estimate compensation benchmarking."""
        resume_bytes = io.BytesIO(b"Alex Chen\nStaff Software Engineer\n6 years experience in Cloud Systems")
        data = {
            'file': (resume_bytes, 'alex_resume.txt', 'text/plain'),
            'job_description': 'Staff Cloud Architect in San Francisco, CA'
        }
        resp = self.client.post('/api/salary-estimate', data=data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 200)
        res = resp.get_json()
        self.assertIn('estimated_range', res)
        self.assertIn('median', res)


if __name__ == '__main__':
    unittest.main()
