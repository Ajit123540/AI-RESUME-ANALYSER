import re
from typing import Dict, List, Any

class ResumeExtractor:
    """Structured entity parser extracting sections, metrics, contact info, and experience items."""

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, Any]:
        """Extract email, phone, links, and location signals."""
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phone_match = re.search(r'\(?\+?\d{1,4}\)?[-.\s]?\d{1,5}[-.\s]?\d{3,5}[-.\s]?\d{3,5}', text)
        linkedin_match = re.search(r'(linkedin\.com/in/[\w-]+)', text, re.IGNORECASE)
        github_match = re.search(r'(github\.com/[\w-]+)', text, re.IGNORECASE)

        return {
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "linkedin": linkedin_match.group(0) if linkedin_match else None,
            "github": github_match.group(0) if github_match else None
        }

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Split resume into common logical sections."""
        section_keywords = [
            "summary", "objective", "experience", "work experience",
            "employment", "projects", "education", "skills",
            "technical skills", "certifications", "achievements", "languages"
        ]

        lines = text.split('\n')
        sections = {"header": []}
        current_section = "header"

        for line in lines:
            line_clean = line.strip().lower().rstrip(':')
            if line_clean in section_keywords or any(line_clean.startswith(kw) for kw in ["work experience", "technical skills", "personal projects"]):
                current_section = line_clean
                if current_section not in sections:
                    sections[current_section] = []
            else:
                sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}

    @staticmethod
    def extract_projects(text: str) -> List[Dict[str, Any]]:
        """Extract project entities from resume text."""
        sections = ResumeExtractor.extract_sections(text)
        project_text = sections.get("projects", "") or sections.get("personal projects", "") or text

        # Find project blocks by titles / bullet points
        lines = [l.strip() for l in project_text.split('\n') if l.strip()]
        projects = []
        current_proj = None

        for line in lines:
            # Match potential project headers (e.g., "AI Resume Analyzer - Flask, Python")
            if len(line) < 80 and not line.startswith(('•', '-', '*')):
                if current_proj:
                    projects.append(current_proj)
                current_proj = {
                    "name": line.split('|')[0].split('-')[0].strip(),
                    "raw_title": line,
                    "bullets": []
                }
            elif current_proj:
                current_proj["bullets"].append(line.lstrip('•-* '))

        if current_proj:
            projects.append(current_proj)

        # Fallback if no explicit blocks found
        if not projects and project_text:
            projects.append({
                "name": "General Projects",
                "raw_title": "Projects",
                "bullets": [l.lstrip('•-* ') for l in lines]
            })

        return projects[:6]

    @staticmethod
    def extract_metrics_and_claims(text: str) -> List[Dict[str, Any]]:
        """Extract quantifiable metrics & achievement statements."""
        lines = text.split('\n')
        claims = []
        
        # Regex for metrics (percentages, dollar amounts, user counts, scale multiples)
        metric_pattern = re.compile(
            r'(\d+%\s*|\$\d+[\d,]*|\b\d+\s*users\b|\b\d+x\b|\b\d+\s*developers\b|\b\d+\s*ms\b|\bincreased\s+by\s+\d+|\breduced\s+by\s+\d+)',
            re.IGNORECASE
        )

        for line in lines:
            line_clean = line.strip()
            if metric_pattern.search(line_clean):
                claims.append({
                    "statement": line_clean.lstrip('•-* '),
                    "metric_matches": metric_pattern.findall(line_clean)
                })

        return claims
