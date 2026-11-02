#!/usr/bin/env python3
"""
type.py - Beat-the-clock typing game for your terminal.

Three levels, each with a countdown timer per text:
    Level 1: 5 words        (20% of final score)
    Level 2: 2 sentences    (30% of final score)
    Level 3: 1 paragraph    (50% of final score)

Final score = 0.20 * Lvl1 accuracy + 0.30 * Lvl2 accuracy + 0.50 * Lvl3 accuracy

Best scores are stored per player name in `highscore.json`, located next to
this script. The file is parsed if it already exists and created if it doesn't.

Pure standard library. Works on Linux, macOS and Windows (Python 3.8+).
Run:  python type.py
"""

import json
import os
import random
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

HIGHSCORE_FILE = Path(__file__).resolve().parent / "highscore.json"
MAX_NAME_LEN = 20
LEADERBOARD_SIZE = 10

# Time limit for a text = base + len(text) / cps
#   cps = characters per second you are expected to sustain (5 chars = 1 word,
#   so 2.5 cps = 30 WPM and 3.5 cps = 42 WPM). Lower cps = more generous timer.
WORDS = [
    "keyboard", "rhythm", "journey", "monitor", "puzzle", "thunder", "velocity",
    "harvest", "lantern", "compass", "balance", "whisper", "orbit", "granite",
    "pixel", "meadow", "shuttle", "crystal", "network", "gadget", "horizon",
    "sparrow", "marathon", "blanket", "fortune", "canyon", "dynamo", "origami",
]

SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes progress, not perfection.",
    "A calm mind types faster than a rushed one.",
    "Every expert was once a beginner who kept going.",
    "The early bird catches the worm, but the second mouse gets the cheese.",
    "Good code is like a good joke; it needs no explanation.",
    "Rain tapped softly on the window while the city slept.",
    "Fast fingers are built one careful keystroke at a time.",
    "She packed her bag, locked the door, and walked toward the sunrise.",
    "Curiosity is the engine of achievement.",
]

PARAGRAPHS = [
    "Typing is a skill that quietly shapes our days. Whether we are writing "
    "an email, fixing a bug, or telling a story, our fingers carry our "
    "thoughts onto the screen. The more naturally the keys respond, the less "
    "we think about them, and the more room we have for ideas.",

    "The first typewriters were noisy, heavy machines that changed how people "
    "worked and wrote. Offices filled with the rhythm of clacking keys and "
    "ringing bells. Today the machines are silent and slim, but the "
    "fundamental layout under our fingers has barely changed in over a "
    "century.",

    "Speed is exciting, but accuracy is what makes speed useful. A fast "
    "typist who makes constant mistakes spends the saved time fixing errors. "
    "Slow down just enough to stay precise, and your speed will rise "
    "naturally as your muscle memory grows stronger every single day.",

    "Beyond the mountains, a small village woke to the sound of church bells "
    "and fresh bread baking. Children ran along the cobblestone streets while "
    "farmers carried baskets of apples to the market. Nothing seemed to "
    "hurry here, and yet every task was finished before the sun went down.",

    "Learning to type without looking at the keys feels awkward at first. "
    "Your eyes want to help, your fingers hesitate, and progress seems slow. "
    "Then one day the words simply appear on the screen as fast as you can "
    "think them, and you realize the effort was worth every minute.",
]

LEVELS = [
    {"name": "Level 1 - Words",     "label": "Word",      "count": 5, "pool": WORDS,
     "cps": 2.5, "base": 2.5, "weight": 0.20,
     "desc": "Type each of the 5 words before its timer runs out."},
    {"name": "Level 2 - Sentences", "label": "Sentence",  "count": 2, "pool": SENTENCES,
     "cps": 3.5, "base": 4.0, "weight": 0.30,
     "desc": "Type each of the 2 sentences before its timer runs out."},
    {"name": "Level 3 - Paragraph", "label": "Paragraph", "count": 1, "pool": PARAGRAPHS,
     "cps": 3.5, "base": 8.0, "weight": 0.50,
     "desc": "Type the whole paragraph before the timer runs out."},
]

