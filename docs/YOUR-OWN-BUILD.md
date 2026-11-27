# Your app lives in your own repositories and your own build

An app you make **is never added to the official Hop-tunes**. It is not a contribution, it is not an update to the official repository, and it
will not appear in anyone else's Hop-tunes. It lives in **your own repositories and your own build**, and you are the one person who has it. That is
the whole idea: you do not have to wait for anyone, and nobody has to approve anything.

## What to do

1. **Fork Hop-tunes** on GitHub (the Fork button on `theStyleWithin/Hop-tunes`) and clone *your fork*, not the official repository.
2. **Fork this toolkit too.** **You never change your fork of the toolkit**, and your agent only reads it: keep it handy, and forward it (or its link) to your
   agent any time you want an app made or changed. The toolkit is essentially complete and set in stone (how apps are set up in Hop-tunes is settled).
3. Give your agent your toolkit fork and your Hop-tunes fork and say what app you want (`PROMPTS.md`). It builds the app in **your** repositories, one of two ways:
   * **A new repository of your own, just for the app** (recommended), then `scripts/inject_app.py` puts it into your fork: `docs/APP-REPOSITORY.md`. Make that
     repository on your own GitHub; it is easy to share and stays focused on the one app.
   * **Directly on a branch of your fork**: `docs/ADD-AN-APP.md`.
4. **Build your own version**, which is how the app reaches you:
   * **From source** on your computer: `docs/TESTING.md` has the commands; then run `./build/hop-tunes`.
   * **As an AppImage (Linux) or a Windows installer / portable exe**: these are built by the GitHub Actions workflows that are already in
     the repository (`.github/workflows/appimage.yml`, `windows.yml`). In *your fork*, turn Actions on, push your branch (pull requests inside
     your fork produce test builds) or push a version tag. A tag must match the version in `CMakeLists.txt`; read `docs/RELEASING.md` in the
     Hop-tunes repository, set your own version number (for example 1.15.0 plus a letter or an extra digit in your fork) and tag that. The
     built files appear on *your fork's* releases page. The official AppImage and Windows downloads cannot be changed: you run your own.
5. **Staying up to date** with official Hop-tunes is optional: update your fork (GitHub's "Sync fork" button, or have your agent merge the official repository's
   `main` into it with `git remote add upstream https://github.com/theStyleWithin/Hop-tunes`). An app kept in its own repository is then put back with
   `inject_app.py` (run it again); an app made directly in the fork is merged, and the files every app touches (`AppsView.qml`, `AppHost.qml`, `qml.qrc`,
   `tests/test_ui.cpp`, and for a networked app also `AppNet.cpp`, `App.cpp`, `SettingsView.qml`) can conflict: the agent resolves them and re-runs the whole
   test suite.

## On an Android phone

The Android app is built from the same source (`docs/android.md` in the Hop-tunes repository: Android SDK, NDK, Qt for Android, and TagLib and
SQLite built for Android). An Android build needs a signing key: sign your own build with your own key (an APK signed with a different key than
the one already installed cannot be installed over it, so uninstall the old one first, which also removes its data). Your fork's Actions do not
build Android, so this is a local job. Your app appears in the phone's apps grid like any other.

## What an agent must not do

* **Never write code anywhere but the person's own repositories** (their new app repository and their fork of Hop-tunes). In particular never in the official
  `theStyleWithin/Hop-tunes` source (you very likely have no access to it anyway: do not ask for any) and never in this toolkit or the person's fork of it.
* **Do not push to, open a pull request against, open an issue on, tag, release from, or message the official `theStyleWithin/Hop-tunes`
  repository about the app.** Not even to "offer" it, unless the person explicitly asks you to. The author alone decides what goes into
  official Hop-tunes, and the default is that your app stays yours. Sharing the app (for example a link in a discussion) is the person's own choice and post.
* If the clone you are working in has the official repository as `origin` (so a push would go there), **stop and ask the person to fork it
  first.** `scripts/inject_app.py` refuses such a clone and `scripts/check_app.py` warns about it. Read and build Hop-tunes from the person's fork.
* Do not change the official repository's version, changelog, release notes, store listings or website to mention the app.
* Do not credit the author with your work and do not call your build official (`PERMISSION-AND-CREDIT.md`).

## If you share your build

You may give your build to friends or publish it from your fork. Then: your fork must stay GPL-3.0-or-later with its source available, you
name it as your own (not "official Hop-tunes"), and the app's own files carry your name, not the author's (`PERMISSION-AND-CREDIT.md`).
Hop-tunes' author does not support builds made this way: your agent and you are the support.
