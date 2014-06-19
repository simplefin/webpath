# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from twisted.trial.unittest import TestCase
from twisted.internet import defer


from webpath.runner import Runner, Context, basicRunner, interpolate



class RunnerTest(TestCase):


    @defer.inlineCallbacks
    def test_registerHandler(self):
        """
        You can register a function to be run for a particular action.
        """
        called = []
        def handle(params, context):
            called.append(params)
            called.append(context)
            return 'something'

        runner = Runner()
        runner.registerHandler('smirk', handle)
        
        context = Context()
        params = {'foo': 'bar'}
        result = yield runner.runSingleAction('smirk', params, context)

        self.assertEqual(called, [params, context], "Should have run the "
                         "function.")
        self.assertEqual(result, 'something', "Should return the result of the"
                         " last function.")


    @defer.inlineCallbacks
    def test_registerHandlers(self):
        """
        You can register more than one handler at a time.
        """
        runner = Runner()
        runner.registerHandlers({
            'func': lambda *a,**kw: 'func',
        })
        result = yield runner.runSingleAction('func', {}, Context())
        self.assertEqual(result, 'func')


    @defer.inlineCallbacks
    def test_runSingleAction(self):
        """
        Running a single action should store the result in the context.
        """
        runner = Runner({
            'open': lambda *a,**kw: 'hello',
        })
        context = Context()

        result = yield runner.runSingleAction('open', {}, context)
        self.assertEqual(context.runner, runner, "Should set the runner")
        self.assertEqual(context.variables['_'], 'hello')
        self.assertEqual(context.results, ['hello'])
        self.assertEqual(result, 'hello')


    @defer.inlineCallbacks
    def test_runActions(self):
        """
        You can run a set of actions.
        """
        runner = Runner({
            'speak': lambda params,context: 'hi',
            'emphasize': lambda params,context: context.variables['_'] + '!',
            'yell': lambda params,context: context.variables['_'].upper(),
        })
        context = Context()

        result = yield runner.runActions([
            {'action': 'speak'},
            {'action': 'yell'},
            {'action': 'emphasize'},
        ], context)
        self.assertEqual(result, 'HI!')
        self.assertEqual(context.variables['_'], result)
        self.assertEqual(context.results, ['hi', 'HI', 'HI!'])


    def test_runActions_Deferred(self):
        """
        Functions can return deferred results but don't have to.
        """
        d = defer.Deferred()
        runner = Runner({
            'speak': lambda params,context: 'hi',
            'gummy': lambda params,context: d,
            'yell': lambda params,context: defer.succeed(context.variables['_'].upper()),
        })
        context = Context()

        result = runner.runActions([
            {'action': 'speak'},
            {'action': 'gummy'},
            {'action': 'yell'},
        ], context)
        self.assertFalse(result.called, "Should not have finished yet")
        d.callback('gummy bear')
        result = self.successResultOf(result)
        self.assertEqual(result, 'GUMMY BEAR')
        self.assertEqual(context.variables['_'], result)
        self.assertEqual(context.results, ['hi', 'gummy bear', 'GUMMY BEAR'])



