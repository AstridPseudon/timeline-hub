# AM source-copy cleanup handoff

Removed `/tmp/vw-m3-am-patch-check.4XAYRf` only after confirming it was owned by
finished worker `vw-m3-am-footage-qualified-current-source` and matched the
retained branch `tl/vw-m3-am-footage-qualified-current-source` at commit
`53d1f5c7282064fcf8802646313bf31612dd8ee8` (parent `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`).
The copy was `107,142,346` apparent / `117,084,160` allocated bytes, 3,101
files, with no symlinks or duplicate inodes. Owner reports, `PATCH`,
`FILELIST`, commands, manifests, and source branch remain retained.

No live cwd/fd, running marker, lease, or peer caller was found. Immediate
post-removal statfs available bytes were `10,142,400,512`; the latest observed
reading at `2026-10-21T04:44:28Z` was `10,142,187,520`, still `595,230,720`
below the 10 GiB floor. Statfs varied with concurrent machine activity. No
product files or tests were involved.

