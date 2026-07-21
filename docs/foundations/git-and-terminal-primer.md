---
title: Git and terminal primer
description: Learn the minimum shell, Git, revision, and package-runner vocabulary needed to follow the harness tutorials safely.
---

# Git and terminal primer

This primer is for readers who have not used a command-line interface or Git
workflow before. It explains the minimum vocabulary used by the installation
and tutorials; it is not a complete Git course.

## Terminal and command vocabulary

A **command-line interface (CLI)** is a text interface for a program. A
**terminal** is the application window in which you run commands. A **shell**
interprets command text. The examples use **Portable Operating System
Interface (POSIX)-style** shell syntax, the
common command form on Linux and macOS and inside Windows Subsystem for Linux
(WSL) or Git Bash. Native PowerShell uses different variable and quoting
syntax, so use the explicitly labeled PowerShell block or WSL.

Run one command at a time, read its output, and stop on an unexpected non-zero
exit. A command can modify files or contact a network; a prompt sent to an AI
agent is different because the agent decides which tools to request. Neither
form is permission to ignore a human checkpoint.

`npx` is npm's package runner. In this repository it downloads and runs the
exactly named Skills CLI package version. It is third-party executable code,
not a built-in harness command, so the install guide pins its version and
discloses its telemetry boundary.

Installation examples also use these shell forms:

- `NAME=value` stores a shell variable; `"$NAME"` reads it while preserving
  spaces as one argument.
- `NAME=value command` sets an environment variable only for that command.
- `$(command)` substitutes printed output; inspect the inner command first.
- Quotes preserve one argument; a trailing `\` continues a displayed command.
- `< file` supplies reviewed input. `for ...; do ...; done` repeats a bounded
  block. `test` checks a condition and returns success or failure.
- `rm -rf` recursively deletes without a recovery prompt. Run it only for the
  exact disposable path created by the same procedure.

## Git vocabulary

| Term | Practical meaning |
| --- | --- |
| Repository | Project files plus Git history and configuration. |
| Working tree | Current files you can edit. |
| Diff | Line-by-line view of changes relative to recorded content. |
| Staging area | Exact set of changes selected for the next commit. |
| Commit | Immutable Git history record of a selected change and message. |
| Branch | Movable name for a line of commits; task work should not begin on the shared base branch. |
| Remote | Named external or local Git repository used to exchange commits. |
| Tag | Human-readable name pointing to a commit; it can be moved unless separately protected and verified. |
| SHA / commit hash | Content-derived identifier for one commit. This documentation uses a full commit hash as immutable source identity. |
| Clone | Local copy of a repository and its history. |
| Pull | Fetch remote changes and integrate them; `--ff-only` refuses an unexpected merge. |
| Push | Send local commits to a remote; it is an external write and needs authorization. |

## Safe inspection commands

Run these from a repository:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git diff --check
git diff
git diff --cached
```

Expected: the first command prints the repository root; the second prints the
current branch; status names changed/untracked files or prints nothing; diff
shows unstaged changes; cached diff shows only staged changes. `git diff
--check` exits non-zero for selected whitespace errors.

Staging with `git add` changes what a future commit will contain; committing
changes history; pushing changes an external remote. Review the staged diff
before a commit and do not push merely because an agent produced a commit.

## Recovery rules

If a command fails, preserve its exact output and inspect `git status --short`.
Do not run destructive reset, cleanup, or deletion commands copied from an
untrusted answer. Ask the repository owner before removing an unfamiliar file.
If you opened the wrong repository, stop and change directories; do not attempt
to adapt the command in place.

For a failed first install, do not improvise a generic remove command. If the
consumer repository was disposable, delete that entire verified fixture from
its parent. Otherwise use the ownership-safe [uninstall
procedure](../how-to/update.md#remove-and-verify-cleanup) and review every managed path first.

Continue with [Software delivery foundations](software-delivery.md) for the
lifecycle concepts or [Install the harness](../how-to/install.md) when this
vocabulary is clear. The official [Git documentation](https://git-scm.com/doc)
is the authority for command behavior.
