import inspect
import os
from functools import wraps
from types import FunctionType
from typing import Callable, Optional, Dict, Any, Union, List
from forged.namespacing.core.symbol import Symbol
from forged.namespacing.core.namespace import Namespace
from forged.namespacing.core.utils import merge_tags
from loguru import logger


# Global default namespace for decorator usage
_default_namespace = Namespace('default')
_pending_class_regs = []  # (cls_name, path, attr_name, tags, freeze, infer_path, include_context)

__all__ = ['register', 'bind_class_methods', '_default_namespace']

def register(
    path: Optional[Union[str, List[str]]] = None,
    *,
    namespace: Optional[Namespace] = None,
    tags: Optional[Dict[str, Any]] = None,
    freeze: bool = False,
    infer_path: bool = False,
    include_context: bool = False,
) -> Callable:
    """
    Decorator to register a symbol, including support for method-level delayed registration.

    Args:
        path (Optional[Union[str, List[str]]]): The path(s) to register the symbol under.
        namespace (Optional[Namespace]): The namespace to register the symbol in. Defaults to _default_namespace.
        tags (Optional[Dict[str, Any]]): Tags to attach to the symbol.
        freeze (bool): Whether to freeze the symbol.
        infer_path (bool): Whether to infer the path from the function name.
        include_context (bool): Whether to include debug context.

    Returns:
        Callable: The decorated function or class.
    """
    def decorator(obj: Any) -> Any:
        nonlocal path
        ns = namespace or _default_namespace

        if isinstance(obj, FunctionType) and obj.__qualname__.count('.') > 0:
            cls_name, _ = obj.__qualname__.split('.')[:2]
            _pending_class_regs.append((
                cls_name, path, obj.__name__, tags,
                freeze, infer_path, include_context
            ))
            return obj

        paths = [path] if isinstance(path, str) else path or [obj.__name__]
        for p in paths:
            symbol = Symbol(value=obj, name=p, tags=tags)
            if freeze:
                symbol.freeze()
            if include_context:
                _attach_debug_context(symbol)
            ns.register(p, symbol)
            logger.info(f"Registered symbol: {symbol} at path: {p}")

        return obj

    return decorator

def bind_class_methods(
    cls: Optional[type] = None,
    *,
    tags: Optional[Dict[str, Any]] = None
) -> Union[type, Callable[[type], type]]:
    """
    Post-processor for class method symbol registration.
    - Merges class-level tags with method-level tags
    - Supports multiple paths (aliasing)
    - Supports path inference and debug context attachment

    Args:
        cls (Optional[type]): The class to bind methods for.
        tags (Optional[Dict[str, Any]]): Tags to attach to the symbols.

    Returns:
        Union[type, Callable[[type], type]]: The decorated class or a decorator function.
    """
    def wrapper(klass: type) -> type:
        cls_name = klass.__name__

        for item in list(_pending_class_regs):
            reg_cls, path, attr_name, local_tags, freeze, infer_path, include_context = item
            if reg_cls != cls_name:
                continue

            attr = getattr(klass, attr_name)
            effective_tags = merge_tags(tags or {}, local_tags or {})

            # Handle multiple paths or path inference
            paths = [path] if isinstance(path, str) else path or []
            if not paths and infer_path:
                paths = [f"{cls_name}.{attr_name}"]

            for p in paths:
                symbol = Symbol(attr, name=p, tags=effective_tags)
                if freeze:
                    symbol.freeze()
                if include_context:
                    _attach_debug_context(symbol)
                _default_namespace.register(p, symbol)
                logger.info(f"Registered class method symbol: {symbol} at path: {p}")

            _pending_class_regs.remove(item)

        # Clear the list after processing
        _pending_class_regs.clear()

        return klass

    return wrapper(cls) if cls else wrapper

def _attach_debug_context(symbol: Symbol) -> None:
    """
    Attaches debug context to a symbol.

    Args:
        symbol (Symbol): The symbol to attach debug context to.
    """
    try:
        frame = inspect.currentframe().f_back.f_back
        if frame:
            info = inspect.getframeinfo(frame)
            symbol.attach_metadata("source_file", info.filename)
            symbol.attach_metadata("source_line", info.lineno)
            symbol.attach_metadata("source_code", info.code_context[0].strip() if info.code_context else "")
    except Exception as e:
        logger.error(f"Failed to attach debug context: {e}")  # Soft fail with logging