# --------------------------------------------------------------------------- #
# Terminal helpers (ANSI colours + raw key input, cross-platform)
# --------------------------------------------------------------------------- #

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[90m"
GREEN = "\033[32m"
RED_BG = "\033[41;97m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
UNDERLINE = "\033[4;97m"

if os.name == "nt":
    import msvcrt
    os.system("")  # enables ANSI escape processing in modern Windows consoles
else:
    import select
    import termios
    import tty


class Keys:
    """Context manager giving non-blocking single-key input."""

    def __enter__(self):
        if os.name != "nt":
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        return self

    def __exit__(self, *exc):
        if os.name != "nt":
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)

    def flush(self):
        """Throw away any keys pressed while nothing was being timed."""
        if os.name == "nt":
            while msvcrt.kbhit():
                msvcrt.getwch()
        else:
            termios.tcflush(self.fd, termios.TCIFLUSH)

    def get(self, timeout):
        """Return pressed character(s) or '' if nothing within `timeout` sec."""
        if os.name == "nt":
            end = time.monotonic() + timeout
            while time.monotonic() < end:
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch in ("\x00", "\xe0"):      # special key (arrows, F-keys)
                        msvcrt.getwch()
                        return ""
                    return ch
                time.sleep(0.005)
            return ""
        ready, _, _ = select.select([self.fd], [], [], timeout)
        if not ready:
            return ""
        data = os.read(self.fd, 64).decode("utf-8", errors="ignore")
        if data.startswith("\x1b"):                  # escape sequence (arrows...)
            return ""
        return data


def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def term_width():
    return max(40, min(shutil.get_terminal_size((80, 24)).columns - 2, 90))


# --------------------------------------------------------------------------- #
# High score file handling
# --------------------------------------------------------------------------- #

def _empty_db():
    return {"version": 1, "players": {}}


def _valid_db(db):
    return (isinstance(db, dict) and isinstance(db.get("players"), dict)
            and all(isinstance(p, dict) for p in db["players"].values()))


def save_highscores(db):
    """Write atomically so a crash can never leave a half-written file."""
    tmp = HIGHSCORE_FILE.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(db, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, HIGHSCORE_FILE)


def load_highscores():
    """Parse highscore.json if it exists, otherwise create it."""
    if HIGHSCORE_FILE.exists():
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as fh:
                db = json.load(fh)
            if _valid_db(db):
                return db
            raise ValueError("unexpected structure")
        except (ValueError, OSError) as err:
            backup = HIGHSCORE_FILE.with_suffix(".json.bak")
            try:
                shutil.copyfile(HIGHSCORE_FILE, backup)
            except OSError:
                pass
            print(f"{YELLOW}highscore.json was unreadable ({err}). "
                  f"A backup was saved to {backup.name} and a fresh file was created.{RESET}")
            time.sleep(1.5)
    db = _empty_db()
    save_highscores(db)
    return db


def record_score(db, name, final, level_accs, wpm):
    """Store the run. Names are unique (case-insensitive). Returns True on new best."""
    key = name.casefold()
    now = datetime.now().isoformat(timespec="seconds")
    player = db["players"].get(key)
    new_best = False
    if player is None:
        player = {"name": name, "best_score": -1.0, "games_played": 0}
        db["players"][key] = player
    player["games_played"] = int(player.get("games_played", 0)) + 1
    player["last_played"] = now
    if final > float(player.get("best_score", -1.0)):
        player.update({
            "name": name,
            "best_score": round(final, 2),
            "best_level_accuracy": [round(a, 2) for a in level_accs],
            "best_wpm": round(wpm, 1),
            "best_date": now,
        })
        new_best = True
    save_highscores(db)
    return new_best


