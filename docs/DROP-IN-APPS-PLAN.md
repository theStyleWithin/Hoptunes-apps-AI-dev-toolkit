# Drop-in apps: planned, not built

> Note: even when drop-in apps exist, an app someone makes stays theirs: it is installed into their own copy of Hop-tunes, never into the official repository or other people's Hop-tunes (`YOUR-OWN-BUILD.md`).

**Status: not built. Do not tell anyone this works.** Today an app is added to the Hop-tunes source and Hop-tunes is rebuilt
(`ADD-AN-APP.md`). The idea below would let a person drop an app folder into their profile and have it appear as a tile with no rebuild, so that
people (and their coding agents) can make apps without compiling Hop-tunes. It is written down so that what gets built later matches what the
toolkit will promise.

## Why it is not simply "load any QML"

An app made by someone else is untrusted code. QML can do far more than draw: the Hop-tunes window shares one QML engine, and its `hop` object
(the player, the profile, the library, settings) and the shared `Theme` singleton are visible to anything loaded in that engine. A drop-in
app must not be able to read the person's library, files or profile, reach the network except through the gateway, or start programs.
A check that scans app source for forbidden words is **not** a security boundary (JavaScript can build names at run time).

## The shape of the plan

* **An app is a folder** in the profile (`apps/<id>/`): `manifest.json` (`id`, `name`, `version`, `description`, `icon`, `entry`, `hosts`, `api`),
  `icon.png`, `main.qml` and its own files. Dropping it in adds a glass tile.
* **A separate QML engine** with no `hop` object. The app gets only a small `app` API: its own data folder (size-capped), a way to ask the
  gateway for the sites declared in its manifest, and read-only "now playing" facts. The engine's import path and URL resolution are limited to
  the app's folder and an allow-list of Qt modules (QtQuick, Controls, Layouts), enforced with a URL interceptor; its network factory sends all
  requests through the gateway's host rules; no raw sockets, no process APIs, no file dialogs outside its data folder.
* **The same consent as Kick**: a first-open card that lists the manifest's sites and what the app can do, per profile, revocable in settings.
  A CPU watchdog and a stop switch. Closing the app destroys its engine.
* **Embedding**: the separate engine renders into an offscreen window shown inside the Hop-tunes window (Qt's `QQuickRenderControl`), with
  keyboard and mouse forwarded; this is the hardest engineering part.
* **Honest limits**, to be written into the user-facing docs: installing someone else's app is still a trust decision; there is no store and no
  review; the sandbox is enforced inside Hop-tunes' process, not by the operating system, and needs hard tests (escape attempts through file
  reads, undeclared hosts, off-list redirects, import tricks) before it is promised.

When this exists, this toolkit gains `docs/APP-FORMAT.md`, a manifest schema, an `app` API reference, drop-in examples and a validator, and the
agent brief changes to build drop-in apps by default. Until then the brief stays as it is.
