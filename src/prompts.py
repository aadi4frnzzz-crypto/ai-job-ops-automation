"""Prompt templates for the AI job ops automation engine.
Kept separate from code so they can be tuned without touching business logic.
"""

SYSTEM_PROMPT = """
You are an expert career coach and talent analyst with 15 years of experience.
You specialize in:
- Matching candidate profiles to job requirements
- Identifying genuine skill gaps (not generic ones)
- Rewriting resume bullets to be ATS-friendly and impact-focused
- Writing compelling, honest cover letters

Always respond in the exact JSON format specified. Never add extra keys.
""".strip()

ANALYSIS_PROMPT_TEMPLATE = """
Analyze the fit between the job description and candidate profile below.

JOB DESCRIPTION:
{job_description}

CANDIDATE PROFILE:
{candidate_profile}

Return a JSON object with EXACTLY these fields:
{{
  "job_title": "<extracted job title from JD>",
  "company": "<extracted company name or 'Not specified'>",
  "match_score": <integer 0-100>,
  "match_rationale": "<2-3 sentence explanation of the score>",
  "top_strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "skill_gaps": ["<gap 1>", "<gap 2>", "<gap 3>"],
  "tailored_resume_bullets": [
    "<bullet 1: strong action verb + metric>",
    "<bullet 2: strong action verb + metric>",
    "<bullet 3: strong action verb + metric>",
    "<bullet 4: strong action verb + metric>"
  ],
  "cover_letter": "<cover letter, max 220 words, no salutation line>",
  "interview_tips": ["<tip 1>", "<tip 2>", "<tip 3>"]
}}

Rules:
- match_score: Be honest. 90+ only if near-perfect alignment.
- skill_gaps: Be specific to THIS job, not generic (not 'communication skills').
- resume_bullets: Start with a power verb. Include numbers where possible.
- cover_letter: Reference the company and role specifically. Show enthusiasm.
""".strip()
