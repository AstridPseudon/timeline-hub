# Original schema source acquisition

Status: blocked at the declared public source producer/input stage.

Declared source:

`git+https://github.com/banodoco/astrid-agent.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python`

Attempted endpoint (the exact declared repository and commit, official public
GitHub API):

`https://api.github.com/repos/banodoco/astrid-agent/git/commits/242f9c4306bf3b501222cb041a9eb246ef47bc85`

Command:

```text
curl --silent --show-error --location --max-time 45 --connect-timeout 10 \
  --header 'Accept: application/vnd.github+json' \
  --header 'X-GitHub-Api-Version: 2022-11-28' \
  --dump-header commit.headers --output commit.json \
  https://api.github.com/repos/banodoco/astrid-agent/git/commits/242f9c4306bf3b501222cb041a9eb246ef47bc85
```

Acquisition result:

- curl exit status: `0` (the HTTP response was delivered).
- HTTP status: `403 Forbidden`.
- Response headers bytes: `152`.
- Response body bytes: `378`.
- Response body: `{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access. If add_repo answers that read access is already available and you need GitHub API or write access, call add_repo again with access:\"push\" to attach the repository with credentials.","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}`
- Response-body SHA-256: `b3e03aaaff81d68730d67392a135ac3fdfdf022880c66632ab188d2fe084cda3`.
- Response-header SHA-256: `7d092419b8f4c18da786b8ecb3a0306c717e9a5f38facce45e3a5d86e4d35934`.

No commit, tree, blob, package metadata, source bytes, redirect, or archive
was returned. Consequently no authenticated original-schema artifact or
commit/tree/subpath proof was acquired. No retry, credential route, `add_repo`,
alternate URL, archive endpoint, package index, cache, installed-file
reconstruction, wheel build, install, or product change was attempted.

The normal maker must receive access to the declared exact source input and
then independently retain and review the original source bytes before
installation. The installed `ArtAgents` direct URL remains unproved equivalent
to the declared `astrid-agent` URL and is not used as a substitute.
