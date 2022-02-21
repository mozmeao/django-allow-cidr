=============================
Django Allow CIDR
=============================

.. image:: https://badge.fury.io/py/django-allow-cidr.svg
    :target: https://badge.fury.io/py/django-allow-cidr

.. image:: https://github.com/mozmeao/django-allow-cidr/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/mozmeao/django-allow-cidr/actions


A Django Middleware to enable use of CIDR IP ranges in ALLOWED_HOSTS.

Quickstart
----------

Install Django Allow CIDR::

    pip install django-allow-cidr

Add the Middleware to your ``MIDDLEWARE`` settings. It should be the first in the list:

.. code-block:: python

    MIDDLEWARE = (
        'allow_cidr.middleware.AllowCIDRMiddleware',
        ...
    )

Add the ``ALLOWED_CIDR_NETS`` setting:

.. code-block:: python

    ALLOWED_CIDR_NETS = ['192.168.1.0/24']

Profit!

Features
--------

* The normal ``ALLOWED_HOSTS`` values will also work as intended. This Middleware is intended to augment,
  not replace, the normal Django function.
* If you do define ``ALLOWED_CIDR_NETS`` and it has values, the middleware will capture what you have in `ALLOWED_HOSTS`,
  set ``ALLOWED_HOSTS`` to `['*']` and take over validation of host headers.
* The ``ALLOWED_CIDR_NETS`` values can be any valid network definition for the `netaddr`_ package.

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
