import re
from typing import Dict, List, Any
from src.intelligence.extractor import ResumeExtractor

class EvidenceVerifier:
    """Evaluate skill evidence strength and verify metric claim support using neutral language."""

    @staticmethod
    def verify_skills(resume_text: str, skills: List[str]) -> Dict[str, Any]:
        """Verify each skill against resume context and assign evidence level."""
        sections = ResumeExtractor.extract_sections(resume_text)
        exp_text = (sections.get("experience", "") + " " + sections.get("work experience", "") + " " + sections.get("projects", "")).lower()
        skills_text = (sections.get("skills", "") + " " + sections.get("technical skills", "")).lower()

        evidence_results = {}

        for skill in skills:
            skill_lower = skill.lower()
            pattern = r'\b' + re.escape(skill_lower) + r'\b'

            exp_matches = len(re.findall(pattern, exp_text))
            skills_section_match = len(re.findall(pattern, skills_text)) > 0

            if exp_matches >= 2:
                level = "HIGH"
                score = 90
                status = "Evidence found"
                loc = "Work Experience / Projects"
            elif exp_matches == 1:
                level = "MEDIUM"
                score = 70
                status = "Evidence found"
                loc = "Projects / Experience section"
            elif skills_section_match:
                level = "WEAK"
                score = 40
                status = "Limited evidence"
                loc = "Skills list only (no project context)"
            else:
                level = "NO EVIDENCE"
                score = 10
                status = "Evidence not found"
                loc = "Not explicitly supported"

            recommendation = (
                "Strong supporting evidence in experience/projects." if level in ["HIGH", "MEDIUM"]
                else f"Consider adding a project or role bullet detailing your hands-on use of {skill}."
            )

            evidence_results[skill] = {
                "skill": skill,
                "level": level,
                "score": score,
                "status": status,
                "location": loc,
                "occurrences_in_experience": exp_matches,
                "recommendation": recommendation
            }

        return evidence_results

    @staticmethod
    def verify_claims(resume_text: str) -> List[Dict[str, Any]]:
        """Identify metric claims that may require methodology verification."""
        claims = ResumeExtractor.extract_metrics_and_claims(resume_text)
        audited_claims = []

        for c in claims:
            stmt = c["statement"]
            reasons = []

            # Audit check 1: Large percentages
            if re.search(r'\b[2-9]\d{2,}%\b|\b1\d{3,}%\b', stmt):
                reasons.append("Large numerical improvement claimed (>200%)")
            
            # Audit check 2: Scale claims without baseline
            if re.search(r'\b\d+\s*million\b|\b100k\b|\b1m\b', stmt, re.IGNORECASE) and not re.search(r'from|scaled from|baseline', stmt, re.IGNORECASE):
                reasons.append("High scale metric mentioned without baseline starting point")

            # Audit check 3: Team size
            if re.search(r'\bmanaged\b|\bled\b', stmt, re.IGNORECASE) and re.search(r'\b\d+\+\s*developers\b|\b\d+\s*engineers\b', stmt, re.IGNORECASE):
                reasons.append("Team scale claim requiring leadership context")

            if reasons or "%" in stmt:
                if not reasons:
                    reasons.append("Metric performance statement without specified measurement method")
                
                audited_claims.append({
                    "claim": stmt,
                    "status": "Potentially unsupported claim",
                    "reasons": reasons,
                    "suggested_improvement": f"Explain how this metric was measured (e.g., benchmark tool, baseline vs new result)."
                })

        return audited_claims
