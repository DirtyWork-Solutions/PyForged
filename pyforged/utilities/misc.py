import importlib.metadata
import importlib.util
import json
import logging
import sys
from pathlib import Path
from typing import Union, List, Dict
import subprocess
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

def is_package_installed(package_name, version=None):
    """
    Check if a particular package (optionally by version) is currently installed.

    :param package_name: Name of the package to check.
    :param version: Optional version of the package to check.
    :return: True if the package (and version, if specified) is installed, False otherwise.
    """
    logging.info(f"Checking if '{package_name}' is enabled.")
    try:
        installed_version = importlib.metadata.version(package_name)
        if version:
            return installed_version == version
        return True
    except importlib.metadata.PackageNotFoundError:
        return False



def get_installed_packages():
    """
    List all installed packages.

    :return: A list of installed package names.
    """
    return sorted([dist.metadata['Name'] for dist in importlib.metadata.distributions()])

def get_package_metadata(package_name) -> Union[dict, None]:
    """
    Retrieve metadata for a specific package.

    :param package_name: Name of the package to retrieve metadata for.
    :return: A dictionary containing the package metadata, or None if the package is not found.
    """
    try:
        metadata = importlib.metadata.metadata(package_name)
        return {key: metadata[key] for key in metadata}
    except importlib.metadata.PackageNotFoundError:
        return None

def is_version_compatible(package_name, version_spec) -> bool:
    """
    Check if the installed version of a package meets a specified version requirement.

    :param package_name: Name of the package to check.
    :param version_spec: Version specifier (e.g., '>=1.0.0').
    :return: True if the installed version meets the requirement, False otherwise.
    """
    try:
        installed_version = Version(importlib.metadata.version(package_name))
        specifier = SpecifierSet(version_spec)
        return installed_version in specifier
    except (importlib.metadata.PackageNotFoundError, InvalidVersion, InvalidSpecifier):
        return False

def list_package_dependencies(package_name: str) -> Union[List[str], None]:
    """
    List all dependencies of a specific package.

    :param package_name: Name of the package to list dependencies for.
    :return: A list of dependencies, or None if the package is not found.
    """
    try:
        metadata = importlib.metadata.metadata(package_name)
        requires = metadata.get_all('Requires-Dist', [])
        return list(requires)
    except importlib.metadata.PackageNotFoundError:
        return None

def get_outdated_packages():
    """
    Get a list of outdated packages in the current environment.

    :return: A list of dictionaries containing package name, current version, and latest version.
    """
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"], capture_output=True, text=True, check=True)
        outdated_packages = json.loads(result.stdout)
        return outdated_packages
    except subprocess.CalledProcessError as e:
        print(f"Failed to get outdated packages. Error: {e}")
        return []


def install_package(package_name, version=None):
    """
    Install a package using pip.

    :param package_name: Name of the package to install.
    :param version: Optional version of the package to install.
    :return: None
    """
    try:
        if version:
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_spec])
        logging.info(f"Package '{package_spec}' installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install package '{package_name}'. Error: {e}")


def upgrade_package(package_name):
    """
    Upgrade a package using pip.

    :param package_name: Name of the package to upgrade.
    :return: None
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
        logging.info(f"Package '{package_name}' upgraded successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to upgrade package '{package_name}'. Error: {e}")


def uninstall_package(package_name):
    """
    Uninstall a package using pip.

    :param package_name: Name of the package to uninstall.
    :return: None
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package_name, "-y"])
        print(f"Package '{package_name}' uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to uninstall package '{package_name}'. Error: {e}")


def get_package_paths(package_names: Union[str, List[str]]) -> Union[str, Dict[str, str]]:
    """
    Get the installation path(s) for one or multiple packages.

    :param package_names: A single package name or a list of package names.
    :return: A single path if a single package name is provided, or a dictionary with package names as keys and their paths as values if a list is provided.
    """
    def get_path(package_name: str) -> str:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return f"Package '{package_name}' not found."
        return str(Path(spec.origin).parent)

    if isinstance(package_names, str):
        return get_path(package_names)
    elif isinstance(package_names, list):
        return {package_name: get_path(package_name) for package_name in package_names}
    else:
        raise TypeError("package_names must be a string or a list of strings")


if __name__ == '__main__':
    print(get_installed_packages())  # List all installed packages
    print(get_package_metadata("requests"))  # Get metadata for 'requests' package
    print(is_version_compatible("requests", ">=2.25.0"))  # Check if 'requests' version is compatible

    # Dependency checking
    dependencies = list_package_dependencies("requests")
    if dependencies is not None:
        print(f"Dependencies for 'requests': {dependencies}")
    else:
        print("Package 'requests' not found.")


    # Outdated Checks
    outdated_packages = get_outdated_packages()
    if outdated_packages:
        print("Outdated packages:")
        for pkg in outdated_packages:
            print(f"{pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
    else:
        print("All packages are up to date.")

    # Example usage
    print(is_package_installed("requests"))  # Check if 'requests' is installed
    print(is_package_installed("requests", "2.28.1"))  # Check if 'requests' version 2.28.1 is installed

    # Get path
    print(get_package_paths("numpy"))  # Single package
    print(get_package_paths(["numpy", "requests", "nonexistent_package"]))  # Multiple packages
