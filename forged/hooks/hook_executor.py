import asyncio
import time
from loguru import logger

# Global middleware for hooks
_hook_middleware = []

def add_hook_middleware(fn):
    """Register a middleware function for hooks."""
    _hook_middleware.append(fn)

def apply_middleware(name: str, args, kwargs):
    for mw in _hook_middleware:
        args, kwargs = mw(name, args, kwargs)
    return args, kwargs

def execute_hooks(name: str, *args, mode: str = 'sync', context: dict = None, retries: int = 3, **kwargs):
    """
    Executes all hooks for a given name with support for:
      - Middleware application
      - Lifecycle callbacks
      - Execution modes: sync, async, deferred
      - Error handling and retries
    """
    from forged.hooks.hook_register import get_registered_hooks
    hooks = get_registered_hooks(name)
    context = context or {}

    # Apply middleware to the arguments
    args, kwargs = apply_middleware(name, args, kwargs)

    results = []
    start_time = time.time()

    if mode == 'sync':
        for priority, hook, enabled, deps in hooks:
            attempt = 0
            while attempt < retries:
                try:
                    result = hook.execute(*args, context=context, **kwargs)
                    results.append(result)
                    break
                except Exception as e:
                    attempt += 1
                    logger.exception(f"Error executing hook {hook} for '{name}' on attempt {attempt}: {e}")
                    if attempt >= retries:
                        logger.error(f"Hook {hook} failed after {retries} attempts.")
    elif mode == 'async':
        loop = asyncio.get_event_loop()
        tasks = []
        for priority, hook, enabled, deps in hooks:
            tasks.append(loop.create_task(async_hook_wrapper(hook, *args, context=context, retries=retries, **kwargs)))
        results = tasks  # Caller can await them.
    elif mode == 'deferred':
        logger.debug(f"Deferred execution for hook '{name}' with args {args} and kwargs {kwargs}")
    else:
        raise ValueError("Invalid mode. Use 'sync', 'async', or 'deferred'.")

    elapsed = time.time() - start_time
    logger.info(f"Executed hooks for '{name}' in {elapsed:.4f} seconds.")
    return results

async def async_hook_wrapper(hook, *args, retries: int = 3, **kwargs):
    attempt = 0
    while attempt < retries:
        try:
            result = hook.execute(*args, **kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as e:
            attempt += 1
            logger.exception(f"Error in async hook {hook} on attempt {attempt}: {e}")
            if attempt >= retries:
                logger.error(f"Async hook {hook} failed after {retries} attempts.")