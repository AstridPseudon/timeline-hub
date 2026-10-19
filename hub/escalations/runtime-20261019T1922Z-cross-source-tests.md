# Real-provider test lane + external source cache identity

Runtime M1 helpers are merging; next required proof uses actual Agent provider. Request one named central lane (Runtime optional integration stays deselected in neutral default suite):

runtime commit-integration env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py

Worker will add that tests file and import Agent only inside integration fixtures. Runtime snapshot remains first on PYTHONPATH; real Agent source/deps used. Local sockets only test service. Please add this named suite or equivalent; I won't edit shared runner infrastructure.

Concrete cache concern: bin/test-run currently keys only repo + target TREE + suite + files + CMD. App three-products and this Runtime lane also consume other repos, so same App/Runtime tree with changed external Agent/Runtime source could return an obsolete cached pass. Recommendation include external source tuple in cache key for cross-product suites; meanwhile I will use --no-cache only when external dependency source changed, record exact source tuple, and never interpret a cached old-source result as new gate evidence. No repeated unchanged-source full run requested. Continue Runtime review/integration while this is answered.
