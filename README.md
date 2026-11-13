# Hoptunes-apps-AI-dev-toolkit

A hand-off package for making your own **Hop-tunes** apps. Take this toolkit to Claude or whatever coding agent you use and say: *"I love
using Hop-tunes, but I wish it had an app that does X."* The agent reads the brief and the manual here, which explain how apps work in
Hop-tunes and what rules they follow, and builds it with you. If you are not satisfied with the current line-up (today that is **Kick**) you do
not have to wait for anyone: make it yourself.

> [!IMPORTANT]
> **If you are a coding agent and a person just handed you this link, start here.**
>
> 1. **Clone both repositories** so you can read them: this toolkit, and the player it is for,
>    [Hop-tunes](https://github.com/theStyleWithin/Hop-tunes) (`git clone https://github.com/theStyleWithin/Hop-tunes`). Reading the official Hop-tunes
>    clone is fine (this toolkit and the official Hop-tunes repository are **read-only reference**: you never change them); **changes are made only in the person's own fork** (ask them to fork Hop-tunes on GitHub and give you their fork). Never push to,
>    or open pull requests on, the official repository.
> 2. Read [`AGENT-BRIEF.md`](AGENT-BRIEF.md) (the rules and how to work), then the files it points to.
> 3. **Then talk to the person.** They gave you only a link, so do not wait to be told and do not start building. Say, warmly and in a few plain
>    sentences, what this is (a hand-off package that lets anyone make their own apps for Hop-tunes, a local-first music player; no permission
>    needed from anyone, the app stays in their own fork and build) and ask something like: ***"Oh, this is interesting! Do you want to make an app
>    for Hop-tunes? What would you like it to do?"*** Then follow `AGENT-BRIEF.md`.

**You do not need the author's permission, and your agent should not ask for it.** The only condition is that you do not credit the author
with your work: read [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md) (it also says what the GPL licence requires).

This repository is only the hand-off package. The player itself lives in the [Hop-tunes](https://github.com/theStyleWithin/Hop-tunes)
repository, which you also give to your agent (an app is added to its source).

## How to use it

1. **Fork** Hop-tunes on GitHub and clone **your fork** (`git clone https://github.com/<you>/Hop-tunes`). You do not fork this toolkit: it always
   stays untouched, and your agent only reads it. Your app lives in your own fork and your own build; it is never added to the official repository
   ([`docs/YOUR-OWN-BUILD.md`](docs/YOUR-OWN-BUILD.md): from source, as an AppImage or a Windows exe built by your fork's Actions).
2. Give your coding agent (Claude or any other) **the link to this toolkit** and your fork of the Hop-tunes source.
3. Tell it what you want, for example:
   *"Read AGENT-BRIEF.md in the toolkit, then help me add an app to Hop-tunes: a sleep timer that pauses the music. Show me a screenshot and run the tests."*
   More wording ideas are in [`docs/PROMPTS.md`](docs/PROMPTS.md).

## What is inside

| File | What it is |
|---|---|
| [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md) | **no permission needed; do not credit the author;** what the GPL licence still requires |
| [`AGENT-BRIEF.md`](AGENT-BRIEF.md) | **start here.** What an app is, the rules (offline first, no telemetry, tests), how the agent should work with you. `AGENTS.md` and `CLAUDE.md` point to it. |
| [`docs/HOW-APPS-WORK.md`](docs/HOW-APPS-WORK.md) | the apps tab, the registry, the host, what an app's QML may use |
| [`docs/YOUR-OWN-BUILD.md`](docs/YOUR-OWN-BUILD.md) | **your app stays in your own fork and build**; how to build it (source, AppImage, Windows) and stay up to date |
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
  must ask first, name the sites they contact, and go through one gateway that can only ask for pages (GET). The one exception is an app's
  *official* sign-in (OAuth), through three exact requests; see [`docs/NETWORK-AND-PRIVACY.md`](docs/NETWORK-AND-PRIVACY.md).
* Written against Hop-tunes 1.10.0. If a file path in these docs does not exist in the Hop-tunes you have, the docs are older than your Hop-tunes:
  tell your agent to read the Hop-tunes source and trust that over these docs.

## Licence

This toolkit's text and scripts are MIT (see `LICENSE`). Hop-tunes is GPL-3.0-or-later: an app you add to Hop-tunes becomes part of it and is
under the same licence (keep the SPDX header in every new file). Details in [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md).
