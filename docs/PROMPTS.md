# What to say to your coding agent

First fork **both** Hop-tunes and this toolkit on GitHub. Keep your toolkit fork handy (you never change it) and give your agent **your toolkit fork** and **your fork of
Hop-tunes**. The agent builds the app in your own repositories and never in the official source: `docs/YOUR-OWN-BUILD.md`. Then say something like:

> Read AGENT-BRIEF.md in the toolkit, then help me make an app for Hop-tunes. I want an app that <what it does>. It <does / does not> need
> the internet. Build it in a new repository of its own and put it into my fork of Hop-tunes with the toolkit's script. Show me what it will look like
> before you finish, and run the tests.

To work directly on your fork instead, say "add it on a branch of my fork". Or, in your own words:

> I love using Hop-tunes, but the apps it has are not what I need and I want <something else>. Use the toolkit. I do not need anyone's permission to make an
> app, so do not ask for it, and do not credit the Hop-tunes author with my work. Only write code in my own repositories.

To change an app you made earlier:

> Here is my toolkit fork, my Hop-tunes fork and my app's repository. Change the app so that <what>, put it into my fork again, and run the whole test suite.

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
