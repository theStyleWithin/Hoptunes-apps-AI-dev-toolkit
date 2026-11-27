# Hop-tunes apps: brief for a coding agent

You are helping a person add an **app** to Hop-tunes. Read this whole file first, then the files it points to. Do not start coding
before you have read "The rules" and "How to work".

## If the person gave you only a link and no request

Read this brief; then **speak first**: say in a few plain sentences what the toolkit is (a hand-off package for making your own Hop-tunes apps; no permission
needed; the app stays in their own repositories and build) and ask, for example, *"Oh, this is interesting! Do you want to make an app for Hop-tunes? What would
you like it to do?"* Do not offer a menu of things to do with the toolkit's documents and do not start building. If they say yes, make sure they have forked
**both** Hop-tunes and this toolkit on GitHub (they keep their toolkit fork handy and never change it) and give you the link to **their fork of Hop-tunes**; then
follow "How to work" below.

## Where you may write code (the hard rule)

**You may write code only in the person's own repositories:**

1. **a new repository of their own, just for this app** (the recommended way: `docs/APP-REPOSITORY.md`), and/or
2. **their own fork of Hop-tunes** (to put the app in and to build and test it there).

**You must never write to, push to, open a pull request or an issue on, tag, or release from the official Hop-tunes repository (`theStyleWithin/Hop-tunes`).**
You very likely cannot even reach it with the access you were given: that is expected. Do not ask for access to it, do not ask for a token, do not look for a way
around it, and do not clone it to work in. Read and build Hop-tunes from **the person's fork**: it is the same code. (If you can read the official repository
without any special access, that is fine for reading only.) **Never change this toolkit, or the person's fork of it**: they only keep it handy to forward to you,
it needs no changes, and your work does not go there. If the `origin` of a clone you are about to commit in is the official `theStyleWithin/Hop-tunes`, **stop and
ask the person to fork first**.

## Permission and credit (read this first)

**The person does not need the author's permission, and neither do you: do not ask for it, just build the app.** The one condition is that
you **never credit the author of Hop-tunes with the work** (no name, no "official", no endorsement; see `PERMISSION-AND-CREDIT.md`, which also
says what the GPL licence requires). You still ask the *person* what they want; you never ask or wait for the author.

