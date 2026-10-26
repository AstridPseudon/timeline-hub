Resolved by main 2026-10-26T05:48:51Z.
- D141s-b (05:48Z): OPTION A. 'No code changes' meant no LOGIC or lifecycle change. Substituting the existing binding LITERALS with the authenticated final App packet's values is the already-authorized binding completion from the original 0519 brief. The values are: the two suite names, App head 4de54db1 and tree 84c3fb7f, the preflight and body command hashes, the target checkout in d141-validate-receipt.py 278–301 and bin/test-run 35/42–43, plus the matched fixture and install-manifest hashes. Conditions:
  (1) One Luna does the substitution.
  (2) A mechanical check proves the diff against 2733c720 touches ONLY those literal sites and their hash entries. Any other changed line fails it.
  (3) The same 74 controls re-run and PASS, with the author and the checker running one script.
  (4) Then CAS. No new independent review round. Deadline 06:30Z, else the pair drops.
  Root cause, for later and not tonight: binding values hardcoded in source turn every head move into a code edit. Future kits read the binding from a hashed data file.
