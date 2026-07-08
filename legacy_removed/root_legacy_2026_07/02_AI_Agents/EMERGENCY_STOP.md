# Emergency Stop

Use this when AI behavior or repository state becomes unsafe.

## Stop Conditions

Stop immediately if any of these occur:

- Unexpected delete.
- Unexpected Git status.
- Private files appear in a parent repo.
- Secret, token, API key, credential, password, cookie, seed phrase, or private key is detected.
- Push is requested without explicit approval.
- History rewrite is requested.
- Large unexpected file movement.
- AI touches a path outside the approved target.
- Tool output suggests hidden side effects.

## Recovery Steps

1. Stop.
2. Do not commit.
3. Do not push.
4. Run `git status --short` for the affected repo.
5. Report touched files or route-level changes.
6. Identify whether private or secret risk exists.
7. Ask Zhuan for review before continuing.

## Report Format

- What triggered stop:
- Target repo:
- Files or routes touched:
- Git status summary:
- Private/secret risk:
- Recommended next action:
