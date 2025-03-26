
import sys
import subprocess
from forged.commons.utilities import pyth

def test_get_python_version():
    assert pyth.get_python_version() == sys.version

def test_is_package_installed():
    assert pyth.is_package_installed("pip")
    assert not pyth.is_package_installed("nonexistent_package")

def test_get_installed_packages():
    packages = pyth.get_installed_packages()
    assert "pip" in packages

def test_get_package_metadata():
    metadata = pyth.get_package_metadata("pip")
    assert metadata is not None
    assert "Name" in metadata
    assert metadata["Name"] == "pip"

def test_is_version_compatible():
    assert pyth.is_version_compatible("pip", ">=20.0.0")
    assert not pyth.is_version_compatible("pip", ">=100.0.0")

def test_list_package_dependencies():
    dependencies = pyth.list_package_dependencies("pip")
    assert dependencies is not None

def test_get_outdated_packages(mocker):
    mocker.patch('subprocess.run', return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout='[]'))
    outdated_packages = pyth.get_outdated_packages()
    assert isinstance(outdated_packages, list)

def test_install_package(mocker):
    mocker.patch('subprocess.check_call', return_value=None)
    pyth.install_package("pytest")
    subprocess.check_call.assert_called_with([sys.executable, "-m", "pip", "install", "pytest"])

def test_upgrade_package(mocker):
    mocker.patch('subprocess.check_call', return_value=None)
    pyth.upgrade_package("pytest")
    subprocess.check_call.assert_called_with([sys.executable, "-m", "pip", "install", "--upgrade", "pytest"])

def test_get_package_paths():
    path = pyth.get_package_paths("pip")
    assert isinstance(path, str)

def test_uninstall_package(mocker):
    mocker.patch('subprocess.check_call', return_value=None)
    pyth.uninstall_package("pytest")
    subprocess.check_call.assert_called_with([sys.executable, "-m", "pip", "uninstall", "pytest", "-y"])

def test_is_package_up_to_date(mocker):
    mocker.patch('subprocess.run', return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout='[]'))
    assert pyth.is_package_up_to_date("pip")

def test_get_latest_package_version(mocker):
    mocker.patch('subprocess.run', return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout='LATEST: 21.0.1\n'))
    assert pyth.get_latest_package_version("pip") == "21.0.1"

def test_get_python_interpreter_path():
    assert pyth.get_python_interpreter_path() == sys.executable