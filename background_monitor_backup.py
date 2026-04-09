import time
import json
import os
import signal
import logging
import sys
from datetime import datetime, date
from pathlib import Path

# ── Optional desktop notifications ──────────────────────────────────────────
try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

# ── Constants ────────────────────────────────────────────────────────────────
CONFIG_FILE   = Path("screen_config.json")
LOG_FILE      = Path("mindbalance.log")
POLL_INTERVAL = 60          # seconds between polls
SLEEP_GAP_MAX = 300         # deltas > this = PC was asleep; skip
ALERT_COOLDOWN = 900        # 15 min between repeat alerts at same level

# Alert thresholds as fractions of daily limit
WARN_LEVELS = {
    "50%":  0.50,
    "75%":  0.75,
    "90%":  0.90,
    "100%": 1.00,
}

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("MindBalance")

# ── Graceful shutdown ────────────────────────────────────────────────────────
_running = True

def _handle_signal(sig, frame):
    global _running
    log.info("Shutdown signal received — stopping monitor.")
    _running = False

signal.signal(signal.SIGINT,  _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)

# ── Config helpers ────────────────────────────────────────────────────────────
DEFAULT_CONFIG = {
    "limit_hours":   4.0,          # daily screen-time limit in HOURS
    "status":        "active",     # "active" | "paused"
    "date":          "",           # YYYY-MM-DD of current tracking day
    "elapsed_secs":  0.0,          # total seconds tracked today
    "last_update":   0.0,          # unix timestamp of last poll
    "history":       {},           # { "YYYY-MM-DD": elapsed_secs }
    "alert_sent":    {},           # { "50%": unix_ts, ... }
}

def _validate_config(cfg: dict) -> dict:
    """Fill missing keys with defaults; coerce bad types."""
    result = dict(DEFAULT_CONFIG)
    result.update(cfg)
    # Coerce numeric fields
    try:
        result["limit_hours"]  = float(result["limit_hours"])
    except (TypeError, ValueError):
        result["limit_hours"]  = 4.0
    try:
        result["elapsed_secs"] = float(result["elapsed_secs"])
    except (TypeError, ValueError):
        result["elapsed_secs"] = 0.0
    try:
        result["last_update"]  = float(result["last_update"])
    except (TypeError, ValueError):
        result["last_update"]  = time.time()
    if not isinstance(result["history"],    dict): result["history"]    = {}
    if not isinstance(result["alert_sent"], dict): result["alert_sent"] = {}
    return result

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r") as f:
                raw = json.load(f)
            return _validate_config(raw)
        except json.JSONDecodeError as e:
            log.warning(f"Config corrupted ({e}); resetting to defaults.")
        except Exception as e:
            log.warning(f"Config read error ({e}); resetting to defaults.")
    cfg = dict(DEFAULT_CONFIG)
    cfg["date"]        = date.today().isoformat()
    cfg["last_update"] = time.time()
    return cfg

def save_config(cfg: dict) -> None:
    # Write to a temp file first, then atomic rename — prevents corruption
    tmp = CONFIG_FILE.with_suffix(".tmp")
    try:
        with tmp.open("w") as f:
            json.dump(cfg, f, indent=2)
        tmp.replace(CONFIG_FILE)
    except Exception as e:
        log.error(f"Failed to save config: {e}")
        if tmp.exists():
            tmp.unlink(missing_ok=True)

# ── Notification helper ──────────────────────────────────────────────────────
def send_alert(title: str, message: str) -> None:
    log.warning(f"ALERT | {title} | {message}")
    if HAS_PLYER:
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="MindBalance",
                timeout=12,
            )
            return
        except Exception as e:
            log.debug(f"Plyer notification failed: {e}")
    # Fallback: visible terminal bell
    print(f"\a🔔  {title}\n   {message}", flush=True)

# ── Day-reset logic ──────────────────────────────────────────────────────────
def maybe_reset_day(cfg: dict, today: str, now: float) -> dict:
    """Reset elapsed counter and alert state when the calendar date changes."""
    if cfg.get("date") == today:
        return cfg

    # Archive yesterday's session
    yesterday = cfg.get("date", "")
    if yesterday:
        cfg["history"][yesterday] = cfg.get("elapsed_secs", 0.0)
        # Keep only last 30 days of history
        if len(cfg["history"]) > 30:
            oldest = sorted(cfg["history"])[0]
            del cfg["history"][oldest]

    log.info(f"New day detected ({yesterday} → {today}). Resetting counters.")
    cfg["date"]        = today
    cfg["elapsed_secs"] = 0.0
    cfg["last_update"] = now
    cfg["alert_sent"]  = {}
    return cfg

