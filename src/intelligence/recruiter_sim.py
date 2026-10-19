from typing import Dict, List, Any

class RecruiterSimulator:
    """Evaluate resume candidate through 3 distinct recruiter personas without bias towards any single lens."""

    @staticmethod
    def simulate_all_lenses(resume_skills: List[str], word_count: int, has_projects: bool, has_metrics: bool, match_score: float) -> Dict[str, Any]:
        """Simulate Startup, Enterprise, and Technical Interviewer perspectives."""

        # 1. Startup Technical Recruiter Perspective
        startup_score = round(min(100, (len(resume_skills) * 4) + (25 if has_projects else 0) + (match_score * 0.4)), 1)
        startup_analysis = {
            "persona": "Startup Technical Recruiter",
            "focus": "Practical tech stack agility, side projects, and immediate hands-on coding capability.",
            "fit_score": startup_score,
            "verdict": "Fast Hiring Potential" if startup_score >= 75 else "Requires Practical Project Proof",
            "strengths": [
                f"Demonstrates hands-on tech stack ({len(resume_skills)} skills).",
                "Includes practical project implementations." if has_projects else "Has coding exposure."
            ],
            "questions_raised": [
                "Can candidate ship feature code independently on Day 1?",
                "How quickly can candidate adapt to fast-paced startup iteration?"
            ]
        }

        # 2. Enterprise Recruiter Perspective
        enterprise_score = round(min(100, (match_score * 0.6) + (30 if word_count > 300 else 15) + (10 if len(resume_skills) > 5 else 0)), 1)
        enterprise_analysis = {
            "persona": "Enterprise Recruiter",
            "focus": "Formal qualification compliance, experience depth, title alignment, and corporate stability.",
            "fit_score": enterprise_score,
            "verdict": "Meets Compliance Standard" if enterprise_score >= 70 else "Review Experience & Degree Requirements",
            "strengths": [
                f"Resume detail level is adequate ({word_count} words).",
                f"Keyword alignment with formal job specification ({match_score}%)."
            ],
            "questions_raised": [
                "Does experience history meet strict minimum year requirements?",
                "Is candidate comfortable with enterprise governance and approval flows?"
            ]
        }

        # 3. Technical Interviewer Perspective
        interviewer_score = round(min(100, (25 if has_metrics else 10) + (match_score * 0.5) + (len(resume_skills) * 3)), 1)
        interviewer_analysis = {
            "persona": "Technical Interviewer",
            "focus": "Engineering depth, architectural trade-offs, metric validity, and problem solving.",
            "fit_score": interviewer_score,
            "verdict": "High Technical Depth" if interviewer_score >= 75 else "Prepare Architectural Probe Questions",
            "strengths": [
                "Includes quantifiable impact metrics." if has_metrics else "Solid technical baseline.",
                f"Relevant skill set breadth ({len(resume_skills)} skills)."
            ],
            "questions_raised": [
                "What trade-offs were made in system design choices?",
                "Can candidate explain metric performance methodology under pressure?"
            ]
        }

        return {
            "startup_recruiter": startup_analysis,
            "enterprise_recruiter": enterprise_analysis,
            "technical_interviewer": interviewer_analysis
        }
