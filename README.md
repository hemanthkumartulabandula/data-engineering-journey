# Data Engineering Journey

A small command-line tool that tracks my daily study streak, and the home base for the hands-on projects I'm building as I learn data engineering.

![Python](https://img.shields.io/badge/python-3.14-blue)
![uv](https://img.shields.io/badge/managed%20with-uv-purple)
![Ruff](https://img.shields.io/badge/linted%20with-ruff-orange)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [What I Learned](#what-i-learned)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

## About

I'm learning data engineering by building real projects instead of only watching tutorials. This repo is where that journey starts.

It does two jobs:

1. **A study-streak tracker.** Learning something new takes consistency more than talent, so I built a tool that logs every study session and shows how many days in a row I've kept going. Seeing the streak grow is a simple way to stay accountable.
2. **A map of my projects.** Each project in the [Roadmap](#roadmap) focuses on a different data engineering skill, from processing large files in Python to building scheduled pipelines and streaming data in real time.

## Features

- Log a study session with a topic and duration in one command
- See your total sessions, total hours and current streak at a glance
- Streak stays alive until midnight, so you don't "lose" it in the morning before you've studied
- Several sessions on the same day count as one streak day
- Dates are time-zone aware, so "today" means today where you live, not wherever the code happens to run
- Data is stored in a plain, readable JSON file, with no database needed

## Demo

```bash
$ uv run journey log "Set up uv and Git" -m 60
Logged 60 min: Set up uv and Git

$ uv run journey log "Learned sets, dates and while loops" -m 45
Logged 45 min: Learned sets, dates and while loops

$ uv run journey stats
Sessions: 3 | Total hours: 2.25 | Current streak: 1 day(s)
```

## Tech Stack

| Tool                                 | Why I used it                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| Python 3.14                          | The core language                                                               |
| [uv](https://docs.astral.sh/uv/)     | Manages the Python version, virtual environment and dependencies in one tool    |
| argparse                             | Turns the script into a proper command-line tool with subcommands and help text |
| pathlib, json                        | Reading and writing the session data safely                                     |
| datetime, zoneinfo                   | Date math for the streak and time-zone-aware "today"                            |
| [Ruff](https://docs.astral.sh/ruff/) | Linting and formatting, so the code stays clean and consistent                  |

The tool uses only Python's standard library at runtime. Ruff is a development dependency.

## Project Structure

```
data-engineering-journey/
├── src/
│   └── data_engineering_journey/
│       ├── __init__.py
│       └── cli.py            # all the CLI logic
├── data/
│   └── sessions.json         # my study log (created automatically)
├── pyproject.toml            # project metadata, dependencies and the `journey` command
├── uv.lock                   # exact dependency versions
├── .python-version
└── README.md
```

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (it will download the right Python version for you)
- Git

### Installation

```bash
git clone https://github.com/hemanthkumartulabandula/data-engineering-journey.git
cd data-engineering-journey
uv sync
```

Check that it works:

```bash
uv run journey --help
```

## Usage

Run every command from the project's root folder (the one with `pyproject.toml`). `uv run` makes sure the command uses this project's own environment.

### Command reference

| Command                                     | What it does                                             |
| ------------------------------------------- | -------------------------------------------------------- |
| `uv run journey log "<topic>"`              | Log a 30-minute study session for today                  |
| `uv run journey log "<topic>" -m <minutes>` | Log a session with a specific length                     |
| `uv run journey stats`                      | Show total sessions, total hours and your current streak |
| `uv run journey --help`                     | List all commands                                        |
| `uv run journey log --help`                 | Show the options for `log`                               |

### Logging a session

The general format is:

```bash
uv run journey log "<what you studied>" -m <minutes>
```

| Part                                    | Required? | Meaning                                                                          |
| --------------------------------------- | --------- | -------------------------------------------------------------------------------- |
| `log`                                   | Yes       | The subcommand for adding a session                                              |
| `"<what you studied>"`                  | Yes       | A short description of the topic. Keep it in quotes so the spaces stay together. |
| `-m <minutes>` or `--minutes <minutes>` | No        | How long you studied, as a whole number. Defaults to 30.                         |

**Examples:**

```bash
# A 30-minute session (the default)
uv run journey log "Read about Python generators"

# A 90-minute session
uv run journey log "Built the wiki-pulse parser" -m 90

# The long form of the option works too
uv run journey log "Practiced SQL window functions" --minutes 45
```

Each command confirms what it saved:

```
Logged 90 min: Built the wiki-pulse parser
```

You can log as many sessions as you like in a day. They all count toward your hours, and the day counts once toward your streak.

### Checking your progress

```bash
uv run journey stats
```

```
Sessions: 12 | Total hours: 14.5 | Current streak: 6 day(s)
```

| Field          | Meaning                                                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sessions       | Every session you've ever logged                                                                                                                         |
| Total hours    | All logged minutes added up, shown in hours                                                                                                              |
| Current streak | Days in a row you've studied, ending today. If you haven't studied yet today, it counts up to yesterday, so the streak isn't lost until the day is over. |

### A typical day

```bash
cd ~/de-projects/data-engineering-journey   # go to the project
uv run journey log "Learned about decorators" -m 60
uv run journey stats                        # check the streak
git add data/sessions.json
git commit -m "Log study session"
git push                                    # keep the log on GitHub up to date
```

### Where the data lives

Sessions are saved in `data/sessions.json`. It's plain JSON, so you can open it in any editor to fix a typo or remove a session. Keep the same format: a list of entries with `date` (`YYYY-MM-DD`), `topic` and `minutes`.

To start over, delete the file. It's created again the next time you log a session.

### Common mistakes

| You see                                              | Cause                                                         | Fix                                            |
| ---------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------- |
| `error: unrecognized arguments: ...`                 | The topic wasn't in quotes, so each word was read separately  | Put the topic in quotes: `"Set up uv and Git"` |
| `error: argument -m/--minutes: invalid int value`    | Minutes weren't a whole number, e.g. `-m 1.5` or `-m one`     | Use whole minutes: `-m 90`                     |
| `error: the following arguments are required: topic` | No topic given                                                | Add a topic after `log`                        |
| `Failed to spawn: journey`                           | Not in the project folder, or the project isn't installed yet | `cd` into the project folder and run `uv sync` |

### Development

Check code quality before committing:

```bash
uv run ruff check .    # find problems
uv run ruff format .   # fix formatting
```

## How It Works

Each session is saved as a small record in `data/sessions.json`:

```json
[
  {
    "date": "2026-10-03",
    "topic": "Set up uv and Git",
    "minutes": 60
  }
]
```

**Saving a session** follows a read → modify → write pattern: load the existing list, add the new session, and write the whole list back. The `data/` folder is created automatically if it doesn't exist, and that step is safe to run every time.

**Counting the streak:**

1. Collect every study date into a set, so duplicate days count once.
2. Start from today. If you haven't studied yet today, start from yesterday instead.
3. Step back one day at a time while each day is in the set, counting as you go.
4. The first missing day ends the streak.

**Time zones:** "today" is calculated in `America/Los_Angeles` time. Servers usually run in UTC, where an evening session in LA would already count as tomorrow. Setting the time zone explicitly keeps the streak correct wherever the code runs. You can change it with the `TIMEZONE` setting in `cli.py`.

## What I Learned

- **Project setup the professional way:** uv, `pyproject.toml`, a `src/` layout and registering a command-line entry point
- **Why virtual environments matter:** each project gets its own isolated packages, so projects don't break each other
- **Writing idempotent code:** steps like `mkdir(parents=True, exist_ok=True)` are safe to run again and again, which is essential for data pipelines that get retried
- **Return values and data flow:** catching what a function returns and passing data between functions
- **Working with dates:** converting between text and `date` objects, date arithmetic with `timedelta`, and why time zones cause real bugs
- **Sets for fast lookups** and **while loops** for repeating until a condition changes
- **Reading tracebacks** from the bottom up, and catching errors early with a linter

## Roadmap

Each project is its own repository, built to practice a specific group of data engineering skills.

| #   | Project                      | What it's about                                                    | Skills                                        | Status  |
| --- | ---------------------------- | ------------------------------------------------------------------ | --------------------------------------------- | ------- |
| 0   | **data-engineering-journey** | This repo: setup and a study-streak CLI                            | uv, Git, argparse, pathlib, datetime          | Done    |
| 1   | **wiki-pulse**               | What is the world reading on Wikipedia right now?                  | Generators, decorators, regex, profiling      | Next    |
| 2   | **my-data-vault**            | Turning my personal data exports into a clean Parquet data lake    | OOP, logging, config, Parquet                 | Planned |
| 3   | **la-bikeshare-showdown**    | LA bike-share trips analyzed in Pandas vs Polars vs DuckDB         | Pandas, Polars, DuckDB                        | Planned |
| 4   | **quakewatch-etl**           | California earthquakes from the USGS API into PostgreSQL           | APIs, pydantic, SQLAlchemy, incremental loads | Planned |
| 5   | **quakewatch-etl v2**        | Making that pipeline bulletproof                                   | pytest, mocking, data quality checks          | Planned |
| 6   | **museum-heist**             | Downloading a museum's public-domain art collection, fast          | Threads, async, multiprocessing               | Planned |
| 7   | **flight-delay-detective**   | Which airline is really late? Millions of flights in Spark         | PySpark                                       | Planned |
| 8   | **weather-lakehouse**        | Weather data stored in bronze, silver and gold layers in the cloud | Cloud storage, boto3                          | Planned |
| 9   | **la-pulse**                 | A daily, scheduled pipeline for LA city data with a dashboard      | Airflow, Streamlit                            | Planned |
| 10  | **wiki-live-stream**         | Watching Wikipedia get edited in real time                         | Kafka, streaming                              | Planned |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Hemanth Kumar Tulabandula**

GitHub: [@hemanthkumartulabandula](https://github.com/hemanthkumartulabandula)

If you're also learning data engineering, feel free to open an issue or reach out. I'm happy to compare notes.
