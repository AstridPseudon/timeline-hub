"""Real Seatbelt/Foundation predicate checks, without launching a renderer."""
import errno
import json
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest

from astrid.core.execution import generic_host as host
from astrid.core.execution.remotion_host_session import _host_browser_executable

PROBE = r'''
import ctypes,json,os,sys
from pathlib import Path
ctypes.CDLL('/System/Library/Frameworks/Foundation.framework/Foundation')
objc=ctypes.CDLL('/usr/lib/libobjc.A.dylib')
ptr=ctypes.c_void_p
objc.objc_getClass.argtypes=[ctypes.c_char_p]; objc.objc_getClass.restype=ptr
objc.sel_registerName.argtypes=[ctypes.c_char_p]; objc.sel_registerName.restype=ptr
send0=ctypes.CFUNCTYPE(ptr,ptr,ptr)(('objc_msgSend',objc))
send1=ctypes.CFUNCTYPE(ptr,ptr,ptr,ptr)(('objc_msgSend',objc))
sendstr=ctypes.CFUNCTYPE(ptr,ptr,ptr,ctypes.c_char_p)(('objc_msgSend',objc))
def sel(name): return objc.sel_registerName(name.encode())
def cls(name): return objc.objc_getClass(name.encode())
pool=send0(send0(cls('NSAutoreleasePool'),sel('alloc')),sel('init'))
def bundle(path):
    string=sendstr(cls('NSString'),sel('stringWithUTF8String:'),path.encode())
    url=send1(cls('NSURL'),sel('fileURLWithPath:'),string)
    value=send1(cls('NSBundle'),sel('bundleWithURL:'),url)
    identifier=send0(value,sel('bundleIdentifier')) if value else None
    if identifier:
        raw=send0(identifier,sel('UTF8String'))
        return ctypes.string_at(raw).decode()
    return None
def attempt(call):
    try: return {'value':call()}
    except OSError as exc: return {'errno':exc.errno}
app,framework,outside,private=sys.argv[1:]
result={'app':bundle(app),'framework':bundle(framework),
        'applications_metadata':attempt(lambda:os.stat('/Applications').st_mode),
        'applications_listing':attempt(lambda:os.listdir('/Applications')),
        'outside_read':attempt(lambda:Path(outside).read_text()),
        'outside_write':attempt(lambda:Path(outside).write_text('forbidden')),
        'private_write':attempt(lambda:Path(private,'allowed.txt').write_text('owned'))}
send0(pool,sel('drain'))
print(json.dumps(result))
'''


@pytest.mark.skipif(sys.platform != 'darwin', reason='real macOS bundle permission consumer')
@pytest.mark.parametrize('renderer', [False, True])
def test_selected_browser_bundle_metadata_is_read_only(tmp_path, renderer):
    browser = _host_browser_executable()
    assert browser is not None
    contents = browser.parent.parent
    private = tmp_path / 'private'
    private.mkdir(mode=0o700)
    outside = tmp_path / 'synthetic-credential.txt'
    outside.write_text('synthetic-outside')
    probe = private / 'bundle_probe.py'
    probe.write_text(PROBE)
    python = Path(sys.executable).resolve()
    runtime = host._python_runtime_library(Path(sys.base_prefix))
    literals = [python, probe, Path('/opt/homebrew/opt/gettext/lib/libintl.8.dylib'),
                Path('/dev/null'), Path('/dev/random'), Path('/dev/urandom')]
    if runtime is not None:
        literals.append(runtime)
    literals = list(dict.fromkeys([*literals, *(p.resolve() for p in literals)]))
    roots = {Path(sysconfig.get_path(name)).resolve() for name in ('stdlib', 'purelib', 'platlib')}
    roots.update(map(Path, ['/usr/lib', '/System/Library/Frameworks/Foundation.framework',
                           '/System/Library/Frameworks/CoreFoundation.framework',
                           '/System/Library/Frameworks/CoreServices.framework',
                           '/System/Volumes/Preboot/Cryptexes/OS/System/Library/dyld',
                           '/System/Volumes/Preboot/Cryptexes/OS/usr/lib']))
    def quote(path):
        return str(path).replace('\\', '\\\\').replace('"', '\\"')
    rules = ['(version 1)', '(deny default)', '(allow process-exec)',
             '(deny process-fork)', '(allow sysctl-read)', '(allow file-read* (literal "/"))']
    for resource in (*roots, *literals, private):
        rules.extend(f'(allow file-read-metadata (literal "{quote(p)}"))' for p in resource.parents)
    for resource in roots | {private}:
        rules.extend([f'(allow file-read* (subpath "{quote(resource)}"))',
                      f'(allow file-map-executable (subpath "{quote(resource)}"))'])
    for resource in literals:
        rules.extend([f'(allow file-read* (literal "{quote(resource)}"))',
                      f'(allow file-map-executable (literal "{quote(resource)}"))'])
    rules.append(f'(allow file-write* (subpath "{quote(private)}"))')
    if renderer:
        rules.extend(host._renderer_browser_read_rules(browser, quote))
    profile = private / 'bundle.sb'
    profile.write_text('\n'.join(rules) + '\n')
    env = {'HOME': str(private), 'TMPDIR': str(private), 'PATH': '/usr/bin:/bin',
           'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1', 'LC_ALL': 'C'}
    result = subprocess.run(['/usr/bin/sandbox-exec', '-f', str(profile), str(python),
                             '-I', '-S', '-B', str(probe), str(contents.parent),
                             str(contents / 'Frameworks/Google Chrome Framework.framework'),
                             str(outside), str(private)],
                            cwd=private, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    observed = json.loads(result.stdout)
    if renderer:
        assert observed['app'] == 'com.google.Chrome'
        assert observed['framework'] == 'com.google.Chrome.framework'
        assert 'value' in observed['applications_metadata']
    else:
        assert observed['app'] is None
        assert observed['framework'] is None
    for operation in ('applications_listing', 'outside_read', 'outside_write'):
        assert observed[operation]['errno'] in (errno.EPERM, errno.EACCES)
    assert observed['private_write'] == {'value': 5}
    assert outside.read_text() == 'synthetic-outside'
