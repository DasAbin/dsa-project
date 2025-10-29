#!/usr/bin/env python3
"""
Student Grievance System - Simple Menu-Driven Program

This program manages student grievances using:
- Python list to store all grievances
- Dictionary for each grievance record
- JSON file for permanent storage

Each grievance has: id, title, description, author, status, upvotes, downvotes, created_at
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List


# Set up file paths - data is stored next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "grievances.json")


def ensure_storage():
    """Make sure the data folder and JSON file exist."""
    # Create data folder if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    # Create empty JSON file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def load_grievances():
    """Load the list of grievances from the JSON file (or return an empty list)."""
    ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Make sure we got a list, not some other data type
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            # If file is corrupted, return empty list
            return []


def save_grievances(grievances):
    """Save the full list of grievances back to the JSON file."""
    ensure_storage()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(grievances, f, indent=2)


def generate_next_id(grievances):
    """Return the next integer id (1 if the list is empty)."""
    if not grievances:
        return 1
    # Find the highest existing id and add 1
    return max(g.get("id", 0) for g in grievances) + 1


def find_grievance(grievances, grievance_id):
    """Find a grievance by id, or return None if missing."""
    # Loop through all grievances to find matching id
    for grievance in grievances:
        if grievance.get("id") == grievance_id:
            return grievance
    return None


def add_grievance(title, description, author):
    """Create a new grievance with title, description, and author."""
    # Load existing grievances from file
    grievances = load_grievances()
    
    # Clean up user input (remove extra spaces)
    title = title.strip()
    description = description.strip()
    author = author.strip()

    # Check if all required fields are provided
    if not title or not description or not author:
        print("Error: Title, description, and author are required.")
        return

    # Create new grievance dictionary with all required fields
    grievance = {
        "id": generate_next_id(grievances),  # Get next available ID
        "title": title,
        "description": description,
        "author": author,
        "status": "open",  # All new grievances start as open
        "upvotes": 0,      # Start with no votes
        "downvotes": 0,
        "created_at": datetime.now().isoformat(timespec="seconds"),  # Current timestamp
    }

    # Add new grievance to the list
    grievances.append(grievance)
    # Save updated list back to file
    save_grievances(grievances)
    print(f"Added grievance #{grievance['id']}: {grievance['title']}")


def list_grievances(status_filter=None, sort_key="date"):
    """Print all grievances, optionally filtered by status and sorted by date or votes."""
    # Load all grievances from file
    grievances = load_grievances()

    # Filter by status if requested
    if status_filter:
        grievances = [g for g in grievances if g.get("status") == status_filter]

    # Sort the list based on user preference
    if sort_key == "votes":
        # Sort by vote score (upvotes - downvotes), highest first
        grievances.sort(key=lambda g: (g.get("upvotes", 0) - g.get("downvotes", 0)), reverse=True)
    else:
        # Sort by creation date, oldest first
        grievances.sort(key=lambda g: g.get("created_at", ""))

    # Show message if no grievances found
    if not grievances:
        print("No grievances found.")
        return

    # Display each grievance in a formatted way
    for g in grievances:
        score = g.get("upvotes", 0) - g.get("downvotes", 0)  # Calculate vote score
        print(
            f"#{g['id']} | {g['status'].upper():8} | score: {score:+d} | "
            f"{g['title']} (by {g['author']})"
        )


def show_grievance(grievance_id):
    """Show full details for one grievance by id."""
    # Load all grievances and find the one with matching ID
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    
    # If not found, show error message
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return

    # Display all details of the grievance
    print(f"ID: {grievance['id']}")
    print(f"Title: {grievance['title']}")
    print(f"Description: {grievance['description']}")
    print(f"Author: {grievance['author']}")
    print(f"Status: {grievance['status']}")
    print(f"Upvotes: {grievance['upvotes']}")
    print(f"Downvotes: {grievance['downvotes']}")
    print(f"Created At: {grievance['created_at']}")


def vote_grievance(grievance_id, vote_type):
    """Increase the upvote or downvote count for a grievance."""
    # Load all grievances and find the one with matching ID
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    
    # If not found, show error message
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return

    # Increase the appropriate vote count
    if vote_type == "up":
        grievance["upvotes"] = grievance.get("upvotes", 0) + 1
    else:
        grievance["downvotes"] = grievance.get("downvotes", 0) + 1

    # Save the updated grievances back to file
    save_grievances(grievances)
    print(
        f"Voted {vote_type} on grievance #{grievance_id}. "
        f"(up: {grievance['upvotes']}, down: {grievance['downvotes']})"
    )


def resolve_grievance(grievance_id):
    """Mark a grievance as resolved."""
    # Load all grievances and find the one with matching ID
    grievances = load_grievances()
    grievance = find_grievance(grievances, grievance_id)
    
    # If not found, show error message
    if not grievance:
        print(f"Grievance #{grievance_id} not found.")
        return

    # Change status to resolved
    grievance["status"] = "resolved"
    # Save the updated grievances back to file
    save_grievances(grievances)
    print(f"Grievance #{grievance_id} marked as resolved.")


def delete_grievance(grievance_id):
    """Remove a grievance by id."""
    # Load all grievances
    grievances = load_grievances()
    original_len = len(grievances)
    
    # Create new list without the grievance to delete
    grievances = [g for g in grievances if g.get("id") != grievance_id]
    
    # Check if anything was actually removed
    if len(grievances) == original_len:
        print(f"Grievance #{grievance_id} not found.")
        return

    # Save the updated list back to file
    save_grievances(grievances)
    print(f"Deleted grievance #{grievance_id}.")


def run_menu():
    """Interactive, menu-driven interface for the grievance system."""
    # Make sure data folder and file exist before starting
    ensure_storage()
    
    # Keep showing menu until user chooses to exit
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
            # Get input from user for new grievance
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            author = input("Author: ").strip()
            add_grievance(title, description, author)

        elif choice == "2":
            # Ask user for filtering and sorting preferences
            status = input("Filter by status (open/resolved or blank): ").strip()
            status_val = status if status in {"open", "resolved"} else None
            sort = input("Sort by (date/votes, default date): ").strip() or "date"
            if sort not in {"date", "votes"}:
                sort = "date"
            list_grievances(status_val, sort)

        elif choice == "3":
            # Get grievance ID from user and show details
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            show_grievance(gid)

        elif choice == "4":
            # Get grievance ID and vote type from user
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
            # Get grievance ID and mark as resolved
            try:
                gid = int(input("Enter id: ").strip())
            except ValueError:
                print("Invalid id.")
                continue
            resolve_grievance(gid)

        elif choice == "6":
            # Get grievance ID and delete it
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
    """Entry point: run interactive menu."""
    run_menu()


if __name__ == "__main__":
    main()
