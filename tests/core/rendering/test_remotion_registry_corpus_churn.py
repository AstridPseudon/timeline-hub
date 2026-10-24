"""Finder/bytecode droppings must not invalidate a launch-bound registry corpus."""
from astrid.core.rendering import remotion_runtime as runtime


def _observation(root):
    return {'module_files': [], 'roots': [str(root)], 'package_roots': [], 'optional_files': [],
            'search_paths': [str(root)]}


def test_generated_names_do_not_change_registry_inputs(tmp_path):
    (tmp_path / 'module.py').write_text('x = 1\n')
    (tmp_path / 'sub').mkdir()
    (tmp_path / 'sub' / 'inner.py').write_text('y = 2\n')
    before = runtime._registry_inputs(_observation(tmp_path))
    for directory in (tmp_path, tmp_path / 'sub'):
        (directory / '.DS_Store').write_bytes(b'finder')
        (directory / '__pycache__').mkdir(exist_ok=True)
        (directory / '__pycache__' / 'module.cpython-311.pyc').write_bytes(b'pyc')
    assert runtime._registry_inputs(_observation(tmp_path)) == before


def test_real_source_changes_still_change_registry_inputs(tmp_path):
    (tmp_path / 'module.py').write_text('x = 1\n')
    before = runtime._registry_inputs(_observation(tmp_path))
    (tmp_path / 'new_module.py').write_text('z = 3\n')
    assert runtime._registry_inputs(_observation(tmp_path)) != before
