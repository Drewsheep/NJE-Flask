from flask import Flask, render_template, request, redirect, abort, session, url_for
from datetime import datetime
import json
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
FILE_PATH = "data/messages.json"
VISITOR_FILE = "data/visitors.json"

def hash_ip(ip_address):
    return hashlib.sha256(ip_address.encode('utf-8')).hexdigest()[:16]

def load_visitors():
    if not os.path.exists(VISITOR_FILE):
        return {"unique_ips": [], "total_visits": 0}
    with open(VISITOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_visitors(data):
    with open(VISITOR_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_messages():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            msg["ip_address"] = hash_ip(msg["ip_address"])
        return messages

def save_messages(messages):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

messages = load_messages()
visitors = load_visitors()

@app.route("/")
def index():
    ip = request.remote_addr

    visitors["total_visits"] += 1

    if ip not in visitors["unique_ips"]:
        visitors["unique_ips"].append(ip)

    save_visitors(visitors)

    query = request.args.get("query", "").lower()
    page = int(request.args.get("page", 1))
    per_page = 5

    if query:
        filtered = [msg for msg in messages if query in msg["name"].lower() or query in msg["message"].lower()]
    else:
        filtered = messages

    total_pages = (len(filtered) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_messages = filtered[start:end]

    moderated_count = sum(1 for msg in messages if msg.get("edited_by_admin"))

    return render_template(
        "index.html",
        messages=paginated_messages,
        logged_in=session.get("logged_in"),
        query=query,
        page=page,
        total_pages=total_pages,
        active_page='home',
        title="Főoldal | Vendégkönyv",
        total_messages=len(filtered),
        moderated_count=moderated_count,
        total_visits=visitors["total_visits"],
        unique_visitors=len(visitors["unique_ips"])
    )

@app.route("/add/", methods=["POST"])
def add():
    name = request.form.get("name")
    message = request.form.get("message")
    rating = request.form.get("rating")

    if name and message:
        ip_address = request.remote_addr

        hashed_ip = hash_ip(ip_address)
        messages.insert(0, {
            "name": name,
            "message": message,
            "rating": int(rating) if rating else None,
            "ip_address": hashed_ip,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "edited_by_admin": False
        })
        save_messages(messages)

    return redirect("/")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect("/admin/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/admin/")
        else:
            return render_template("login.html", error="Hibás felhasználónév vagy jelszó!")

    return render_template("login.html", title="Bejelentkezés | Vendégkönyv", active_page='login')

@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    return redirect("/")

@app.route("/admin/")
def admin():
    if not session.get("logged_in"):
        return redirect("/login/")

    query = request.args.get("query", "").lower()
    page = int(request.args.get("page", 1))
    per_page = 5

    if query:
        filtered = [msg for msg in messages if query in msg["name"].lower() or query in msg["message"].lower()]
    else:
        filtered = messages

    total_pages = (len(filtered) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_messages = filtered[start:end]

    return render_template(
        "admin.html",
        messages=paginated_messages,
        page=page,
        total_pages=total_pages,
        query=query,
        active_page='admin',
        logged_in=session.get("logged_in"),
        total_messages=len(filtered),
        title="Admin Panel | Vendégkönyv"
    )

@app.route("/stats/")
def stats():
    total_messages = len(messages)

    moderated_count = sum(1 for msg in messages if msg.get("edited_by_admin"))

    return render_template(
        "stats.html",
        title="Statisztika | Vendégkönyv",
        active_page="stats",
        logged_in=session.get("logged_in"),
        total_messages=total_messages,
        moderated_count=moderated_count,
        total_visits=visitors["total_visits"],
        unique_visitors=len(visitors["unique_ips"])
    )

@app.route("/delete/<int:index>/")
def delete(index):
    if not session.get("logged_in"):
        return redirect("/login/")

    if 0 <= index < len(messages):
        messages.pop(index)
        save_messages(messages)

    return redirect("/admin/")

@app.route("/delete_all/")
def delete_all():
    if not session.get("logged_in"):
        return redirect("/login/")

    global messages
    messages = []
    save_messages(messages)
    return redirect("/admin/")

@app.route("/edit/<int:index>/", methods=["GET", "POST"])
def edit(index):
    if not session.get("logged_in"):
        return redirect("/login/")

    if 0 <= index < len(messages):
        msg = messages[index]

        if request.method == "POST":
            new_message = request.form.get("message")
            new_rating = request.form.get("rating")

            if new_message:
                msg["message"] = new_message

            if new_rating:
                msg["rating"] = int(new_rating)

            msg["edited_by_admin"] = True
            save_messages(messages)
            return redirect("/admin/")


        return render_template(
            "edit.html",
            msg=msg,
            index=index,
            active_page='admin',
            title="Üzenet szerkesztése | Vendégkönyv",
            logged_in=session.get("logged_in")
        )

    return redirect("/admin/")

if __name__ == "__main__":
    app.run(debug=True)