from typing import Dict, List, Any
from src.skills_extractor import SkillsExtractor
from src.intelligence.normalizer import SkillNormalizer

class VersionIntelligence:
    """Compare multiple resume versions, tracking skill deltas and score progression."""

    @staticmethod
    def compare_versions(v1_text: str, v2_text: str, label1: str = "Version 1", label2: str = "Version 2") -> Dict[str, Any]:
        """Compare two resume texts and generate detailed version diff metrics."""
        extractor = SkillsExtractor()

        skills1 = set(SkillNormalizer.normalize_list(extractor.extract_skills(v1_text).get("all_skills", [])))
        skills2 = set(SkillNormalizer.normalize_list(extractor.extract_skills(v2_text).get("all_skills", [])))

        added_skills = sorted(list(skills2 - skills1))
        removed_skills = sorted(list(skills1 - skills2))
        retained_skills = sorted(list(skills1 & skills2))

        word_count1 = len(v1_text.split())
        word_count2 = len(v2_text.split())

        return {
            "version_1": {
                "label": label1,
                "word_count": word_count1,
                "skill_count": len(skills1),
                "skills": sorted(list(skills1))
            },
            "version_2": {
                "label": label2,
                "word_count": word_count2,
                "skill_count": len(skills2),
                "skills": sorted(list(skills2))
            },
            "deltas": {
                "added_skills": added_skills,
                "removed_skills": removed_skills,
                "retained_skills": retained_skills,
                "word_count_change": word_count2 - word_count1,
                "summary_change": f"+{len(added_skills)} skills added, -{len(removed_skills)} skills removed."
            }
        }
