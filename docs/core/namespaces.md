# Namespaces 
###### (part of the PyForged Core)
Namespaces are

### Index

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