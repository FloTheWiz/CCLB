from datetime import datetime
import os
import json

from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_discord import DiscordOAuth2Session, requires_authorization
from flask_minify import Minify
import timeago

from utils import get_stats_from_save, beautify

app = Flask(__name__)
Minify(app=app, html=True, js=True, cssless=True)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET") 
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN") ## unused, I think. 

discord = DiscordOAuth2Session(app)


def get_recent_data():
    # This is example "recent_changes" data.

    # This is a list in database.json
    # db['recent_changes']: list
    example = [
        {
            "board_name": "Example 1",
            "verified": True,
            "timestamp": datetime.now(),
            "rank": 1,
            "qualifier": "Score",
            "qualifier_amount": "1",
            "user": {
                "name": "F.l.0",
                "flag": "gb",
                "id": 1166877695754375220,
                "css": """
    background: -webkit-linear-gradient(#eee, #333);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;""",
            },
        },
        {
            "board_name": "Test Leaderboard 2",
            "verified": False,
            "timestamp": datetime.now(),
            "rank": 1,
            "qualifier": "Score",
            "qualifier_amount": "1",
            "user": {
                "name": "F.l.0",
                "flag": "gb",
                "id": 1166877695754375220,
                "pfp": "example.com",
                "css": "color: #c0c0c0;",
            },
        },
        {
            "board_name": "Test Leaderboard 3",
            "verified": False,
            "timestamp": datetime.now(),
            "rank": 1,
            "qualifier": "Score",
            "qualifier_amount": "1",
            "user": {
                "name": "F.l.0",
                "flag": "gb",
                "id": 1166877695754375220,
                "pfp": "example.com",
                "css": "color: #c0ffc0;",
            },
        },
        {
            "board_name": "Test Leaderboard 3",
            "verified": False,
            "timestamp": datetime.now(),
            "rank": 3,
            "qualifier": "Score",
            "qualifier_amount": "10 Tretrigintillion",
            "user": {
                "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "flag": "fr",
                "id": 1166877695754375220,
                "pfp": "example.com",
                "css": "color: #c0c0c0;",
            },
        },
        {
            "board_name": "Test Leaderboard 2",
            "verified": False,
            "timestamp": datetime.now(),
            "rank": 2,
            "qualifier": "Score",
            "qualifier_amount": "1",
            "user": {
                "name": "F.l.0",
                "flag": "gb",
                "id": 1166877695754375220,
                "pfp": "example.com",
                "css": """    background: -webkit-linear-gradient(#eee, #ff1111);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;""",
            },
        },
    ]
    return example


# Load leaderboards and submissions from JSON files
def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


@app.context_processor
def date_processor():
    def format_date(date):
        now = datetime.now()
        return str(timeago.format(date, now))

    return dict(format_date=format_date)


@app.context_processor
def inject_user():
    return dict(authorized=session.get("discord_user"))


leaderboards = {"main": {"name": "Competitive", "description": "Big balls"}}


@app.route("/")
def home():
    recent_data = get_recent_data()
    return render_template(
        "home.html", recent_changes=recent_data, leaderboards=leaderboards
    )


@app.route("/leaderboards")
def leaderboards_page():
    return render_template(
        "leaderboards.html",
    )


@app.route("/user/<int:user_id>")
def view_user(user_id):
    db = load_json("database.json")
    user = db["users"].get(user_id, None)
    return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
