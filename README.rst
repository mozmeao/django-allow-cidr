=============================
Django Allow CIDR
=============================

.. image:: https://badge.fury.io/py/django-allow-cidr.svg
    :target: https://badge.fury.io/py/django-allow-cidr

.. image:: https://travis-ci.org/mozmeao/django-allow-cidr.svg?branch=master
    :target: https://travis-ci.org/mozmeao/django-allow-cidr

A Django Middleware to enalbe use of CIDR IP ranges in ALLOWED_HOSTS.

Documentation
-------------

The full documentation is at https://django-allow-cidr.readthedocs.io.

Quickstart
----------

Install Django Allow CIDR::

    pip install django-allow-cidr

Add the Middleware to your `MIDDLEWARE_CLASSES` (for Django < 1.10) or `MIDDLEWARE` settings.
It should be the first in the list:

.. code-block:: python

    MIDDLEWARE = (
        'allow_cidr.middleware.AllowCIDRMiddleware',
        ...
    )

Add the `ALLOW_CIDR_NETS` setting:

.. code-block:: python

    ALLOW_CIDR_NETS = ['192.168.1.0/24']

Profit!

Features
--------

* The normal `ALLOWED_HOSTS` values will also work as intended. This Middleware is intended to augment,
  not replace, the normal Django function.
* If you do define `ALLOW_CIDR_NETS` and it has values, the middleware will capture what you have in `ALLOWED_HOSTS`,
  set `ALLOWED_HOSTS` to `['*']` and take over validation of host headers.
* The `ALLOW_CIDR_NETS` values can be any valid network definition for the `netaddr`_ package.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _netaddr: https://netaddr.readthedocs.io/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
