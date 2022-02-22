.. :changelog:

History
-------

0.4.0 (2022-02-22)
++++++++++++++++++

* Drop Django support for non-LTS and non-latest Django (so, removing 1.x, 2.0, 2.1, 3.0, 3.1)
* Drop support for older Python releases (2.x, 3.5)
* Add Django 4.0 to tox's test matrix
* Add Python 3.7 through 3.10 to tox's test matrix; 3.6 to 3.10 are now the only tested versions
* Switch CI to Github Actions

0.3.1 (2018-07-31)
++++++++++++++++++

* Fix issue #6: Accept passed in `get_response` function for Middleware in Django >= 1.10.
* Publish updated docs that fix the `ALLOWED_CIDR_NETS` typo.

0.3.0 (2018-02-21)
++++++++++++++++++

* Disable middleware if ALLOWED_HOSTS is set to `['*']`.

0.2.0 (2018-02-21)
++++++++++++++++++

* Handle host names with ports (Thanks Giorgos!).

0.1.0 (2018-02-16)
++++++++++++++++++

* First release on PyPI.
