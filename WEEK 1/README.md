🚀 Week 1 — Engineering Mindset Bootcamp

A complete summary of everything learned & delivered
(System Engineering + Node.js + Git Mastery + API Forensics + Automation)

🟦 DAY 1 — System Reverse Engineering + Node & Terminal (8 hrs)
✅ Topics Covered

System info retrieval

Shell configuration

Node.js runtime metrics

Logging & filesystem interactions

🛠 Exercises Completed
1️⃣ sysinfo.js

Outputs:

Hostname

Available Disk Space (GB)

Top 5 open ports

Default gateway

Logged-in users count

2️⃣ Shell Aliases Added

Stored in .bashrc / .zshrc:

alias gs="git status"
alias files="ls -lha"
alias ports="lsof -i -P -n | grep LISTEN"

3️⃣ Node runtime metrics

Logged:

process.cpuUsage()

process.resourceUsage()
Saved to:
logs/day1-sysmetrics.json

📦 Deliverables

sysinfo.js

Screenshot of aliases in .bashrc/.zshrc

logs/day1-sysmetrics.json

🟩 DAY 2 — Node CLI & Concurrency (8 hrs)
🛠 Built a CLI Tool: stats.js

Command:

stats.js --lines <file> --chars <file> --words <file>

✔ Features:

Count lines, words, characters

Process 3 files concurrently

Generate performance report per file:

{
  "file": "data1.txt",
  "executionTimeMs": 51,
  "memoryMB": 14.3
}

⭐ Bonus:

Remove duplicate lines

Save output as:
output/unique-<filename>

📦 Deliverables

stats.js

logs/performance*.json

Unique output files in /output

🟨 DAY 3 — Git Mastery (Reset + Revert + Cherry-pick + Stash) (8 hrs)
🛠 Exercises Completed
1️⃣ Repo with 10 commits

Commit 5 intentionally contains a syntax error

Used git bisect to find breaking commit

2️⃣ Release Workflow

Created branch: release/v0.1

Cherry-picked selective commits from main → release

3️⃣ Stash Use-case

Stashed changes

Switched branches

Restored cleanly

📦 Deliverables

bisect-log.txt

cherry-pick-report.md

stash-proof.txt

Commit graph screenshot

🟥 DAY 4 — HTTP / API Forensics (cURL + Postman) (8 hrs)
🛠 Exercises Completed
1️⃣ GitHub API analysis using cURL

Extracted:

Rate-limit remaining

ETag

Server header

Saved as: curl-headers.txt

2️⃣ Pagination analysis

Fetched:

https://api.github.com/users/octocat/repos?page=1&per_page=5


Documented:

Link headers

Page navigation logic

Saved as: pagination-analysis.md

3️⃣ Postman API Collection

GET user

GET repos (3 pages)

Exported collection JSON

4️⃣ Built HTTP Server

Endpoints:

/ping → returns timestamp

/headers → returns request headers

/count → maintains live counter

📦 Deliverables

curl-headers.txt

pagination-analysis.md

Postman collection .json

server.js

🟪 DAY 5 — Automation & Mini-CI Pipeline (8 hrs)
🛠 Exercises Completed
1️⃣ healthcheck.sh

Pings server every 10s

Logs failures to:
logs/health.log

2️⃣ Husky Pre-commit Pipeline

Validations added:
✔ .env must not exist in Git
✔ All JS auto-formatted with Prettier
✔ Logs folder must be ignored

Captured screenshots of failed & successful commits.

3️⃣ Packaging: bundle-<timestamp>.zip

Included in ZIP:

src/

logs/

docs/

checksums.sha1

4️⃣ Cron Job (Task Scheduler)

Scheduled every 5 minutes:

*/5 * * * * /path/to/healthcheck.sh


Screenshot provided of the cron entry.

📦 Deliverables

healthcheck.sh

Husky hook screenshots

bundle-*.zip

checksums.sha1

Cron job screenshot

🎯 WEEK 1 Summary — What You Actually Learned
Core Skills:

System reverse engineering

Bash & terminal mastery

Node.js internals & concurrency

Git at a professional level

API debugging (cURL + Postman)

Building automation pipelines

Using cron for scheduled tasks

Creating production packaging bundles

Implementing CI-like checks with Husky

Engineering Mindset Developed:

Debug systematically

Automate everything

Work with logs + metrics

Understand how systems behave under the hood

Apply Git like a real software engineer

If you want, I can also generate:
✅ A README.md
✅ A portfolio-friendly version
✅ A visual diagram of your week
Just tell me!
