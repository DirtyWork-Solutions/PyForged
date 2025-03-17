import unittest
from pyforged.metaspaces import MetaManager

class TestMetaManager(unittest.TestCase):

    def setUp(self):
        self.meta_manager = MetaManager()

    def test_set_and_get_identity(self):
        identity = "test_identity"
        self.meta_manager.set_identity(identity)
        self.assertEqual(self.meta_manager.get_identity(), identity)

    def test_set_and_get_runtime_context(self):
        key = "test_key"
        value = "test_value"
        self.meta_manager.set_runtime_context(key, value)
        self.assertEqual(self.meta_manager.get_runtime_context(key), value)

    def test_add_and_get_dependency(self):
        name = "test_dependency"
        dependency = object()
        self.meta_manager.add_dependency(name, dependency)
        self.assertEqual(self.meta_manager.get_dependency(name), dependency)

    def test_enable_and_disable_feature_flag(self):
        flag = "test_flag"
        self.meta_manager.enable_feature_flag(flag)
        self.assertTrue(self.meta_manager.is_feature_flag_enabled(flag))
        self.meta_manager.disable_feature_flag(flag)
        self.assertFalse(self.meta_manager.is_feature_flag_enabled(flag))

    def test_save_and_load_metadata(self):
        file_path = "test_metadata.json"
        self.meta_manager.set_runtime_context("key1", "value1")
        self.meta_manager.save_metadata(file_path)
        self.meta_manager.set_runtime_context("key1", "value2")
        self.meta_manager.load_metadata(file_path)
        self.assertEqual(self.meta_manager.get_runtime_context("key1"), "value1")

    def test_set_event_hook(self):
        def on_set_identity(identity):
            self.assertEqual(identity, "hooked_identity")

        self.meta_manager.set_event_hook('on_set_identity', on_set_identity)
        self.meta_manager.set_identity("hooked_identity")

if __name__ == '__main__':
    unittest.main()