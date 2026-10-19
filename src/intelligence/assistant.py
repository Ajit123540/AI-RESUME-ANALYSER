import re
from typing import Dict, List, Optional


class AssistantIntelligence:
    """Intelligent Career & Resume Copilot providing deep domain answers offline (Local Mode)

    and via external LLM with automatic graceful fallback.
    """

    KNOWLEDGE_BASE = [
        {
            "intent": "ats_optimization",
            "keywords": ["ats", "applicant tracking", "pass ats", "beat ats", "scanner", "parseability", "ats score"],
            "title": "ATS Optimization Best Practices",
            "reply": """To maximize ATS (Applicant Tracking System) pass rates:
1. **Clean Formatting**: Use a single-column layout. Avoid tables, text boxes, headers/footers, and embedded icons that parser engines (Workday, Taleo, Greenhouse) strip out.
2. **Standard Section Headers**: Use universal titles: `Work Experience`, `Education`, `Skills`, and `Projects`. Unconventional titles like *"Where I've Been"* cause parsing drops.
3. **Exact Keyword Alignment**: Mirror high-priority technical skills and methodologies from the job description naturally in your bullet points.
4. **Quantified Metrics**: Ensure at least 30% of your experience bullets contain measurable metrics (%, $, latency, throughput, scale).
5. **File Format**: Standard PDF is universally accepted, but DOCX is safest for older legacy systems. Keep file size under 5 MB."""
        },
        {
            "intent": "scoring_explanation",
            "keywords": ["match score", "how is score calculated", "scoring formula", "tf-idf", "tfidf", "algorithm", "rubric"],
            "title": "ResumeAI Scoring Methodology",
            "reply": """ResumeAI scores candidates deterministically using a 3-pillar explainable rubric:
1. **Keyword Overlap (40% Weight)**: Normalized frequency match between candidate competencies and job requirements.
2. **TF-IDF Semantic Similarity (40% Weight)**: Term Frequency-Inverse Document Frequency cosine vector similarity, measuring contextual alignment beyond exact keyword matches.
3. **Required Skills Coverage (20% Weight)**: Verification of mandatory qualifying tools specified by the recruiter.

In Local Mode, this runs 100% on your machine using spaCy NLP and mathematical vector geometry — zero external APIs, zero cost, and 100% data privacy."""
        },
        {
            "intent": "bullet_points",
            "keywords": ["bullet", "bullet point", "x-y-z", "xyz", "action verb", "improve bullet", "rewrite bullet", "resume writing"],
            "title": "Google X-Y-Z Resume Bullet Formula",
            "reply": """Top tech companies (including Google) recommend the **X-Y-Z Formula**:
> *"Accomplished [X], as measured by [Y], by doing [Z]"*

- **Weak**: *"Worked on microservices for data processing."*
- **Strong (X-Y-Z)**: *"Architected a high-throughput telemetry microservice in Python and FastAPI [Z], processing 85,000 events/sec with sub-20ms latency [Y], reducing infrastructure costs by 34% [X]."*

**Key Rules**:
- Begin every bullet with a decisive past-tense leadership verb (*Spearheaded, Engineered, Orchestrated, Automated*).
- Never start with passive phrases like *"Responsible for"* or *"Helped with"*."""
        },
        {
            "intent": "salary_negotiation",
            "keywords": ["salary", "negotiate", "compensation", "offer", "counteroffer", "pay", "raise", "equity", "rsu"],
            "title": "Strategic Compensation Negotiation",
            "reply": """Key tactics for negotiating top-tier compensation:
1. **Anchor with Market Percentiles**: Never disclose current pay or give the first number. Ask: *"What is the budgeted compensation band for this role at the 75th percentile?"*
2. **Evaluate Total Compensation**: Don't fixate only on base salary. Negotiate signing bonuses, equity (RSUs/Options), performance incentives, and remote stipends.
3. **Leverage Evidence Proofs**: Cite specific past deliverables from your resume (e.g. revenue driven, latency reduced, costs saved) to justify upper-bracket positioning.
4. **Get Written Offers Before Countering**: Always thank the recruiter, request 48-72 hours to review the total package, and return with a data-backed counter proposal."""
        },
        {
            "intent": "interview_prep",
            "keywords": ["interview", "star method", "behavioral", "mock interview", "interview tips", "questions to ask"],
            "title": "STAR Method & Technical Interview Preparation",
            "reply": """Master the **STAR Framework** for behavioral and architectural rounds:
- **Situation**: Context of the company, product, or challenge (1-2 sentences).
- **Task**: The exact engineering objective you were responsible for.
- **Action**: The specific technologies, architectures, and algorithms you chose and implemented.
- **Result**: Quantifiable business or technical outcome (e.g. 99.99% uptime, 40% faster queries).

**Questions to Ask the Interviewer**:
- *"What is the most critical technical debt item your team plans to resolve in the next two quarters?"*
- *"How do engineers here balance delivery velocity with architectural rigor?"*"""
        },
        {
            "intent": "github_verification",
            "keywords": ["github", "code proof", "code evidence", "verify code", "github verifier", "repos", "repositories", "proof of work"],
            "title": "GitHub Live Code Evidence Verifier",
            "reply": """The **GitHub Live Code Evidence Verifier** provides proof-of-work validation to combat resume inflation:
1. **Public Code Proof**: Cross-references claimed resume skills against real public GitHub repositories and language byte breakdowns.
2. **Confidence Score (0-100%)**: Evaluates code recency, open-source star count, test coverage, and documentation health.
3. **Discovered Hidden Strengths**: Identifies technologies actively used in candidate repositories that were omitted from their resume.
4. **Self-Reported vs Verified**: Distinguishes between verifiable public artifacts and enterprise/proprietary employer work.

To run an audit, switch to the **GitHub Verifier** tab, enter a username (e.g. `alexchen-dev` or `torvalds`), and click **Verify Live Code Evidence**!"""
        },
        {
            "intent": "ats_rebuilder",
            "keywords": ["rebuild", "fix errors", "ats friendly resume", "rebuilder", "repair resume", "clean resume", "errors in resume", "give back new resume", "rebuild resume"],
            "title": "ATS Error Audit & Resume Rebuilder",
            "reply": """The **ATS Error Audit & Resume Rebuilder Engine** audits your resume across 6 critical dimensions and generates a brand new, fully optimized ATS resume:
1. **Error Detection**: Audits contact completeness, section headers, passive phrasing (*"responsible for"*), unquantified bullets, and filler buzzwords.
2. **Standard ATS Taxonomy**: Reorganizes your background into standard sections (*Summary, Core Technical Skills, Professional Experience, Projects, Education*).
3. **Google X-Y-Z Bullets**: Transforms every achievement into *Accomplished [X] measured by [Y] by doing [Z]*.
4. **1-Click Export**: Download as clean ATS PDF, plain text TXT, or copy directly to clipboard.

To run it, go to the **ATS Rebuilder** tab, upload your resume (or load sample), and click **Audit Errors & Rebuild ATS Resume**!"""
        },
        {
            "intent": "platform_features",
            "keywords": ["features", "modules", "tools", "what can this app do", "fairness audit", "recruiter lens", "simulator"],
            "title": "ResumeAI Intelligence Platform Capabilities",
            "reply": """ResumeAI provides 13 integrated enterprise intelligence modules:
1. **Single Resume Analysis**: Full fit score, competency radar, and verified skill proofs.
2. **GitHub Code Evidence Verifier**: Verifies resume claims against live GitHub repos and star metrics.
3. **Interactive Keyword Heatmap**: Real-time visual highlighting of matched vs missing terms.
4. **Batch Screening & Ranking**: Rapidly ranks hundreds of candidates with CSV/JSON exports.
5. **3-Lens Recruiter Simulation**: Reviews candidate from Startup, Enterprise, and Principal Tech angles.
6. **Demographic Fairness Audit**: Verifies screening model neutrality across candidate variations.
7. **Career Trajectory Engine**: Projects 3 progressive career vectors with timeline and salary outlook.
8. **Salary Benchmarking**: Experience-calibrated compensation estimates and negotiation drivers.
9. **ATS Raw Terminal & Pre-Flight Scorecard**: Detects parsing pitfalls and tests extractability.
10. **Interactive Mock Interview**: Progressive technical interrogation in Local or AI mode.
11. **Executive Dossier PDF Export**: Instant professional multi-page printable audit.
12. **AI Resume Enhancer**: Google X-Y-Z formula rewriter with before/after diffs.
13. **Dynamic Cover Letter Generator**: Contextual role-matched letters."""
        },
        {
            "intent": "employment_gap",
            "keywords": ["gap", "employment gap", "career break", "unemployed", "layoff"],
            "title": "Addressing Career Breaks & Employment Gaps",
            "reply": """How to frame career gaps effectively:
1. **Be Transparent and Direct**: Address it briefly in 1 sentence without over-apologizing (e.g., *"Professional sabbatical focused on independent technical upskilling and open-source contributions"*).
2. **Highlight Active Learning**: Showcase open-source contributions, freelance client work, certifications (AWS, CKA), or portfolio projects built during the period.
3. **Use a Functional/Hybrid Layout**: Group projects by core competency rather than rigid chronological date blocks.
4. **Focus on Readiness**: Emphasize how the break clarified your career trajectory and prepared you for high-impact focus in your next role."""
        }
    ]

    @classmethod
    def get_local_response(cls, message: str, resume_context: Optional[str] = None) -> Dict:
        """Find the most relevant domain answer from the local knowledge base."""
        query = message.lower().strip()
        best_match = None
        best_score = 0

        for item in cls.KNOWLEDGE_BASE:
            score = 0
            for kw in item["keywords"]:
                if kw in query:
                    score += 10 + len(kw)
            if score > best_score:
                best_score = score
                best_match = item

        if best_match and best_score >= 8:
            reply = best_match["reply"]
            if resume_context and ("my resume" in query or "my score" in query or "my match" in query):
                reply = f"**{best_match['title']}**\n\n{reply}\n\n*Tip: Apply this directly to the resume loaded in your workspace for immediate score improvement.*"
            return {
                "reply": reply,
                "title": best_match["title"],
                "generation_mode": "local_knowledge_base",
                "matched_intent": best_match["intent"]
            }

        # Fallback smart assistant response
        return {
            "reply": f"""I understand you're asking about: *"{message}"*.

As your **ResumeAI Assistant**, here is what I recommend:
1. **Align with Target Role**: Review your job description in Tab 1 and compare it against your loaded resume using our **Keyword Heatmap**.
2. **Follow the X-Y-Z Formula**: Frame your achievements as: *"Accomplished [X], measured by [Y], by doing [Z]"*.
3. **Verify ATS Extractability**: Test your document in **Tab 11 (ATS Scanner)** to ensure all contact details and headings parse cleanly.
4. **Practice Rounds**: Run a mock interview session in **Tab 12** to test how you articulate these competencies under pressure.

*You can also ask me specifically about ATS optimization, scoring formulas, salary negotiation, or bullet point rewrites!*""",
            "title": "Resume Strategy Guidance",
            "generation_mode": "local_knowledge_base",
            "matched_intent": "general_guidance"
        }
