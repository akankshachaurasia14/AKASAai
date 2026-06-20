"""
AKASAai — local web app backend.

Runs entirely on your machine. Flask serves the pink/violet chat UI and
answers every command in Python (the same logic as the original
assistant.py), so the "brain" of AKASAai is Python, while the browser
just renders the page and handles your microphone/speaker via the
Web Speech API (something only a browser can do — there's no Python
equivalent for in-page mic capture).

Run with:
    pip install flask
    python app.py
Then open:
    http://127.0.0.1:5000
"""

import datetime
import webbrowser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ASSISTANT_NAME = "AKASAai"


def get_response(command: str) -> str:
    """
    Core command logic, ported directly from the original assistant.py.
    Returns the text AKASAai should say/display. Returns the literal
    string '__GOODBYE__' when the user wants to end the conversation,
    matching the original script's sentinel value.
    """
    if not command:
        return "Please say or type a command so I can help."

    command = command.strip().lower()

    # Theme commands — the backend doesn't change the UI itself (that's
    # CSS state in the browser), but it confirms the action in words so
    # the frontend knows which theme to switch to.
    if "dark" in command and "theme" in command or command in ("dark theme", "dark mode", "night mode"):
        if "light" not in command and "bright" not in command:
            return "__THEME_DARK__"
    if ("bright" in command or "light" in command) and "theme" in command or command in ("bright theme", "light mode"):
        if "dark" not in command:
            return "__THEME_LIGHT__"

    if any(word in command for word in ["hello", "hi", "hey"]):
        return (f"Hello! I am {ASSISTANT_NAME}. I can switch themes, open websites, "
                f"play music, search the web, and tell you the time or date.")

    if "how are you" in command or "how's it going" in command:
        return "I'm doing great, thank you! Ready to help with whatever you need."

    if "what can you do" in command or "help" in command or "commands" in command:
        return ("I can change my theme (just say 'dark theme' or 'bright theme'), "
                "tell the time or date, search the web, open any website, play music, "
                "and chat with you. Just ask!")

    if "your name" in command or "who are you" in command:
        return f"I am {ASSISTANT_NAME}, your personal pink-powered assistant."

    if "joke" in command:
        return "Why did the programmer quit his job? Because he didn't get arrays."

    if "thank" in command:
        return "You're very welcome! I'm glad I could help."

    if "time" in command:
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}."

    if "date" in command:
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."

    # Music streaming — backend tells the browser which URL to open,
    # since only the browser (not the Python process) should control
    # the user's own browser tabs.
    if "play music" in command or "music" in command:
        if "spotify" in command:
            return "__OPEN__https://www.spotify.com__Opening Spotify for you."
        if "soundcloud" in command:
            return "__OPEN__https://soundcloud.com__Opening SoundCloud."
        return "__OPEN__https://music.youtube.com__Opening YouTube Music for you."

    if "weather" in command:
        return "__OPEN__https://www.google.com/search?q=weather__Opening weather results."

    if command.startswith("search "):
        query = command[len("search "):].strip()
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            return f"__OPEN__{url}__Searching the web for \"{query}\"."
        return "What should I search for?"

    if command.startswith("open "):
        site = command[len("open "):].strip()
        if site:
            url = site
            if not url.startswith("http"):
                url = f"https://{site}" if "." in site else f"https://{site}.com"
            return f"__OPEN__{url}__Opening {site} for you."
        return "Which website should I open?"

    if any(word in command for word in ["bye", "exit", "quit", "goodbye", "stop"]):
        return "__GOODBYE__"

    return ("I didn't quite catch that. Try asking me to switch theme, open a "
            "website, play music, or tell you the time.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/command", methods=["POST"])
def handle_command():
    data = request.get_json(silent=True) or {}
    command = data.get("command", "")
    response = get_response(command)
    return jsonify({"response": response})


if __name__ == "__main__":
    import os

    # Render (and most hosts) assign a port via the PORT environment
    # variable and route public traffic to it. Locally, that variable
    # won't exist, so we fall back to 5000 and open the browser for you.
    port = int(os.environ.get("PORT", 5000))
    is_local = "PORT" not in os.environ

    if is_local:
        url = f"http://127.0.0.1:{port}"
        print(f"AKASAai is running. Opening {url} ...")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        app.run(debug=True, host="127.0.0.1", port=port)
    else:
        # On a real host, bind to 0.0.0.0 so external traffic can reach it.
        app.run(debug=False, host="0.0.0.0", port=port)
