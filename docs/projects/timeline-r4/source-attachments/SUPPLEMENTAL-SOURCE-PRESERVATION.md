# Supplemental source preservation

This note accompanies the Timeline R4 source handover. It records source bytes that are not part of the four product candidate refs; it does not qualify or apply them. Exact file sizes, SHA-256 values, original identities, and limitations are in `source-attachments.json`.

- Three App-hydrator Git blobs are retained by full blob OID. Their original paths and parents are unknown, so they are unqualified historical variants.
- The primary App audio-resume/editor changes are preserved as an exact WIP patch against source commit `513bf4ea200c1b09c60a4fb30579004c334c2146`. This is the Remotion 4.0.503 variant and is unqualified; the current candidate uses a separate Remotion 4.0.509 setup.
- The four J029 files are exact source members from the historical `timeline-r4-handover-20261017.zip` (SHA-256 `143c29812b87fd4b34b20858a7f354878d088c876f88d397fd009676e7b054ac`). They are a historical snapshot; no current checkout or newer source identity is asserted.
- The staged `d4178b2` tree adds no unique Timeline R4 source relative to the published SDK candidate ancestry. The other staged commit, `1086b68`, has a missing tree object and remains an incomplete archival record; no missing content is reconstructed.

No operational process handles, local Runtime/Host state, or unrelated receipt scratch are included.
