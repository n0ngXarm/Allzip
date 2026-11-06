---
name: allzip-maintenance
description: Maintain, test and package Allzip; use for this repository's runtime, installer and release changes.
---

# Allzip

Read root AGENTS.md and PROJECT_PROGRESS.md first. This skill applies only to this repository.

Read allzip/core.py and zip_folder.py; Windows UI lives in allzip/windows_gui.py. Preserve Linux CLI/Nautilus behavior. Stage archives beside the input and publish only after verification; failures must preserve existing output. Do not report success after silently skipping unreadable inputs. Keep ZIP64, Unicode paths, empty folders and duplicate-name safeguards.

Run `python -m unittest discover -s tests -v`. For installer changes, run the Windows installer workflow and inspect `scripts/verify_windows_install.py` results against the exact commit. Native setup should remain per-user and require no Python on the target machine. Preserve application licenses and corresponding source. Do not install dependencies, publish a release or change scope without authorization in the current task.

Record changed behavior, actual checks and remaining limitations in PROJECT_PROGRESS.md. Do not substitute Linux/source tests for installed Windows runtime acceptance.