def show_leaderboard(db, highlight=None):
    players = sorted(db["players"].values(),
                     key=lambda p: float(p.get("best_score", 0)), reverse=True)
    print(f"{BOLD}{CYAN}  LEADERBOARD{RESET}")
    if not players:
        print(f"  {DIM}No scores yet - be the first!{RESET}")
        return
    print(f"  {DIM}{'#':>2}  {'Name':<{MAX_NAME_LEN}} {'Score':>7} {'WPM':>6} {'Games':>6}{RESET}")
    for i, p in enumerate(players[:LEADERBOARD_SIZE], 1):
        mark = BOLD + YELLOW if highlight and p["name"].casefold() == highlight.casefold() else ""
        print(f"  {mark}{i:>2}  {p['name']:<{MAX_NAME_LEN}} "
              f"{float(p.get('best_score', 0)):>6.1f}% "
              f"{float(p.get('best_wpm', 0)):>6.1f} "
              f"{int(p.get('games_played', 0)):>6}{RESET}")


# --------------------------------------------------------------------------- #
# Game logic
# --------------------------------------------------------------------------- #

def accuracy(target, typed):
    """Fraction of target characters typed correctly in the right position."""
    correct = sum(1 for a, b in zip(target, typed) if a == b)
    return correct, len(target)


def time_limit(level, target):
    return round(level["base"] + len(target) / level["cps"], 1)


def wrap_target(target, typed, width):
    """Colour the target text by progress and wrap it without losing indices."""
    lines, current, cur_len = [], "", 0
    idx = 0
    for token in re.findall(r"\S+\s*", target):
        if cur_len + len(token) > width and current:
            lines.append(current)
            current, cur_len = "", 0
        for ch in token:
            if idx < len(typed):
                current += (GREEN + ch + RESET) if typed[idx] == ch else (RED_BG + ch + RESET)
            elif idx == len(typed):
                current += UNDERLINE + ch + RESET
            else:
                current += DIM + ch + RESET
            idx += 1
        cur_len += len(token)
    if current:
        lines.append(current)
    return lines


def draw(header, target, typed, remaining, limit):
    width = term_width()
    frac = max(0.0, remaining / limit)
    bar_len = min(40, width - 16)
    filled = int(round(bar_len * frac))
    colour = GREEN if frac > 0.5 else (YELLOW if frac > 0.25 else RED)
    bar = colour + "#" * filled + RESET + DIM + "-" * (bar_len - filled) + RESET

    lines = [f"{BOLD}{CYAN}{header}{RESET}", ""]
    lines += ["  " + l for l in wrap_target(target, typed, width - 4)]
    lines += ["",
              f"  {colour}{BOLD}{max(0.0, remaining):5.1f}s{RESET} [{bar}]",
              "",
              f"  {DIM}Enter = submit now   Backspace = fix   Ctrl+C = quit{RESET}"]
    sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines) + "\033[J")
    sys.stdout.flush()


def run_item(keys, header, target, limit):
    """Time one text. Returns (typed, seconds_used, timed_out)."""
    typed = ""
    clear()
    keys.flush()
    start = time.monotonic()
    while True:
        elapsed = time.monotonic() - start
        remaining = limit - elapsed
        draw(header, target, typed, remaining, limit)
        if remaining <= 0:
            return typed, limit, True
        chunk = keys.get(0.05)
        for ch in chunk:
            if ch in "\r\n":
                return typed, time.monotonic() - start, False
            if ch in ("\x7f", "\x08"):
                typed = typed[:-1]
            elif ch == "\x03":
                raise KeyboardInterrupt
            elif ch.isprintable() and len(typed) < len(target):
                typed += ch
        if typed == target:
            draw(header, target, typed, limit - (time.monotonic() - start), limit)
            return typed, time.monotonic() - start, False


def countdown(label):
    for n in (3, 2, 1):
        sys.stdout.write(f"\r  {BOLD}{YELLOW}{label} starts in {n}...{RESET}   ")
        sys.stdout.flush()
        time.sleep(0.8)
    sys.stdout.write("\r\033[K")


