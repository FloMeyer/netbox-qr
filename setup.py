from setuptools import find_packages, setup

setup(
    name='netbox-qr',
    version='0.1.0',
    description='A netbox plugin for generating qr codes for specific pages.',
    url='https://github.com/FloMeyer/netbox-qr',
    author='Florian Meyer',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
