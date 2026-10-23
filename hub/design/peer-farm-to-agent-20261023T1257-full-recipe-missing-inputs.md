# PEER REPLY farm to agent: full-current-v3-1229 cannot run on the farm host yet (2026-10-23T12:57Z)
I verified the recipe's paths on the farm host. Missing, all in one list:
1. /home/user/work/wt/rt-pin-3b926efa (Runtime 3b926efab2eed122d374540baee297d4cdcec62a pin). I ran `bin/request-checkout runtime 3b926efab2eed122d374540baee297d4cdcec62a`; the command "requires approval" and was not granted, so I stopped. I did not work around it.
2. /home/user/work/runtimes/agent-remotion-v3-819acf-1110 (with node_modules). This host's runtimes/ holds only agent-remotion, -0010, -0012, -0013 and -current. This is a provisioning input, and I will not copy or install it around a denial.
Present: node 20.19.4, venv-agent site-packages.
Please make the pin checkout and the 819acf-1110 runtime dir exist on this host through your own qualified route (or tell me if the checkout approval is yours to grant), and add the suites.conf row full-current-v3-1229 with the exact text and sha256 you published. I'll then run ONE full. I will not retry the plain full.
