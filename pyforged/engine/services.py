import inspect
import logging
import asyncio
from typing import Any, Callable, Dict, Type, Optional
from threading import Lock

logging.basicConfig(level=logging.INFO)


class ServiceNotRegisteredException(Exception):
    pass


class ServiceInitializationException(Exception):
    pass


class ServiceRegistry:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[..., Any]] = {}
        self._singletons: Dict[str, Any] = {}
        self._aliases: Dict[str, str] = {}
        self._lifecycle_hooks: Dict[str, Dict[str, Optional[Callable]]] = {}
        self._lock = Lock()
        self._middleware: Dict[str, Callable[[Any], Any]] = {}

    def register(self, service_name: str, instance: Any, singleton: bool = False,
                 aliases: Optional[list] = None,
                 on_init: Optional[Callable] = None, on_shutdown: Optional[Callable] = None):
        with self._lock:
            logging.info(f"Registering service: {service_name}")
            self._services[service_name] = instance
            if singleton:
                self._singletons[service_name] = instance
            self._lifecycle_hooks[service_name] = {'on_init': on_init, 'on_shutdown': on_shutdown}
            if aliases:
                for alias in aliases:
                    self._aliases[alias] = service_name

    def register_factory(self, service_name: str, factory: Callable[..., Any], singleton: bool = True,
                         aliases: Optional[list] = None,
                         on_init: Optional[Callable] = None, on_shutdown: Optional[Callable] = None):
        with self._lock:
            logging.info(f"Registering factory for service: {service_name}")
            self._factories[service_name] = factory
            if singleton:
                self._singletons[service_name] = None
            self._lifecycle_hooks[service_name] = {'on_init': on_init, 'on_shutdown': on_shutdown}
            if aliases:
                for alias in aliases:
                    self._aliases[alias] = service_name

    def middleware(self, hook_name: str, middleware_func: Callable[[Any], Any]):
        logging.info(f"Registering middleware for: {hook_name}")
        self._middleware[hook_name] = middleware_func

    def get(self, service_name: str) -> Any:
        resolved_name = self._aliases.get(service_name, service_name)
        with self._lock:
            if resolved_name in self._singletons and self._singletons[resolved_name]:
                return self._singletons[resolved_name]

            if resolved_name in self._factories:
                try:
                    instance = self._factories[resolved_name]()
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
        constructor_signature = inspect.signature(service_class.__init__)
        dependencies = {
            name: self.get(param.annotation.__name__)
            for name, param in constructor_signature.parameters.items()
            if name != 'self'
        }
        return service_class(**dependencies)

    async def shutdown(self):
        with self._lock:
            for service_name, hooks in self._lifecycle_hooks.items():
                if hooks['on_shutdown'] and service_name in self._singletons:
                    result = hooks['on_shutdown'](self._singletons[service_name])
                    if asyncio.iscoroutine(result):
                        await result


# Example Usage

class Database:
    def connect(self):
        logging.info("Connecting to the database.")

    def disconnect(self):
        logging.info("Disconnecting from the database.")


class Logger:
    def log(self, message: str):
        logging.info(f"Logger: {message}")


class UserService:
    def __init__(self, database: Database, logger: Logger):
        self.database = database
        self.logger = logger

    def create_user(self, username: str):
        self.database.connect()
        self.logger.log(f"User {username} created.")
        self.database.disconnect()


async def main():
    registry = ServiceRegistry()

    registry.register_factory("Database", Database, singleton=True,
                              on_init=lambda db: db.connect(),
                              on_shutdown=lambda db: db.disconnect())
    registry.register("Logger", Logger(), singleton=True, aliases=["ILogging"])

    user_service: UserService = registry.inject_dependencies(UserService)
    user_service.create_user("alice")

    await registry.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
