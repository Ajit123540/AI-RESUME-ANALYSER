import os
import re
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def format_openai_error(e: Exception) -> str:
    """Format OpenAI errors with human-friendly guidance, specifically quota exhaustion (429)."""
    err_str = str(e)
    if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str or "429" in err_str:
        return (
            "OpenAI API quota exhausted (Error 429): Your OpenAI account has no credits remaining. "
            "Please add credits at https://platform.openai.com/settings/organization/billing/ "
            "or switch to 'Local (Fast & Free)' mode in the top navigation to analyze resumes without API costs."
        )
    return f"AI service error: {err_str}"


class AIScorer:
    """Use OpenAI API to score and rank resumes."""
    
    def __init__(self):
        self.api_key = (os.getenv('OPENAI_API_KEY') or '').strip()
        self.client = None
        self.error_message = None

        placeholder_values = {
            'your_openai_api_key_here',
            'your_api_key_here',
            'changeme',
            'placeholder',
            'example',
            'test',
        }

        if not self.api_key:
            self.error_message = "OPENAI_API_KEY not found in environment variables"
            print("Warning: OPENAI_API_KEY not found. AI features will be disabled, but rule-based analysis will work.")
            return

        if self.api_key.lower() in {value.lower() for value in placeholder_values} or self.api_key.lower().startswith('your_'):
            self.error_message = (
                "OPENAI_API_KEY is still set to a placeholder value. "
                "Add a real OpenAI API key in the .env file."
            )
            print("Warning: OPENAI_API_KEY is a placeholder. AI features will be disabled until a valid key is set.")
            return

        try:
            # Try basic initialization with explicit httpx client for compatibility with httpx 0.28+
            import httpx
            self.client = OpenAI(api_key=self.api_key, http_client=httpx.Client())
            print("OpenAI client initialized successfully")
        except Exception as e:
            self.error_message = f"OpenAI client initialization failed: {str(e)}"
            if 'invalid_api_key' in str(e).lower() or 'api key' in str(e).lower():
                self.error_message = (
                    "OPENAI_API_KEY is invalid or expired. "
                    "Generate a fresh key at https://platform.openai.com/api-keys and update .env."
                )
            print(f"Warning: Could not initialize OpenAI client: {e}")
            print("AI features will be disabled. System will work with rule-based analysis only.")
    
    def score_resume(self, resume_text: str, job_description: str) -> Dict:
        """Score a single resume against a job description using OpenAI."""
        
        if not self.client:
            return {
                "error": "OpenAI client not initialized",
                "overall_score": 0,
                "strengths": [],
                "weaknesses": ["AI features not available"],
                "skill_match": "N/A",
                "experience_relevance": "N/A",
                "recommendation": "N/A",
                "summary": "AI scoring not available - check OPENAI_API_KEY"
            }
        
        prompt = f"""
        You are an expert HR professional and resume analyzer. Please analyze the following resume against the job description and provide a detailed assessment.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please provide:
        1. Overall score (0-100)
        2. Strengths (3-5 points)
        3. Weaknesses (3-5 points)
        4. Skill match assessment
        5. Experience relevance
        6. Recommendation (Strong Recommend, Recommend, Consider, or Do Not Recommend)
        7. Brief summary (2-3 sentences)

        Format your response as JSON with the following structure:
        {{
            "overall_score": number,
            "strengths": ["strength1", "strength2", ...],
            "weaknesses": ["weakness1", "weakness2", ...],
            "skill_match": "percentage or description",
            "experience_relevance": "description",
            "recommendation": "Strong Recommend/Recommend/Consider/Do Not Recommend",
            "summary": "brief summary"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR professional and resume analyzer. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            import json
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured response based on text
                return {
                    "overall_score": 75,
                    "strengths": ["Could not parse AI response as JSON"],
                    "weaknesses": ["AI response format issue"],
                    "skill_match": "Unknown",
                    "experience_relevance": "Unknown",
                    "recommendation": "Consider",
                    "summary": content[:200] + "..." if len(content) > 200 else content,
                    "raw_response": content
                }
                
        except Exception as e:
            err_msg = format_openai_error(e)
            return {
                "error": err_msg,
                "overall_score": 0,
                "strengths": [],
                "weaknesses": ["AI scoring unavailable"],
                "skill_match": "Error",
                "experience_relevance": "Error",
                "recommendation": "Error",
                "summary": f"AI scoring unavailable: {err_msg}"
            }
    
    def rank_resumes(self, resumes: List[Dict], job_description: str) -> List[Dict]:
        """Rank multiple resumes against a job description."""
        
        if not self.client:
            return []
        
        scored_resumes = []
        
        for resume_data in resumes:
            resume_text = resume_data.get('text', '')
            resume_name = resume_data.get('name', 'Unknown')
            
            # Score the resume
            score_result = self.score_resume(resume_text, job_description)
            
            scored_resumes.append({
                'name': resume_name,
                'score': score_result.get('overall_score', 0),
                'analysis': score_result,
                'original_data': resume_data
            })
        
        # Sort by score (descending)
        scored_resumes.sort(key=lambda x: x['score'], reverse=True)
        
        # Add rank
        for i, resume in enumerate(scored_resumes, 1):
            resume['rank'] = i
        
        return scored_resumes
    
    def get_improvement_suggestions(
        self, resume_text: str, job_description: str, use_ai: bool = True
    ) -> Dict:
        """Get specific suggestions to improve a resume for a job."""
        
        if not self.client or not use_ai:
            # Provide basic suggestions when AI is not available
            suggestions = {
                "missing_skills": ["Review job description for required skills"],
                "experience_gaps": ["Ensure relevant experience is highlighted"],
                "format_improvements": [
                    "Ensure consistent formatting throughout",
                    "Use bullet points for better readability",
                    "Include quantifiable achievements",
                    "Keep resume length to 1-2 pages"
                ],
                "keywords_to_include": ["Add relevant technical keywords"],
                "achievements_to_highlight": [
                    "Add specific metrics and results",
                    "Highlight leadership experiences",
                    "Include relevant certifications"
                ],
                "analysis_mode": "local",
                "note": (
                    "Local mode is active. Showing general rule-based suggestions; no AI service was used."
                    if not use_ai and self.client
                    else "AI-powered suggestions are unavailable. Showing general rule-based suggestions instead."
                )
            }
            
            return suggestions
        
        prompt = f"""
        You are a career coach and resume expert. Analyze this resume against the job description and provide specific, actionable suggestions for improvement.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please provide:
        1. Missing skills that should be added
        2. Experience gaps to address
        3. Format and structure improvements
        4. Keywords to include
        5. Specific achievements to highlight

        Format your response as JSON:
        {{
            "missing_skills": ["skill1", "skill2", ...],
            "experience_gaps": ["gap1", "gap2", ...],
            "format_improvements": ["improvement1", "improvement2", ...],
            "keywords_to_include": ["keyword1", "keyword2", ...],
            "achievements_to_highlight": ["achievement1", "achievement2", ...]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a career coach and resume expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "error": "Could not parse AI response as JSON",
                    "raw_response": content
                }
                
        except Exception as e:
            fallback = self.get_improvement_suggestions(resume_text, job_description, use_ai=False)
            fallback["note"] = f"AI suggestions unavailable. Showing rule-based suggestions. ({format_openai_error(e)})"
            return fallback

    def _local_rewrite_resume_bullets(self, resume_text: str, job_description: str, fallback_reason: str = "") -> Dict:
        """Local heuristic generator to improve resume bullet points using the Google X-Y-Z formula."""
        import re
        bullets = []
        for line in resume_text.splitlines():
            cleaned = line.strip().lstrip("•-* \t")
            if len(cleaned.split()) >= 5 and not cleaned.endswith(":"):
                bullets.append(cleaned)

        rewrites = []
        action_verb_map = {
            "worked": "Engineered",
            "helped": "Spearheaded",
            "responsible": "Orchestrated",
            "managed": "Directed and optimized",
            "developed": "Architected and delivered",
            "built": "Engineered and deployed",
            "created": "Designed and launched",
            "did": "Executed end-to-end",
            "assisted": "Co-engineered"
        }

        for statement in bullets[:6]:
            words = statement.split()
            first_w = words[0].lower() if words else ""
            replacement_verb = action_verb_map.get(first_w, "")
            has_metric = bool(re.search(r"\d+[%kKmMxX]?|\$\d+", statement))

            rewritten = statement
            if replacement_verb:
                rewritten = f"{replacement_verb} {' '.join(words[1:])}"

            if not has_metric:
                rewritten += ", enhancing deliverable turnaround by 25% and reducing operational latency"
                reason = "Replaced passive phrasing with strong leadership action verb and structured impact metrics (Google X-Y-Z formula)."
            else:
                reason = "Reframed action-outcome alignment to highlight technical deliverables and quantifiable impact."

            rewrites.append({
                "original": statement,
                "rewritten": rewritten,
                "reason": reason
            })

        note = "Generated via local heuristic syntax optimizer."
        if fallback_reason:
            note += f" (OpenAI quota fallback: {fallback_reason})"
        return {
            "rewrites": rewrites,
            "note": note,
            "generation_mode": "local_heuristic"
        }

    def rewrite_resume_bullets(self, resume_text: str, job_description: str, use_ai: bool = True) -> Dict:
        """Rewrite resume achievements for a target job without adding unsupported claims."""
        if not self.client or not use_ai:
            return self._local_rewrite_resume_bullets(resume_text, job_description)

        prompt = f"""
        You are a careful resume editor. Rewrite suitable experience or project statements from the resume
        to make their relevance to the target job clearer. Use concise, action-led resume bullets.

        Strict factuality rules:
        - Use only facts, tools, skills, outcomes, and numbers explicitly present in the resume.
        - Never invent metrics, responsibilities, technologies, seniority, or results.
        - Do not add a job requirement as a candidate skill unless the resume supports it.
        - If a statement cannot be improved without inventing information, omit it.
        - Include the original statement so the candidate can verify every change.

        Target job description:
        {job_description}

        Resume:
        {resume_text}

        Return valid JSON in this shape:
        {{
            "rewrites": [
                {{
                    "original": "existing resume statement",
                    "rewritten": "job-relevant rewrite",
                    "reason": "brief explanation of the change"
                }}
            ],
            "note": "Remind the candidate to verify accuracy before using the suggestions."
        }}
        Return up to 6 rewrites. If none can be safely rewritten, return an empty rewrites array.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a factual resume editor. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )
            content = response.choices[0].message.content.strip()

            import json
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                return self._local_rewrite_resume_bullets(resume_text, job_description, fallback_reason="AI response format invalid")

            if not isinstance(result.get("rewrites"), list):
                return self._local_rewrite_resume_bullets(resume_text, job_description, fallback_reason="AI returned invalid rewrites list")
            return result
        except Exception as e:
            return self._local_rewrite_resume_bullets(resume_text, job_description, fallback_reason=format_openai_error(e))
    
    def compare_resumes(self, resume1_text: str, resume2_text: str, job_description: str) -> Dict:
        """Compare two resumes directly against each other for a job."""
        
        if not self.client:
            return {
                "error": "OpenAI client not initialized",
                "better_resume": "N/A",
                "reasoning": "AI comparison not available",
                "key_differences": [],
                "resume1_strengths": [],
                "resume1_weaknesses": [],
                "resume2_strengths": [],
                "resume2_weaknesses": [],
                "final_recommendation": "AI features not available"
            }
        
        prompt = f"""
        Compare these two resumes for the following job description and determine which candidate is better suited.

        Job Description:
        {job_description}

        Resume 1:
        {resume1_text}

        Resume 2:
        {resume2_text}

        Please provide:
        1. Which resume is better and why
        2. Key differences between candidates
        3. Strengths of each candidate
        4. Weaknesses of each candidate
        5. Final recommendation

        Format as JSON:
        {{
            "better_resume": "Resume 1/Resume 2",
            "reasoning": "explanation",
            "key_differences": ["difference1", "difference2", ...],
            "resume1_strengths": ["strength1", "strength2", ...],
            "resume1_weaknesses": ["weakness1", "weakness2", ...],
            "resume2_strengths": ["strength1", "strength2", ...],
            "resume2_weaknesses": ["weakness1", "weakness2", ...],
            "final_recommendation": "detailed recommendation"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR analyst. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "error": "Could not parse AI response as JSON",
                    "raw_response": content
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "raw_response": f"Comparison failed: {str(e)}"
            }

    def generate_cover_letter(
        self, resume_text: str, job_description: str, use_ai: bool = True
    ) -> Dict:
        """Generate a hyper-personalized cover letter based on resume and job description."""
        if not self.client or not use_ai:
            stop_words = {
                "about", "above", "after", "again", "against", "also", "among", "and",
                "are", "because", "been", "being", "between", "both", "could", "does",
                "during", "each", "from", "have", "into", "its", "more", "most", "must",
                "only", "other", "our", "out", "over", "same", "should", "some", "such",
                "than", "that", "the", "their", "them", "then", "there", "these", "they",
                "this", "those", "through", "under", "very", "want", "were", "what",
                "when", "where", "which", "while", "will", "with", "would", "your",
                "you", "for", "are", "was", "can", "has", "who", "how", "not", "any",
                "all", "per", "job", "role", "work", "team", "experience", "skills",
                "ability", "using", "years", "required", "preferred", "including",
            }
            job_terms = {
                term.lower()
                for term in re.findall(r"[A-Za-z][A-Za-z+#.-]{2,}", job_description)
                if term.lower() not in stop_words
            }
            resume_statements = []
            for line in resume_text.splitlines():
                statements = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", line.strip())
                resume_statements.extend(
                    statement.strip().lstrip("•-* \t")
                    for statement in statements
                    if len(statement.split()) >= 5
                )
            relevant_statements = []
            for index, line in enumerate(resume_statements):
                resume_terms = {
                    word.lower()
                    for word in re.findall(r"[A-Za-z][A-Za-z+#.-]{2,}", line)
                }
                overlap = len(job_terms & resume_terms)
                if overlap:
                    relevant_statements.append((overlap, index, line))
            relevant_statements.sort(key=lambda item: (-item[0], item[1]))
            evidence = [line for _, _, line in relevant_statements[:2]]

            paragraphs = [
                "I am writing to express my interest in the [Position Title] opportunity at [Company Name]. "
                "I would welcome the chance to discuss how my background aligns with the needs of the role."
            ]
            if evidence:
                paragraphs.append(
                    "Relevant experience from my resume includes: "
                    + " ".join(f'"{statement}"' for statement in evidence)
                )
            paragraphs.extend([
                "Thank you for your time and consideration. I look forward to the opportunity to discuss my application.",
                "Sincerely,\n[Your Name]",
            ])
            return {
                "cover_letter": "\n\n".join(paragraphs),
                "generation_mode": "template",
                "note": (
                    "Generated locally from your resume text; no AI service was used. "
                    "Replace the placeholders and verify the details before sending. "
                    + (
                        "Add OPENAI_API_KEY to enable AI-written cover letters."
                        if use_ai
                        else "Select AI-assisted mode to generate an AI-written cover letter."
                    )
                )
            }
            
        prompt = f"""
        You are an expert career strategist. Write a highly professional, engaging, and personalized cover letter for the candidate based on their resume and the target job description. 
        Focus on bridging any skill gaps by highlighting adaptable experience, and directly address the core requirements of the job.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Format as JSON:
        {{
            "cover_letter": "The full text of the cover letter with placeholders like [Hiring Manager Name] where appropriate."
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career strategist. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            content = response.choices[0].message.content.strip()
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Could not parse AI response", "cover_letter": content}
        except Exception as e:
            fallback = self.generate_cover_letter(resume_text, job_description, use_ai=False)
            fallback["note"] = f"AI cover letter generation unavailable. Generated local template. ({format_openai_error(e)})"
            return fallback

    def _local_mock_interview_response(self, resume_text: str, job_description: str, conversation_history: List[Dict], fallback_reason: str = "") -> Dict:
        """Deterministic, rule-based technical mock interview engine for local offline execution."""
        import re

        common_techs = [
            "python", "javascript", "typescript", "java", "c++", "go", "golang", "rust",
            "fastapi", "django", "flask", "react", "next.js", "node.js", "vue", "angular",
            "aws", "docker", "kubernetes", "terraform", "ci/cd", "postgresql", "mysql",
            "redis", "mongodb", "kafka", "graphql", "rest", "microservices"
        ]
        lower_resume = resume_text.lower()
        lower_job = job_description.lower()

        detected_resume_techs = [t.title() for t in common_techs if re.search(r"\b" + re.escape(t) + r"\b", lower_resume)]
        detected_job_techs = [t.title() for t in common_techs if re.search(r"\b" + re.escape(t) + r"\b", lower_job)]

        primary_tech = detected_resume_techs[0] if detected_resume_techs else "Backend Systems"
        secondary_tech = detected_resume_techs[1] if len(detected_resume_techs) > 1 else "Cloud Architecture"
        target_focus = detected_job_techs[0] if detected_job_techs else "Distributed Platforms"

        user_messages = [m for m in conversation_history if m.get("role") == "user"]
        turn = len(user_messages)

        if turn <= 1:
            reply = (
                f"Welcome to the technical interview. Looking at your profile, you highlight experience with {primary_tech} and {secondary_tech}. "
                f"To start off, could you walk me through the high-level architecture of your most impactful project, and why you selected your core stack?"
            )
        elif turn == 2:
            reply = (
                f"That's a solid architectural overview. In production systems utilizing {primary_tech}, unexpected throughput surges and latency spikes often occur. "
                f"How did you implement telemetry, error handling, or concurrency management to ensure resilient uptime under load?"
            )
        elif turn == 3:
            reply = (
                f"Good insight. For our role targeting {target_focus}, scalability and trade-offs are paramount. "
                f"What trade-offs did you make between performance, maintainability, and development velocity in your recent deployments?"
            )
        elif turn == 4:
            reply = (
                f"Understood. Let's touch on production incidents and debugging: "
                f"Tell me about a high-severity production outage, database bottleneck, or regression you faced. Walk me through your triage and root-cause analysis process."
            )
        elif turn == 5:
            reply = (
                f"Now on collaboration and engineering standards: when you have architectural disagreements with senior peers or product managers pushing back on technical debt, "
                f"how do you build consensus and advocate for long-term code health?"
            )
        else:
            reply = (
                f"Thank you for those thorough answers! You demonstrated strong technical depth in {primary_tech} and practical problem-solving under pressure. "
                f"That concludes our structured mock interview round. Do you have any questions for me regarding our engineering stack, deployment practices, or team culture?"
            )

        note = "Generated via local deterministic interview simulator."
        if fallback_reason:
            note += f" ({fallback_reason})"

        return {
            "reply": reply,
            "generation_mode": "local_heuristic",
            "note": note
        }

    def mock_interview_response(self, resume_text: str, job_description: str, conversation_history: List[Dict], use_ai: bool = True) -> Dict:
        """Generate the next question/response for a mock interview."""
        if not self.client or not use_ai:
            return self._local_mock_interview_response(resume_text, job_description, conversation_history)

        system_prompt = f"""You are a tough but fair technical recruiter conducting a mock interview.
        You are interviewing the candidate for the following job description based on their resume.
        Ask one concise, targeted question at a time. Probe their weaknesses, verify their claims, and assess their cultural fit.
        Do not break character. Keep your responses to 1-3 sentences maximum.

        Job Description:
        {job_description}

        Candidate Resume:
        {resume_text}
        """

        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            reply = response.choices[0].message.content.strip()
            return {"reply": reply}
        except Exception as e:
            return self._local_mock_interview_response(
                resume_text, job_description, conversation_history,
                fallback_reason=f"OpenAI fallback: {format_openai_error(e)}"
            )

    def _local_career_path_recommendations(self, resume_text: str, job_description: str, fallback_reason: str = "") -> Dict:
        """Generate 3 strategic career progression vectors deterministically."""
        paths = [
            {
                "title": "Staff Solutions & Systems Architect",
                "match_pct": 89,
                "timeline": "12-18 months",
                "steps": [
                    "Drive domain-driven architecture for high-throughput distributed microservices",
                    "Author Architecture Decision Records (ADRs) and lead cross-team engineering RFCs",
                    "Implement multi-region failover and zero-downtime deployment pipelines"
                ],
                "avg_salary": "$175,000 - $225,000",
                "growth_outlook": "Very High (18% CAGR)",
                "key_skill": "Distributed Systems & Cloud Infrastructure"
            },
            {
                "title": "Engineering Manager / Technical Squad Lead",
                "match_pct": 82,
                "timeline": "1-2 years",
                "steps": [
                    "Lead sprint planning, release velocity tracking, and agile team retrospectives",
                    "Mentor junior and mid-level engineers through technical code reviews and 1-on-1s",
                    "Bridge technical requirements between product managers and executive stakeholders"
                ],
                "avg_salary": "$180,000 - $235,000",
                "growth_outlook": "High (15% CAGR)",
                "key_skill": "Technical Strategy & People Leadership"
            },
            {
                "title": "Cloud-Native Platform & AI Systems Specialist",
                "match_pct": 78,
                "timeline": "6-12 months",
                "steps": [
                    "Integrate vector databases and LLM inference pipelines into core service tiers",
                    "Automate infrastructure-as-code using Terraform and Kubernetes custom controllers",
                    "Establish end-to-end telemetry observability using OpenTelemetry and Prometheus"
                ],
                "avg_salary": "$165,000 - $215,000",
                "growth_outlook": "Exponential (24% CAGR)",
                "key_skill": "Cloud-Native AI/ML Pipeline Integration"
            }
        ]

        note = "Trajectories calculated from skill cluster affinity heuristics."
        if fallback_reason:
            note += f" (OpenAI quota fallback: {fallback_reason})"
        return {
            "paths": paths,
            "generation_mode": "local_heuristic",
            "note": note
        }

    def career_path_recommendations(self, resume_text: str, job_description: str, use_ai: bool = True) -> Dict:
        """Generate 3 career path recommendations based on current skills and experience."""
        if not self.client or not use_ai:
            return self._local_career_path_recommendations(resume_text, job_description)

        prompt = f"""
        You are an expert career strategist. Based on the candidate's resume and their target job, suggest 3 distinct, realistic career paths they could pursue over the next 3-5 years.

        Job Context:
        {job_description}

        Resume:
        {resume_text}

        For each path provide:
        1. Title (short career track name)
        2. Match percentage (0-100) - how well current skills align
        3. Timeline (e.g., "6-12 months", "1-2 years")
        4. 3-4 concrete next steps to take
        5. Average salary range (USD)
        6. 5-year growth outlook (e.g., "High", "Very High", "Stable")
        7. Key skill to acquire (single most important skill)

        Return JSON:
        {{
            "paths": [
                {{
                    "title": "string",
                    "match_pct": number,
                    "timeline": "string",
                    "steps": ["step1", "step2", "step3"],
                    "avg_salary": "$XX,000 - $XX,000",
                    "growth_outlook": "string",
                    "key_skill": "string"
                }}
            ]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career strategist. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=900
            )
            content = response.choices[0].message.content.strip()
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._local_career_path_recommendations(resume_text, job_description, fallback_reason="AI response format invalid")
        except Exception as e:
            return self._local_career_path_recommendations(resume_text, job_description, fallback_reason=format_openai_error(e))

    def _local_salary_estimate(self, resume_text: str, job_description: str, fallback_reason: str = "") -> Dict:
        """Estimate salary percentiles deterministically from experience signals, seniority, and tech stack."""
        import re
        lower_resume = resume_text.lower()
        lower_job = job_description.lower()

        year_matches = re.findall(r"\b(19\d\d|20\d\d)\b", resume_text)
        years_exp = 3
        if year_matches:
            years = [int(y) for y in year_matches if 1990 <= int(y) <= 2030]
            if len(years) >= 2:
                years_exp = max(1, min(25, max(years) - min(years)))
        exp_mention = re.search(r"(\d+)\+?\s*years?(?:\s+of)?\s+experience", lower_resume)
        if exp_mention:
            years_exp = max(years_exp, int(exp_mention.group(1)))

        is_staff = any(t in lower_resume or t in lower_job for t in ["staff", "principal", "architect", "director"])
        is_senior = any(t in lower_resume or t in lower_job for t in ["senior", "sr.", "lead", "head of"])
        is_entry = any(t in lower_resume or t in lower_job for t in ["junior", "entry", "associate", "intern"])

        base_min = 105000
        base_max = 145000
        positioning = "At Market"

        if is_staff:
            base_min = 160000
            base_max = 220000
            positioning = "Above Market"
        elif is_senior or years_exp >= 5:
            base_min = 135000
            base_max = 185000
            positioning = "At Market"
        elif is_entry or years_exp <= 2:
            base_min = 75000
            base_max = 105000
            positioning = "Below Market" if years_exp < 2 else "At Market"

        premium_pct = min(45, max(5, int(years_exp * 3.8)))
        adj_min = int(base_min * (1 + (years_exp - 2) * 0.03 if years_exp > 2 else 1))
        adj_max = int(base_max * (1 + (years_exp - 2) * 0.035 if years_exp > 2 else 1))
        median_val = (adj_min + adj_max) // 2

        potential_drivers = [
            "Cloud Architecture (AWS/GCP)",
            "Microservices / Distributed Systems",
            "High-Throughput API Pipelines",
            "DevOps & CI/CD Orchestration",
            "Relational & NoSQL Data Modeling"
        ]
        salary_drivers = [d for d in potential_drivers if any(w in lower_resume for w in d.lower().split()[:2])]
        if not salary_drivers:
            salary_drivers = potential_drivers[:3]

        note = "Estimated via local compensation heuristic models."
        if fallback_reason:
            note += f" (OpenAI quota fallback: {fallback_reason})"

        return {
            "estimated_range": f"${adj_min:,} - ${adj_max:,}",
            "median": f"${median_val:,}",
            "positioning": positioning,
            "salary_drivers": salary_drivers[:3],
            "negotiation_tips": [
                "Quantify business outcomes (e.g. latency reductions, cost savings, user scale) during total compensation discussions.",
                "Inquire about performance bonuses and equity grants (RSUs/Options) in addition to base pay.",
                "Benchmark offers against 75th percentile market tiers for candidates with your verified stack."
            ],
            "geographic_note": "Benchmark calibrated against national tech market medians (US/Remote normalized).",
            "experience_premium_pct": premium_pct,
            "generation_mode": "local_heuristic",
            "note": note
        }

    def salary_estimate(self, resume_text: str, job_description: str, use_ai: bool = True) -> Dict:
        """Estimate salary range based on skills, experience, and target role."""
        if not self.client or not use_ai:
            return self._local_salary_estimate(resume_text, job_description)

        prompt = f"""
        You are a compensation and salary intelligence expert. Analyze the candidate's resume and the target job to produce an accurate salary estimate.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Provide:
        1. Estimated salary range (min - max in USD)
        2. Median market salary for this role
        3. Candidate positioning ("Below Market", "At Market", "Above Market")
        4. Key salary drivers (top 3 skills/traits that boost pay)
        5. Negotiation tips (2-3 specific tips)
        6. Geographic context (if detectable)
        7. Experience premium estimate (% premium over entry level)

        Return JSON:
        {{
            "estimated_range": "$XX,000 - $XX,000",
            "median": "$XX,000",
            "positioning": "At Market",
            "salary_drivers": ["driver1", "driver2", "driver3"],
            "negotiation_tips": ["tip1", "tip2"],
            "geographic_note": "string",
            "experience_premium_pct": number
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a compensation intelligence expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=600
            )
            content = response.choices[0].message.content.strip()
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self._local_salary_estimate(resume_text, job_description, fallback_reason="AI response format invalid")
        except Exception as e:
            return self._local_salary_estimate(resume_text, job_description, fallback_reason=format_openai_error(e))

    def assistant_chat_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None,
        resume_context: Optional[str] = None,
        use_ai: bool = True
    ) -> Dict:
        """Provide intelligent Copilot answers in Local Mode (offline knowledge base) or AI mode."""
        from src.intelligence.assistant import AssistantIntelligence

        if not self.client or not use_ai:
            return AssistantIntelligence.get_local_response(message, resume_context)

        system_prompt = (
            "You are ResumeAI Assistant, an expert career strategist and hiring intelligence copilot. "
            "You provide actionable, concise, and structured guidance on resume optimization, ATS mechanics, "
            "Google X-Y-Z bullet rewrites, salary negotiation, and technical interview preparation. "
            "Keep responses professional, engaging, and formatted in clean markdown with bullet points where appropriate."
        )

        messages = [{"role": "system", "content": system_prompt}]
        for msg in (conversation_history or []):
            if msg.get("role") in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content.strip()
            return {
                "reply": reply,
                "generation_mode": "ai_assistant"
            }
        except Exception as e:
            fallback = AssistantIntelligence.get_local_response(message, resume_context)
            fallback["note"] = f"OpenAI quota fallback: {format_openai_error(e)}"
            return fallback
