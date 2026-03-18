from datetime import datetime, UTC
from flask import Flask, render_template_string
import os

app = Flask(__name__)

STATUS_PAGE = """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Cloud App Status</title>
        <style>
            :root {
                --bg-1: #0f172a;
                --bg-2: #1e293b;
                --ok: #22c55e;
                --card: rgba(255, 255, 255, 0.12);
                --text: #e2e8f0;
                --muted: #94a3b8;
            }
            * { box-sizing: border-box; }
            body {
                margin: 0;
                min-height: 100vh;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                color: var(--text);
                background: radial-gradient(circle at 20% 10%, #334155 0%, var(--bg-1) 40%, var(--bg-2) 100%);
                display: grid;
                place-items: center;
                padding: 20px;
            }
            .card {
                width: min(700px, 100%);
                background: var(--card);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
            }
            h1 {
                margin: 0 0 8px;
                font-size: 1.8rem;
            }
            .subtitle {
                margin: 0 0 20px;
                color: var(--muted);
            }
            .row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 12px 0;
                border-top: 1px solid rgba(255, 255, 255, 0.15);
            }
            .row:first-of-type { border-top: 0; }
            .status {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-weight: 600;
            }
            .dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: var(--ok);
                box-shadow: 0 0 12px var(--ok);
            }
            code {
                color: #bae6fd;
                background: rgba(0, 0, 0, 0.2);
                padding: 2px 8px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <main class="card">
            <h1>Cloud Deployment Test</h1>
            <p class="subtitle">Visual status page for quick deployment checks.</p>

            <div class="row">
                <span>Service</span>
                <span class="status"><span class="dot"></span>Running</span>
            </div>
            <div class="row">
                <span>Environment</span>
                <code>{{ environment }}</code>
            </div>
            <div class="row">
                <span>Health Endpoint</span>
                <code>/health -> ok</code>
            </div>
            <div class="row">
                <span>Server UTC Time</span>
                <code>{{ now_utc }}</code>
            </div>
        </main>
    </body>
</html>
"""


@app.get("/")
def home() -> tuple[dict[str, str], int]:
    return (
        {
            "message": "Python cloud deployment test app is running.",
            "environment": os.getenv("ENVIRONMENT", "local"),
        },
        200,
    )


@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return ({"status": "ok"}, 200)


@app.get("/dashboard")
def dashboard() -> str:
    return render_template_string(
        STATUS_PAGE,
        environment=os.getenv("ENVIRONMENT", "local"),
        now_utc=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
