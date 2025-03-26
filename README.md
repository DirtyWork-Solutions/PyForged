# PyForged
###### _[See Full Docs Here](docs/INDEX.md)_

PyForged aims to be that sweet spot between developer ergonomics and flexibility. Designed as a modular toolkit to simplify and standardize the foundational aspects of building robust, extensible software systems. It focuses on common development pain points and provides flexible, interoperable components to support core software architecture needs across different domains.

It offers six primary building blocks:


---

1. Namespaces

A flexible, implementation-agnostic system for organizing and referencing elements (like events, hooks, configs, etc.) using dot-notation (something.subthing.another). This helps create a consistent and intuitive way to manage scopes and relationships, without prescribing how data is stored or retrieved.


---

2. Events

A unified mechanism for defining and handling signals, observations, or notifications across an application. These are designed to be backend-agnostic (e.g., can use PyDispatcher, RxPy, or custom logic) and allow different components to react to changes or emit information in a loosely coupled manner.


---

3. Hooks

Extensibility points that allow users or third-party code to plug in custom behavior without modifying the core logic. These are useful for triggering custom logic at predefined points in a system’s lifecycle — a key tool for plugin architectures, customization, and inversion of control.


---

4. Reports

A lightweight reporting and logging layer, built around Loguru, providing a friendly interface for outputting logs, metrics, audits, and other diagnostics. It helps unify application reporting and makes it easy to plug into different observability tools or logging backends.


---

5. Mods

A utility system for defining, discovering, and managing modular extensions or plugins. It integrates with hooks, configs, events, and namespaces to create a smooth plugin experience. Mods support dynamic loading, dependency resolution, and declarative integration with other components of the SDK.


---

6. Configs

Built on OmegaConf, this component provides structured, hierarchical configuration management. It supports merging, overrides, environment variable integration, and more, giving the SDK and the apps using it a powerful and consistent config layer.


---

Summary

This SDK is not a framework — it's a foundational toolkit. It gives you the right abstractions and tools to build applications, libraries, or plugins with clean separation of concerns, high extensibility, and good developer ergonomics. Whether you're writing a simple CLI tool or a modular plugin-based system, this SDK helps you build smarter, not harder.


---

Want to add goals, philosophy, or examples to this description?

