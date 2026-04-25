"""AI Job Ops Automation: CLI entry point.

Usage:
    python main.py --jd examples/jd.txt --profile examples/profile.txt
    python main.py --jd examples/jd.txt --profile examples/profile.txt --out output/result.json
"""
import argparse
import json
import logging
import sys
from pathlib import Path

from llm import analyze_job_fit


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def load_file(path: str) -> str:
    """Read a text file and return its content."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8")


def save_output(result: dict, out_path: str) -> None:
    """Save the result JSON to a file."""
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    logging.getLogger(__name__).info("Output saved to %s", out_path)


def print_summary(result: dict) -> None:
    """Pretty-print key results to stdout."""
    print("\n" + "=" * 60)
    print(f"  JOB:   {result.get('job_title', 'Unknown')} @ {result.get('company', 'Unknown')}")
    print(f"  MATCH: {result.get('match_score', 0)}/100")
    print("=" * 60)

    print("\nMATCH RATIONALE:")
    print(f"  {result.get('match_rationale', '')}")

    print("\nTOP STRENGTHS:")
    for s in result.get("top_strengths", []):
        print(f"  + {s}")

    print("\nSKILL GAPS:")
    for g in result.get("skill_gaps", []):
        print(f"  - {g}")

    print("\nTAILORED RESUME BULLETS:")
    for b in result.get("tailored_resume_bullets", []):
        print(f"  * {b}")

    print("\nCOVER LETTER:")
    print(result.get("cover_letter", ""))

    print("\nINTERVIEW TIPS:")
    for t in result.get("interview_tips", []):
        print(f"  > {t}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Job Ops: Analyse job fit with GPT-4o"
    )
    parser.add_argument("--jd",      required=True,  help="Path to job description .txt")
    parser.add_argument("--profile", required=True,  help="Path to candidate profile .txt")
    parser.add_argument("--out",     default=None,   help="Output JSON path (optional)")
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        jd = load_file(args.jd)
        profile = load_file(args.profile)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Running AI job fit analysis...")
    try:
        result = analyze_job_fit(jd, profile)
    except (RuntimeError, ValueError) as exc:
        logger.error("Analysis failed: %s", exc)
        sys.exit(2)

    print_summary(result)

    out_path = args.out or "output/analysis.json"
    save_output(result, out_path)


if __name__ == "__main__":
    main()
