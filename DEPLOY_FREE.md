# Deploying CCWT for free (no cost to your users)

This app needs a live Python/Flask backend (it computes the wavelet transform
per upload), so it can't run as a static site. Below are free-tier hosts that
support Flask. All of them serve the app publicly at no cost to visitors —
you just create a free account with the host.

Files already prepared in this repo for these hosts:
- `requirements.txt` — pinned Python dependencies
- `Procfile` — process command for Render/Railway-style hosts
- `runtime.txt` — Python version hint

In all cases you must set one environment variable on the host:
- `SESSION_SECRET` — any long random string (used to sign Flask sessions).
  Generate one locally with: `python3 -c "import secrets; print(secrets.token_hex(32))"`

## Option 1: Render (free web service)

1. Push this repo to GitHub (or connect Replit's GitHub integration).
2. On https://render.com, create a **New Web Service** from that repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn --bind=0.0.0.0:$PORT app:app`
5. Add environment variable `SESSION_SECRET`.
6. Deploy. Render's free tier spins the app down when idle (cold start ~30-60s
   on the next request) — fine for a low-traffic research tool.

## Option 2: PythonAnywhere (free tier)

1. Create a free account at https://www.pythonanywhere.com.
2. Upload the project files (or `git clone` your GitHub repo in a Bash console).
3. Create a virtualenv and `pip install -r requirements.txt`.
4. In the **Web** tab, create a new web app, choose "Manual configuration",
   Python 3.11, and point the WSGI file's `application` import at this
   project's `app` object (`from app import app as application`).
5. Set `SESSION_SECRET` in the WSGI file or via `os.environ` before import.
6. Reload the web app. You get a free `<username>.pythonanywhere.com` URL.

## Option 3: Fly.io (free allowance)

1. Install the `flyctl` CLI and run `fly launch` in this project directory
   (it detects the Procfile/Python app automatically).
2. Accept the generated `fly.toml`, or set the internal port to match
   `$PORT` (Fly sets `PORT` automatically; the Procfile already uses it).
3. Run `fly secrets set SESSION_SECRET=<your-random-string>`.
4. Run `fly deploy`. You get a free `<app-name>.fly.dev` URL.

## Notes

- None of these free tiers offer a paid-grade SLA — expect occasional cold
  starts or sleep-on-idle behavior under free plans. For an open-science tool
  with light, sporadic usage this is usually acceptable.
- If your facility later gets institutional hosting or a small budget, moving
  back to Replit's autoscale deployment (or any of these hosts' paid tier)
  removes the idle/cold-start behavior.
