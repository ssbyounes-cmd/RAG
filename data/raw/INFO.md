# Type Against the Clock

A terminal typing game: beat the timer on every text, across three levels, and chase your best score on a local leaderboard.

---

## 1. A short history of typing, and why it matters

**Before the keyboard.** For centuries, writing meant pen and ink. Inventors tried to mechanize it from the early 1700s onward, but nothing was fast or reliable enough to catch on.

**The typewriter (1860s-1870s).** Christopher Latham Sholes, together with Carlos Glidden and Samuel Soule, patented a practical typewriter in 1868 in Milwaukee. In 1873 the Remington company (a firearms and sewing-machine maker) began manufacturing it. This machine popularized the **QWERTY** layout, which is still under your fingers today.

**Touch typing (1880s).** Early typists used two or three fingers and looked at the keys. Public speed contests, such as the well-known 1888 match between Frank McGurrin and Louis Traub, helped prove that memorizing the keyboard and using all ten fingers without looking was dramatically faster. Typing schools and "typing pools" soon followed, and typing became a mainstream profession, especially for women entering office work.

**Better layouts and better machines (1930s-1960s).** August Dvorak patented the Dvorak Simplified Keyboard in 1936, arranged to put common letters on the home row. Electric typewriters, notably IBM's, removed the effort of pressing heavy mechanical keys and pushed speeds higher. The IBM Selectric (1961) became an icon of the office.

**Teletypes and computers (1950s-1980s).** Typewriter keyboards became the standard way to talk to computers, first through teleprinters and terminals, then through personal computers. Software such as Mavis Beacon Teaches Typing (1987) brought structured typing lessons to home computers.

**Today.** Typing happens on laptops, phones, tablets, and even virtual keyboards. Online tools such as TypeRacer, Monkeytype, and many others let people measure and compare their speed worldwide in seconds.

### Why typing is important

* **Productivity.** Most knowledge work (emails, documents, code, chats) runs through a keyboard. Faster, more accurate typing saves hours over a career.
* **Thinking flow.** When typing is automatic, your attention goes to *what* you want to say, not *where* the keys are.
* **Accuracy.** Speed only helps if the text is correct. Fixing mistakes wipes out the time saved, which is why this game scores accuracy, not raw speed.
* **Ergonomics.** Good touch-typing habits (posture, relaxed hands, no constant looking down) reduce strain and fatigue.
* **Education and accessibility.** Typing is a core digital skill for students, and it is an essential communication tool for many people who find handwriting difficult.
* **Career opportunities.** Data entry, transcription, programming, journalism, customer support, and many other roles value fast, accurate typists.

---

## 2. The fastest typists on record

Typing records are messy. They depend on the keyboard layout (QWERTY vs. Dvorak), the device (manual typewriter, electric typewriter, computer), how long the test lasts (a one-minute burst vs. 50 minutes), the rules for errors, and whether Guinness or any official body actually supervised the attempt. All speeds are in **words per minute (WPM)**, where one "word" is conventionally five keystrokes.

| Typist | Speed | Year | Details |
|---|---|---|---|
| **Stella Pajunas-Garnand** (USA) | 216 WPM | 1946 | Highest recorded typewriter speed, set on an IBM electric typewriter with the QWERTY layout during a one-minute test. Widely cited as the fastest ever on a typewriter. |
| **Barbara Blackburn** (USA) | 212 WPM peak, ~150 WPM sustained for 50 minutes | 1980s (Guinness entry; often dated 2005 in later sources) | Used the Dvorak layout. Long recognized by Guinness as the fastest English-language alphanumeric typist. Her record is disputed by some in the typing community because it is old, used a non-QWERTY layout, and has been surpassed unofficially. |
| **Michael Shestov** (Russia) | ~160 WPM average over 5 minutes (801 words) | 1996 | Often cited as a leading example of sustained speed. |
| **Sean Wrona** (USA) | 256 WPM sprint on TypeRacer; 174 WPM over 50 minutes (unofficial) | 2010 | Won the first Ultimate Typing Championship in 2010 (averaging about 163 WPM in the final event). His 256 WPM was a short-text sprint, and his 174 WPM, 50-minute run beat Blackburn's endurance mark but was not supervised by Guinness. |
| **Guilherme Sandrini** (Brazil) | up to ~290 WPM | 2010s | Reported as the highest online sprint speed on short text selections (on typingzone.com). It is not an official world record. |

**Takeaways**

* On a **typewriter**, Stella Pajunas-Garnand's 216 WPM is the number everyone points to.
* For **officially recognized Guinness** speed, the name is Barbara Blackburn.
* On **computers and online tests**, Sean Wrona and Guilherme Sandrini set the highest short-burst numbers, and these are generally unofficial.
* For comparison, an average adult types roughly 40 WPM, and 70-80 WPM is considered very good.

*Records were compiled from public sources (typing sites, Guinness citations, and encyclopedic references). Figures and dates differ slightly between sources, so treat them as approximate.*

---

## 3. How to run the script and test yourself

### Requirements

* **Python 3.8 or newer.**
* No extra packages to install; the script uses only the standard library.
* An interactive terminal at least ~80 columns wide.
  * Linux / macOS: any terminal.
  * Windows: Windows Terminal, PowerShell, or a modern `cmd` window (ANSI colors enabled automatically).

### Run it

```bash
python type.py
# or, on some systems:
python3 type.py
```

### How the game works

1. You enter your **name**. Names are unique: typing the same name again (case-insensitive) continues your existing record.
2. Each text is shown with a **countdown timer**. Type it before time runs out:
   * Correct characters turn **green**, mistakes turn **red**, and the next character to type is underlined.
   * **Backspace** fixes mistakes.
   * **Enter** submits early. The text is also submitted automatically if you finish it perfectly.
   * When the timer hits zero, whatever you have typed is scored, and unfinished text counts against you.
3. Three levels:

| Level | Content | Weight in final score |
|---|---|---|
| 1 | 5 words | 20% |
| 2 | 2 sentences | 30% |
| 3 | 1 paragraph | 50% |

### Scoring

```
Level accuracy = correctly placed characters / total characters in the level
Final score    = 0.20 x Lvl 1 + 0.30 x Lvl 2 + 0.50 x Lvl 3
```

A character counts as correct only if it matches the target at the same position. Level 3 is worth half of the final score, so don't burn out early.

### The high score file

On the first run, `highscore.json` is created in the same folder as `type.py`. On later runs it is parsed and updated. Each player is stored under their unique name:

```json
{
  "version": 1,
  "players": {
    "alice": {
      "name": "Alice",
      "best_score": 91.35,
      "best_level_accuracy": [100.0, 94.4, 87.3],
      "best_wpm": 58.2,
      "best_date": "2026-11-01T14:20:05",
      "games_played": 4,
      "last_played": "2026-11-01T14:31:47"
    }
  }
}
```

* Only your **best** score is kept, though `games_played` counts every attempt.
* If the file is corrupted, it is copied to `highscore.json.bak` and a fresh file is created.
* Delete `highscore.json` to reset the leaderboard.

### Tweaking difficulty

At the top of `type.py` you can edit the word, sentence, and paragraph lists, or change each level's timer. A text's limit is `base + length / cps`, where `cps` is the characters-per-second you are expected to sustain. Raise `cps` for a harder game; lower it for more breathing room.

### Tips

* Keep your eyes on the text, not the keyboard.
* Stay accurate first, and speed will come on its own.
* Don't panic when the bar turns red; backspacing a mistake costs less than leaving it.
* Press **Ctrl+C** at any time to quit.

Good luck, and happy typing!
