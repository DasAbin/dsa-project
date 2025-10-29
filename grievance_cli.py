#!/usr/bin/env python3

import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "grievances.json")


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def load_grievances():
    ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []


def save_grievances(grievances):
    ensure_storage()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(grievances, f, indent=2)


def generate_next_id(grievances):
    if not grievances:
        return 1
    return max(g.get("id", 0) for g in grievances) + 1


def find_grievance(grievances, grievance_id):
    for grievance in grievances:
        if grievance.get("id") == grievance_id:
            return grievance
    return None


def add_grievance(title, description, author):
    grievances = load_grievances()
    title = title.strip()
    description = description.strip()
    author = author.strip()
    if not title or not description or not author:
        print("Error: Title, description, and author are required.")
        return
    grievance = {
        "id": generate_next_id(grievances),
        "title": title,
        "description": description,
        "author": author,
        "status": "open",
        "upvotes": 0,
        "downvotes": 0,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    grievances.append(grievance)
    save_grievances(grievances)
    print(f"Added grievance #{grievance['id']}: {grievance['title']}")


def list_grievances(status_filter=None, sort_key="date"):
    grievances = load_grievances()
    if status_filter:
        grievances = [g for g in grievances if g.get("status") == status_filter]
    if sort_key == "votes":
        grievances.sort(key=lambda g: (g.get("upvotes", 0) - g.get("downvotes", 0)), reverse=True)
    else:
        grievances.sort(key=lambda g: g.get("created_at", ""))
    if not grievances:
        print("No grievances found.")
        return
    for g in grievances:
        score = g.get("upvotes", 0) - g.get("downvotes", 0)
        print(
            f"#{g['id']} | {g['status'].upper():8} | score: {score:+d} | "
            f"{g['title']} (by {g['author']})"
        )


def show_grievance(grievance_id):
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return
    print(f"ID: {grievance['id']}")
    print(f"Title: {grievance['title']}")
    print(f"Description: {grievance['description']}")
    print(f"Author: {grievance['author']}")
    print(f"Status: {grievance['status']}")
    print(f"Upvotes: {grievance['upvotes']}")
    print(f"Downvotes: {grievance['downvotes']}")
    print(f"Created At: {grievance['created_at']}")


def vote_grievance(grievance_id, vote_type):
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return
    if vote_type == "up":
        grievance["upvotes"] = grievance.get("upvotes", 0) + 1
    else:
        grievance["downvotes"] = grievance.get("downvotes", 0) + 1
    save_grievances(grievances)
    print(
        f"Voted {vote_type} on grievance #{grievance_id}. "
        f"(up: {grievance['upvotes']}, down: {grievance['downvotes']})"
    )


def resolve_grievance(grievance_id):
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return
    grievance["status"] = "resolved"
    save_grievances(grievances)
    print(f"Grievance #{grievance_id} marked as resolved.")


def delete_grievance(grievance_id):
    grievances = load_grievances()
    original_len = len(grievances)
    grievances = [g for g in grievances if g.get("id") != grievance_id]
    if len(grievances) == original_len:
        print(f"Grievance #{grievance_id} not found.")
        return
    save_grievances(grievances)
    print(f"Deleted grievance #{grievance_id}.")


def run_menu():
    ensure_storage()
    while True:
        print("\nStudent Grievance System - Menu")
        print("1) Add grievance")
        print("2) List grievances")
        print("3) Show grievance by id")
        print("4) Vote on grievance (up/down)")
        print("5) Resolve grievance")
        print("6) Delete grievance")
        print("0) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            author = input("Author: ").strip()
            add_grievance(title, description, author)

        elif choice == "2":
            status = input("Filter by status (open/resolved or blank): ").strip()
            status_val = status if status in {"open", "resolved"} else None
            sort = input("Sort by (date/votes, default date): ").strip() or "date"
            if sort not in {"date", "votes"}:
                sort = "date"
            list_grievances(status_val, sort)

        elif choice == "3":
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            show_grievance(gid)

        elif choice == "4":
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            vtype = input("Vote type (up/down): ").strip()
            if vtype not in {"up", "down"}:
                print("Invalid vote type.")
                continue
            vote_grievance(gid, vtype)

        elif choice == "5":
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            resolve_grievance(gid)

        elif choice == "6":
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            delete_grievance(gid)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Please choose a valid option.")



def main():
    run_menu()


if __name__ == "__main__":
    main()
