# GitBook setup

This repository is ready for GitBook sync.

Suggested settings:

- Project directory: `./`
- Root file: `docs/README.md`
- Summary file: `docs/SUMMARY.md`

Before GitBook is published, the demo uses relative links to `docs/playbooks/` so local and GitHub Pages reviewers can still open the playbooks.

After GitBook publishes the space, update `GITBOOK_BASE_URL` in `src/entralab/demo.py` so playbook links open the public GitBook pages.

Do not tag `v0.1.0` until GitBook is public, the demo has been regenerated, and the public playbook links have been verified.
