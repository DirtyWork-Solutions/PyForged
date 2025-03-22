import pytest
import asyncio
from forged.hooks.hook_config import load_hook_config
from forged.hooks.hook_executor import execute_hooks, add_hook_middleware
from forged.hooks.hook_register import register_hook, unregister_hook, get_registered_hooks
from forged.hooks.native_hooks import DefaultPreHook

def test_load_hook_config_json():
    config = load_hook_config('files/test_config.json')
    assert isinstance(config, dict)

def test_load_hook_config_yaml():
    config = load_hook_config('files/test_config.yaml')
    assert isinstance(config, dict)

@pytest.fixture
def hook():
    hook_name = 'test_hook'
    hook = DefaultPreHook()
    register_hook(hook_name, hook)
    yield hook_name, hook
    unregister_hook(hook_name, hook)

def test_register_hook(hook):
    hook_name, hook_instance = hook
    hooks = get_registered_hooks(hook_name)
    assert (10, hook_instance, True, []) in hooks

def test_unregister_hook(hook):
    hook_name, hook_instance = hook
    unregister_hook(hook_name, hook_instance)
    hooks = get_registered_hooks(hook_name)
    assert (10, hook_instance, True, []) not in hooks

def test_execute_hooks_sync(hook):
    hook_name, _ = hook
    results = execute_hooks(hook_name, 'arg1', mode='sync')
    assert len(results) == 1

@pytest.mark.asyncio
async def test_execute_hooks_async(hook):
    hook_name, _ = hook
    results = await execute_hooks(hook_name, 'arg1', mode='async')
    assert len(results) == 1

@pytest.fixture
def middleware_hook():
    hook_name = 'test_hook'
    hook = DefaultPreHook()
    register_hook(hook_name, hook)
    yield hook_name, hook
    unregister_hook(hook_name, hook)

def test_add_hook_middleware(middleware_hook):
        hook_name, _ = middleware_hook

        def sample_middleware(name, args, kwargs):
            return args + ('middleware_arg',), kwargs

        add_hook_middleware(sample_middleware)
        results = execute_hooks(hook_name, 'arg1', mode='sync')
        assert results[0] == (('arg1', 'middleware_arg'), {})