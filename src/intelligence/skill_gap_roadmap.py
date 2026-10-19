from typing import Dict, List, Any

class SkillGapAndRoadmapEngine:
    """Analyze skill gaps and generate personalized weekly learning roadmaps."""

    @staticmethod
    def analyze_gaps(candidate_skills: List[str], required_skills: List[str], job_description: str = "") -> Dict[str, Any]:
        """Categorize missing skills by priority."""
        candidate_set = set(s.lower() for s in candidate_skills)
        req_set = set(s.lower() for s in required_skills)
        job_text_lower = job_description.lower()

        matched = []
        high_priority = []
        medium_priority = []
        low_priority = []

        for req in required_skills:
            req_lower = req.lower()
            if req_lower in candidate_set:
                matched.append(req)
            else:
                # Determine priority based on presence in job text & industry criticality
                freq = job_text_lower.count(req_lower)
                is_core = any(core in req_lower for core in ["python", "java", "react", "aws", "docker", "sql", "kubernetes", "api"])
                
                if freq >= 2 or is_core:
                    high_priority.append({
                        "skill": req,
                        "priority": "HIGH",
                        "reason": f"Core requirement mentioned repeatedly ({freq}x) in target job role."
                    })
                elif freq == 1:
                    medium_priority.append({
                        "skill": req,
                        "priority": "MEDIUM",
                        "reason": f"Mentioned in job description responsibilities."
                    })
                else:
                    low_priority.append({
                        "skill": req,
                        "priority": "LOWER",
                        "reason": "Secondary/preferred skill."
                    })

        return {
            "matched_skills": sorted(matched),
            "high_priority_missing": high_priority,
            "medium_priority_missing": medium_priority,
            "low_priority_missing": low_priority,
            "total_missing_count": len(high_priority) + len(medium_priority) + len(low_priority)
        }

    @staticmethod
    def generate_roadmap(candidate_skills: List[str], missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generate a 4-week step-by-step personalized learning roadmap."""
        roadmap = []
        clean_missing = [s.strip() for s in missing_skills if s and s.strip()]

        if not clean_missing:
            return [
                {
                    "week": "Week 1-2",
                    "title": "Advanced Mastery & Portfolio Optimization",
                    "skill_focus": "Existing Stack Mastery",
                    "tasks": ["Build an end-to-end showcase project utilizing your primary technical stack.", "Optimize GitHub README documentation."],
                    "status": "Completed"
                }
            ]

        # Map missing skills into weekly blocks
        week_1_skill = clean_missing[0] if len(clean_missing) > 0 else "System Architecture"
        week_2_skill = clean_missing[1] if len(clean_missing) > 1 else f"Integration with {week_1_skill}"
        week_3_skill = clean_missing[2] if len(clean_missing) > 2 else "Cloud & Deployment Fundamentals"
        week_4_skill = clean_missing[3] if len(clean_missing) > 3 else "CI/CD & Capstone Integration"

        roadmap.append({
            "week": "Week 1",
            "title": f"Fundamentals of {week_1_skill}",
            "skill_focus": week_1_skill,
            "tasks": [
                f"Complete introductory syntax & core concepts of {week_1_skill}.",
                f"Build a standalone hello-world module using {week_1_skill}."
            ],
            "status": "Not Started"
        })

        roadmap.append({
            "week": "Week 2",
            "title": f"Integration: {week_1_skill} + Existing Stack",
            "skill_focus": f"{week_1_skill} & {week_2_skill}",
            "tasks": [
                f"Connect {week_1_skill} with your current backend/database setup.",
                f"Implement basic CRUD and error handling for {week_2_skill}."
            ],
            "status": "Not Started"
        })

        roadmap.append({
            "week": "Week 3",
            "title": f"Applied Project: {week_3_skill}",
            "skill_focus": week_3_skill,
            "tasks": [
                f"Configure deployment / environment variables for {week_3_skill}.",
                f"Add unit tests & integration checks."
            ],
            "status": "Not Started"
        })

        roadmap.append({
            "week": "Week 4",
            "title": "Capstone Deployment & Resume Update",
            "skill_focus": week_4_skill,
            "tasks": [
                f"Deploy full application stack incorporating {week_1_skill} and {week_3_skill}.",
                "Add project bullet point to resume highlighting newly demonstrated skills."
            ],
            "status": "Not Started"
        })

        return roadmap
