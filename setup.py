#!/usr/bin/env python
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from allow_cidr/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("allow_cidr", "__init__.py")

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="django-allow-cidr",
    version=version,
    description="""A Django Middleware to enable use of CIDR IP ranges in ALLOWED_HOSTS.""",
    long_description=readme + "\n\n" + history,
    author="Paul McLanahan",
    author_email="pmac@mozilla.com",
    url="https://github.com/mozmeao/django-allow-cidr",
    packages=[
        "allow_cidr",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
    ],
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords="django-allow-cidr",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
