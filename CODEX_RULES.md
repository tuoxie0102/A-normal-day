# Project Maintenance Rules

## Workflow Before Changes

- Before each task, read `README.md`, `docs/archives/`, `docs/reports/`, and the files directly related to the current task.
- Before making any change, run `git status`.
- If a new file is needed, explain why before creating it.

## File Placement Rules

- Do not create new report-style Markdown files in the project root.
- Put temporary reports in `docs/reports/`.
- Move outdated documents into `docs/archives/`.
- Keep the root directory focused on core entry files and essential project files only.

## Change Safety Rules

- Do not delete source code, assets, dialogue text, or `README.md` without explicit confirmation.
- Do not rewrite core business logic unless explicitly requested.
- If Git appears abnormal, stop immediately and report it. Do not force-push on your own.

## Change Reporting Rules

- After each change, state which files were modified.
- After each independent task, create one commit.

## Commit Message Rules

- `feat:` new feature
- `fix:` bug fix
- `ui:` interface improvement
- `docs:` documentation update
- `chore:` project maintenance
- `release:` release version
