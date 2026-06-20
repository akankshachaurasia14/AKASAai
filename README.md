# AKASAai — Local Web App (Python + Flask)

A pink/violet animated AI-assistant UI, backed by a real Python process.
The browser renders the page and handles your microphone/speaker (via the
browser's built-in Web Speech API — there's no Python equivalent for
in-page mic capture, so that part is necessarily JS). Every command you
type or speak is sent to the Python backend, which decides the answer.

## Project structure

```
akasaai_webapp/
├── app.py                 # Flask server + all command logic (Python)
├── templates/
│   └── index.html         # UI: same markup/CSS as before, JS calls the backend
└── README.md
```

## Setup

```bash
pip install flask
```

(If you also want the original desktop version's voice/text-to-speech
packages for some other script, those aren't needed here — this app uses
the browser's voice features instead.)

## Run

```bash
python app.py
```

This starts a local server and opens **http://127.0.0.1:5000** in your
browser automatically. If it doesn't open by itself, just visit that
address manually.

## How it works

- `app.py` defines `get_response(command)` — the exact same decision
  logic as the original assistant (greetings, time, date, jokes, music,
  search, open-website, goodbye), now served over HTTP at `/api/command`.
- `templates/index.html` is your original animated UI, unchanged in
  appearance. Its JavaScript now calls the Python backend with
  `fetch('/api/command', ...)` for every command instead of deciding
  answers itself.
- Special response codes (`__THEME_DARK__`, `__THEME_LIGHT__`,
  `__OPEN__<url>__<message>`, `__GOODBYE__`) are decided by Python and
  interpreted by the frontend to switch themes, open a browser tab, or
  end the conversation — keeping all "decision-making" in Python while
  letting the browser do what only a browser can (render gradients/
  animation, open new tabs, capture your voice).

## Stopping the server

Press `Ctrl+C` in the terminal where it's running.

## Deploying to a public URL (Render, free tier)

`127.0.0.1` only ever works on the machine running the server — it can
never become a public link. To get a real `https://something.onrender.com`
URL anyone can open, deploy to Render:

1. **Push this folder to a GitHub repo** (a free GitHub account if you
   don't have one already). The repo just needs `app.py`,
   `templates/index.html`, and `requirements.txt` at the structure shown
   above.

2. **Sign up at [render.com](https://render.com)** using GitHub login —
   no credit card needed for the free tier.

3. **New → Web Service** → connect your GitHub repo.

4. Render auto-detects Python. Set these two fields if it doesn't fill
   them in for you:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`

5. Click **Create Web Service**. After the build finishes (1-3 minutes),
   Render gives you a URL like `https://akasaai.onrender.com` — that's
   your permanent public link.

### What to expect on the free tier

- No credit card, no time limit on the free tier itself.
- The free instance **sleeps after 15 minutes of no traffic**. The next
  visitor's first request takes ~30-60 seconds to wake it back up — after
  that it's instant until it goes idle again. This is normal for free
  hosting, not a bug in this app.
- If you outgrow that (e.g. you don't want the sleep delay), Render's
  paid Starter tier (~$7/mo) keeps it always-on.

### Why this works where your laptop didn't

Render gives the app a real public IP and domain, and assigns the port
via a `PORT` environment variable — `app.py` already reads that
automatically (falling back to `127.0.0.1:5000` when run locally, where
`PORT` doesn't exist). You don't need to change any code between
local testing and deploying.

## Notes on voice

- Voice input/output uses Chrome/Edge's Web Speech API. If your browser
  doesn't support it, the mic button will tell you so — type your
  commands instead.
- No audio leaves your machine for typed commands; for voice input,
  Chrome sends audio to Google's speech service to transcribe it (this
  is a browser-level behavior, same as in the original HTML file).
