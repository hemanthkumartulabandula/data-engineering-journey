"""Study-streak CLI: log daily learning sessions and track your streak."""

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

DATA_FILE = Path("data/sessions.json")
TIMEZONE = ZoneInfo("America/Los_Angeles")
def today() -> date:
    """Return today's date in my local time zone."""
    return datetime.now(TIMEZONE).date()


def load_sessions() -> list[dict]:
    """Return all saved sessions, or an empty list if none exist yet."""
    # if DATA_FILE does not exist, return an empty list
    if not DATA_FILE.exists():
        return []

    # open it and return json.load(f)
    with open(DATA_FILE) as f:
        return json.load(f)


def save_sessions(sessions: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(sessions, f, indent=2)


def log_session(topic: str, minutes: int) -> None:
    """Add a new session for today."""
    todays_date = today().isoformat()
    new_session = {"date": todays_date, "topic": topic, "minutes": minutes}
    sessions = load_sessions()
    sessions.append(new_session)
    save_sessions(sessions)
    print(f"Logged {minutes} min: {topic}")


def current_streak(sessions: list[dict]) -> int:
    """Count consecutive study days ending today (or yesterday)."""
    study_days = {date.fromisoformat(s["date"]) for s in sessions}

    day = today()

    if day not in study_days:
        day = day - timedelta(days=1)
    count = 0
    while day in study_days:
        count += 1
        day = day - timedelta(days=1)

    return count


def show_stats() -> None:
    """Print totals and the current streak."""
    sessions = load_sessions()
    total_sessions = len(sessions)
    total_minutes = sum(s["minutes"] for s in sessions)
    total_hours = round(total_minutes / 60, 2)
    streak = current_streak(sessions)
    print(
        f"Sessions: {total_sessions} | Total hours: {total_hours} | Current streak: {streak} day(s)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Track your DE study streak.")
    sub = parser.add_subparsers(dest="command", required=True)

    log_p = sub.add_parser("log", help="Log a study session")
    log_p.add_argument("topic", help="What you studied")
    log_p.add_argument("-m", "--minutes", type=int, default=30)

    sub.add_parser("stats", help="Show totals and current streak")

    args = parser.parse_args()
    if args.command == "log":
        log_session(args.topic, args.minutes)
    elif args.command == "stats":
        show_stats()
