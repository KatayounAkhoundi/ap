# Advanced Programming (AP) — Java

University coursework for the **Advanced Programming** course, written entirely in **Java**.

The repository contains weekly lab exercises, midterm and final exam solutions, a domain-scraping tools project, and a console-based **Library Management System** as the final project.

## Repository Structure

```
ap/
├── exercises/
│   ├── ex2/           # Lab exercises 2 — pattern printing & Pacman game engine
│   ├── ex3/           # Lab exercises 3 — OOP fundamentals (classes & objects)
│   ├── ex4/           # Lab exercises 4 — objects-early exercises (Circuit, Employee, ...)
│   ├── EX7/           # Exercise 7 — library system with pluggable storage backends
│   ├── midtermExam/   # Midterm exam solutions
│   ├── FinalExam/     # Final exam solutions
│   ├── MidtermProj/   # Midterm project — console library manager
│   └── projects/      # Web tools — domain scraper, HTML parser, media downloader
└── projects/
    └── finalproject/  # Final project — Library Management System
```

## Lab Exercises

| Folder | Topic | Highlights |
|--------|-------|------------|
| `ap/exercises/ex2` | Console input/output & 2D patterns | Square-frame printing, text-based **Pacman** game engine |
| `ap/exercises/ex3` | Classes & objects | `Book` and `Library` member modeling with encapsulation |
| `ap/exercises/ex4` | Objects-early design | `Circuit`, `Employee`, `HallLight`, `Letter` tester classes |
| `ap/exercises/EX7` | Persistence & storage abstraction | One library system, three storage backends — tab-split files, JSON, and SQLite — selected at runtime through `config.properties` |

## Exams

- **`ap/exercises/midtermExam/`** — midterm exam solutions (`Shop`, `Laptop`, `Case` class hierarchy).
- **`ap/exercises/FinalExam/`** — final exam solutions (`Product`, `Pen`, `Book` inheritance and tools).

## Midterm Project

**`ap/exercises/MidtermProj/`** — a console library manager supporting student/admin roles, book loans, and file-based persistence.

## Web Tools Project

**`ap/exercises/projects/`** — a set of utilities built around domain scraping:

- `DomainHtmlScraper` — crawls and saves all pages of a target domain
- `HtmlFetcher` / `HtmlFileManager` — download and store HTML pages
- `HtmlParser` / `HtmlAnalyzer` — parse and analyze HTML content
- `ImageUrlExtractor` / `ImageAndAudioDownloader` — extract and download media
- `DirectoryTools` / `FileTools` — file-system helpers

Target domain and save directory are configured in `Conf.java`.
