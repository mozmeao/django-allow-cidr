#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `django-allow-cidr` middleware.
"""

from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.test import override_settings, TestCase, RequestFactory

from allow_cidr.middleware import AllowCIDRMiddleware


class TestAllowCIDRMiddleware(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(ALLOWED_HOSTS=['thedude.abides.com', '.lebowski.biz'])
    def test_cidr_net(self):
        """Some nets are set in settings.py; Try them."""
        mw = AllowCIDRMiddleware()
        self.assertEqual(settings.ALLOWED_HOSTS, ['*'])
        req = self.rf.get('/', HTTP_HOST='192.168.1.11')
        self.assertIsNone(mw.process_request(req))
        req = self.rf.get('/', HTTP_HOST='192.168.2.200')
        self.assertIsNone(mw.process_request(req))
        req = self.rf.get('/', HTTP_HOST='192.168.2.200:8000')
        self.assertIsNone(mw.process_request(req))
        with self.assertRaises(DisallowedHost):
            req = self.rf.get('/', HTTP_HOST='192.168.3.200')
            mw.process_request(req)

    @override_settings(ALLOWED_HOSTS=['thedude.abides.com', '.lebowski.biz'])
    def test_other_hosts(self):
        """The hosts defined in ALLOWED_HOSTS should still work."""
        mw = AllowCIDRMiddleware()
        self.assertEqual(settings.ALLOWED_HOSTS, ['*'])
        req = self.rf.get('/', HTTP_HOST='thedude.abides.com')
        self.assertIsNone(mw.process_request(req))
        req = self.rf.get('/', HTTP_HOST='thebig.lebowski.biz')
        self.assertIsNone(mw.process_request(req))
        with self.assertRaises(DisallowedHost):
            req = self.rf.get('/', HTTP_HOST='donnie.net')
            mw.process_request(req)

    @override_settings(ALLOWED_HOSTS=['thedude.abides.com', '.lebowski.biz'],
                       ALLOWED_CIDR_NETS=[])
    def test_other_hosts_no_nets(self):
        """The hosts defined in ALLOWED_HOSTS should work when middleware is off."""
        with self.assertRaises(MiddlewareNotUsed):
            AllowCIDRMiddleware()
        self.assertEqual(settings.ALLOWED_HOSTS, ['thedude.abides.com', '.lebowski.biz'])