class basicRunnerTest(TestCase):


    @defer.inlineCallbacks
    def test_loop(self):
        """
        You can loop over a list of things
        """
        called = []
        def func(params, context):
            called.append(params['arg'])
            return 'hey, ' + params['arg']

        runner = basicRunner({'func': func})
        context = Context()
        
        result = yield runner.runSingleAction('loop', {
                'action': 'loop',
                'iterable': ['jim', 'john', 'joe'],
                'actions': [
                    {'action': 'func', 'arg': '$item'},
                ],
            }, context)
        self.assertEqual(result, 'hey, joe', "Should return last result")
        self.assertEqual(called, ['jim', 'john', 'joe'],
                         "Should replace $item with the item")


    @defer.inlineCallbacks
    def test_set(self):
        """
        You can save the last result in a variable.
        """
        runner = basicRunner({
            'func': lambda *a: 'hello',
        })
        context = Context()

        result = yield runner.runActions([
            {'action': 'func'},
            {'action': 'set', 'key': 'something', 'value': '$_'},
        ], context)
        self.assertEqual(result, 'hello', "save should return the previous "
                         "result")
        self.assertEqual(context.variables['_'], 'hello')
        self.assertEqual(context.variables['something'], 'hello')


    @defer.inlineCallbacks
    def test_ask(self):
        """
        You can ask the calling system for some information.
        """
        runner = basicRunner()
        context = Context(lambda key, prompt, **kw: 'A robot %s' % (key,))
        result = yield runner.runSingleAction('ask', {
            'action': 'ask',
            'key': 'THE KEY',
            'prompt': 'Who are you?',
        }, context)
        self.assertEqual(result, 'A robot THE KEY')
        self.assertEqual(context.variables['THE KEY'], 'A robot THE KEY')


    @defer.inlineCallbacks
    def test_dump(self):
        """
        You can dump a subset of the available data.
        """
        runner = basicRunner()
        context = Context()
        result = yield runner.runActions([
            {'action': 'set', 'key': 'foo', 'value': 'foo value'},
            {'action': 'set', 'key': 'bar', 'value': 'bar value'},
            {'action': 'dump', 'keys': ['bar']},
        ], context)
        self.assertEqual(result, {'bar': 'bar value'})



class ContextTest(TestCase):


    def test_variables(self):
        context = Context()
        context.variables['foo'] = 'bar'


    def test_getUserInput(self):
        """
        A context can be made to request user input.
        """
        d = defer.Deferred()
        called = []
        def getUserInput(key, prompt, **kwargs):
            called.append(key)
            called.append(prompt)
            called.append(kwargs)
            return d
        context = Context(getUserInput)
        result = context.getUserInput('id', 'What is your id?')
        self.assertFalse(result.called)
        self.assertEqual(called, ['id', 'What is your id?', {}])
        d.callback('foo')
        self.assertEqual(self.successResultOf(result), 'foo')


    def test_requests(self):
        """
        It should use a requests session by default.
        """
        import requests
        c = Context()
        self.assertTrue(isinstance(c.requests, requests.Session),
                        "Should have a .requests attr that is a Session")



class interpolateTest(TestCase):


    def test_basic(self):
        """
        You can replace $vars with values from a dict
        """
        variables = {'foo': [1, 2, 'foo']}
        original = {'hey': '$foo'}
        result = interpolate(original, variables)
        self.assertEqual(result, {'hey': [1, 2, 'foo']})
        self.assertEqual(original, {'hey': '$foo'})


    def test_nonVars(self):
        """
        Non variables should be ignored.
        """
        variables = {'foo': 'foo value'}
        original = {'hey': 5}
        result = interpolate(original, variables)
        self.assertEqual(result, {'hey': 5})


    def test_deep_dict(self):
        """
        All depths of dictionary should be traversed.
        """
        variables = {'foo': 'foo value'}
        original = {'hey': {'something': '$foo'}}
        result = interpolate(original, variables)
        self.assertEqual(result, {'hey': {'something': 'foo value'}})


    def test_deep_list(self):
        """
        All depths of lists should be traversed.
        """
        variables = {'foo': 'foo value'}
        original = {'hey': ['this', '$foo', 'thing']}
        result = interpolate(original, variables)
        self.assertEqual(result, {'hey': ['this', 'foo value', 'thing']})


    def test_attributes(self):
        """
        You can do attribute access.
        """
        class Foo:
            name = 'something'
        variables = {'foo': Foo()}
        original = {'foo': '$foo.name'}
        result = interpolate(original, variables)
        self.assertEqual(result, {'foo': 'something'})


    def test_array(self):
        """
        You can do index-based access
        """
        variables = {'foo': [1, 'apple', 'cannon']}
        original = {'foo': '$foo[1]'}
        result = interpolate(original, variables)
        self.assertEqual(result, {'foo': 'apple'})

