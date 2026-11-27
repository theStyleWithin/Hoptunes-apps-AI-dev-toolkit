# Making your app in its own repository, then putting it into your fork

There are two ways to build an app. **This is the recommended one**; the other (working directly on a branch of your fork of Hop-tunes) is in
`ADD-AN-APP.md`.

| | **A. Its own repository** (recommended) | **B. Directly in your fork of Hop-tunes** |
|---|---|---|
| where the app's code lives | a **new repository of your own**, just for this app | a branch of your fork of Hop-tunes |
| how it reaches Hop-tunes | `scripts/inject_app.py` copies it into your fork and registers it | you edit the fork's files by hand |
| easy to share | yes: one small, focused repository you can show to anyone (for example in a discussion on Hop-tunes' GitHub, if *you* choose to; an agent never posts there) | harder: the app is mixed into a copy of the whole player |
| when Hop-tunes updates | update your fork, run the injector again | merge the official `main` into the fork and fix conflicts |
| good for | almost every app | an app that needs deep changes all over Hop-tunes |

Either way, the **code is only ever written in your own repositories** (the new app repository and/or your fork of Hop-tunes). Never in the official Hop-tunes
repository, never in the toolkit (`YOUR-OWN-BUILD.md`).

## Why the person forks the toolkit and Hop-tunes

* **Fork Hop-tunes** on GitHub: your fork is where your build of Hop-tunes (with your apps in it) lives, and it is the copy of the player your agent reads,
  builds and tests with. An agent usually cannot reach, and must never write to, the official repository.
* **Fork this toolkit**: you keep your fork handy and forward it to your agent whenever you want it to make or change an app. **You never change your fork of the
  toolkit** and neither does the agent: it is the instructions, not a workspace.
* **Make a new repository for each app** (workflow A): the agent builds the app there.

## The layout of an app repository

```
my-app/
  app.json                 the manifest (below)
  qml/MyApp.qml            the screen (any QML Item; its file name ends in App.qml)
  images/app-myapp.png     optional icon: a square PNG, transparent background, 128 to 256 px
  tests/ui_test.inc        the UI test: the C++ source of one or more test functions (see below)
  files/...                optional: new files for a networked app, copied into the fork at the same path (src/apps/MyClient.cpp, ...)
  patches/01-*.patch       optional: edits to existing files (a networked app: CMakeLists.txt, AppNet.cpp, App.cpp, SettingsView.qml), made with `git diff`
  README.md                what it is and how to put it into a fork (the scaffold writes this)
```

`app.json`:

```json
{ "id": "myapp", "name": "my app", "blurb": "one plain sentence about what it does", "net": false,
  "qml": "MyApp.qml", "icon": "", "leaves": false }
```

* `id`: lower-case letters and digits, starting with a letter. `name`: the lower-case tile name. `blurb`: the line that pops up over the tile (no double
  quotes or backslashes); for a networked app say that it uses the internet.
* `net`: `true` if the app uses the internet. A networked app also needs the gateway, `App.cpp` and settings wiring (`NETWORK-AND-PRIVACY.md`, "The places to
  touch for a new networked app"): new C++ files go in `files/`, the edits to existing files in `patches/` (regenerate them whenever Hop-tunes changes).
* `qml`: the file in `qml/` (the QML type is the file name without `.qml`). `icon`: a file in `images/`, or `""` for the plain glass tile.
* `leaves`: `true` only if the app emits its own `leave()` signal and should be wired like Kick (rare).

`tests/ui_test.inc` is plain C++: the text of the test function(s) as they would sit inside `TestUi`'s `private slots:` section (see `examples/sleep-timer/`).
The injector puts it **immediately before** `appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow` between `// BEGIN hoptunes-app:<id>` and `// END hoptunes-app:<id>`
marker lines (so running it again replaces it in place). Tests open the tile with `click("appTile_<id>")`, wait with `QTRY_VERIFY`, close with Esc, and call
`shot("...")` (`TESTING.md`).

## The two scripts

```sh
# 1. make the repository (once)
python3 scripts/new_app_repo.py myapp --name "my app" --type MyApp --blurb "what it does" --dir ~/code/hoptunes-my-app
cd ~/code/hoptunes-my-app && git init     # the person publishes it to their own GitHub if they like

# 2. build the real app in it (qml/, images/, tests/ui_test.inc ...), then put it into the person's FORK of Hop-tunes
python3 scripts/inject_app.py ~/code/hoptunes-my-app --fork ~/code/Hop-tunes --dry-run     # shows what it would change
python3 scripts/inject_app.py ~/code/hoptunes-my-app --fork ~/code/Hop-tunes

# 3. in the fork: build and run the WHOLE test suite (TESTING.md), look at the screenshot, try it
```

`new_app_repo.py` writes a working hello-world app (it builds and its test passes as it is), so an agent starts from something that works.

`inject_app.py`:

* **refuses to run in a clone whose origin is the official `theStyleWithin/Hop-tunes`**: apps only ever go into the person's own fork;
* copies the QML, the icon and `files/`; registers the app in `src/ui/qml.qrc`, in `allApps` in `AppsView.qml` (appended at the **end**), and in `AppHost.qml`
  (the `names` map, the `sourceComponent` chain and a `Component`); inserts the test; applies `patches/*.patch` in order;
* **can be run again** after you change the app: files are overwritten, the registry entry and the test are replaced in place, a patch that is already applied
  is skipped, and a patch that no longer applies stops with a clear message (regenerate it against the fork's Hop-tunes);
* never touches git history and never pushes; it ends by running `check_app.py` on the fork. To undo an injection, work on a branch in the fork and delete it.

If a registration anchor is not found (a future Hop-tunes that changed `AppsView.qml` or `AppHost.qml`), it stops and says which file and step to do by hand
(`ADD-AN-APP.md`); trust the Hop-tunes source over these documents.

## Sharing an app

An app repository is small and self-contained, so it is easy to show to other people: the README says how to put it into a fork. Posting it (for example a
link in a GitHub discussion on Hop-tunes) is the **person's** choice and the person's own post; an agent never posts, opens issues or pull requests on the
official repository (`YOUR-OWN-BUILD.md`). Others can then inject it into their own fork with this toolkit.

## Licence and credit

An app that is put into Hop-tunes becomes part of it and is under **GPL-3.0-or-later**, so an app repository is GPL-3.0-or-later too: keep the SPDX line in every
file, add the licence text as `LICENSE` (copy it from the Hop-tunes repository) before publishing, and put the person's own name on their work. Never credit the
author of Hop-tunes with the app (`PERMISSION-AND-CREDIT.md`).
