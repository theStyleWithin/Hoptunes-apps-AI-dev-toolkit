# What to say to your coding agent

First fork Hop-tunes on GitHub and give the agent this toolkit (the folder, or the link to this repository) and **your fork** of the Hop-tunes
source. The app stays in your fork and your own build: `docs/YOUR-OWN-BUILD.md`. Then say something like:

> Read AGENT-BRIEF.md in the toolkit, then help me add an app to Hop-tunes. I want an app that <what it does>. It <does / does not> need
> the internet. Show me what it will look like before you finish, and run the tests.

Or, in your own words:

> I love using Hop-tunes, but it only has one app and I want <something else>. Use the toolkit. I do not need anyone's permission to make an
> app, so do not ask for it, and do not credit the Hop-tunes author with my work.

Good things to tell it:

* **What the screen shows and what each button does**, in plain words ("a big countdown, four buttons for 15, 30, 60 and 90 minutes").
* **Whether it needs the internet**, and if so which website. If you do not know, ask the agent to find out and tell you before it builds.
* **What it should remember** (nothing, or a list kept on your computer).
* **That it must follow the rules in the brief**: offline first, nothing sent anywhere, a permission card for anything online.

Things to ask for at the end:

* "Show me a screenshot." (the brief tells it how)
* "Run the whole test suite and tell me anything that failed."
* "Explain in plain words what this app contacts on the internet, if anything."

If the agent says it can make an app that works without rebuilding Hop-tunes: that is **planned, not built** (`docs/DROP-IN-APPS-PLAN.md`).
