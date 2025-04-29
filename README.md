# 📊 Hyperstats — Real-Time Metagame Analytics for Brawl Stars using Python + PostgreSQL

**Hyperstats** is a complete data engineering and analysis pipeline built around the official Brawl Stars API. It automatically collects, enriches, stores, and analyzes gameplay data from top-ranked players in order to uncover trends in the competitive metagame.

---

## 🚀 Objectives

- Extract data from high-level matches (Top 200 global players)
- Enrich battle logs with player equipment details (gadgets, star powers, gears)
- Store clean, structured data in a relational database
- Maintain only recent and relevant data with automated cleanup
- Provide a terminal interface for executing analytics queries and commands

---

## 🔍 Key Features

- ✅ Automatic collection of the Top 200 players and their latest battles
- ✅ Data enrichment using player profiles to fetch gadgets, gears, and star powers
- ✅ Storage in a normalized PostgreSQL database using a **Star Schema**
- ✅ Scheduled deletion of outdated records (customizable interval)
- ✅ Interactive terminal interface for querying user rates, win rates, maps, and more
- ✅ Logging, colored output, and progress bars for professional-level usability

---

## 🧠 Concepts and Skills Practiced

- REST API integration and JSON parsing
- ETL pipeline design (extract, transform, load)
- Data modeling with fact and dimension tables
- SQL for analytics (joins, aggregates, views)
- Duplicate handling, data retention policies
- Modular architecture and CLI design
- Best practices with clean code and reusable scripts

---

## 🛠️ Technologies & Libraries

| Category         | Tools & Libraries             |
|------------------|-------------------------------|
| Language         | Python 3.11+                  |
| Database         | PostgreSQL                    |
| API Integration  | `requests`                    |
| DB Access (Python)| `psycopg2`                   |
| Parsing & Timing | `datetime`, `pathlib`         |
| CLI Interface    | `colorama`, `tqdm`            |
| Logging          | `logging` (Python built-in)   |
| Data Models      | `dataclasses`, `typing`       |