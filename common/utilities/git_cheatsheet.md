# Git / GitHub cheatsheet

The commands you'll actually use in this course, in the order you'll
typically use them.

## One-time setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Getting a repository

```bash
git clone <repo-url>          # copy an existing GitHub repo locally
cd <repo-name>
```

## Everyday workflow

```bash
git status                    # what changed?
git add <file>                # stage a specific file
git add .                     # stage everything changed
git commit -m "short, clear message"
git push                      # send your commits to GitHub
git pull                      # get the latest commits from GitHub
```

## Branches (use one per week/feature)

```bash
git checkout -b week1         # create and switch to a new branch
git push -u origin week1      # push it to GitHub the first time
git checkout main             # switch back to main
```

## Opening a Pull Request (PR)

1. Push your branch (see above).
2. On GitHub, open a Pull Request from your branch into `main`.
3. Describe what you changed and why.
4. Merge once it looks good (or after review, if working with others).

## Undoing things (safely)

```bash
git restore <file>            # discard uncommitted changes to a file
git log --oneline             # see recent commit history
git revert <commit-hash>      # undo a specific commit with a new commit
```

## Good habits for this course

- Commit after each meaningful step (e.g. "extract frames from video",
  not one giant commit at the end of the week).
- Write commit messages that describe *what changed*, not "update" or "fix".
- Never commit large generated files (extracted frames, trained model
  weights, datasets) — that's exactly what each week's `.gitignore` is for.
