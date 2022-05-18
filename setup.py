from setuptools import setup, find_namespace_packages

setup(
    name="HAP-python-modernforms",
    version='1.0.0',
    description='',
    packages=find_namespace_packages(include=['pyhap.*']),
    include_package_data=False,
    install_requires=['HAP-python[QRCode]', 'requests']
)
