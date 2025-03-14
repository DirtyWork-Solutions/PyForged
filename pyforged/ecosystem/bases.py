import os
import json
from pathlib import Path
import importlib.metadata


class PyForgeProjectRegistry:
    REGISTRY_FILE = Path.home() / ".native.json"

    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        if self.REGISTRY_FILE.exists():
            with open(self.REGISTRY_FILE, "r") as f:
                self.registry = json.load(f)
        else:
            self.registry = {}

    def _save_registry(self):
        with open(self.REGISTRY_FILE, "w") as f:
            json.dump(self.registry, f, indent=4)

    def register_project(self, project_name, project_path, version="1.0.0", dependencies=None, project_type="default",
                         interoperability=None):
        """
        Registers a new PyForge project with metadata, including dependencies and interoperability.
        """
        project_id = os.path.basename(project_path)
        self.registry[project_id] = {
            "name": project_name,
            "path": str(Path(project_path).resolve()),
            "version": version,
            "dependencies": dependencies or {},
            "project_type": project_type,
            "interoperability": interoperability or {}
        }
        self._save_registry()
        return f"Project '{project_name}' registered successfully."

    def list_projects(self):
        """Lists all registered PyForge projects."""
        return self.registry

    def get_project(self, project_id):
        """Retrieves metadata for a specific project."""
        return self.registry.get(project_id, "Project not found.")

    def check_dependencies(self, project_id):
        """Checks and validates dependencies for a given project."""
        project = self.registry.get(project_id)
        if not project:
            return "Project not found."

        dependencies = project.get("dependencies", {})
        missing_deps = {dep: ver for dep, ver in dependencies.items() if not self._is_dependency_installed(dep, ver)}

        if missing_deps:
            return {"status": "Missing dependencies", "details": missing_deps}
        return {"status": "All dependencies satisfied"}

    def _is_dependency_installed(self, package_name, required_version):
        """Checks if a specific package is installed and matches the required version using importlib.metadata."""
        try:
            installed_version = importlib.metadata.version(package_name)
            return installed_version == required_version
        except importlib.metadata.PackageNotFoundError:
            return False

    def remove_project(self, project_id):
        """Removes a project from the registry."""
        if project_id in self.registry:
            del self.registry[project_id]
            self._save_registry()
            return f"Project '{project_id}' removed."
        return "Project not found."


# Example Usage
if __name__ == "__main__":
    registry = PyForgeProjectRegistry()
    print(registry.register_project("MyPyForgeApp",
                                    "./my_project",
                                    dependencies={"PyExtend": "1.2.3"},
                                    interoperability={"PySync": "enabled"}))
    print(registry.list_projects())
    print(registry.get_project("my_project"))
    print(registry.check_dependencies("my_project"))
    print(registry.remove_project("my_project"))
