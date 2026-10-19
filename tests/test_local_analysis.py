import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import app as flask_app
from src.analyzer import ResumeAnalyzer
from src.local_scorer import LocalScorer


class LocalScorerTests(unittest.TestCase):
    def test_identical_texts_have_full_tfidf_similarity(self):
        scorer = LocalScorer({"and", "the"})
        similarity = scorer._tfidf_similarity(
            "Python and Django developer",
            "Python and Django developer"
        )
        self.assertEqual(similarity, 100.0)

    def test_local_score_exposes_components_and_recommendation(self):
        scorer = LocalScorer({"and", "the"})
        result = scorer.score_resume(
            "Python Django AWS PostgreSQL",
            "Python Django AWS PostgreSQL developer",
            {"combined_score": 100},
            {"all_skills": ["python", "django", "aws", "postgresql"]},
            ["Python", "Django"],
            {"all_skills": ["python", "django"]}
        )
        self.assertEqual(result["analysis_mode"], "local")
        self.assertEqual(result["scoring_breakdown"]["required_skill_match"], 100.0)
        self.assertEqual(result["recommendation"], "Strong Recommend")


class LocalAnalyzerTests(unittest.TestCase):
    def test_local_analysis_and_batch_ranking_never_call_openai_scorer(self):
        analyzer = ResumeAnalyzer(use_ai=False)
        analyzer.use_ai = True
        with patch.object(
            analyzer.ai_scorer,
            "score_resume",
            side_effect=AssertionError("OpenAI scoring must not run in local mode")
        ), patch.object(
            analyzer.ai_scorer,
            "rank_resumes",
            side_effect=AssertionError("OpenAI ranking must not run in local mode")
        ):
            analysis = analyzer.analyze_resume(
                "Python Django AWS PostgreSQL built data services",
                "Python Django AWS PostgreSQL developer",
                analysis_mode="local"
            )
            self.assertEqual(analysis["analysis_mode"], "local")
            self.assertGreater(
                analysis["ai_analysis"]["scoring_breakdown"]["tfidf_similarity"], 0
            )

            with tempfile.TemporaryDirectory() as directory:
                strong_resume = Path(directory) / "strong.txt"
                weak_resume = Path(directory) / "weak.txt"
                strong_resume.write_text(
                    "Python Django AWS PostgreSQL data platform", encoding="utf-8"
                )
                weak_resume.write_text(
                    "Garden design, landscape maintenance, and plant care", encoding="utf-8"
                )
                results = analyzer.batch_analyze(
                    [str(weak_resume), str(strong_resume)],
                    "Python Django AWS PostgreSQL data developer",
                    analysis_mode="local"
                )

        self.assertEqual(Path(results[0]["file_name"]).name, "strong.txt")
        self.assertEqual(results[0]["local_ranking"]["rank"], 1)
        self.assertEqual(results[1]["local_ranking"]["rank"], 2)

    def test_flask_upload_uses_local_mode_without_calling_ai_scorer(self):
        client = flask_app.app.test_client()
        page = client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'value="local" selected', page.data)
        with patch.object(
            flask_app.analyzer.ai_scorer,
            "score_resume",
            side_effect=AssertionError("OpenAI scoring must not run in local mode")
        ):
            response = client.post(
                "/api/analyze",
                data={
                    "file": (BytesIO(b"Python Django AWS PostgreSQL"), "resume.txt"),
                    "job_description": "Python Django AWS developer",
                    "analysis_mode": "local"
                },
                content_type="multipart/form-data"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["analysis_mode"], "local")
        self.assertIn("scoring_breakdown", response.get_json()["ai_analysis"])

    def test_local_cover_letter_uses_template_and_interview_is_unavailable(self):
        result = flask_app.analyzer.ai_scorer.generate_cover_letter(
            "Built Python services for data processing.",
            "Seeking a Python developer.",
            use_ai=False
        )
        self.assertEqual(result["generation_mode"], "template")
        self.assertIn("no AI service was used", result["note"])

        client = flask_app.app.test_client()
        response = client.post(
            "/api/interview-chat",
            json={
                "resume_text": "Python and Django developer with 4 years experience",
                "job_description": "Seeking Python backend engineer",
                "analysis_mode": "local",
                "history": []
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.get_json())
        self.assertEqual(response.get_json().get("generation_mode"), "local_heuristic")


    def test_openai_quota_exhausted_falls_back_to_local_scorer(self):
        """When OpenAI returns error 429 quota exhausted, analyze_resume must gracefully fall back to local scorer."""
        analyzer = ResumeAnalyzer(use_ai=True)
        with patch.object(
            analyzer.ai_scorer,
            "score_resume",
            return_value={"error": "OpenAI API quota exhausted (Error 429): credit_balance_exhausted"}
        ):
            result = analyzer.analyze_resume(
                "Python Django AWS developer with 5 years experience.",
                "Python Django AWS developer",
                analysis_mode="ai"
            )
            # Must succeed with local mode fallback
            self.assertEqual(result["analysis_mode"], "local")
            self.assertIn("scoring_breakdown", result["ai_analysis"])
            self.assertIn("OpenAI credits exhausted", result["ai_analysis"].get("fallback_note", ""))


    def test_local_features_work_without_openai(self):
        """Verify local heuristic fallbacks work for bullets, career paths, and salary estimate."""
        ai_scorer = flask_app.analyzer.ai_scorer

        # Bullet rewrites in local mode
        bullets_res = ai_scorer.rewrite_resume_bullets(
            "Developed Python microservices for backend data processing.\nManaged PostgreSQL database optimization.",
            "Seeking Senior Python Developer with microservices experience.",
            use_ai=False
        )
        self.assertIn("rewrites", bullets_res)
        self.assertGreater(len(bullets_res["rewrites"]), 0)
        self.assertEqual(bullets_res.get("generation_mode"), "local_heuristic")

        # Career paths in local mode
        paths_res = ai_scorer.career_path_recommendations(
            "Python developer with AWS and Docker experience.",
            "Cloud Systems Architect",
            use_ai=False
        )
        self.assertIn("paths", paths_res)
        self.assertEqual(len(paths_res["paths"]), 3)
        self.assertEqual(paths_res.get("generation_mode"), "local_heuristic")

        # Salary estimate in local mode
        salary_res = ai_scorer.salary_estimate(
            "Senior Python Developer with 6 years experience in AWS and PostgreSQL.",
            "Senior Backend Engineer",
            use_ai=False
        )
        self.assertIn("estimated_range", salary_res)
        self.assertIn("median", salary_res)
        self.assertIn("positioning", salary_res)
        self.assertEqual(salary_res.get("generation_mode"), "local_heuristic")

        # Assistant Chat in local mode
        assistant_res = ai_scorer.assistant_chat_response(
            "How do I beat ATS scanners and optimize keywords?",
            use_ai=False
        )
        self.assertIn("reply", assistant_res)
        self.assertIn("ATS Optimization", assistant_res.get("title", ""))
        self.assertEqual(assistant_res.get("generation_mode"), "local_knowledge_base")

        client = flask_app.app.test_client()
        chat_resp = client.post(
            "/api/assistant-chat",
            json={
                "message": "What is the X-Y-Z formula for bullets?",
                "analysis_mode": "local"
            }
        )
        self.assertEqual(chat_resp.status_code, 200)
        self.assertIn("reply", chat_resp.get_json())
        self.assertIn("X-Y-Z", chat_resp.get_json()["reply"])
        self.assertEqual(chat_resp.get_json().get("mode"), "local")

        # Test salary negotiation intent in local mode
        salary_chat = client.post(
            "/api/assistant-chat",
            json={
                "message": "How do I negotiate salary after an offer?",
                "analysis_mode": "local"
            }
        )
        self.assertEqual(salary_chat.status_code, 200)
        self.assertIn("negotiat", salary_chat.get_json()["reply"].lower())

        # Test index.html contains auth modal and assistant widget markup
        index_res = client.get("/")
        self.assertEqual(index_res.status_code, 200)
        html = index_res.data.decode("utf-8")
        self.assertIn("auth-welcome-modal-backdrop", html)
        self.assertIn("auth-welcome-username", html)
        self.assertIn("assistant-launcher-btn", html)
        self.assertIn("assistant-chat-panel", html)
        self.assertIn("nav-user-container", html)
        self.assertIn("github-panel", html)
        self.assertIn("GitHub Verifier", html)

        # Test login.html and signup.html routes
        login_res = client.get("/login")
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("login-form", login_res.data.decode("utf-8"))

        signup_res = client.get("/signup")
        self.assertEqual(signup_res.status_code, 200)
        self.assertIn("signup-form", signup_res.data.decode("utf-8"))

        # Test GitHubCodeVerifier directly
        from src.intelligence.github_verifier import GitHubCodeVerifier
        gh_data = GitHubCodeVerifier.evaluate_evidence(
            "alexchen-dev",
            "Alex Chen. Skills: Python, TypeScript, Go, FastAPI, Docker, Redis, AWS."
        )
        self.assertEqual(gh_data["username"], "alexchen-dev")
        self.assertGreater(gh_data["evidence_score"], 70)
        self.assertGreater(len(gh_data["verified_skills"]), 0)
        self.assertIn("recruiter_summary", gh_data)

        # Test /api/github-verify endpoint
        gh_res = client.post(
            "/api/github-verify",
            json={
                "username": "alexchen-dev",
                "resume_text": "Alex Chen. Skills: Python, Go, Docker."
            }
        )
        self.assertEqual(gh_res.status_code, 200)
        gh_json = gh_res.get_json()
        self.assertEqual(gh_json.get("username"), "alexchen-dev")
        self.assertIn("evidence_score", gh_json)
        self.assertIn("highlighted_projects", gh_json)

        # Test ATSResumeRebuilder directly
        from src.intelligence.ats_rebuilder import ATSResumeRebuilder
        rebuild_data = ATSResumeRebuilder.rebuild_ats_resume(
            "Alex Chen\nDeveloper\nWorked on microservices and helped with APIs.\nSkills: Python, Docker, team player."
        )
        self.assertEqual(rebuild_data["candidate_name"], "Alex Chen")
        self.assertGreater(rebuild_data["ats_score_after"], 85)
        self.assertGreater(rebuild_data["errors_count"], 0)
        self.assertIn("rebuilt_markdown", rebuild_data)
        self.assertIn("PROFESSIONAL SUMMARY", rebuild_data["rebuilt_markdown"])

        # Test /api/ats-rebuild-resume endpoint
        ats_res = client.post(
            "/api/ats-rebuild-resume",
            json={
                "resume_text": "Alex Chen\nSenior Engineer\nBuilt Python microservices.",
                "analysis_mode": "local"
            }
        )
        self.assertEqual(ats_res.status_code, 200)
        ats_json = ats_res.get_json()
        self.assertEqual(ats_json.get("candidate_name"), "Alex Chen")
        self.assertIn("ats_score_after", ats_json)
        self.assertIn("sections", ats_json)


if __name__ == "__main__":
    unittest.main()
