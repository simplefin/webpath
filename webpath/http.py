# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from twisted.internet import threads


def request(params, context):
    """
    Make an HTTP request.
    """
    requests = context.requests
    return threads.deferToThread(requests.request, **params['kwargs'])