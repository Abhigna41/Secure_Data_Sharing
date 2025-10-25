# Commit Grouping Guide for Secure Data Sharing System

This document summarizes the canonical commit groupings you can use when updating the project. Each section lists the primary directories that roll up into a single commit so you avoid one-commit-per-file noise.

## Template & UI Updates
- Affects: `templates/`, CSS/JS tweaks embedded in HTML, minor icon/spacing changes.
- Use message type: `refactor` or `feat` (when adding new views).
- Example summary: `refactor: modernize dashboard and template styling`.

## Core Application Logic
- Affects: `app_simple.py`, `abe_crypto.py`, supporting helpers in root module.
- Use message type: `feat` for new features, `fix` for bug patches.
- Example summary: `feat: add policy checker route to simple app`.

## Documentation & Admin Notes
- Affects: `Readme.md`, `PROJECT_DOCUMENTATION.md`, and files under `docs/`.
- Use message type: `docs`.
- Example summary: `docs: describe deployment workflow`.

## Test & Tooling
- Affects: `test_*.py`, `startup_test.py`, scripts that validate routes, and batch helpers.
- Use message type: `test` or `chore`.
- Example summary: `test: extend Flask flow coverage for admin pages`.

## Secrets & Configuration Hygiene
- Affects: `.gitignore`, removal of sensitive artifacts, environment placeholders.
- Use message type: `chore`.
- Example summary: `chore: drop tracked firebase credentials`.

When preparing a commit, review the touched paths and pick the single grouping that best represents the change. This keeps the history concise while still informative.
