import re
from typing import Dict, List, Any

class InterviewRiskAnalyzer:
    """Analyze resume claims to identify interview risk areas and generate practice interview questions."""

    HIGH_RISK_TERMS = {
        "microservices": {
            "risk_level": "HIGH",
            "why": "Microservices involve complex distributed system trade-offs, service communication, and deployment patterns.",
            "questions": [
                "Why did you choose microservices over a monolithic architecture?",
                "How did you handle inter-service communication and data consistency?",
                "How did you manage distributed transactions and service discovery?"
            ],
            "concepts": ["CAP Theorem", "gRPC / REST", "Circuit Breaker Pattern", "Eventual Consistency"]
        },
        "kubernetes": {
            "risk_level": "HIGH",
            "why": "Container orchestration requires deep knowledge of networking, pods, ingress, and deployment strategies.",
            "questions": [
                "What objects (Pods, Deployments, Services, Ingress) did you configure?",
                "How did you handle persistent storage and secrets management?",
                "How did you monitor cluster health and auto-scaling?"
            ],
            "concepts": ["kubectl", "Ingress Controllers", "StatefulSets", "Helm Charts"]
        },
        "machine learning": {
            "risk_level": "HIGH",
            "why": "ML models are probed heavily for dataset preprocessing, model evaluation metrics, and overfitting prevention.",
            "questions": [
                "How did you evaluate model performance and handle data imbalance?",
                "What algorithms were compared, and why was this specific model selected?",
                "How did you deploy and monitor the model in production?"
            ],
            "concepts": ["Precision / Recall / F1", "Cross-Validation", "Feature Engineering", "MLOps"]
        },
        "jwt": {
            "risk_level": "MEDIUM",
            "why": "Authentication claims trigger questions on security vulnerabilities, token storage, and revocation.",
            "questions": [
                "Where did you store JWT tokens on the client side and why?",
                "How did you handle token expiration and refresh tokens?",
                "How do you revoke a valid JWT token before expiry?"
            ],
            "concepts": ["HttpOnly Cookies vs LocalStorage", "RS256 vs HS256", "OAuth2", "CSRF Protection"]
        },
        "aws": {
            "risk_level": "MEDIUM",
            "why": "Cloud services trigger questions on architecture cost, security IAM, and service selection.",
            "questions": [
                "Which specific AWS services did you utilize and how were they configured?",
                "How did you handle IAM roles and security group permissions?",
                "What strategies were used for cost optimization?"
            ],
            "concepts": ["S3 / EC2 / Lambda", "IAM Policies", "VPC & Subnets", "CloudWatch"]
        },
        "docker": {
            "risk_level": "MEDIUM",
            "why": "Containerization prompts questions on image optimization, multi-stage builds, and networking.",
            "questions": [
                "How did you optimize your Dockerfile layer caching and image size?",
                "What is the difference between CMD and ENTRYPOINT?",
                "How did you set up container networking with Docker Compose?"
            ],
            "concepts": ["Multi-stage builds", "Docker Compose", "Layer Caching", "Volume Mounting"]
        }
    }

    @classmethod
    def analyze_interview_risks(cls, resume_text: str) -> List[Dict[str, Any]]:
        """Identify high-stakes statements and generate interview questions."""
        text_lower = resume_text.lower()
        risks = []

        for term, meta in cls.HIGH_RISK_TERMS.items():
            if term in text_lower:
                # Find matching context sentence
                sentences = [s.strip() for s in resume_text.split('.') if term in s.lower()]
                context_sentence = sentences[0] if sentences else f"Mentions {term}"

                risks.append({
                    "claim": context_sentence,
                    "term": term.title(),
                    "risk_level": meta["risk_level"],
                    "why": meta["why"],
                    "likely_questions": meta["questions"],
                    "concepts_to_master": meta["concepts"]
                })

        # Fallback if no specific high-risk keywords found
        if not risks:
            risks.append({
                "claim": "General Technical Experience",
                "term": "Software Development",
                "risk_level": "LOW",
                "why": "Standard technical claims require general architectural clarity.",
                "likely_questions": [
                    "Can you walk me through your most complex project?",
                    "What was the toughest technical bug you faced and how did you resolve it?",
                    "How do you approach testing and code quality?"
                ],
                "concepts_to_master": ["System Design", "Testing", "Version Control"]
            })

        return risks
