"""
Tests for `django-allow-cidr` middleware.
"""
from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.test import RequestFactory, TestCase, override_settings

from allow_cidr import middleware


def _fake_get_response(*args, **kwards):
    pass


class TestAllowCIDRMiddleware(TestCase):
    def setUp(self):
        middleware.ORIG_ALLOWED_HOSTS = []
        self.rf = RequestFactory()

    def _get_middleware(self):
        return middleware.AllowCIDRMiddleware(get_response=_fake_get_response)

    @override_settings(ALLOWED_HOSTS=["thedude.abides.com", ".lebowski.biz"])
    def test_cidr_net(self):
        """Some nets are set in settings.py; Try them."""
        mw = self._get_middleware()
        self.assertEqual(settings.ALLOWED_HOSTS, ["*"])
        req = self.rf.get("/", HTTP_HOST="192.168.1.11")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="192.168.2.200")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="192.168.2.200:8000")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="[2001:db8:0:1::11]")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="[2001:db8:0:2::200]")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="[2001:db8:0:2::200]:8000")
        self.assertIsNone(mw(req))
        with self.assertRaises(DisallowedHost):
            req = self.rf.get("/", HTTP_HOST="192.168.3.200")
            mw(req)
        with self.assertRaises(DisallowedHost):
            req = self.rf.get("/", HTTP_HOST="[2001:db8:0:3::200]")
            mw(req)

    @override_settings(ALLOWED_HOSTS=["thedude.abides.com", ".lebowski.biz"])
    def test_other_hosts(self):
        """The hosts defined in ALLOWED_HOSTS should still work."""
        mw = self._get_middleware()
        self.assertEqual(settings.ALLOWED_HOSTS, ["*"])
        req = self.rf.get("/", HTTP_HOST="thedude.abides.com")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="thebig.lebowski.biz")
        self.assertIsNone(mw(req))
        req = self.rf.get("/", HTTP_HOST="thebig.lebowski.biz:8000")
        self.assertIsNone(mw(req))
        with self.assertRaises(DisallowedHost):
            req = self.rf.get("/", HTTP_HOST="donnie.net")
            mw(req)

    @override_settings(
        ALLOWED_HOSTS=["thedude.abides.com", ".lebowski.biz"], ALLOWED_CIDR_NETS=[]
    )
    def test_other_hosts_no_nets(self):
        """The hosts defined in ALLOWED_HOSTS should work when middleware is off."""
        with self.assertRaises(MiddlewareNotUsed):
            middleware.AllowCIDRMiddleware(get_response=_fake_get_response)
        self.assertEqual(
            settings.ALLOWED_HOSTS, ["thedude.abides.com", ".lebowski.biz"]
        )

    @override_settings(ALLOWED_HOSTS=["*"], ALLOWED_CIDR_NETS=["192.168.1.1"])
    def test_hosts_star_disable(self):
        """The middleware should deactivate if ALLOWED_HOSTS is '*'"""
        with self.assertRaises(MiddlewareNotUsed):
            middleware.AllowCIDRMiddleware(get_response=_fake_get_response)
        self.assertEqual(settings.ALLOWED_HOSTS, ["*"])
