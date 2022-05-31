from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'netbox_qr',
    version = '0.1.4',
    python_requires='>=3',
    license='Apache 2.0',
    description = 'A netbox plugin for generating qr codes for specific pages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Florian Meyer',
    author_email = 'flo@flomeyer.de',
    url = 'https://github.com/FloMeyer/netbox-qr',
    download_url = 'https://github.com/FloMeyer/netbox-qr/archive/refs/tags/v0.1.0.tar.gz',
    keywords = ['netbox', 'qrcode'],
    install_requires=[
            'segno',
            'Pillow<9.0.0',
            'qrcode-artistic',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
