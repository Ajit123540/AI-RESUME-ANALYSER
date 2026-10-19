from typing import Dict, List, Any

class ImplicitSkillDetector:
    """Infer unlisted skills implied by project tech stacks and experience combinations."""

    RULES = [
        {
            "requires_any": [["flask", "django", "fastapi", "express", "spring", "rails"]],
            "implies": [
                {"skill": "REST API", "confidence": "HIGH", "category": "Backend Development"},
                {"skill": "Backend Development", "confidence": "HIGH", "category": "Software Architecture"},
                {"skill": "API Integration", "confidence": "HIGH", "category": "Backend Development"}
            ]
        },
        {
            "requires_any": [["mysql", "postgresql", "mongodb", "sqlite", "oracle"]],
            "implies": [
                {"skill": "Database Design", "confidence": "HIGH", "category": "Data Engineering"},
                {"skill": "CRUD Operations", "confidence": "HIGH", "category": "Backend Development"},
                {"skill": "Data Modeling", "confidence": "MEDIUM", "category": "Data Engineering"}
            ]
        },
        {
            "requires_any": [["docker", "kubernetes", "jenkins", "terraform"]],
            "implies": [
                {"skill": "Containerization", "confidence": "HIGH", "category": "DevOps"},
                {"skill": "DevOps", "confidence": "HIGH", "category": "Cloud & Infrastructure"},
                {"skill": "Deployment Pipelines", "confidence": "MEDIUM", "category": "DevOps"}
            ]
        },
        {
            "requires_any": [["react", "angular", "vue", "next.js"]],
            "implies": [
                {"skill": "Frontend Architecture", "confidence": "HIGH", "category": "Web Development"},
                {"skill": "State Management", "confidence": "MEDIUM", "category": "Web Development"},
                {"skill": "Responsive Design", "confidence": "HIGH", "category": "Web Development"}
            ]
        },
        {
            "requires_any": [["jwt", "oauth", "authentication"]],
            "implies": [
                {"skill": "Authentication", "confidence": "HIGH", "category": "Security"},
                {"skill": "Authorization", "confidence": "HIGH", "category": "Security"},
                {"skill": "Web Security", "confidence": "MEDIUM", "category": "Security"}
            ]
        }
    ]

    @classmethod
    def detect_implicit_skills(cls, explicit_skills: List[str]) -> List[Dict[str, Any]]:
        """Infer hidden/implicit skills based on explicit skill set."""
        explicit_lower = set(s.lower() for s in explicit_skills)
        implicit_map: Dict[str, Dict[str, Any]] = {}

        for rule in cls.RULES:
            for req_group in rule["requires_any"]:
                if any(tech in explicit_lower for tech in req_group):
                    for imp in rule["implies"]:
                        skill_name = imp["skill"]
                        if skill_name.lower() not in explicit_lower:
                            implicit_map[skill_name] = {
                                "skill": skill_name,
                                "confidence": imp["confidence"],
                                "category": imp["category"],
                                "advice": f"Demonstrated via hands-on usage. Consider adding if you can explain experience."
                            }

        return list(implicit_map.values())
