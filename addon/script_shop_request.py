


"""
mitmdump -s addon/script_request.py -v alert
"""


import sys
import collections
import random
from enum import Enum
import requests
import logging
import json
import mitmproxy
from mitmproxy import http
from mitmproxy import ctx
from mitmproxy.exceptions import TlsProtocolException
from mitmproxy.proxy.protocol import TlsLayer, RawTCPLayer

class Listener:

    def request(self,flow: http.HTTPFlow):
        """
        拦截请求数据
        :param flow:
        :return:
        """

        ctx.log.alert(flow.request.url)

        if "igetcool-share.igetcool.com" in flow.request.url in flow.request.url:

            ctx.log.alert("http_request ====>")

            ctx.log.info(flow.request.url)

            ctx.log.alert(flow.request.scheme)

            flow.request.scheme = "http"

            flow.request.port = 80

            flow.request.host = "shopapi.igetcool.com"

            flow.request.headers["source "] = "test"

            ctx.log.alert("<==== http_request")




    def response(self,flow:http.HTTPFlow):
        """
        拦截返回结果
        :param flow:
        :return:
        """

        if "app-api-common-server" in flow.request.url or "app-api-course-server" in flow.request.url:

            ctx.log.alert("http_response ====>")

            url_path = flow.request.path

            ctx.log.alert(flow.request.url)

            ctx.log.alert(url_path)

            # ctx.log.alert(flow.response.text)

            ctx.log.alert("<==== http_response")




addons=[
    Listener()
]


class InterceptionResult(Enum):
    success = True
    failure = False
    skipped = None

class _TlsStrategy:
    """
    Abstract base class for interception strategies.
    """

    def __init__(self):
        # A server_address -> interception results mapping
        self.history = collections.defaultdict(lambda: collections.deque(maxlen=500))

    def should_intercept(self, server_address):
        """
        Returns:
            True, if we should attempt to intercept the connection.
            False, if we want to employ pass-through instead.
        """
        raise NotImplementedError()

    def record_success(self, server_address):
        self.history[server_address].append(InterceptionResult.success)

    def record_failure(self, server_address):
        self.history[server_address].append(InterceptionResult.failure)

    def record_skipped(self, server_address):
        self.history[server_address].append(InterceptionResult.skipped)


class ConservativeStrategy(_TlsStrategy):
    """
    Conservative Interception Strategy - only intercept if there haven't been any failed attempts
    in the history.
    """

    def should_intercept(self, server_address):
        if InterceptionResult.failure in self.history[server_address]:
            return False
        return True


class ProbabilisticStrategy(_TlsStrategy):
    """
    Fixed probability that we intercept a given connection.
    """

    def __init__(self, p):
        self.p = p
        super(ProbabilisticStrategy, self).__init__()

    def should_intercept(self, server_address):
        return random.uniform(0, 1) < self.p


class TlsFeedback(TlsLayer):
    """
    Monkey-patch _establish_tls_with_client to get feedback if TLS could be established
    successfully on the client connection (which may fail due to cert pinning).
    """

    def _establish_tls_with_client(self):
        server_address = self.server_conn.address

        try:
            super(TlsFeedback, self)._establish_tls_with_client()
        except TlsProtocolException as e:
            tls_strategy.record_failure(server_address)
            raise e
        else:
            tls_strategy.record_success(server_address)


# inline script hooks below.

tls_strategy = None


def load(l):
    l.add_option(
        "tlsstrat", int, 0, "TLS passthrough strategy (0-100)",
    )


def configure(updated):


    global tls_strategy
    if ctx.options.tlsstrat > 0:
        tls_strategy = ProbabilisticStrategy(float(ctx.options.tlsstrat) / 100.0)
    else:
        tls_strategy = ConservativeStrategy()


def next_layer(next_layer):
    """
    This hook does the actual magic - if the next layer is planned to be a TLS layer,
    we check if we want to enter pass-through mode instead.
    """
    if isinstance(next_layer, TlsLayer) and next_layer._client_tls:
        server_address = next_layer.server_conn.address

        if tls_strategy.should_intercept(server_address):
            # We try to intercept.
            # Monkey-Patch the layer to get feedback from the TLSLayer if interception worked.
            next_layer.__class__ = TlsFeedback
        else:
            # We don't intercept - reply with a pass-through layer and add a "skipped" entry.
            mitmproxy.ctx.log("TLS passthrough for %s" % repr(next_layer.server_conn.address), "info")
            next_layer_replacement = RawTCPLayer(next_layer.ctx, ignore=True)
            next_layer.reply.send(next_layer_replacement)
            tls_strategy.record_skipped(server_address)