# Onboarding Health Service

This intentionally small Python fixture supports the AI SDLC Harness first
feature tutorial. It exposes `/version` and a fallback response. The tutorial
asks the learner to add a read-only `/health` route through an evidence-backed
workflow.

Run the starting tests with `python3 -m unittest -v`. The `.disabled` file is
an intentionally wrong test used only by the recovery drill; normal unittest
discovery does not execute it.
