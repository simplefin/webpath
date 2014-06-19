from twisted.internet import task, defer
from twisted.python import usage

import sys

from webpath.runner import basicRunner, Context
from webpath import http



class Serializer(object):


    def load_yaml(self, fh):
        import yaml
        return yaml.load(fh.read())


    def dump_yaml(self, data, fh):
        import yaml
        fh.write(yaml.dump(data, default_flow_style=False))
        fh.flush()


    def load_json(self, fh):
        import json
        return json.loads(fh.read())


    def dump_json(self, data, fh):
        import json
        fh.write(json.dumps(data, indent=2))
        fh.flush()



class RunOptions(usage.Options):

    synopsis = 'Run a set of steps'

    optParameters = [
        ('input', 'i', None, "Input filename (default stdin)"),
        ('input-format', 'f', "yaml", "Input format"),
        ('output', 'o', None, "Output filename (default stdout)"),
        ('output-format', 'F', "yaml", "Output format"),
    ]


    @defer.inlineCallbacks
    def doCommand(self, options, global_options):
        ifh = sys.stdin
        if options['input']:
            ifh = open(options['input'], 'rb')

        ofh = sys.stdout
        if options['output']:
            ofh = open(options['output'], 'wb')


        serializer = Serializer()
        load = getattr(serializer, 'load_' + options['input-format'])

        actions = load(ifh)

        context = Context()
        runner = basicRunner()
        http.installHTTPHandlers(runner)

        result = yield runner.runActions(actions, context)

        dump = getattr(serializer, 'dump_' + options['output-format'])
        dump(result, ofh)



class Options(usage.Options):
    
    subCommands = [
        ('run', None, RunOptions, RunOptions.synopsis),
    ]


def main(reactor, args):
    options = Options()
    options.parseOptions(args[1:])
    subOptions = options.subOptions
    return defer.maybeDeferred(subOptions.doCommand, subOptions, options)


def run():
    task.react(main, [sys.argv])
