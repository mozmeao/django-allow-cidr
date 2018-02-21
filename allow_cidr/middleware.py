from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.http.request import split_domain_port, validate_host

from netaddr import AddrFormatError, IPNetwork

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


ORIG_ALLOWED_HOSTS = []


class AllowCIDRMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        allowed_cidr_nets = getattr(settings, 'ALLOWED_CIDR_NETS', None)

        if not allowed_cidr_nets:
            raise MiddlewareNotUsed()

        self.allowed_cidr_nets = [IPNetwork(net) for net in allowed_cidr_nets]
        if settings.ALLOWED_HOSTS != ['*']:
            # add them to a global so that we keep the original setting
            # for multiple instances of the middleware.
            ORIG_ALLOWED_HOSTS.extend(settings.ALLOWED_HOSTS)
            settings.ALLOWED_HOSTS = ['*']
        elif not ORIG_ALLOWED_HOSTS:
            # ALLOWED_HOSTS was originally set to '*' so no checking is necessary
            raise MiddlewareNotUsed()

    def process_request(self, request):
        host = request.get_host()
        domain, port = split_domain_port(host)
        if domain and validate_host(domain, ORIG_ALLOWED_HOSTS):
            return None

        for net in self.allowed_cidr_nets:
            try:
                if domain in net:
                    return None
            except AddrFormatError:
                # not an IP
                break

        raise DisallowedHost("Invalid HTTP_HOST header: %r." % host)
