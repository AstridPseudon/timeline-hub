"""Renderer selection in the trusted installed Host composition.

This is a selection, not authority supplied by a task. Only the profile
producer accepts an already admitted closure; the retained installed launch
and authenticated preparation bind its serialized representation.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

from .remotion_closure import RemotionClosureBinding
from .declared_executables import ExecutableBinding, FilePin


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _path(value):
    if not isinstance(value, str):
        raise ValueError('renderer selection path is invalid')
    path = Path(value)
    if not path.is_absolute() or str(path) != value or path.resolve(strict=True) != path:
        raise ValueError('renderer selection path must be canonical')
    return path


@dataclass(frozen=True)
class HostRendererSelection:
    closure: RemotionClosureBinding
    node: ExecutableBinding

    def payload(self):
        if type(self.closure) is not RemotionClosureBinding or type(self.node) is not ExecutableBinding:
            raise ValueError('renderer producer requires independently admitted typed inputs')
        self.closure.require_retained_transport()
        self.node.verify()
        if self.node.name != 'node' or self.node.executable.path != self.node.executable.resolved:
            raise ValueError('renderer requires the canonical admitted Node selection')
        c = self.closure
        return {'version': 'astrid.host-renderer-selection/v1', 'project': str(c.project),
                'installed_project': str(c.installed_project), 'verification_receipt': str(c.receipt),
                'receipt_sha256': c.receipt_digest, 'manifest_sha256': c.manifest_digest,
                'lock_sha256': c.lock_digest,
                'closure_sha256': _digest([(str(p), h) for p, h in c.files]),
                'node_executable': str(self.node.executable.path),
                'node_sha256': hashlib.sha256(self.node.executable.path.read_bytes()).hexdigest(),
                'node_admission_sha256': _digest(self.node.evidence())}


def renderer_selection_payload(value):
    fields = {'version', 'project', 'installed_project', 'verification_receipt', 'receipt_sha256',
              'manifest_sha256', 'lock_sha256', 'closure_sha256', 'node_executable', 'node_admission_sha256', 'node_sha256'}
    if not isinstance(value, dict) or set(value) != fields or value['version'] != 'astrid.host-renderer-selection/v1':
        raise ValueError('renderer selection shape is invalid')
    for name in fields - {'version', 'project', 'installed_project', 'verification_receipt', 'node_executable'}:
        if not isinstance(value[name], str) or re.fullmatch('[0-9a-f]{64}', value[name]) is None:
            raise ValueError('renderer selection digest is invalid')
    for name in ('project', 'installed_project', 'verification_receipt', 'node_executable'):
        raw = value[name]
        if (not isinstance(raw, str) or not raw or "\0" in raw or not Path(raw).is_absolute()
                or ".." in Path(raw).parts or str(Path(raw)) != raw):
            raise ValueError('renderer selection path is invalid')
    return json.loads(json.dumps(value))


def validate_renderer_selection(value, *, retained=None):
    value = renderer_selection_payload(value)
    for name in ('project', 'installed_project', 'verification_receipt', 'node_executable'):
        _path(value[name])
    if retained is None:
        binding = RemotionClosureBinding.admit(**{k: value[k] for k in (
            'project', 'installed_project', 'verification_receipt', 'receipt_sha256', 'manifest_sha256', 'lock_sha256')})
    else:
        # Retain admission facts, never mutable-byte results. Every invocation
        # below still enumerates the whole installation and hashes every pin.
        binding = retained
        if (type(binding) is not RemotionClosureBinding
                or (str(binding.project), str(binding.installed_project), str(binding.receipt),
                    binding.receipt_digest, binding.manifest_digest, binding.lock_digest) != tuple(value[k] for k in (
                        'project', 'installed_project', 'verification_receipt', 'receipt_sha256', 'manifest_sha256', 'lock_sha256'))):
            raise ValueError('renderer retained selection differs')
    binding.require_retained_transport()
    if _digest([(str(p), h) for p, h in binding.files]) != value['closure_sha256']:
        raise ValueError('renderer selected closure changed')
    # Full executable dependency admission is checked through the original
    # owner's inspection channel after activation. No local inspection fallback.
    pin = FilePin.measure(Path(value['node_executable']))
    if pin.sha256 != 'sha256:' + value['node_sha256']:
        raise ValueError('renderer selected Node changed')
    return binding


def activate_renderer_selection(value):
    from .declared_executables import _bind
    binding = validate_renderer_selection(value)
    node = _bind('node', Path(value['node_executable']))
    if _digest(node.evidence()) != value['node_admission_sha256']:
        raise ValueError('renderer Node admission changed')
    return HostRendererSelection(binding, node)
