import unittest
from pyforged.services import ServiceRegistry, ServiceNotRegisteredException, ServiceInitializationException

class TestServiceRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = ServiceRegistry()

    def test_register_and_get_service(self):
        service_name = "test_service"
        service_instance = object()
        self.registry.register(service_name, service_instance)
        self.assertEqual(self.registry.get(service_name), service_instance)

    def test_register_and_get_singleton_service(self):
        service_name = "singleton_service"
        service_instance = object()
        self.registry.register(service_name, service_instance, singleton=True)
        self.assertEqual(self.registry.get(service_name), service_instance)

    def test_register_factory_and_get_service(self):
        service_name = "factory_service"
        service_instance = object()
        factory = lambda: service_instance
        self.registry.register_factory(service_name, factory)
        self.assertEqual(self.registry.get(service_name), service_instance)

    def test_service_not_registered_exception(self):
        with self.assertRaises(ServiceNotRegisteredException):
            self.registry.get("non_existent_service")

    def test_service_initialization_exception(self):
        service_name = "faulty_service"
        factory = lambda: (_ for _ in ()).throw(Exception("Initialization failed"))
        self.registry.register_factory(service_name, factory)
        with self.assertRaises(ServiceInitializationException):
            self.registry.get(service_name)

    def test_middleware(self):
        service_name = "middleware_service"
        service_instance = object()
        self.registry.register(service_name, service_instance)

        def before_access_middleware(service_name):
            self.assertEqual(service_name, "middleware_service")

        self.registry.middleware('before_service_access', before_access_middleware)
        self.registry.get(service_name)

    def test_health_check(self):
        service_name = "health_service"
        service_instance = object()
        self.registry.register(service_name, service_instance)
        self.registry._health_checks[service_name] = lambda: True
        self.assertTrue(self.registry.check_health(service_name))

    def test_health_check_not_registered_exception(self):
        with self.assertRaises(ServiceNotRegisteredException):
            self.registry.check_health("non_existent_service")

if __name__ == '__main__':
    unittest.main()