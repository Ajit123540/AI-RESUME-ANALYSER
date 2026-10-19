import re
from typing import List, Dict, Set

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not installed. Advanced NLP features will be limited.")


class SkillsExtractor:
    """Extract skills from resume text using NLP and pattern matching."""
    
    def __init__(self):
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
                self.nlp = None
        else:
            self.nlp = None
        
        # Common technical skills database
        self.technical_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'perl', 'lua', 'bash',
            'powershell', 'sql', 'html', 'css', 'assembly', 'fortran', 'cobol',
            
            # Web Technologies
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
            'asp.net', 'rails', 'laravel', 'jquery', 'bootstrap', 'tailwind', 'sass',
            'webpack', 'vite', 'next.js', 'nuxt.js', 'gatsby',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
            'terraform', 'ansible', 'chef', 'puppet', 'linux', 'nginx', 'apache',
            'microservices', 'serverless', 'containerization',
            
            # Data & ML
            'machine learning', 'deep learning', 'data science', 'tensorflow', 'pytorch',
            'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'spark', 'hadoop',
            'tableau', 'power bi', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'redis', 'elasticsearch', 'data mining', 'nlp', 'computer vision',
            
            # Mobile Development
            'ios', 'android', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin',
            'objective-c', 'java', 'mobile development',
            
            # Tools & Frameworks
            'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello', 'asana',
            'visual studio', 'vscode', 'intellij', 'eclipse', 'postman', 'swagger',
            'junit', 'selenium', 'cypress', 'jest', 'mocha',
            
            # Security
            'cybersecurity', 'penetration testing', 'network security', 'encryption',
            'authentication', 'authorization', 'oauth', 'jwt', 'ssl/tls', 'firewall',
            
            # Soft Skills (for context)
            'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
            'agile', 'scrum', 'kanban', 'time management', 'critical thinking'
        }
        
        # Skill patterns for better matching
        self.skill_patterns = [
            r'\b(?:knowledge|experience|proficient|skilled|expert|familiar)\s+(?:in|with|of)?\s*([^.]+)',
            r'\b(?:used|utilized|implemented|developed|built|created|designed)\s+([^.]+)',
            r'\b(?:technologies|tools|languages|frameworks|libraries)[：:]\s*([^.]+)',
        ]
    
    def extract_skills(self, text: str) -> Dict:
        """Extract skills from resume text."""
        text_lower = text.lower()
        found_skills = set()
        
        # Direct keyword matching
        for skill in self.technical_skills:
            if skill.lower() in text_lower:
                found_skills.add(skill)
        
        # Pattern-based extraction
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Extract potential skills from the matched text
                words = re.findall(r'\b[a-zA-Z]+\b', match)
                for word in words:
                    if word.lower() in self.technical_skills:
                        found_skills.add(word)
        
        # Use spaCy for noun phrase extraction if available
        noun_phrases = []
        if self.nlp:
            doc = self.nlp(text)
            for chunk in doc.noun_chunks:
                phrase = chunk.text.lower().strip()
                if phrase in self.technical_skills:
                    found_skills.add(phrase)
                noun_phrases.append(phrase)
        
        # Categorize skills
        categorized_skills = self._categorize_skills(found_skills)
        
        return {
            'all_skills': sorted(list(found_skills)),
            'categorized': categorized_skills,
            'skill_count': len(found_skills),
            'noun_phrases': noun_phrases[:20]  # Limit for readability
        }
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize skills into groups."""
        categories = {
            'Programming Languages': [],
            'Web Technologies': [],
            'Cloud & DevOps': [],
            'Data & ML': [],
            'Mobile Development': [],
            'Tools & Frameworks': [],
            'Security': [],
            'Soft Skills': [],
            'Other': []
        }
        
        # Simple categorization based on skill lists
        prog_langs = {'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
                     'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'perl', 'lua', 'bash',
                     'powershell', 'sql', 'html', 'css', 'assembly', 'fortran', 'cobol'}
        
        web_tech = {'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
                   'asp.net', 'rails', 'laravel', 'jquery', 'bootstrap', 'tailwind', 'sass',
                   'webpack', 'vite', 'next.js', 'nuxt.js', 'gatsby'}
        
        cloud_devops = {'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
                       'terraform', 'ansible', 'chef', 'puppet', 'linux', 'nginx', 'apache',
                       'microservices', 'serverless', 'containerization'}
        
        data_ml = {'machine learning', 'deep learning', 'data science', 'tensorflow', 'pytorch',
                 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'spark', 'hadoop',
                 'tableau', 'power bi', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
                 'redis', 'elasticsearch', 'data mining', 'nlp', 'computer vision'}
        
        mobile = {'ios', 'android', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin',
                'objective-c', 'java', 'mobile development'}
        
        tools = {'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello', 'asana',
                'visual studio', 'vscode', 'intellij', 'eclipse', 'postman', 'swagger',
                'junit', 'selenium', 'cypress', 'jest', 'mocha'}
        
        security = {'cybersecurity', 'penetration testing', 'network security', 'encryption',
                  'authentication', 'authorization', 'oauth', 'jwt', 'ssl/tls', 'firewall'}
        
        soft_skills = {'leadership', 'communication', 'teamwork', 'problem solving', 
                      'project management', 'agile', 'scrum', 'kanban', 'time management', 
                      'critical thinking'}
        
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in prog_langs:
                categories['Programming Languages'].append(skill)
            elif skill_lower in web_tech:
                categories['Web Technologies'].append(skill)
            elif skill_lower in cloud_devops:
                categories['Cloud & DevOps'].append(skill)
            elif skill_lower in data_ml:
                categories['Data & ML'].append(skill)
            elif skill_lower in mobile:
                categories['Mobile Development'].append(skill)
            elif skill_lower in tools:
                categories['Tools & Frameworks'].append(skill)
            elif skill_lower in security:
                categories['Security'].append(skill)
            elif skill_lower in soft_skills:
                categories['Soft Skills'].append(skill)
            else:
                categories['Other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def compare_skills(self, resume_skills: Dict, required_skills: List[str]) -> Dict:
        """Compare extracted skills with required skills."""
        resume_skill_set = set(skill.lower() for skill in resume_skills['all_skills'])
        required_skill_set = set(skill.lower() for skill in required_skills)
        
        matched_skills = resume_skill_set & required_skill_set
        missing_skills = required_skill_set - resume_skill_set
        
        match_percentage = (len(matched_skills) / len(required_skill_set) * 100) if required_skill_set else 0
        
        return {
            'matched_skills': sorted(list(matched_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'match_percentage': round(match_percentage, 2),
            'total_required': len(required_skill_set),
            'total_matched': len(matched_skills)
        }
