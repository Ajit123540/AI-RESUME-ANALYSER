import re
from typing import List, Dict, Set
from collections import Counter


class KeywordMatcher:
    """Match keywords between resume and job description."""
    
    def __init__(self):
        self.common_stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'this',
            'that', 'these', 'those', 'am', 'as', 'if', 'when', 'then', 'there',
            'here', 'what', 'which', 'who', 'whom', 'whose', 'where', 'why',
            'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'when',
            'where', 'why', 'how', 'about', 'above', 'after', 'again', 'against',
            'below', 'between', 'into', 'through', 'during', 'before', 'under',
            'again', 'further', 'once'
        }
    
    def extract_keywords(self, text: str, min_length: int = 3) -> Set[str]:
        """Extract keywords from text, removing stop words."""
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = {word for word in words 
                   if word not in self.common_stop_words 
                   and len(word) >= min_length}
        
        return keywords
    
    def extract_phrases(self, text: str, phrase_length: int = 2) -> Set[str]:
        """Extract meaningful phrases from text."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        words = [word for word in words if word not in self.common_stop_words]
        
        phrases = set()
        for i in range(len(words) - phrase_length + 1):
            phrase = ' '.join(words[i:i + phrase_length])
            phrases.add(phrase)
        
        return phrases
    
    def calculate_match_score(self, resume_text: str, job_description: str) -> Dict:
        """Calculate keyword match score between resume and job description."""
        # Extract keywords from both texts
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description)
        
        # Extract phrases
        resume_phrases = self.extract_phrases(resume_text)
        job_phrases = self.extract_phrases(job_description)
        
        # Calculate matches
        keyword_matches = resume_keywords & job_keywords
        phrase_matches = resume_phrases & job_phrases
        
        # Calculate scores
        keyword_score = len(keyword_matches) / len(job_keywords) if job_keywords else 0
        phrase_score = len(phrase_matches) / len(job_phrases) if job_phrases else 0
        
        # Combined score (70% keywords, 30% phrases)
        combined_score = (keyword_score * 0.7) + (phrase_score * 0.3)
        
        return {
            'keyword_score': round(keyword_score * 100, 2),
            'phrase_score': round(phrase_score * 100, 2),
            'combined_score': round(combined_score * 100, 2),
            'matched_keywords': list(keyword_matches),
            'matched_phrases': list(phrase_matches),
            'missing_keywords': list(job_keywords - resume_keywords),
            'total_job_keywords': len(job_keywords),
            'total_resume_keywords': len(resume_keywords)
        }
    
    def find_keyword_frequency(self, text: str, keywords: List[str]) -> Dict[str, int]:
        """Find frequency of specific keywords in text."""
        text_lower = text.lower()
        frequency = {}
        
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = re.findall(pattern, text_lower)
            frequency[keyword] = len(matches)
        
        return frequency
