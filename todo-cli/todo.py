#!/usr/bin/env python3
import argparse, json, os, sys
from datetime import datetime

DB = "todo.json"

def load():
    if not os.path.exists(DB): return []
    with open(DB, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError: return []

def save(items):
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

def add(text, priority):
    items = load()
    items.append({
        "id": (max([i["id"] for i in items]) + 1) if items else 1,
        "text": text,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds")
    })
    save(items)
    print(f"Added: [{items[-1]['id']}] {text} (p{priority})")

def list_items(show_all):
    items = load()
    if not items:
        print("No tasks yet. Use: python todo.py add \"Task text\"")
        return
    view = items if show_all else [i for i in items if not i["done"]]
    if not view:
        print("Nothing to show. Use --all to see completed tasks.")
        return
    for i in view:
        status = "✓" if i["done"] else "•"
        print(f"[{i['id']:>2}] {status}  (p{i['priority']}) {i['text']}")

def done(task_id):
    items = load()
    for i in items:
        if i["id"] == task_id:
            i["done"] = True
            save(items)
            print(f"Completed: [{task_id}] {i['text']}")
            return
    print(f"Task id {task_id} not found.", file=sys.stderr)

def delete(task_id):
    items = load()
    new_items = [i for i in items if i["id"] != task_id]
    if len(new_items) == len(items):
        print(f"Task id {task_id} not found.", file=sys.stderr)
        return
    save(new_items)
    print(f"Deleted task [{task_id}].")

def clear(done_only):
    items = load()
    if done_only:
        items = [i for i in items if not i["done"]]
    else:
        items = []
    save(items)
    print("Cleared completed tasks." if done_only else "Cleared all tasks.")

def main():
    p = argparse.ArgumentParser(description="Simple To-Do CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("text", help="Task description")
    p_add.add_argument("-p", "--priority", type=int, default=3, choices=range(1,6),
                       help="Priority 1 (high) to 5 (low). Default 3.")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="Show all (incl. done)")

    p_done = sub.add_parser("done", help="Mark a task complete")
    p_done.add_argument("id", type=int, help="Task id")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task id")

    p_clear = sub.add_parser("clear", help="Clear tasks")
    p_clear.add_argument("--done", action="store_true", help="Only clear completed")

    args = p.parse_args()
    if args.cmd == "add": add(args.text, args.priority)
    elif args.cmd == "list": list_items(args.all)
    elif args.cmd == "done": done(args.id)
    elif args.cmd == "delete": delete(args.id)
    elif args.cmd == "clear": clear(args.done)

if __name__ == "__main__":
    main()