How the person gets a runnable build (from source, an AppImage, a Windows exe built by their fork's Actions, or an Android APK) is in `docs/YOUR-OWN-BUILD.md`.

## How settled this is

The way apps are set up in Hop-tunes (the apps grid, the registry, the host, the gateway) is settled, and this toolkit is essentially complete and
set in stone: build apps for the person's own fork of Hop-tunes (via their own app repository, or directly in the fork) on the code as it is, following these documents. The toolkit changes only if something
major changes about how apps work in Hop-tunes. If a path or detail here does not match the Hop-tunes you have, the Hop-tunes source wins: tell the
person, and do not edit the toolkit.

## What Hop-tunes is

Hop-tunes is a local-first music player for Linux and Windows (and an Android app) inspired by the Zune software: C++20, Qt 6 (QML), CMake +
Ninja, GStreamer/libmpv, TagLib, SQLite. Licence: GPL-3.0-or-later. Its promises, which you must never break:
**no accounts required, no telemetry, nothing phoned home, works fully offline.** Source: https://github.com/theStyleWithin/Hop-tunes

## What an "app" is (today)

An app is a small screen that is part of Hop-tunes and opens inside its window from the **apps** tab (a tab that is off until the person
switches it on in settings). The apps tab is a **grid of glass tiles** (five across on a computer, three on a phone) that the person can drag
anywhere, file in folders they name and colour, and that Hop-tunes remembers; **a new app takes the first free spot by itself**, so you never
touch the grid code. **Today apps are built into Hop-tunes**: adding one means adding a QML file plus a few lines to the Hop-tunes source and
building Hop-tunes. Drop-in apps that need no rebuild are *planned, not built*: see `docs/DROP-IN-APPS-PLAN.md`. Never tell the person an app can be
installed without rebuilding; it cannot yet.

Four real apps live in Hop-tunes today: **Kick** (a networked app: browse and watch live streams, download and record them, playlists, a pretend
chat), the **Internet Archive** (find and play music, films and books), **DeviantArt** (browse artwork from public feeds) and **neko cafe** (an
offline game). In this toolkit, `examples/sleep-timer/` is a tiny app with no network, verified to build and pass the tests against Hop-tunes 1.15.0.
Apps can be much more than these: timers, lyrics and stats screens, visualizers, radio or podcast helpers, small games, anything that fits a
screen inside a local-first player. Apps that use the internet must follow `docs/NETWORK-AND-PRIVACY.md`. (The game shelf in the collection,
with its optional SteamGridDB cover picker, is a collection tab, not an app; it is a good second example of an opt-in networked feature.)

## The rules

1. **Offline is the default.** An app that does not need the internet must not use it. Only code under `src/net/` and `src/apps/` may touch
   the network, and only through the gateway `AppNet`. A test (`onlyTheGatewayTouchesTheNetwork` in `tests/test_net.cpp`) fails if any other
   source uses QtNetwork, sockets, `XMLHttpRequest` or `WebSocket`. QML must never load `https://` pictures or data by itself.
2. **A networked app asks first.** It needs a permission card that lists the exact sites it contacts and what is sent, an entry in
   settings > apps settings to take the permission back, its sites declared in `AppNet::hostsFor`, and it connects only while it is open.
   Read `docs/NETWORK-AND-PRIVACY.md` before writing any networked app.
3. **No telemetry, no tracking, no accounts.** Apps do not sign in to anything outside (there is no sign-in support in the gateway, on purpose).
   Anything the person keeps (a list, a setting) lives in their local profile and is never uploaded. Guests keep nothing. The only secret an
   app may ever send is a key the person typed in themselves, to one named host (`docs/NETWORK-AND-PRIVACY.md`, rule 9).
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
   answers. Check that they have forked Hop-tunes (and the toolkit), and ask which way they prefer to build: **a new repository for the app, then put into their
   fork** (recommend this), or **directly on a branch of their fork**.
2. Read `docs/HOW-APPS-WORK.md`, then `docs/APP-REPOSITORY.md` (or `docs/ADD-AN-APP.md` for the direct way), then look at `examples/sleep-timer/` (the smallest
   complete app) and, if the app is like one of them, at the real app it resembles (the table in `HOW-APPS-WORK.md`).
3. **New repository way:** `python3 <toolkit>/scripts/new_app_repo.py ...` makes the app repository with a working hello-world app; build the real app in it.
   Then `python3 <toolkit>/scripts/inject_app.py <app repository> --fork <the person's fork of Hop-tunes>` puts it into the fork (it refuses the official
   repository). **Direct way:** make a branch in the person's fork and add the app following `docs/ADD-AN-APP.md`.
4. Build and test in the fork (`docs/TESTING.md`). Run `python3 <toolkit>/scripts/check_app.py <app-id> --repo <the person's fork of Hop-tunes>` and fix every FAIL. It
   is a help, not a judge: it checks that the app is registered and has a test, nothing more, so a clean result does not mean the app works. The whole `ctest`
   run is the proof.
5. Take a screenshot with the test harness (`HOPTUNES_UI_SHOTS`, see `docs/TESTING.md`) and show the person what it looks like, on a computer
   and, for an app with its own screen, at phone size (`docs/TESTING.md`, "Checking an app on a phone-sized window").
6. Read `docs/LESSONS.md` if anything behaves strangely: it lists mistakes that were already made once.
7. Show the person how to get their own runnable build (`docs/YOUR-OWN-BUILD.md`), and tell them plainly what works and what you could not test. If they want to
   share the app, the app repository is what they share (`docs/APP-REPOSITORY.md`): you never post it anywhere yourself.

## Definition of done

The app opens from its tile (which sits in the grid and can be dragged and filed like every other), closes with Esc and the back button, fits a
phone-sized window, does nothing on the network unless it declared and was allowed to, has a UI test that passes, passes `scripts/check_app.py`, and
the whole `ctest` suite is green (the one known-red CI check named `floor` is not yours, and a rare hang in a music test is not yours either:
`docs/TESTING.md`). If you changed shared C++, compile the Android build too, with and without the networked apps.