# ── Alert logic ──────────────────────────────────────────────────────────────
def check_and_alert(cfg: dict, elapsed_secs: float, limit_secs: float, now: float) -> dict:
    ratio = elapsed_secs / limit_secs if limit_secs > 0 else 0.0

    elapsed_h = elapsed_secs / 3600
    limit_h   = limit_secs  / 3600

    for label, threshold in WARN_LEVELS.items():
        if ratio < threshold:
            continue  # not reached yet

        last_sent = cfg["alert_sent"].get(label, 0)

        # For sub-100% warnings, send only once per day (cooldown = rest of day).
        # For 100% (over-limit), repeat every ALERT_COOLDOWN seconds.
        cooldown = ALERT_COOLDOWN if label == "100%" else 86400

        if now - last_sent < cooldown:
            continue  # already alerted recently for this level

        if label == "100%":
            over_h = elapsed_h - limit_h
            over_m = over_h * 60
            title   = "⛔ MindBalance: Limit Exceeded!"
            message = (
                f"You've been on-screen {elapsed_h:.1f}h — "
                f"{over_m:.0f} min OVER your {limit_h:.1f}h limit. "
                "Time to step away!"
            )
        else:
            remaining_m = (limit_secs - elapsed_secs) / 60
            title   = f"⚠️ MindBalance: {label} of Daily Limit"
            message = (
                f"Screen time: {elapsed_h:.1f}h / {limit_h:.1f}h. "
                f"Only {remaining_m:.0f} min remaining."
            )

        send_alert(title, message)
        cfg["alert_sent"][label] = now

    return cfg

# ── Main monitor loop ────────────────────────────────────────────────────────
def monitor() -> None:
    log.info("MindBalance monitor started.")

    while _running:
        now   = time.time()
        today = date.today().isoformat()

        cfg = load_config()
        cfg = maybe_reset_day(cfg, today, now)

        if cfg.get("status") == "active":
            last_update = cfg.get("last_update", now)
            delta = now - last_update

            if 0 < delta < SLEEP_GAP_MAX:
                cfg["elapsed_secs"] = cfg.get("elapsed_secs", 0.0) + delta
            elif delta >= SLEEP_GAP_MAX:
                log.info(f"Large time gap ({delta:.0f}s) — PC was likely asleep. Skipping.")

            cfg["last_update"] = now

            elapsed_secs = cfg["elapsed_secs"]
            limit_secs   = cfg["limit_hours"] * 3600  # ✅ FIX: limit in seconds

            elapsed_h  = elapsed_secs / 3600
            limit_h    = cfg["limit_hours"]
            remaining_m = max(0, (limit_secs - elapsed_secs) / 60)

            log.info(
                f"Status: {elapsed_h:.2f}h / {limit_h:.1f}h used | "
                f"{remaining_m:.0f} min remaining | "
                f"ratio={elapsed_secs/limit_secs*100:.1f}%"
            )

            cfg = check_and_alert(cfg, elapsed_secs, limit_secs, now)

        elif cfg.get("status") == "paused":
            log.info("Tracking is paused.")

        save_config(cfg)

        # Interruptible sleep — checks _running flag every second
        for _ in range(POLL_INTERVAL):
            if not _running:
                break
            time.sleep(1)

    log.info("MindBalance monitor stopped cleanly.")

# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MindBalance Screen-Time Monitor")
    parser.add_argument("--limit", type=float, help="Daily screen-time limit in hours")
    parser.add_argument("--pause", action="store_true", help="Pause tracking")
    parser.add_argument("--resume", action="store_true", help="Resume tracking")
    parser.add_argument("--status", action="store_true", help="Print current status and exit")
    args = parser.parse_args()

    if args.limit or args.pause or args.resume or args.status:
        cfg = load_config()
        if args.limit:
            cfg["limit_hours"] = args.limit
            log.info(f"Daily limit set to {args.limit}h")
        if args.pause:
            cfg["status"] = "paused"
            log.info("Tracking paused.")
        if args.resume:
            cfg["status"] = "active"
            cfg["last_update"] = time.time()  # reset to avoid phantom time
            log.info("Tracking resumed.")
        if args.status:
            elapsed_h = cfg.get("elapsed_secs", 0) / 3600
            limit_h   = cfg.get("limit_hours", 4.0)
            print(f"\nMindBalance Status")
            print(f"  Date    : {cfg.get('date')}")
            print(f"  Elapsed : {elapsed_h:.2f}h / {limit_h:.1f}h")
            print(f"  Status  : {cfg.get('status')}")
            sys.exit(0)
        save_config(cfg)
        if not (args.status or args.pause):
            monitor()
    else:
        monitor()