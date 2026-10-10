# AFS layout migration

`git pull origin main` completed before changes in an isolated checkout. The
experiment decision record moved from the root to
`docs/decisions/experiment-decisions.md`; its contents are unchanged. Six
consumer documents now point to that living record.

Validation: content equality against `origin/main:DECISIONS.md`, a search for
old references, and `git diff --check`. This documentation change does not
verify experiment execution or hardware results.
