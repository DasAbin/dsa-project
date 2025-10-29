Student Grievance System (CLI)
================================

A simple command-line Student Grievance System built with Python and JSON storage. Students can submit grievances; others can upvote/downvote; issues can be listed, shown, resolved, or deleted. Designed to be easy to explain for a data structures subject.

Requirements
------------
- Python 3.10+
- No external packages required

Project Structure
-----------------
```
README.md
grievance_cli.py
data/grievances.json
```

Quick Start
-----------
1) Ensure Python 3.10+ is installed.
2) Run with no arguments for the interactive menu:
```
python grievance_cli.py
```
   The JSON data file is created automatically on first use. Data is saved inside
   the `data` folder next to `grievance_cli.py`, so you can run it from any directory.

How to Use (Interactive Menu)
------------------------------
Run the program:
```
python grievance_cli.py
```

Then follow the menu prompts:
- **1) Add grievance**: Enter title, description, and author
- **2) List grievances**: View all, filter by status (open/resolved), and sort by date or votes
- **3) Show grievance by id**: View full details of a specific grievance
- **4) Vote on grievance**: Upvote or downvote a grievance by id
- **5) Resolve grievance**: Mark a grievance as resolved by id
- **6) Delete grievance**: Remove a grievance by id
- **0) Exit**: Quit the program

Design Notes
------------
- Stores grievances in a JSON list at `data/grievances.json`.
- Each grievance has: `id`, `title`, `description`, `author`, `status`, `upvotes`, `downvotes`, `created_at`.
- Data structures used: **Python list** (for storing grievances), **dictionaries** (for each grievance record).

Plain-English Explanation (how it works)
---------------------------------------
- **Where is data saved?** In a file called `data/grievances.json` next to the script.
- **What is a grievance?** A small record with an `id`, `title`, `description`,
  `author`, a `status` (open/resolved), vote counts, and the time it was created.
- **How does add work?** It reads the current list, creates a new item with the
  next `id`, then saves the updated list.
- **How does list work?** It reads all items, optionally filters by `status`,
  then sorts either by creation time or by vote score.
- **How does vote work?** It finds the item by `id` and increments either
  `upvotes` or `downvotes`, then saves.
- **How does resolve/delete work?** Resolve changes `status` to `resolved`.
  Delete removes the record from the list.

Troubleshooting
---------------
- **It says file not found or doesn't save data**: Just run the program once;
  the app auto-creates the `data` folder and `grievances.json`. Because the
  script uses an absolute path relative to itself, running it from another
  directory also works.
- **JSON got corrupted** (rare): Delete `data/grievances.json` and run again;
  a fresh empty list will be created.

Help
----
Just run the program and follow the on-screen menu prompts.
