"""Registry validation judges the projected child environment."""
import pytest

from astrid.core.rendering import remotion_runtime as runtime


def _env(tmp_path, **extra):
    return {'HOME': str(tmp_path), 'PATH': '/usr/bin:/bin', **extra}


def test_interactive_git_variables_are_accepted_and_never_reach_the_probe(tmp_path):
    context = runtime._registry_context(
        _env(tmp_path, GIT_EDITOR='true', GIT_PAGER='cat', GIT_TERMINAL_PROMPT='0'), generator=False)
    assert context['HOME'] == str(tmp_path)
    assert not any(key.startswith('GIT_') for key in context)


@pytest.mark.parametrize('generator', [False, True])
@pytest.mark.parametrize('name', ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_CONFIG_GLOBAL', 'GIT_INDEX_FILE', 'PYTHONSTARTUP'])
def test_ambient_git_redirection_and_startup_hooks_never_reach_children(tmp_path, name, generator):
    from astrid.core.subprocess_env import build_child_subprocess_env
    clean = _env(tmp_path)
    ambient = {**clean, name: str(tmp_path / 'x')}
    context = runtime._registry_context(ambient, generator=generator)
    expected = runtime._registry_context(clean, generator=generator)
    assert context == expected
    assert runtime._canonical(context) == runtime._canonical(expected)
    assert build_child_subprocess_env(base=ambient, parent=ambient) == build_child_subprocess_env(base=clean, parent=clean)


@pytest.mark.parametrize('name', ['PYTHONPATH', 'ASTRID_SOURCE_STATE', 'XDG_STATE_HOME', 'XDG_CONFIG_HOME'])
def test_malformed_projected_paths_name_the_variable_and_fix(tmp_path, name):
    with pytest.raises(runtime.RemotionValidationError, match=name + '.*absolute'):
        runtime._registry_context(_env(tmp_path, **{name: 'relative'}), generator=False)
    # Generator children do not receive these renderer-only selectors.
    assert runtime._registry_context(_env(tmp_path, **{name: 'relative'}), generator=True) == runtime._registry_context(_env(tmp_path), generator=True)


@pytest.mark.parametrize('value', [':/absolute', '/absolute:', '/absolute:relative'])
def test_projected_pythonpath_refuses_empty_and_relative_entries(tmp_path, value):
    import os
    with pytest.raises(runtime.RemotionValidationError, match='PYTHONPATH.*remove empty or relative'):
        runtime._registry_context(_env(tmp_path, PYTHONPATH=value.replace(':', os.pathsep)), generator=False)
