# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from twisted.internet import threads
from lxml.html import fromstring, tostring



def request(params, context):
    """
    Make an HTTP request.
    """
    requests = context.requests
    return threads.deferToThread(requests.request, **params['kwargs'])


def getForms(params, context):
    """
    Extract all forms from html.
    """
    x = fromstring(params['html'])
    forms = x.forms
    ret = []
    for form in forms:
        ret.append({
            'html': tostring(form),
            'form': form.attrib,
            'data': dict(form.fields),
        })
    return ret