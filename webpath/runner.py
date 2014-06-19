# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from twisted.internet import defer


class Runner(object):
    """
    I run a set of steps.
    """

    def __init__(self, handlers=None):
        self._handlers = {}
        if handlers:
            self.registerHandlers(handlers)


    def registerHandler(self, action, handler_fn):
        """
        @param action: String name of action to handle.
        @param handler_fn: Function to handle a particular action.  This
            function should accept two arguments: C{params} and C{context}.
        """
        self._handlers[action] = handler_fn


    def registerHandlers(self, handlers):
        """
        Register multiple handlers.

        @param handlers: Dict of handler names to handler functions.
        """
        self._handlers.update(handlers)


    @defer.inlineCallbacks
    def runActions(self, actions, context):
        """
        Run a set of actions.
        """
        for action in actions:
            params = interpolate(action, context.variables)
            result = yield self.runSingleAction(
                params['action'], params, context)
        defer.returnValue(result)


    def runSingleAction(self, action, params, context):
        """
        Run the handler for an action.

        @param action: String name of action.
        @param params: Dict of parameters to the handler.
        @param context: A L{Context} for the handler.
        """
        context.runner = self
        d = defer.maybeDeferred(self._handlers[action], params, context)
        d.addCallback(context.saveResult)
        return d


@defer.inlineCallbacks
def _loop(params, context):
    """
    Loop through some actions in the context of a L{Runner} run.
    """
    for item in params['iterable']:
        context.variables['item'] = item
        result = yield context.runner.runActions(params['actions'], context)
    defer.returnValue(result)


def _set(params, context):
    """
    Save the last result as a variable.
    """
    value = params['value']
    context.variables[params['key']] = value
    return value


@defer.inlineCallbacks
def _ask(params, context):
    """
    Ask the system for some information.
    """
    value = yield context.getUserInput(params['key'], params['prompt'])
    context.variables[params['key']] = value
    defer.returnValue(value)


def _dump(params, context):
    """
    Dump the current variables (or a subset of them).
    """
    subset_keys = params['keys']
    result = {}
    for key in subset_keys:
        result[key] = context.variables[key]
    return result




def basicRunner(handlers=None):
    handlers = handlers or {}
    handlers.update({
        'loop': _loop,
        'set': _set,
        'ask': _ask,
        'dump': _dump,
    })
    return Runner(handlers)



def _interpolateItem(item, variables):
    """
    Replace all occurrences of $vars in C{item} with value from C{variables}.

    @type item: anything
    @type variables: dict
    """
    if type(item) in (str, unicode):
        if item.startswith('$'):
            var_name = item[1:]
            item = eval(var_name, {"__builtins__":None}, variables)
    elif type(item) in (dict,):
        item = interpolate(item, variables)
    elif type(item) in (tuple, list):
        item = [_interpolateItem(x, variables) for x in item]
    return item


def interpolate(params, variables):
    """
    Replace all occurrences of $vars in C{params} with value from C{variables}.

    @type params: dict
    @type variables: dict
    """
    result = {}
    for k, v in params.items():
        result[k] = _interpolateItem(v, variables)
    return result



class Context(object):
    """
    I am the shared context of a single run of steps.
    """

    runner = None
    requests = None


    def __init__(self, user_input_func=None):
        import requests
        self.results = []
        self.variables = {}
        self._user_input_func = user_input_func
        self.requests = requests.Session()


    def __repr__(self):
        return '<Context runner=%r variables=%r results=%r>' % (
            self.runner, self.variables, self.results)


    def saveResult(self, result):
        """
        @param result: Save a result.
        """
        self.variables['_'] = result
        self.results.append(result)
        return result


    def getUserInput(self, key, prompt, **kwargs):
        """
        Ask a user for input.

        @param key: Uniqueish, computer-friendly key for this query.
        @param prompt: Human-friendly text prompt
        @param **kwargs: Additional arguments.

        @return: The Deferred user input.
        """
        return defer.maybeDeferred(self._user_input_func,
                                   key, prompt, **kwargs)


