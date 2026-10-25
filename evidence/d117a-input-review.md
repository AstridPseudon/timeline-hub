# D117a independent input/integrity review

Result: **PASS** for the exact supported OMP local/offline stage-input seam.

This is a source/integrity review only. It does not qualify an ordinary full
stage, installed profile, service command, or render.

## Authentic retained source receipt

The retained author receipt reports one authorized anonymous Git fetch, exit
`0`, with `GIT_LFS_SKIP_SMUDGE=1`, for:

- OMP commit: `9e282751c0059e37d2f6fbc14ffa0b450710bd23`
- OMP tree: `2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f`
- LFS pointer blobs: `0`
- `local_source` exit: `0`
- `extract` exit: `0`
- OMP version: `17.4.0`
- frozen Bun-lock SHA-256: `f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee`
- extracted source-tree SHA-256: `3a84ac8be7d11434de8b22f4f0f1d643582ecc01c644e347bb0e056401da7b2e`

The retained codeload archive digest is
`ee8b3117370f6f2b3aa1a7f0f3ba8948113fb61fd1abc963b47cb82716c1bbdf`.
The separately generated local Git archive digest is
`a7673f9f9b77d24989a5a84b70380f77af3dd869a7be2b94c8d56de404065ecb`.
They are distinct transport artifacts; no equivalence was inferred.

The temporary clone/archive/extract used by the author is gone. These facts
are receipt evidence, not a claim that the fetched artifact remains available.

## Exact production seam

Unchanged source, with line references:

1. `astrid/installer/cli.py:105` reads and validates the install manifest.
2. `astrid/installer/core.py:246` calls `self.backend.stage(manifest, self.root, self.data)`.
3. `astrid/installer/backend.py:408` calls
   `install_tools(manifest, folder / "tools", platform_target(), self.run)`.
4. `astrid/installer/tools.py:466` selects `pins["omp"]` through `omp_source`;
   `tools.py:510` calls
   `_install_omp_source(selected, load_omp_recipe(), omp, target, self.run, env)`
   for a pinned Git source.
5. `tools.py:340` calls `omp_source_url(selected["repo"], selected["sha"])`.
   An absolute local path or `file://` URL passes `local_repository` and returns
   `None` (`tools.py:169-181`, `tools.py:45-53`).
6. The `None` branch at `tools.py:348-354` calls exactly
   `local_source(selected["repo"], selected["sha"], root / "source.download")`
   followed by `extract(archive, container)`.

Therefore the supported offline manifest input is:

```json
"tools": {
  "omp": {
    "source": {
      "repo": "/absolute/path/to/existing/git-repository",
      "sha": "9e282751c0059e37d2f6fbc14ffa0b450710bd23"
    }
  }
}
```

`local_source` requires the SHA to resolve to a Git commit, rejects links and
submodules from `ls-tree`, and creates the archive with `git archive`
(`tools.py:184-211`). The OMP path then checks the extracted tree digest is
computable, the frozen Bun lock, package version, native archive SHA-256, native
ABI marker, and final lock (`tools.py:362-431`). The local source archive has
no codeload/tarball SHA-256 check; its integrity is commit/tree based plus the
post-extraction checks. This is why the local Git archive hash must not be
substituted for the retained codeload hash.

## Custody and qualification limits

- The exact OMP source receipt is authentic as retained evidence, but the
  source artifact is not available in this worktree and was not recreated.
- The retained applied Agent identity is commit
  `cd3f5480350d1ca68c9d8ec16aeae2863501c2a4` / tree
  `523893dcf54dbe756db8fe2915d14055b1da660b`; the retained applied Runtime
  identity is commit `62040eeab98747dfb65abb6366236bf213109d6c` / tree
  `a522511414947e48e317a5e5c2103483b121a750`. Narrow read-only `git
  cat-file` checks did not find the exact applied Agent objects or applied
  Runtime commit in the permitted existing clones; the Runtime tree object was
  present. No current or near-match tree was substituted.
- The first ordinary missing input is therefore the exact applied deployment
  source set needed by `Backend.stage`, not the OMP local/offline seam.
- No ordinary stage was run. Complete-stage peak, installed profile,
  service argv, seven-key carrier, and render remain unknown.
- No network/fetch/clone/acquisition/stage/render/test/typecheck/lint or source
  edit was performed by this review.

## Static evidence

Current source hashes exactly match the retained integration-source hashes:

```text
a0b2bfc178787f7d863a1180bdbc73a6c5690e7d5b91ebd008b98c57b1e6ef09  astrid/installer/core.py
8707791013bbc0ea885d818e62286165931e33a4be03f6bb87af9c84c01a1139  astrid/installer/backend.py
c0da1099b958bbde0d6a3bfe513193c839e9fe93ef028373ae086b30badf400a  astrid/installer/tools.py
9faec7eb6ff285d935ac6adcaf0b698a4f7fcf95eb3e7a108e665b6a4e24605b  astrid/installer/omp/recipe.json
```

Python AST parsing and recipe JSON/pin checks passed. No product files were
changed.
