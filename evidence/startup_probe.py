"""Disposable C3 Runtime/Agent startup probe; no owner configuration."""
from pathlib import Path
import json
import traceback

from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

base = Path('/tmp/w-23303af769/c3-startup')
base.mkdir(mode=0o700)
root = base / 'realm'
RealmStore.initialize(root).close()
provider = load_timeline_commit_provider('astrid')
print(json.dumps({'provider_loaded': provider.provider_id}), flush=True)
daemon = RuntimeDaemon(
    root, support_root=base / 'support', log_directory=base / 'logs',
    host='127.0.0.1', port=0, authoring_profile='astrid',
)
try:
    daemon.start()
    print(json.dumps({'startup': 'ready', 'loopback_only': True}), flush=True)
except Exception as error:
    print(json.dumps({'startup': 'failed', 'exception': type(error).__name__,
                      'reason': str(error)}), flush=True)
    traceback.print_exc()
    raise
finally:
    daemon.stop()
