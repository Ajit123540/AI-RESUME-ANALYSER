import math
import re
from collections import Counter
from typing import Dict, List, Optional, Set


class LocalScorer:
    """Score resumes locally using keyword overlap and TF-IDF cosine similarity."""

    def __init__(self, stop_words: Optional[Set[str]] = None):
        self.stop_words = stop_words or set()

    def score_resume(
        self,
        resume_text: str,
        job_description: str,
        keyword_result: Dict,
        resume_skills: Dict,
        required_skills: Optional[List[str]] = None,
        job_skills: Optional[Dict] = None
    ) -> Dict:
        """Return a transparent, deterministic resume score without an external model."""
        keyword_score = float(keyword_result.get("combined_score", 0.0))
        tfidf_score = self._tfidf_similarity(resume_text, job_description)

        resume_skill_set = {
            skill.lower() for skill in resume_skills.get("all_skills", [])
        }
        target_skills = required_skills or (job_skills or {}).get("all_skills", [])
        target_skill_set = {skill.lower() for skill in target_skills}
        skill_score = (
            len(resume_skill_set & target_skill_set) / len(target_skill_set) * 100
            if target_skill_set else None
        )

        if skill_score is None:
            overall_score = round(keyword_score * 0.5 + tfidf_score * 0.5, 2)
        else:
            overall_score = round(
                keyword_score * 0.4 + tfidf_score * 0.4 + skill_score * 0.2,
                2
            )

        if overall_score >= 85:
            recommendation = "Strong Recommend"
        elif overall_score >= 70:
            recommendation = "Recommend"
        elif overall_score >= 50:
            recommendation = "Consider"
        else:
            recommendation = "Do Not Recommend"

        strengths = []
        weaknesses = []
        if keyword_score >= 70:
            strengths.append(f"Strong keyword alignment ({keyword_score:.1f}%)")
        elif keyword_score < 40:
            weaknesses.append(f"Limited keyword overlap ({keyword_score:.1f}%)")
        if tfidf_score >= 50:
            strengths.append(f"Relevant resume content (TF-IDF similarity {tfidf_score:.1f}%)")
        elif tfidf_score < 25:
            weaknesses.append(f"Low overall text similarity ({tfidf_score:.1f}%)")
        if skill_score is not None:
            if skill_score >= 70:
                strengths.append(f"Required skill match ({skill_score:.1f}%)")
            elif skill_score < 40:
                weaknesses.append(f"Missing many target skills ({skill_score:.1f}% match)")

        return {
            "overall_score": overall_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "skill_match": f"{skill_score:.1f}%" if skill_score is not None else "Not specified",
            "experience_relevance": f"TF-IDF text similarity: {tfidf_score:.1f}%",
            "recommendation": recommendation,
            "summary": (
                f"Local analysis scored this resume at {overall_score:.1f}% using "
                "keyword overlap, TF-IDF similarity, and available skill matches."
            ),
            "analysis_mode": "local",
            "scoring_breakdown": {
                "keyword_match": round(keyword_score, 2),
                "tfidf_similarity": round(tfidf_score, 2),
                "required_skill_match": (
                    round(skill_score, 2) if skill_score is not None else None
                ),
                "weights": (
                    {"keyword_match": 0.4, "tfidf_similarity": 0.4, "required_skill_match": 0.2}
                    if skill_score is not None
                    else {"keyword_match": 0.5, "tfidf_similarity": 0.5}
                )
            }
        }

    @staticmethod
    def _tokens(text: str, stop_words: Set[str]) -> List[str]:
        return [
            token for token in re.findall(r"\b[a-zA-Z0-9][a-zA-Z0-9+#.-]*\b", text.lower())
            if token not in stop_words and len(token) > 1
        ]

    def _tfidf_similarity(self, resume_text: str, job_description: str) -> float:
        documents = [
            Counter(self._tokens(resume_text, self.stop_words)),
            Counter(self._tokens(job_description, self.stop_words))
        ]
        if not documents[0] or not documents[1]:
            return 0.0

        document_frequency = Counter()
        for document in documents:
            document_frequency.update(document.keys())

        vocabulary = set(document_frequency)
        vectors = []
        for document in documents:
            token_total = sum(document.values())
            vector = {
                token: (frequency / token_total)
                * (math.log((len(documents) + 1) / (document_frequency[token] + 1)) + 1)
                for token, frequency in document.items()
            }
            vectors.append(vector)

        dot_product = sum(
            vectors[0].get(token, 0.0) * vectors[1].get(token, 0.0)
            for token in vocabulary
        )
        norm_resume = math.sqrt(sum(value * value for value in vectors[0].values()))
        norm_job = math.sqrt(sum(value * value for value in vectors[1].values()))
        if not norm_resume or not norm_job:
            return 0.0
        return round(max(0.0, min(1.0, dot_product / (norm_resume * norm_job))) * 100, 2)
