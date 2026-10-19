from typing import Dict, List, Any
from src.intelligence.extractor import ResumeExtractor

class ProjectMatcher:
    """Analyze resume projects against target job descriptions with spatial allocation suggestions."""

    @staticmethod
    def match_projects(resume_text: str, job_description: str) -> List[Dict[str, Any]]:
        """Rank resume projects by relevance to job description."""
        projects = ResumeExtractor.extract_projects(resume_text)
        job_lower = job_description.lower() if job_description else ""

        matched_projects = []

        for p in projects:
            p_name = p["name"]
            bullets_text = " ".join(p["bullets"]).lower()
            combined_text = f"{p_name.lower()} {bullets_text}"

            # Calculate match score based on keyword co-occurrence with job text
            words_in_proj = set(combined_text.split())
            job_words = set(w for w in job_lower.split() if len(w) > 3)

            matched_terms = words_in_proj & job_words
            relevance = round(min(98, max(45, (len(matched_terms) * 12) + (30 if job_lower else 50))), 1)

            # Spatial recommendation
            if relevance >= 80:
                layout_advice = "HIGH RELEVANCE: Allocate 4-5 key bullet points. Move near the top of Projects section."
            elif relevance >= 60:
                layout_advice = "MODERATE RELEVANCE: Keep 2-3 concise bullets focusing on matching technologies."
            else:
                layout_advice = "LOW RELEVANCE: Condense to 1-2 summary lines or replace with a closer job match."

            matched_projects.append({
                "project_name": p_name,
                "relevance_score": relevance,
                "matched_terms": list(matched_terms)[:6],
                "bullet_count": len(p["bullets"]),
                "layout_recommendation": layout_advice
            })

        # Sort by relevance descending
        matched_projects.sort(key=lambda x: x["relevance_score"], reverse=True)
        return matched_projects
