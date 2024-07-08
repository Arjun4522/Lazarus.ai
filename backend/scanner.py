import nbformat
import re
import pkg_resources
import sys
import requests
import json

def extract_dependencies_from_notebook(notebook_path):
    """
    Extract dependencies from a Jupyter notebook, including versions if specified.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    dependencies = {}
    pip_pattern = re.compile(r'!pip install ([a-zA-Z0-9\-_\.\[\]]+)(==[0-9\.]+)?')
    import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)')

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            for line in cell['source'].split('\n'):
                pip_match = pip_pattern.search(line)
                import_match = import_pattern.search(line)
                if pip_match:
                    package = pip_match.group(1)
                    version = pip_match.group(2)
                    if version:
                        dependencies[package] = version.lstrip('==')
                    else:
                        dependencies[package] = None
                elif import_match:
                    module_name = import_match.group(1).split('.')[0]
                    dependencies[module_name] = None
    
    # Try to get versions for packages without versions using pkg_resources
    stdlib_modules = set(sys.builtin_module_names)
    for package in list(dependencies):
        if dependencies[package] is None and package not in stdlib_modules:
            try:
                version = pkg_resources.get_distribution(package).version
                dependencies[package] = version
            except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                dependencies[package] = "version not found"
            except pkg_resources.extern.packaging.requirements.InvalidRequirement:
                del dependencies[package]
    
    return dependencies

def get_latest_version_from_pypi(package_name):
    """
    Get the latest version of a package from PyPI.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.RequestException:
        return "version not found"

def handle_missing_versions(dependencies):
    """
    Handle dependencies with missing versions by searching PyPI for the latest version.
    """
    for package, version in dependencies.items():
        if version == "version not found":
            latest_version = get_latest_version_from_pypi(package)
            dependencies[package] = latest_version
    return dependencies

def save_dependencies_to_json(dependencies, output_file):
    """
    Save dependencies to a JSON file.
    """
    with open(output_file, 'w') as f:
        json.dump(dependencies, f, indent=4)

# Example usage
notebook_path = 'test.ipynb'
dependencies = extract_dependencies_from_notebook(notebook_path)
dependencies = handle_missing_versions(dependencies)
print("Final dependencies with versions:", dependencies)

# Specify the output file path
output_file = 'dependencies.json'

# Save dependencies to JSON file
save_dependencies_to_json(dependencies, output_file)
print(f"Dependencies saved to {output_file}")
