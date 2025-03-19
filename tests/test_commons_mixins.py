import unittest
import json
import yaml
import os
from pyforged.commons.patterns.mixins import JSONSerializedBasic, YAMLSerializedBasic, SerializedMixin, BasicSingleton, ObservableMixin, ReprMixin

class TestMixins(unittest.TestCase):

    def setUp(self):
        self.file_path = "test_file.json"

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_json_serialization(self):
        class TestClass(JSONSerializedBasic):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

        obj = TestClass("value1", 123)
        json_str = obj.to_json()
        self.assertEqual(json.loads(json_str), {"attr1": "value1", "attr2": 123})

        new_obj = TestClass.from_json(json_str)
        self.assertEqual(new_obj.attr1, "value1")
        self.assertEqual(new_obj.attr2, 123)

    def test_yaml_serialization(self):
        class TestClass(YAMLSerializedBasic):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

        obj = TestClass("value1", 123)
        yaml_str = obj.to_yaml()
        self.assertEqual(yaml.safe_load(yaml_str), {"attr1": "value1", "attr2": 123})

        new_obj = TestClass.from_yaml(yaml_str)
        self.assertEqual(new_obj.attr1, "value1")
        self.assertEqual(new_obj.attr2, 123)

    def test_serialized_mixin(self):
        class TestClass(SerializedMixin):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

        obj = TestClass("value1", 123)
        obj.serialize_to_file(self.file_path, format='json')
        new_obj = TestClass.deserialize_from_file(self.file_path, format='json')
        self.assertEqual(new_obj.attr1, "value1")
        self.assertEqual(new_obj.attr2, 123)

    def test_singleton(self):
        class TestClass(BasicSingleton):
            pass

        obj1 = TestClass()
        obj2 = TestClass()
        self.assertIs(obj1, obj2)

    def test_observable(self):
        class TestObserver:
            def __init__(self):
                self.updated = False
                self.args = None
                self.kwargs = None

            def update(self, *args, **kwargs):
                self.updated = True
                self.args = args
                self.kwargs = kwargs

        class TestClass(ObservableMixin):
            pass

        obj = TestClass()
        observer = TestObserver()
        obj.add_observer(observer)
        obj.notify_observers("arg1", key="value")
        self.assertTrue(observer.updated)
        self.assertEqual(observer.args, ("arg1",))
        self.assertEqual(observer.kwargs, {"key": "value"})

    def test_repr_mixin(self):
        class TestClass(ReprMixin):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

        obj = TestClass("value1", 123)
        self.assertEqual(repr(obj), "TestClass(attr1='value1', attr2=123)")

if __name__ == '__main__':
    unittest.main()