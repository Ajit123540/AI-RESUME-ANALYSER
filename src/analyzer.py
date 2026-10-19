from typing import Dict, List, Optional
from src.parser import ResumeParser
from src.keyword_matcher import KeywordMatcher
from src.skills_extractor import SkillsExtractor
from src.ai_scorer import AIScorer
from src.local_scorer import LocalScorer
from src.intelligence.orchestrator import IntelligenceOrchestrator


class ResumeAnalyzer:
    """Main analyzer orchestrating all resume analysis components."""
    
    def __init__(self, use_ai: bool = True):
        self.parser = ResumeParser()
        self.keyword_matcher = KeywordMatcher()
        self.skills_extractor = SkillsExtractor()
        self.use_ai = use_ai
        self.local_scorer = LocalScorer(self.keyword_matcher.common_stop_words)
        
        # Always create AI scorer for fallback suggestions
        self.ai_scorer = AIScorer()
        
        if use_ai and self.ai_scorer.client:
            self.use_ai = True
            print("AI features enabled")
        else:
            self.use_ai = False
            if self.ai_scorer.error_message:
                print(f"AI features disabled: {self.ai_scorer.error_message}")
            else:
                print("AI features disabled: Rule-based analysis will be used")
    
    def analyze_resume(self, resume_text: str, job_description: str = "", 
                      required_skills: Optional[List[str]] = None,
                      analysis_mode: Optional[str] = None) -> Dict:
        """Perform comprehensive resume analysis."""
        if analysis_mode not in (None, "local", "ai"):
            raise ValueError("analysis_mode must be 'local' or 'ai'")
        use_ai = self.use_ai and analysis_mode != "local"
        selected_mode = "ai" if use_ai else "local"
        
        # Extract skills
        skills_result = self.skills_extractor.extract_skills(resume_text)
        
        # Keyword matching if job description provided
        keyword_result = {}
        if job_description:
            keyword_result = self.keyword_matcher.calculate_match_score(
                resume_text, job_description
            )
        
        # Skills comparison if required skills provided
        skills_comparison = {}
        if required_skills:
            skills_comparison = self.skills_extractor.compare_skills(
                skills_result, required_skills
            )
        
        # AI scoring if enabled and job description provided
        ai_result = {}
        if use_ai and self.ai_scorer and job_description:
            ai_result = self.ai_scorer.score_resume(resume_text, job_description)
            if ai_result.get("error"):
                # OpenAI call failed (e.g., quota exhausted / 429 / offline)
                # Automatically fall back to local scorer so analysis completes cleanly
                job_skills = self.skills_extractor.extract_skills(job_description)
                local_result = self.local_scorer.score_resume(
                    resume_text,
                    job_description,
                    keyword_result,
                    skills_result,
                    required_skills,
                    job_skills
                )
                local_result["openai_error"] = ai_result.get("error")
                local_result["fallback_note"] = (
                    "OpenAI credits exhausted (Error 429). The system automatically completed your analysis using the Local NLP Scorer."
                )
                ai_result = local_result
                selected_mode = "local"
        elif job_description:
            job_skills = self.skills_extractor.extract_skills(job_description)
            ai_result = self.local_scorer.score_resume(
                resume_text,
                job_description,
                keyword_result,
                skills_result,
                required_skills,
                job_skills
            )
        
        # Calculate overall assessment
        overall_assessment = self._calculate_overall_assessment(
            keyword_result, skills_result, skills_comparison, ai_result
        )

        # 14-Module Intelligence Platform Analysis
        intel_platform = IntelligenceOrchestrator.run_full_intelligence(
            resume_text=resume_text,
            job_description=job_description,
            required_skills=required_skills or (skills_comparison.get("missing_skills", []) + skills_comparison.get("matched_skills", [])),
            base_keyword_score=(
                ai_result.get("overall_score", keyword_result.get("combined_score", 0.0))
                if selected_mode == "local"
                else keyword_result.get("combined_score", 0.0)
            ),
            base_ai_result=ai_result
        )
        
        return {
            'skills_analysis': skills_result,
            'keyword_matching': keyword_result,
            'skills_comparison': skills_comparison,
            'ai_analysis': ai_result,
            'analysis_mode': selected_mode,
            'overall_assessment': overall_assessment,
            'intelligence_platform': intel_platform,
            'resume_text_length': len(resume_text),
            'word_count': len(resume_text.split())
        }
    
    def analyze_file(self, file_path: str, job_description: str = "",
                    required_skills: Optional[List[str]] = None,
                    analysis_mode: Optional[str] = None) -> Dict:
        """Analyze resume from file."""
        try:
            resume_text = self.parser.parse_file(file_path)
            result = self.analyze_resume(
                resume_text, job_description, required_skills, analysis_mode
            )
            result['file_name'] = file_path
            result['parse_success'] = True
            return result
        except Exception as e:
            return {
                'file_name': file_path,
                'parse_success': False,
                'error': str(e)
            }
    
    def analyze_uploaded_file(self, file_content: bytes, filename: str,
                            job_description: str = "",
                            required_skills: Optional[List[str]] = None,
                            analysis_mode: Optional[str] = None) -> Dict:
        """Analyze uploaded resume file."""
        try:
            resume_text = self.parser.parse_uploaded_file(file_content, filename)
            result = self.analyze_resume(
                resume_text, job_description, required_skills, analysis_mode
            )
            result['file_name'] = filename
            result['parse_success'] = True
            return result
        except Exception as e:
            return {
                'file_name': filename,
                'parse_success': False,
                'error': str(e)
            }
    
    def batch_analyze(self, file_paths: List[str], job_description: str = "",
                     required_skills: Optional[List[str]] = None,
                     analysis_mode: Optional[str] = None) -> List[Dict]:
        """Analyze multiple resume files."""
        results = []
        
        for file_path in file_paths:
            result = self.analyze_file(
                file_path, job_description, required_skills, analysis_mode
            )
            results.append(result)
        
        # AI ranking if enabled
        use_ai = self.use_ai and analysis_mode != "local"
        if use_ai and self.ai_scorer and job_description:
            try:
                # Prepare data for AI ranking
                resumes_for_ranking = []
                for result in results:
                    if result.get('parse_success'):
                        resumes_for_ranking.append({
                            'name': result.get('file_name', 'Unknown'),
                            'text': result.get('resume_text', '')
                        })
                
                if resumes_for_ranking:
                    ranked_results = self.ai_scorer.rank_resumes(
                        resumes_for_ranking, job_description
                    )
                    
                    # Merge AI ranking with existing results
                    ranked_dict = {r['name']: r for r in ranked_results}
                    for result in results:
                        if result.get('parse_success'):
                            file_name = result.get('file_name')
                            if file_name in ranked_dict:
                                result['ai_ranking'] = ranked_dict[file_name]
            except Exception as e:
                print(f"AI ranking failed: {e}")
        elif job_description and not use_ai:
            successful = [r for r in results if r.get('parse_success')]
            failed = [r for r in results if not r.get('parse_success')]
            successful.sort(
                key=lambda result: result.get('ai_analysis', {}).get('overall_score', 0),
                reverse=True
            )
            for rank, result in enumerate(successful, 1):
                result['local_ranking'] = {
                    'rank': rank,
                    'score': result.get('ai_analysis', {}).get('overall_score', 0),
                    'method': 'TF-IDF, keyword, and skill-match score'
                }
            results = successful + failed
        
        return results
    
    def get_improvement_suggestions(self, resume_text: str, 
                                   job_description: str,
                                   analysis_mode: Optional[str] = None) -> Dict:
        """Get improvement suggestions (AI-powered or rule-based)."""
        if analysis_mode not in (None, "local", "ai"):
            raise ValueError("analysis_mode must be 'local' or 'ai'")
        if self.ai_scorer:
            return self.ai_scorer.get_improvement_suggestions(
                resume_text,
                job_description,
                use_ai=self.use_ai and analysis_mode == "ai"
            )
        else:
            # Provide basic suggestions when AI scorer is not available
            return {
                'error': 'AI scorer not initialized'
            }
    
    def compare_resumes(self, resume1_path: str, resume2_path: str,
                       job_description: str) -> Dict:
        """Compare two resumes using AI."""
        if not (self.use_ai and self.ai_scorer):
            return {
                'error': 'AI scoring not enabled or available'
            }
        
        try:
            resume1_text = self.parser.parse_file(resume1_path)
            resume2_text = self.parser.parse_file(resume2_path)
            
            return self.ai_scorer.compare_resumes(
                resume1_text, resume2_text, job_description
            )
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def _calculate_overall_assessment(self, keyword_result: Dict,
                                     skills_result: Dict,
                                     skills_comparison: Dict,
                                     ai_result: Dict) -> Dict:
        """Calculate overall assessment from all components."""
        
        assessment = {
            'strengths': [],
            'weaknesses': [],
            'recommendation': 'Consider',
            'confidence_score': 0
        }
        
        # Extract strengths from skills
        if skills_result.get('categorized'):
            for category, skills in skills_result['categorized'].items():
                if skills:
                    assessment['strengths'].append(
                        f"Strong {category} background ({len(skills)} skills)"
                    )
        
        # Extract from keyword matching
        if keyword_result:
            score = keyword_result.get('combined_score', 0)
            if score > 70:
                assessment['strengths'].append(
                    f"Excellent keyword match ({score}%)"
                )
            elif score < 40:
                assessment['weaknesses'].append(
                    f"Low keyword match ({score}%)"
                )
        
        # Extract from skills comparison
        if skills_comparison:
            match_pct = skills_comparison.get('match_percentage', 0)
            if match_pct > 70:
                assessment['strengths'].append(
                    f"High required skills match ({match_pct}%)"
                )
            elif match_pct < 40:
                assessment['weaknesses'].append(
                    f"Missing many required skills ({match_pct}% match)"
                )
        
        # Use AI assessment if available
        if ai_result and not ai_result.get('error'):
            assessment['recommendation'] = ai_result.get('recommendation', 'Consider')
            assessment['confidence_score'] = ai_result.get('overall_score', 0)
            
            # Add AI insights
            if ai_result.get('strengths'):
                assessment['strengths'].extend(ai_result['strengths'])
            if ai_result.get('weaknesses'):
                assessment['weaknesses'].extend(ai_result['weaknesses'])
        else:
            # Calculate simple confidence score without AI
            confidence = 0
            if keyword_result:
                confidence += keyword_result.get('combined_score', 0) * 0.4
            if skills_comparison:
                confidence += skills_comparison.get('match_percentage', 0) * 0.3
            if skills_result.get('skill_count', 0) > 5:
                confidence += 20
            
            assessment['confidence_score'] = min(confidence, 100)
            
            # Set recommendation based on confidence
            if assessment['confidence_score'] >= 70:
                assessment['recommendation'] = 'Recommend'
            elif assessment['confidence_score'] >= 50:
                assessment['recommendation'] = 'Consider'
            else:
                assessment['recommendation'] = 'Do Not Recommend'
        
        return assessment

    def verify_github_evidence(self, username_or_url: str, resume_text: str = "") -> Dict:
        """Evaluate candidate code evidence directly against live GitHub repositories."""
        from src.intelligence.github_verifier import GitHubCodeVerifier
        return GitHubCodeVerifier.evaluate_evidence(username_or_url, resume_text)

    def rebuild_ats_friendly_resume(self, resume_text: str, job_description: str = "", use_ai: bool = False) -> Dict:
        """Audit resume errors and rebuild a complete, 100% ATS-friendly resume."""
        from src.intelligence.ats_rebuilder import ATSResumeRebuilder
        return ATSResumeRebuilder.rebuild_ats_resume(resume_text, job_description, use_ai=use_ai)


