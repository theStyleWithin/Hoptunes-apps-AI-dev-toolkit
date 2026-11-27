# Hoptunes-apps-AI-dev-toolkit

A hand-off package for making your own **Hop-tunes** apps. Take this toolkit to Claude or whatever coding agent you use and say: *"I love
using Hop-tunes, but I wish it had an app that does X."* The agent reads the brief and the manual here, which explain how apps work in
Hop-tunes and what rules they follow, and builds it with you. If you are not satisfied with the current line-up (today: **Kick**, the **Internet Archive**, **DeviantArt** and a little game, **neko cafe**) you do
not have to wait for anyone: make it yourself.

> [!IMPORTANT]
> **If you are a coding agent and a person just handed you this link, start here.**
>
> 1. **Where you may write code (read this first).** Only in the **person's own repositories**: a **new repository of their own for the app**, and/or **their own
>    fork of Hop-tunes**. **Never in the official Hop-tunes repository** (`theStyleWithin/Hop-tunes`; you very likely cannot even reach it, so do not ask for
>    access, tokens or a way around that), and **never in this toolkit or the person's fork of it** (they only keep it handy to forward to you; it needs no changes).
>    Never push to, open pull requests or issues on, or tag in the official repository.
> 2. **Get the Hop-tunes source from the person's fork** (ask them for its link if you only have the toolkit: they should fork **both** Hop-tunes and this toolkit on
>    GitHub). It is the same code as the official one, and it is the copy you read, build and test with.
> 3. Read [`AGENT-BRIEF.md`](AGENT-BRIEF.md) (the rules and how to work), then the files it points to.
> 4. **Then talk to the person.** They gave you only a link, so do not wait to be told and do not start building. Say, warmly and in a few plain
>    sentences, what this is (a hand-off package that lets anyone make their own apps for Hop-tunes, a local-first music player; no permission
>    needed from anyone, the app stays in their own repositories and build) and ask something like: ***"Oh, this is interesting! Do you want to make an app
>    for Hop-tunes? What would you like it to do?"*** Then follow `AGENT-BRIEF.md`.

**You do not need the author's permission, and your agent should not ask for it.** The only condition is that you do not credit the author
with your work: read [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md) (it also says what the GPL licence requires).

