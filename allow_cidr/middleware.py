from distutils.version import StrictVersion

import django
from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.http.request import split_domain_port, validate_host
from netaddr import AddrFormatError, IPNetwork

ORIG_ALLOWED_HOSTS = []


class AllowCIDRMiddleware:
    def __init__(self, get_response, *args, **kwargs):

        self.get_response = get_response

        if StrictVersion(django.get_version()) < StrictVersion("2.2"):
            raise NotImplementedError(
                "This version of django-allow-cidr requires at least Django 2.2"
            )

        super(AllowCIDRMiddleware, self).__init__(*args, **kwargs)

        allowed_cidr_nets = getattr(settings, "ALLOWED_CIDR_NETS", None)

        if not allowed_cidr_nets:
            raise MiddlewareNotUsed()

        self.allowed_cidr_nets = [IPNetwork(net) for net in allowed_cidr_nets]
        if settings.ALLOWED_HOSTS != ["*"]:
            # add them to a global so that we keep the original setting
            # for multiple instances of the middleware.
            ORIG_ALLOWED_HOSTS.extend(settings.ALLOWED_HOSTS)
            settings.ALLOWED_HOSTS = ["*"]
        elif not ORIG_ALLOWED_HOSTS:
            # ALLOWED_HOSTS was originally set to '*' so no checking is necessary
            raise MiddlewareNotUsed()

    def __call__(self, request):
        # Processing the request before we generate the response
        host = request.get_host()
        domain, port = split_domain_port(host)

        if not domain or not validate_host(domain, ORIG_ALLOWED_HOSTS):
            should_raise = True
            for net in self.allowed_cidr_nets:
                try:
                    if domain in net:
                        should_raise = False
                        break
                except AddrFormatError:
                    # not an IP
                    break

            if should_raise:
                raise DisallowedHost("Invalid HTTP_HOST header: %r." % host)

        response = self.get_response(request)

        return response
