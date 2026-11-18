# AFS layout migration

`git pull origin main` completed before changes in an isolated checkout. The
experiment decision record moved from the root to
`docs/decisions/experiment-decisions.md`; its contents are unchanged. Five
derived consumer documents now point to that living record. The captured
specification remains byte-identical to the main-branch input; its old path is
historical source text rather than an instruction to restore the root file.

Validation: content equality against `origin/main:DECISIONS.md`, a search for
old references, and `git diff --check`. This documentation change does not
verify experiment execution or hardware results.

The zero-byte dated research placeholder was replaced by a continuous
`training-factory` unit with ordered questions, explicitly untested hypotheses,
method, existing evidence and next action. Root catalogs distinguish recorded
provider leads from inspected sources. Local links and whitespace passed; no
research result, budget decision, paid run or public claim was approved.

2026-11-18 review correction: restored the captured specification verbatim and
pointed `SOURCES.md` to the two inputs containing external references. The
provider register summarizes choices but contains no external citations.
