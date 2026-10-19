from typing import Dict, List, Set

class SkillNormalizer:
    """Normalize skill variations, aliases, and technologies into canonical names."""
    
    CANONICAL_MAP = {
        # Languages
        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "py": "Python",
        "python": "Python",
        "cpp": "C++",
        "c++": "C++",
        "c#": "C#",
        "csharp": "C#",
        "golang": "Go",
        "go": "Go",
        
        # Web & Frameworks
        "react": "React",
        "reactjs": "React",
        "react.js": "React",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "vue.js": "Vue.js",
        "angular": "Angular",
        "angularjs": "Angular",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "express": "Express.js",
        "expressjs": "Express.js",
        "django": "Django",
        "flask": "Flask",
        "spring": "Spring Boot",
        "springboot": "Spring Boot",
        "spring boot": "Spring Boot",
        "next": "Next.js",
        "nextjs": "Next.js",
        "next.js": "Next.js",

        # Cloud & DevOps
        "aws": "AWS",
        "amazon web services": "AWS",
        "azure": "Microsoft Azure",
        "microsoft azure": "Microsoft Azure",
        "gcp": "Google Cloud Platform",
        "google cloud": "Google Cloud Platform",
        "docker": "Docker",
        "k8s": "Kubernetes",
        "kubernetes": "Kubernetes",
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "terraform": "Terraform",
        "jenkins": "Jenkins",

        # Databases
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "mongo": "MongoDB",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "sqlite": "SQLite",

        # Data Science & ML
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "dl": "Deep Learning",
        "deep learning": "Deep Learning",
        "nlp": "Natural Language Processing",
        "tf": "TensorFlow",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit": "scikit-learn",
        "scikit-learn": "scikit-learn",
        "pandas": "Pandas",
        "numpy": "NumPy"
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        """Return the canonical name for a given skill string."""
        clean = skill.strip().lower()
        return cls.CANONICAL_MAP.get(clean, skill.strip().title() if len(skill.strip()) > 3 else skill.strip().upper())

    @classmethod
    def normalize_list(cls, skills: List[str]) -> List[str]:
        """Normalize a list of skills and remove duplicates preserving canonical casing."""
        normalized: Set[str] = set()
        for s in skills:
            if s and s.strip():
                normalized.add(cls.normalize(s))
        return sorted(list(normalized))
