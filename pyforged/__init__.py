import pkg_resources
import json

import requests

def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['info']['version']
    else:
        return None

def get_package_info(package_name):
    try:
        distribution = pkg_resources.get_distribution(package_name)
        package_info = {
            "name": distribution.project_name,
            "version": distribution.version,
            "location": distribution.location,
            "requires": [str(req) for req in distribution.requires()]
        }
        return package_info
    except pkg_resources.DistributionNotFound:
        return None

def get_all_installed_packages(include_versions=False):
    installed_packages = pkg_resources.working_set
    packages_info = {}
    for dist in installed_packages:
        if include_versions:
            packages_info[dist.project_name] = dist.version
        else:
            packages_info[dist.project_name] = None
    return packages_info

def main():
    package_name = input("Enter the package name (or leave empty to list all packages): ")
    if package_name:
        package_info = get_package_info(package_name)
        if package_info:
            print(json.dumps(package_info, indent=4))
        else:
            print(f"Package '{package_name}' is not installed.")
    else:
        include_versions = input("Include versions? (yes/no): ").strip().lower() == 'yes'
        packages_info = get_all_installed_packages(include_versions)
        print(json.dumps(packages_info, indent=4))

if __name__ == "__main__":
    main()
    print(get_all_installed_packages(True))
    print(get_latest_version("pyforged"))