# Your app lives in your own copy of Hop-tunes

An app you make **is never added to the official Hop-tunes**. It is not a contribution, it is not an update to the official repository, and it
will not appear in anyone else's Hop-tunes. It lives in **your own fork and your own build**, and you are the one person who has it. That is
the whole idea: you do not have to wait for anyone, and nobody has to approve anything.

## What to do

1. **Fork Hop-tunes** on GitHub (the Fork button on `theStyleWithin/Hop-tunes`) and clone *your fork*, not the official repository.
2. Give your agent **the link to this toolkit**. You do not fork or edit the toolkit: it always stays untouched, and the agent only reads it.
3. Give your agent your fork and the toolkit and say what app you want (`PROMPTS.md`). It works on a branch in **your fork**.
4. **Build your own version**, which is how the app reaches you:
   * **From source** on your computer: `docs/TESTING.md` has the commands; then run `./build/hop-tunes`.
   * **As an AppImage (Linux) or a Windows installer / portable exe**: these are built by the GitHub Actions workflows that are already in
     the repository (`.github/workflows/appimage.yml`, `windows.yml`). In *your fork*, turn Actions on, push your branch (pull requests inside
     your fork produce test builds) or push a version tag. A tag must match the version in `CMakeLists.txt`; read `docs/RELEASING.md` in the
     Hop-tunes repository, set your own version number (for example 1.10.0 plus a letter or an extra digit in your fork) and tag that. The
     built files appear on *your fork's* releases page. The official AppImage and Windows downloads cannot be changed: you run your own.
5. **Staying up to date** with official Hop-tunes is optional: your agent can merge the official repository's `main` into your fork
   (`git remote add upstream https://github.com/theStyleWithin/Hop-tunes`). The files every app touches (`AppsView.qml`, `AppHost.qml`,
   `qml.qrc`, `tests/test_ui.cpp`) can then conflict; the agent resolves them and re-runs the whole test suite.

## What an agent must not do

* **Do not push to, open a pull request against, open an issue on, tag, release from, or message the official `theStyleWithin/Hop-tunes`
  repository about the app.** Not even to "offer" it, unless the person explicitly asks you to. The author alone decides what goes into
  official Hop-tunes, and the default is that your app stays yours.
* If the clone you are working in has the official repository as `origin` (so a push would go there), **stop and ask the person to fork it
  first.** `scripts/check_app.py` warns about this too. (A clone of the official repository just to read and learn from is fine, and it is
  how an agent starts; the app itself is only ever built in the person's fork.)
* Do not modify this toolkit or push to it either: it is read-only reference, and so is the official Hop-tunes repository. The only repository an agent
  changes is the person's own fork of Hop-tunes.
* Do not change the official repository's version, changelog, release notes, store listings or website to mention the app.
* Do not credit the author with your work and do not call your build official (`PERMISSION-AND-CREDIT.md`).

## If you share your build

You may give your build to friends or publish it from your fork. Then: your fork must stay GPL-3.0-or-later with its source available, you
name it as your own (not "official Hop-tunes"), and the app's own files carry your name, not the author's (`PERMISSION-AND-CREDIT.md`).
Hop-tunes' author does not support builds made this way: your agent and you are the support.
