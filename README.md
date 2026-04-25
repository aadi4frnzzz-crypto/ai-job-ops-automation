# ai-job-ops-automation

![Python](https://img.shields.io/badge/Python-3.11-blue) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Output](https://img.shields.io/badge/Output-Structured_JSON-orange)

An **AI-powered job application automation tool** that takes a job description and your resume profile, then uses GPT-4o to generate:
- Match score (0-100) with rationale
- Specific skill gaps for THIS job
- Tailored ATS-friendly resume bullets
- Personalised cover letter
- Interview preparation tips

## Project Structure

```
ai-job-ops-automation/
|-- src/
|   |-- prompts.py     # System + user prompt templates (separate from code)
|   |-- llm.py         # OpenAI client wrapper with JSON mode + error handling
|   |-- main.py        # CLI entry point with argparse and file I/O
|-- examples/
|   |-- jd.txt         # Sample: Flipkart Data Analyst job description
|   |-- profile.txt    # Sample: candidate profile template
|-- output/            # Auto-generated JSON output (gitignored)
|-- requirements.txt
|-- README.md
```

## Setup

```bash
# 1. Clone
git clone https://github.com/aadi4frnzzz-crypto/ai-job-ops-automation.git
cd ai-job-ops-automation

# 2. Install
pip install -r requirements.txt

# 3. Set your OpenAI API key
export OPENAI_API_KEY=sk-your-key-here

# 4. Run with sample files
cd src
python main.py --jd ../examples/jd.txt --profile ../examples/profile.txt

# 5. Specify custom output path
python main.py --jd ../examples/jd.txt --profile ../examples/profile.txt --out ../output/flipkart.json
```

## Output Contract

Every run produces a structured JSON with these fields:

```json
{
  "job_title": "Data Analyst",
  "company": "Flipkart",
  "match_score": 78,
  "match_rationale": "Strong Python and SQL alignment...",
  "top_strengths": ["3 years at Google", "ETL pipeline experience", "..."],
  "skill_gaps": ["No BI tool (Tableau/Looker)", "No BigQuery experience", "..."],
  "tailored_resume_bullets": [
    "Engineered ETL pipeline reducing data latency by 40%...",
    "..."
  ],
  "cover_letter": "Dear Hiring Manager, ...",
  "interview_tips": ["Prepare supply chain KPI examples...", "..."]
}
```

## Architecture

```
examples/jd.txt + examples/profile.txt
            |
            v
     [src/main.py]  <-- CLI, file loading, output
            |
            v
      [src/llm.py]  <-- OpenAI GPT-4o with JSON mode enforced
            |
      [src/prompts.py] <-- Structured prompt templates
            |
            v
     output/analysis.json
```

## How to Use for Real Applications

1. Paste any job description into a `.txt` file
2. Update `examples/profile.txt` with your actual background
3. Run the script, review the match score and gaps
4. Use the generated bullets and cover letter as a starting draft
5. Review and personalise before submitting

## Security Notes

- **Never commit your API key** — always use env vars
- Add `.env` to `.gitignore` if using `python-dotenv`
- The `output/` folder is gitignored — your outputs stay local
- No data is sent anywhere other than OpenAI

## Design Decisions

- **JSON mode enforced** (`response_format: json_object`) — no parsing failures
- **Prompts separate from code** — tune without breaking logic
- **Temperature 0.3** — structured, consistent output over creativity
- **argparse CLI** — designed for scripting and automation, not just demos

## License

MIT
