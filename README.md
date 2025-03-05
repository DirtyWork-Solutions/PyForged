# ⚒️ PyForged

A modular Python ecosystem, comprised of a suite of separate but interoperable packages designed to accelerate deployment.
### 🔹 Key Features

#### ✅ Modularity & Extensibility
Packages work independently or together.
Extend functionality with plugins, hooks, and dynamic loading.
Flexible configuration options (file-based, DB-backed, in-memory).


## The Ecosystem

The ecosystem is available altogether or 

### Projects under the PyForged umbrella

| Project Name          | Description                                                                                                   | Pain Point(s)                                                                                      | Status                         |
|-----------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|--------------------------------|
| **PyForged** 🔥       | The very core for the ecosystem. All elements can be installed with: <br/><br/> *pip install pyforged[suite]* | N/A                                                                                                | **Alpha** </br> - v*0.2.0*     | 
| **Bedrocked** 🪨      | Foundation library offering essential utilities for configuration, logging, error handling, and more.         | Inconsistent configurations, poor logging standards, lack of reusable utility functions            | **Alpha** </br> - v*0.1.0*     | 
| **RuneCaller** 🀄     | Flexible framework for event management, hooks, and dynamic plugin systems.                                   | Lack of structured event handling, limited extensibility, poor observability of dynamic processes. | **Alpha** </br> - v*0.1.0*     |
| **WardKeeper** 🔑     | Security and access control framework handling authentication, authorization, and policy enforcement.         | Fragmented security implementations, inconsistent access controls, limited integration options.	   | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **EssenceBinder** 🖇️ | Abstraction, interaction, and management of anything and everything.                                          | Ad-hoc data models, poor lifecycle management, fragile interfaces between components.              | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **Concordance** ✈️    | Distributed synchronization and data consistency management across processes and systems.                     | Data drift across services, lack of real-time sync, high operational complexity.                   | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **FlowSculptor** 🔀   | Workflow orchestration and process automation system for defining and managing complex workflows.             | Manual processes, brittle automation, poor visibility into multi-step processes.                   | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **HexCrafter** 🪄     | Automation & Intelligent Actions.  	                                                                          |                                                                                                    | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **WatchTowered** 📊   | Real-time monitoring, performance metrics collection, and analytics aggregation.                              | Fragmented monitoring, reactive issue detection, no unified performance view.	                     | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **VaultKeeper** 🗄️	  | Data storage abstraction layer providing flexible storage management across databases, files, and services.   | Inconsistent data access, limited portability across storage backends, redundant integration code	 | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **CovenantLedger** 📖 | Audit logging, compliance tracking, and regulatory reporting framework for full traceability.                 | Missing audit trails, compliance gaps, difficult regulatory reporting.                             | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |
| **ChimeBringer** 📣   | Centralized messaging and notification delivery system with extensible channels and formats.                  | Notification silos, lack of centralized message management, poor multi-channel support             | 🔐 *CLOSED ALPHA PRODUCTION* ❌ |

. 

--------------------------------------------

## Installation

To install the entire suite, use the following command:

```sh
pip install pyforged[suite]
```

To install individual packages, use:

```sh
pip install pyforged[package_name]
```

Replace package_name with the desired package, e.g., bedrocked, runecaller, etc.

### Installation Mixes

*PyForged* is available with purposefully utile and or interoperable combinations of the ecosystems packages, shown below, that are installed just as demonstrated above after replacing '_suite_' with the name of the mix.


#### Available Installation Mixes

| Package // Mix     | suite | std |   |   |   |          | | 
|--------------------|-------|-----|---|---|---|----------|-|
| **Bedrocked**      | ❎     | ❎   | ❎ | ❎ | ❌ | 
| **RuneCaller**     | ❎     | ❎   |   |   |   |          |
| **WardKeeper**     | ❎     | ❎   |   |   |   |          |
| **EssenceBinder**  | ❎     |     |   |   |   |          |
| **Concordance**    | ❎     |     |   |   |   |          |
| **HexCrafter**     | ❎     |     |   |   |   |          |
| **CovenantLedger** | ❎     |     |   |   |   |          |
.

--------------------------------------------

## Usage



You can find the **_[full docs here](docs/INDEX.md)_**.

--------------------------------------------

## The Project

The package not the ecosystem.

### Contributing
We welcome contributions! Please read our Contributing Guidelines for more details.  

### License
This project is licensed under the MIT License - see the [LICENSE file](LICENSE.md) for details.

### Acknowledgments
Thanks to all contributors and maintainers.
Special thanks to the open-source community