def play_level(keys, number, level):
    clear()
    print(f"\n  {BOLD}{CYAN}{level['name']}{RESET}  "
          f"{DIM}(worth {int(level['weight'] * 100)}% of your score){RESET}\n")
    print(f"  {level['desc']}")
    print(f"  {DIM}Unfinished text counts against your accuracy.{RESET}\n")
    keys.__exit__(None, None, None)     # back to normal input for the prompt
    try:
        input("  Press Enter when you are ready... ")
    finally:
        keys.__enter__()
    countdown(f"Level {number}")

    total_correct = total_chars = 0
    total_time = 0.0
    items = random.sample(level["pool"], level["count"])
    for i, target in enumerate(items, 1):
        limit = time_limit(level, target)
        header = f"{level['name']}  -  {level['label']} {i}/{level['count']}"
        typed, used, timed_out = run_item(keys, header, target, limit)
        correct, chars = accuracy(target, typed)
        total_correct += correct
        total_chars += chars
        total_time += used
        pct = 100 * correct / chars
        status = f"{RED}time's up{RESET}" if timed_out else f"{GREEN}on time{RESET}"
        print(f"\n  Result: {BOLD}{pct:.0f}%{RESET} accurate  ({status})")
        time.sleep(1.4)

    acc = 100 * total_correct / total_chars
    wpm = (total_correct / 5) / (total_time / 60) if total_time > 0 else 0.0
    return {"accuracy": acc, "wpm": wpm, "time": total_time}


def play_game(keys):
    results = [play_level(keys, n, lvl) for n, lvl in enumerate(LEVELS, 1)]
    accs = [r["accuracy"] for r in results]
    final = sum(lvl["weight"] * r["accuracy"] for lvl, r in zip(LEVELS, results))
    total_time = sum(r["time"] for r in results)
    # overall WPM = time-weighted across the levels
    wpm = (sum(r["wpm"] * r["time"] for r in results) / total_time) if total_time else 0.0
    return final, accs, wpm


def grade(score):
    if score >= 97: return "Keyboard Legend"
    if score >= 90: return "Speed Demon"
    if score >= 75: return "Solid Typist"
    if score >= 50: return "Getting There"
    return "Keep Practicing"


def show_results(final, accs, wpm, new_best):
    clear()
    print(f"\n  {BOLD}{CYAN}FINAL RESULTS{RESET}\n")
    for lvl, a in zip(LEVELS, accs):
        print(f"  {lvl['name']:<24} {a:6.1f}%  x {int(lvl['weight'] * 100):>2}%"
              f"  = {a * lvl['weight']:5.1f}")
    print(f"  {'-' * 50}")
    print(f"  {BOLD}Final score: {final:.1f}%{RESET}   ({grade(final)})")
    print(f"  Average speed: {wpm:.1f} WPM")
    if new_best:
        print(f"\n  {BOLD}{YELLOW}*** New personal best! ***{RESET}")
    print()


def ask_name(db):
    while True:
        name = " ".join(input("  Enter your name: ").split())[:MAX_NAME_LEN]
        if name:
            break
        print("  Name cannot be empty.")
    existing = db["players"].get(name.casefold())
    if existing:
        print(f"  Welcome back, {BOLD}{existing['name']}{RESET}! "
              f"Your best so far: {float(existing.get('best_score', 0)):.1f}%")
        name = existing["name"]          # keep the originally registered spelling
    else:
        print(f"  Registered new player: {BOLD}{name}{RESET}")
    return name


def main():
    if not sys.stdin.isatty():
        sys.exit("type.py needs an interactive terminal.")

    db = load_highscores()
    clear()
    print(f"\n  {BOLD}{CYAN}=== TYPE AGAINST THE CLOCK ==={RESET}\n")
    show_leaderboard(db)
    print()
    name = ask_name(db)

    try:
        while True:
            with Keys() as keys:
                final, accs, wpm = play_game(keys)
            new_best = record_score(db, name, final, accs, wpm)
            show_results(final, accs, wpm, new_best)
            show_leaderboard(db, highlight=name)
            print()
            again = input("  Play again? [y/N] ").strip().lower()
            if again != "y":
                break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sys.stdout.write(RESET)
    print("\n  Thanks for playing!\n")


if __name__ == "__main__":
    main()
