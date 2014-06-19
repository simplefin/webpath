# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from twisted.trial.unittest import TestCase
from twisted.internet import defer

from mock import MagicMock


from webpath import http
from webpath.runner import Context


class httpTest(TestCase):


    @defer.inlineCallbacks
    def test_request(self):
        """
        You can make HTTP requests using the requests api.
        """
        fake = MagicMock()
        fake.request.return_value = 'foo'
        context = Context()
        context.requests = fake
        result = yield http.request({
            'action': 'http',
            'kwargs': {
                'method': 'get',
            },
        }, context)
        fake.request.assert_called_once_with(**{'method': 'get'})
        self.assertEqual(result, 'foo', "Should return result of request()")


    @defer.inlineCallbacks
    def test_request_async(self):
        """
        The request should be asynchronous.
        """
        fake = MagicMock()
        fake.request.return_value = 'foo'
        context = Context()
        context.requests = fake
        d = http.request({
            'action': 'http',
            'kwargs': {
                'method': 'get',
            },
        }, context)
        self.assertFalse(d.called, "Should not be done yet")
        result = yield d
        self.assertEqual(result, 'foo', "Should return result of request()")

