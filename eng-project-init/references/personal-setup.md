# Personal Setup

## GitHub Clone Defaults

When initializing a repository cloned from GitHub for this user, set the repository-local Git email:

```bash
git config user.email "40706446+Lumysia@users.noreply.github.com"
```

Rules:

- Apply only to the current repository, never global Git config.
- Use only when the repository was cloned from GitHub or the user explicitly asks for this identity.
- Preserve an existing repository-local email unless it is missing or the user asks to replace it.
- Verify with `git config user.email` after setting it.
