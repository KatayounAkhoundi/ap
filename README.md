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

## Final Project — Library Management System

**`ap/projects/finalproject/`** — a complete console-based library management system with role-based menus for students and employees.

### Features

- **Student management** — sign-up, sign-in, and profile handling (`StudentManager`, `StudentFileManager`)
- **Book management** — add, search, and list books with sample data initialization (`BookManager`)
- **Borrow workflow** — borrow requests, approval/rejection by employees, borrow records and return tracking (`BorrowRequestManager`, `BorrowManager`)
- **Employee management** — employee accounts and performance tracking (`EmployeeManager`, `EmployeePerformanceManager`)
- **Statistics & reports** — borrow statistics, per-student reports, and employee performance reports (`StatisticsManager`, `BorrowStatistics`, `StudentStatistics`)
- **File persistence** — every entity is persisted through its own file manager so data survives restarts

### Class Layout

```
finalproject/
├── LibrarySystem.java       # application core and session state
├── MenuHandler.java         # role-based console menus
├── *Manager.java            # business logic per entity
├── *FileManager.java        # file persistence per entity
└── *.java                   # domain models (Book, Student, Employee, ...)
```

## Build & Run

Requires **JDK 8 or later**. All sources are plain Java with no external dependencies.

```bash
# Compile the final project
javac -d out ap/projects/finalproject/*.java

# Run the library management system
java -cp out ap.projects.finalproject.LibrarySystem
```

Run other exercises the same way, using their package-qualified main class, e.g.:

```bash
javac -d out ap/exercises/EX7/*.java
java -cp out ap.exercises.EX7.Main
```

For `EX7`, the storage backend (`tabsplit`, `json`, or `sqlite`) is chosen via `config.properties`, created automatically on first run.

## Author

- **Katayoun Akhoundi** — [@KatayounAkhoundi](https://github.com/KatayounAkhoundi)

> Educational repository for course purposes.
