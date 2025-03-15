import importlib.metadata
from typing import Union

from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

def is_package_installed(package_name, version=None):
    """
    Check if a particular package (optionally by version) is currently installed.

    :param package_name: Name of the package to check.
    :param version: Optional version of the package to check.
    :return: True if the package (and version, if specified) is installed, False otherwise.
    """
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


if __name__ == '__main__':
    print(get_installed_packages())  # List all installed packages
    print(get_package_metadata("requests"))  # Get metadata for 'requests' package
    print(is_version_compatible("requests", ">=2.25.0"))  # Check if 'requests' version is compatible

    # Example usage
    print(is_package_installed("requests"))  # Check if 'requests' is installed
    print(is_package_installed("requests", "2.28.1"))  # Check if 'requests' version 2.28.1 is installed