# Namespaces 
###### (part of the PyForged Core)
The **namespacing** package is a powerful tool designed to manage and organize symbols within a hierarchical structure, 
known as _namespaces_. 

This package provides a flexible and efficient way to handle configuration settings, application 
state, and other key-value pairs in a structured manner. By leveraging namespaces, you can create isolated contexts for 
different parts of your application, ensuring that symbols are well-organized and easily accessible.

### Key Concepts

1. **Namespace**: A namespace is a container that holds symbols, which are key-value pairs. Namespaces can be nested, 
                  allowing for a hierarchical organization of symbols.

2. **Symbol**: A symbol represents a key-value pair within a namespace. Symbols can have additional metadata, such as tags 
               and access control lists (ACLs), to provide more context and control over their usage.

3. **Composite Namespace**: A composite namespace is a collection of multiple namespaces combined into a single logical 
                            namespace. This allows for the aggregation of symbols from different namespaces, providing a unified view.

4. **Layer**: In a composite namespace, each namespace is considered a layer. Layers can have attributes such as read-only 
              status and priority, which determine their behavior within the composite namespace. 

5. **Mounting**: Mounting allows you to attach a sub-namespace under a specific prefix within another namespace. This is 
                 useful for organizing related symbols under a common path.

6. **Decorators**: The package provides decorators to simplify the registration of symbols within namespaces. 
                   These decorators can be used to register functions, methods, and classes as symbols, making it easy to integrate with existing code.

By using the **namespacing** package, you can create a robust and scalable system for managing configuration and state in 
your application, ensuring that symbols are well-organized and easily accessible.


## Index

1. [General Usage]()
2. [Forged]()

d

## General Usage
something 

### s

```python
# Step 1: Create a Namespace
from forged.namespacing.core.namespace import Namespace
from forged.namespacing.registry.composable import CompositeNamespace

# Create individual namespaces
config_ns = Namespace("config")
db_ns = Namespace("database")

# Step 2: Register Symbols
config_ns.register("api.key", "my-secret-key")
db_ns.register("host", "localhost")
db_ns.register("port", 5432)

# Step 3: Resolve Symbols
api_key = config_ns.resolve("api.key")
db_host = db_ns.resolve("host")
db_port = db_ns.resolve("port")

print(f"API Key: {api_key}")
print(f"Database Host: {db_host}")
print(f"Database Port: {db_port}")

# Step 4: Composite Namespace
global_ns = CompositeNamespace(config_ns, db_ns)

# Resolve symbols from the composite namespace
api_key_global = global_ns.resolve("api.key")
db_host_global = global_ns.resolve("host")

print(f"API Key (Global): {api_key_global}")
print(f"Database Host (Global): {db_host_global}")

# Step 5: Mounting Namespaces
plugins_ns = Namespace("plugins")
auth_ns = Namespace("auth")
auth_ns.register("token", "auth-token")

# Mount auth namespace under plugins
global_ns.mount("plugins.auth", auth_ns)

# Resolve mounted namespace symbols
auth_token = global_ns.resolve("plugins.auth.token")
print(f"Auth Token: {auth_token}")
```

This example demonstrates how to create and use namespaces, register and resolve symbols, combine namespaces into a composite namespace, and mount sub-namespaces.

### Using the `register` Decorator

The `register` decorator is used to register symbols in a namespace. This guide will walk you through the usage of the `register` decorator, including its parameters and examples.

#### Importing the Decorator

First, ensure you import the `register` decorator from the appropriate module:

```python
from forged.namespacing.core.decorators import register
```

#### Parameters

- `path` (**Optional**[Union[**_str_**, **_List_**[str]]): The path(s) to register the symbol under. If not provided, the function or class name will be used.
- ``namespace`` (**Optional**[**_Namespace_**]): The namespace to register the symbol in. _Defaults to _default_namespace._
tags (Optional[Dict[str, Any]]): Tags to attach to the symbol.
- ``freeze`` (**_bool_**): Whether to freeze the symbol, preventing further modifications.
- ``infer_path`` (**_bool_**): Whether to infer the path from the function name.
- ``include_context`` (**_bool_**): Whether to include debug context.

#### Examples

##### Registering a Function

```Python
@register(path="my.custom.path")
def my_function():
    return "Hello, World!"
```

##### Registering a Function _with Tags_

```Python
@register(path="my.custom.path", tags={"version": "1.0", "author": "John Doe"})
def my_function():
    return "Hello, World!"
```

##### Registering a Function _with Path Inference_

```Python
@register(infer_path=True)
def my_function():
    return "Hello, World!"
```

##### Registering a Class Method

```Python
class MyClass:
    @register(path="my.class.method")
    def my_method(self):
        return "Hello from method!"
```

#### Notes
- If **path** is not provided, the function or class name will be used as the default path.
- The **namespace** parameter allows you to specify a custom namespace for registration.
- The **freeze** parameter prevents further modifications to the registered symbol.

This guide should help you effectively use the ``register`` decorator in your project.