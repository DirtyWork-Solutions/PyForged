"""
This module provides a service registry for managing the lifecycle of services in a Python application.
It includes functionality for registering services, factories, middleware, and health checks, as well as
injecting dependencies and managing service lifecycles.

**Classes:**
    - ServiceNotRegisteredException:
      Exception raised when a requested service is not registered.

    - ServiceInitializationException:
      Exception raised when a service fails to initialize.

    - ServiceRegistry:
      A registry for managing services, factories, middleware, and health checks.


**Functions:**
    - *check_all_services_health:*
      Checks the health of all registered services.

    - *periodic_health_check:*
      Periodically checks the health of all registered services.
"""

import inspect
import logging
import asyncio
from typing import Any, Callable, Dict, Type, Optional, Union, List
from threading import Lock

logging.basicConfig(level=logging.INFO)

class ServiceNotRegisteredException(Exception):
    """Exception raised when a requested service is not registered."""
    pass

class ServiceInitializationException(Exception):
    """Exception raised when a service fails to initialize."""
    pass

class ServiceRegistry:
    """
    A registry for managing services, factories, middleware, and health checks.

    Methods:
        - register: Registers a service instance.
        - register_factory: Registers a factory for creating service instances.
        - unregister: Unregisters a service.
        middleware: Registers a middleware function for a specific hook.
        get: Retrieves a service instance.
        inject_dependencies: Injects dependencies into a service class.
        register_health_check: Registers a health check for a service.
        check_health: Checks the health of a specific service.
        list_services: Lists all registered services.
        get_service_metadata: Retrieves metadata for a specific service.
        shutdown: Shuts down all services, calling their shutdown hooks.
    """
    def __init__(self):
        """Initializes the service registry."""
        self._services = {}
        self._factories = {}
        self._singletons = {}
        self._aliases = {}
        self._lifecycle_hooks = {}
        self._lock = Lock()
        self._middleware = {}
        self._health_checks = {}
        self._service_versions = {}
        self._service_metadata = {}

    def register(self, service_name: str, instance: Any, singleton: bool = False,
                 dependencies: Optional[List[str]] = None, aliases: Optional[List[str]] = None,
                 on_init: Optional[Callable] = None, on_shutdown: Optional[Callable] = None,
                 version: str = "1.0.0", metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Registers a service instance.

        Args:
            service_name (str): The name of the service.
            instance (Any): The service instance.
            singleton (bool): Whether the service is a singleton.
            dependencies (Optional[List[str]]): List of dependencies for the service.
            aliases (Optional[List[str]]): List of aliases for the service.
            on_init (Optional[Callable]): Initialization hook for the service.
            on_shutdown (Optional[Callable]): Shutdown hook for the service.
            version (str): Version of the service.
            metadata (Optional[Dict[str, Any]]): Metadata for the service.
        """
        with self._lock:
            logging.info(f"Registering service: {service_name}")
            self._services[service_name] = instance
            if singleton:
                self._singletons[service_name] = instance
            self._lifecycle_hooks[service_name] = {'on_init': on_init, 'on_shutdown': on_shutdown}
            self._service_versions[service_name] = version
            self._service_metadata[service_name] = metadata or {}
            if aliases:
                for alias in aliases:
                    self._aliases[alias] = service_name
            if dependencies:
                for dependency in dependencies:
                    self.get(dependency)

    def register_factory(self, service_name: str, factory: Union[Callable[..., Any], Callable[..., asyncio.Future]],
                         singleton: bool = True, aliases: Optional[List[str]] = None,
                         on_init: Optional[Callable] = None, on_shutdown: Optional[Callable] = None,
                         version: str = "1.0.0", metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Registers a factory for creating service instances.

        Args:
            service_name (str): The name of the service.
            factory (Union[Callable[..., Any], Callable[..., asyncio.Future]]): The factory function.
            singleton (bool): Whether the service is a singleton.
            aliases (Optional[List[str]]): List of aliases for the service.
            on_init (Optional[Callable]): Initialization hook for the service.
            on_shutdown (Optional[Callable]): Shutdown hook for the service.
            version (str): Version of the service.
            metadata (Optional[Dict[str, Any]]): Metadata for the service.
        """
        with self._lock:
            logging.info(f"Registering factory for service: {service_name}")
            self._factories[service_name] = factory
            if singleton:
                self._singletons[service_name] = None
            self._lifecycle_hooks[service_name] = {'on_init': on_init, 'on_shutdown': on_shutdown}
            self._service_versions[service_name] = version
            self._service_metadata[service_name] = metadata or {}
            if aliases:
                for alias in aliases:
                    self._aliases[alias] = service_name

    def unregister(self, service_name: str) -> None:
        """
        Unregisters a service.

        Args:
            service_name (str): The name of the service to unregister.
        """
        with self._lock:
            logging.info(f"Unregistering service: {service_name}")
            resolved_name = self._aliases.pop(service_name, service_name)
            self._services.pop(resolved_name, None)
            self._factories.pop(resolved_name, None)
            self._singletons.pop(resolved_name, None)
            self._lifecycle_hooks.pop(resolved_name, None)
            self._service_versions.pop(resolved_name, None)
            self._service_metadata.pop(resolved_name, None)

    def middleware(self, hook_name: str, middleware_func: Callable[[Any], Any]) -> None:
        """
        Registers a middleware function for a specific hook.

        Args:
            hook_name (str): The name of the hook.
            middleware_func (Callable[[Any], Any]): The middleware function.
        """
        logging.info(f"Registering middleware for: {hook_name}")
        self._middleware[hook_name] = middleware_func

    def get(self, service_name: str) -> Any:
        """
        Retrieves a service instance.

        Args:
            service_name (str): The name of the service to retrieve.

        Returns:
            Any: The service instance.

        Raises:
            ServiceNotRegisteredException: If the service is not registered.
            ServiceInitializationException: If the service fails to initialize.
        """
        resolved_name = self._aliases.get(service_name, service_name)
        with self._lock:
            if resolved_name in self._singletons and self._singletons[resolved_name]:
                return self._singletons[resolved_name]

            if resolved_name in self._factories:
                try:
                    instance = self._factories[resolved_name]()
                    if asyncio.iscoroutine(instance):
                        instance = asyncio.run(instance)
                    if middleware := self._middleware.get('after_init'):
                        middleware(instance)
                    if self._lifecycle_hooks[resolved_name]['on_init']:
                        self._lifecycle_hooks[resolved_name]['on_init'](instance)
                    if resolved_name in self._singletons:
                        self._singletons[resolved_name] = instance
                    return instance
                except Exception as e:
                    raise ServiceInitializationException(f"Failed to initialize service {resolved_name}") from e

            if resolved_name in self._services:
                return self._services[resolved_name]

        raise ServiceNotRegisteredException(f"Service {service_name} not registered.")

    def inject_dependencies(self, service_class: Type) -> Any:
        """
        Injects dependencies into a service class.

        Args:
            service_class (Type): The service class.

        Returns:
            Any: The service class instance with dependencies injected.
        """
        constructor_signature = inspect.signature(service_class.__init__)
        dependencies = {
            name: self.get(param.annotation.__name__)
            for name, param in constructor_signature.parameters.items()
            if name != 'self'
        }
        return service_class(**dependencies)

    def register_health_check(self, service_name: str, health_check: Callable[[], bool]) -> None:
        """
        Registers a health check for a service.

        Args:
            service_name (str): The name of the service.
            health_check (Callable[[], bool]): The health check function.
        """
        with self._lock:
            logging.info(f"Registering health check for service: {service_name}")
            self._health_checks[service_name] = health_check

    def check_health(self, service_name: str) -> bool:
        """
        Checks the health of a specific service.

        Args:
            service_name (str): The name of the service.

        Returns:
            bool: True if the service is healthy, False otherwise.

        Raises:
            ServiceNotRegisteredException: If the health check for the service is not registered.
        """
        with self._lock:
            if service_name in self._health_checks:
                return self._health_checks[service_name]()
            raise ServiceNotRegisteredException(f"Health check for service {service_name} not registered.")

    def list_services(self) -> List[str]:
        """
        Lists all registered services.

        Returns:
            List[str]: A list of registered service names.
        """
        with self._lock:
            return list(self._services.keys())

    def get_service_metadata(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves metadata for a specific service.

        Args:
            service_name (str): The name of the service.

        Returns:
            Optional[Dict[str, Any]]: The metadata for the service, or None if not available.
        """
        with self._lock:
            return self._service_metadata.get(service_name)

    async def shutdown(self) -> None:
        """
        Shuts down all services, calling their shutdown hooks.
        """
        with self._lock:
            for service_name, hooks in self._lifecycle_hooks.items():
                if hooks['on_shutdown'] and service_name in self._singletons:
                    result = hooks['on_shutdown'](self._singletons[service_name])
                    if asyncio.iscoroutine(result):
                        await result

def check_all_services_health(registry: ServiceRegistry):
    """
    Checks the health of all registered services.

    Args:
        registry (ServiceRegistry): The service registry.
    """
    for service_name in registry.list_services():
        try:
            health_status = registry.check_health(service_name)
            logging.info(f"Health check for {service_name}: {'Healthy' if health_status else 'Unhealthy'}")
        except ServiceNotRegisteredException as e:
            logging.error(e)

async def periodic_health_check(registry: ServiceRegistry, interval: int):
    """
    Periodically checks the health of all registered services.

    Args:
        registry (ServiceRegistry): The service registry.
        interval (int): The interval in seconds between health checks.
    """
    while True:
        check_all_services_health(registry)
        await asyncio.sleep(interval)