This repository is only the hand-off package. The player itself lives in the [Hop-tunes](https://github.com/theStyleWithin/Hop-tunes)
repository, of which you use **your own fork** (an app is added to its source).

## How to use it

1. **Fork both repositories** on GitHub: **Hop-tunes** and **this toolkit**. **You never change your fork of the toolkit**: keep it handy, and forward it (or its
   link) to your coding agent whenever you want an app made or changed. The agent only reads it. Your agent also needs your fork of Hop-tunes (clone **your fork**:
   `git clone https://github.com/<you>/Hop-tunes`).
2. Tell your agent what you want, for example:
   *"Read AGENT-BRIEF.md in the toolkit, then help me make an app for Hop-tunes: a sleep timer that pauses the music. Show me a screenshot and run the tests."*
   More wording ideas are in [`docs/PROMPTS.md`](docs/PROMPTS.md).
3. **The agent builds the app, in one of two ways** (it asks you which, and recommends the first):
   * **In a new repository of your own, just for that app** (recommended): focused on the one app, easy to share, and then put into your fork of Hop-tunes with a
     script. [`docs/APP-REPOSITORY.md`](docs/APP-REPOSITORY.md).
   * **Directly on a branch of your fork of Hop-tunes**: [`docs/ADD-AN-APP.md`](docs/ADD-AN-APP.md).
4. Build your own Hop-tunes from your fork (from source, as an AppImage or a Windows exe built by your fork's Actions):
   [`docs/YOUR-OWN-BUILD.md`](docs/YOUR-OWN-BUILD.md). The app is never added to the official repository.

## What is inside

| File | What it is |
|---|---|
| [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md) | **no permission needed; do not credit the author;** what the GPL licence still requires |
| [`AGENT-BRIEF.md`](AGENT-BRIEF.md) | **start here.** What an app is, the rules (offline first, no telemetry, tests), how the agent should work with you. `AGENTS.md` and `CLAUDE.md` point to it. |
| [`docs/HOW-APPS-WORK.md`](docs/HOW-APPS-WORK.md) | the apps tab (a grid of glass tiles the person arranges and files in folders), the registry, the host, phones, what an app's QML may use |
| [`docs/YOUR-OWN-BUILD.md`](docs/YOUR-OWN-BUILD.md) | **the code is only ever written in your own repositories**; how to build your Hop-tunes (source, AppImage, Windows, Android) and stay up to date |
| [`docs/APP-REPOSITORY.md`](docs/APP-REPOSITORY.md) | **the recommended way:** an app in its own repository, put into your fork with `scripts/inject_app.py` |
| [`docs/ADD-AN-APP.md`](docs/ADD-AN-APP.md) | adding an app directly to your fork, step by step (the manual way) |
| [`docs/NETWORK-AND-PRIVACY.md`](docs/NETWORK-AND-PRIVACY.md) | the privacy promises, the gateway every online app must use, and the places to wire a new online app (read before any app that needs the internet) |
| [`docs/TESTING.md`](docs/TESTING.md) | building, running the tests, taking screenshots |
| [`docs/LESSONS.md`](docs/LESSONS.md) | mistakes that were already made once, so they are not made again |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | what to say to your agent |
| [`docs/DROP-IN-APPS-PLAN.md`](docs/DROP-IN-APPS-PLAN.md) | the planned way to add apps without rebuilding Hop-tunes (not built yet) |
| [`examples/sleep-timer/`](examples/sleep-timer/) | a complete, tested example app, as an app repository (and as a patch for the direct way) |
| [`scripts/new_app_repo.py`](scripts/new_app_repo.py) | makes a new app repository with a working hello-world app in it |
| [`scripts/inject_app.py`](scripts/inject_app.py) | puts an app repository into your fork of Hop-tunes (refuses the official repository) |
| [`scripts/check_app.py`](scripts/check_app.py) | checks an app was added correctly: `python3 scripts/check_app.py <app-id> --repo <your fork of Hop-tunes>` |

## Honest status

* **Apps are built into Hop-tunes today.** Adding one means adding a QML file and a few lines to the Hop-tunes source, then building Hop-tunes
  (instructions inside; your agent can do it). **Drop-in apps that need no rebuild are planned, not built**, because an app someone else wrote
  must be sandboxed properly first: see [`docs/DROP-IN-APPS-PLAN.md`](docs/DROP-IN-APPS-PLAN.md).
* The rules matter more than the code: Hop-tunes promises no required accounts, no telemetry and nothing phoned home. Apps that use the internet
  must ask first, name the sites they contact, and go through one gateway that can only ask for pages (GET). There is no sign-in in any app. The
  one narrow exception is a key the person typed in themselves, sent to one host (the game shelf's optional SteamGridDB cover picker); see
  [`docs/NETWORK-AND-PRIVACY.md`](docs/NETWORK-AND-PRIVACY.md).
* **This toolkit is essentially complete and set in stone.** The way apps are set up in Hop-tunes (the apps grid, the registry, the host, the gateway) is
  settled with the polished interface of Hop-tunes 1.15.0, so apps should be built for people's own forks of Hop-tunes on those recent changes. The
  toolkit is only updated if something **major** changes about how apps work in Hop-tunes; small changes to Hop-tunes do not need a new toolkit.
* Written against Hop-tunes 1.15.0 (the apps tab became a grid of glass tiles in 1.13.0, and the person can drag the tiles and file them in folders since 1.14.0). If a file path in these docs does not exist in the Hop-tunes you have, the docs are older than your Hop-tunes:
  tell your agent to read the Hop-tunes source and trust that over these docs.

## Licence

This toolkit's text and scripts are MIT (see `LICENSE`). Hop-tunes is GPL-3.0-or-later: an app you add to Hop-tunes becomes part of it and is
under the same licence (keep the SPDX header in every new file). Details in [`PERMISSION-AND-CREDIT.md`](PERMISSION-AND-CREDIT.md).
