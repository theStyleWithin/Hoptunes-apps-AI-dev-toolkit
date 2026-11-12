# Hoptunes-apps-AI-dev-toolkit
a handoff development toolkit for Hoptunes apps development take this hand off package to claude ai or whatever coder agent you use and make whatever you want if you're unsatified with the currently line up of apps and you just want to make it yourself.

**For [Hop-tunes](https://github.com/theStyleWithin/Hop-tunes)**, the local-first music player. This repository is only the handoff package; the
player itself (and the two apps that exist so far) live in the Hop-tunes repository. The two go hand in hand.

## How to use it

1. Get the Hop-tunes source: `git clone https://github.com/theStyleWithin/Hop-tunes`
2. Give your coding agent (Claude or any other) **this toolkit** and the Hop-tunes source.
3. Tell it what you want, for example:
   *"Read AGENT-BRIEF.md in the toolkit, then help me add an app to Hop-tunes: a sleep timer that pauses the music. Show me a screenshot and run the tests."*
   More wording ideas are in [`docs/PROMPTS.md`](docs/PROMPTS.md).

## What is inside

| File | What it is |
|---|---|
| [`AGENT-BRIEF.md`](AGENT-BRIEF.md) | **start here.** What an app is, the rules (offline first, no telemetry, tests), how the agent should work with you. `AGENTS.md` and `CLAUDE.md` point to it. |
| [`docs/HOW-APPS-WORK.md`](docs/HOW-APPS-WORK.md) | the apps tab, the registry, the host, what an app's QML may use |
| [`docs/ADD-AN-APP.md`](docs/ADD-AN-APP.md) | adding an app, step by step |
| [`docs/NETWORK-AND-PRIVACY.md`](docs/NETWORK-AND-PRIVACY.md) | the privacy promises and the gateway every online app must use (read before any app that needs the internet) |
| [`docs/TESTING.md`](docs/TESTING.md) | building, running the tests, taking screenshots |
| [`docs/LESSONS.md`](docs/LESSONS.md) | mistakes that were already made once, so they are not made again |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | what to say to your agent |
| [`docs/DROP-IN-APPS-PLAN.md`](docs/DROP-IN-APPS-PLAN.md) | the planned way to add apps without rebuilding Hop-tunes (not built yet) |
| [`examples/sleep-timer/`](examples/sleep-timer/) | a complete, tested example app (a patch you can apply and build) |
| [`scripts/check_app.py`](scripts/check_app.py) | checks an app was added correctly: `python3 scripts/check_app.py <app-id> --repo <Hop-tunes folder>` |

## Honest status

* **Apps are built into Hop-tunes today.** Adding one means adding a QML file and a few lines to the Hop-tunes source, then building Hop-tunes
  (instructions inside; your agent can do it). **Drop-in apps that need no rebuild are planned, not built**, because an app someone else wrote
  must be sandboxed properly first: see [`docs/DROP-IN-APPS-PLAN.md`](docs/DROP-IN-APPS-PLAN.md).
* The rules matter more than the code: Hop-tunes promises no required accounts, no telemetry and nothing phoned home. Apps that use the internet
  must ask first, name the sites they contact, and go through one gateway.
* Written against Hop-tunes 1.9.0. If a file path in these docs does not exist in the Hop-tunes you have, the docs are older than your Hop-tunes:
  tell your agent to read the Hop-tunes source and trust that over these docs.

## Licence

This toolkit's text and scripts are MIT (see `LICENSE`). Hop-tunes is GPL-3.0-or-later: an app you add to Hop-tunes becomes part of it and is
under the same licence (keep the SPDX header in every new file).
