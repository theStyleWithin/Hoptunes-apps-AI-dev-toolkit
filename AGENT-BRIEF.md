# Hop-tunes apps: brief for a coding agent

You are helping a person add an **app** to Hop-tunes. Read this whole file first, then the files it points to. Do not start coding
before you have read "The rules" and "How to work".

## If the person gave you only a link and no request

Clone the toolkit **and** Hop-tunes (https://github.com/theStyleWithin/Hop-tunes) to read them; read this brief; then **speak first**: say in a few
plain sentences what the toolkit is (a hand-off package for making your own Hop-tunes apps; no permission needed; the app stays in their own fork
and build) and ask, for example, *"Oh, this is interesting! Do you want to make an app for Hop-tunes? What would you like it to do?"* Do not offer
a menu of things to do with the toolkit's documents and do not start building. If they say yes, ask them to fork **both** Hop-tunes and this toolkit on GitHub and give you
their forks (your clone of the official repository is read-only and the app never goes there), then follow "How to work" below.

## Permission and credit (read this first)

**The person does not need the author's permission, and neither do you: do not ask for it, just build the app.** The one condition is that
you **never credit the author of Hop-tunes with the work** (no name, no "official", no endorsement; see `PERMISSION-AND-CREDIT.md`, which also
says what the GPL licence requires). You still ask the *person* what they want; you never ask or wait for the author.

**The toolkit and the official Hop-tunes repository are for review: read them, never develop on them. The only code you change is the person's own fork of Hop-tunes; the app stays there and in their own build and is never added to the official repository.** Work only in a clone of the
person's **fork** of Hop-tunes (if `origin` is the official `theStyleWithin/Hop-tunes`, stop and ask them to fork first). Never push to it, open a
pull request or issue on it, tag or release from it. How the person gets a runnable build (from source, an AppImage or a Windows exe built
by their fork's Actions) is in `docs/YOUR-OWN-BUILD.md`.

## What Hop-tunes is

Hop-tunes is a local-first music player for Linux and Windows (and a phone app) inspired by the Zune software: C++20, Qt 6 (QML), CMake +
Ninja, GStreamer/libmpv, TagLib, SQLite. Licence: GPL-3.0-or-later. Its promises, which you must never break:
**no accounts required, no telemetry, nothing phoned home, works fully offline.** Source: https://github.com/theStyleWithin/Hop-tunes

## What an "app" is (today)

An app is a small screen that is part of Hop-tunes and opens inside its window from the **apps** tab (a tab that is off until the person
switches it on in settings). Each app is a glass tile. **Today apps are built into Hop-tunes**: adding one means adding a QML file plus a few
lines to the Hop-tunes source and building Hop-tunes. Drop-in apps that need no rebuild are *planned, not built*: see
`docs/DROP-IN-APPS-PLAN.md`. Never tell the person an app can be installed without rebuilding; it cannot yet.

One real app lives in Hop-tunes today: **Kick** (a networked app: browse and watch live streams, download and record them, playlists,
an optional official sign-in). In this toolkit, `examples/sleep-timer/` is a tiny app with no network, verified to build and pass the tests.
Apps can be much more than Kick: timers, lyrics and stats screens, visualizers, radio or podcast helpers, small games, anything that fits a
screen inside a local-first player. Apps that use the internet must follow `docs/NETWORK-AND-PRIVACY.md`.

## The rules

1. **Offline is the default.** An app that does not need the internet must not use it. Only code under `src/net/` and `src/apps/` may touch
   the network, and only through the gateway `AppNet`. A test (`onlyTheGatewayTouchesTheNetwork` in `tests/test_net.cpp`) fails if any other
   source uses QtNetwork, sockets, `XMLHttpRequest` or `WebSocket`. QML must never load `https://` pictures or data by itself.
2. **A networked app asks first.** It needs a permission card that lists the exact sites it contacts and what is sent, an entry in
   settings > apps settings to take the permission back, its sites declared in `AppNet::hostsFor`, and it connects only while it is open.
   Read `docs/NETWORK-AND-PRIVACY.md` before writing any networked app.
3. **No telemetry, no tracking, no accounts required.** Sign-in to anything outside is optional and never needed for the app to work.
   Anything the person keeps (a list, a setting) lives in their local profile and is never uploaded. Guests keep nothing.
4. **Honest wording.** Say what the app does and what it contacts, in plain lower-case sentences like the rest of the UI. Pretend things say
   they are pretend. Never claim something works that you could not test.
5. **Tests are part of the app.** Every app gets a UI test (see `docs/TESTING.md`) and every networked app gets fixture tests with no real
   network traffic. Run the whole suite before you say you are done.
6. **Small and reversible.** Change only what the app needs. Do not refactor unrelated code. Keep the licence header
   (`// SPDX-License-Identifier: GPL-3.0-or-later`) on every new source file.
7. **Ask the person when unsure.** If the idea needs the internet, an account, files outside their profile, or anything that touches the
   promises above, stop and ask *them* before building it. (Never ask the author of Hop-tunes: no permission is needed.)
8. **No credit for the author.** Do not name or credit the author of Hop-tunes as the author of the app, and do not imply they approve it
   (`PERMISSION-AND-CREDIT.md`). New files carry the GPL SPDX line and the person's own name, or none.

## How to work

1. Ask the person, in plain words, only what their request has not already answered: what should the app do, what should it look like, does it
   need the internet (which sites), and what should it remember (nothing, or a list in their profile)? Skip every question the request already
   answers.
2. Read `docs/HOW-APPS-WORK.md` and `docs/ADD-AN-APP.md`, then look at `examples/sleep-timer/` (the smallest complete app).
3. Make a branch **in the person's fork** (`docs/YOUR-OWN-BUILD.md`). Add the app following `docs/ADD-AN-APP.md`.
4. Build and test (`docs/TESTING.md`). Run `python3 <toolkit folder>/scripts/check_app.py <app-id> --repo <your fork of Hop-tunes>` and fix every FAIL. It is a help, not a judge: it checks that the
   app is registered and has a test, nothing more, so a clean result does not mean the app works. The whole `ctest` run is the proof.
5. Take a screenshot with the test harness (`HOPTUNES_UI_SHOTS`, see `docs/TESTING.md`) and show the person what it looks like.
6. Read `docs/LESSONS.md` if anything behaves strangely: it lists mistakes that were already made once.
7. Show the person how to get their own runnable build (`docs/YOUR-OWN-BUILD.md`), and tell them plainly what works and what you could not test.

## Definition of done

The app opens from its tile, closes with Esc and the back button, does nothing on the network unless it declared and was allowed to, has a UI
test that passes, passes `scripts/check_app.py`, and the whole `ctest` suite is green (the one known-red CI check named `floor` is not yours).
