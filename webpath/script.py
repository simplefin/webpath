from twisted.internet import task, defer
from twisted.python import usage



class RunOptions(usage.Options):

    synopsis = 'Run a set of steps'


class Options(usage.Options):
    
    subCommands = [
        ('run', None, RunOptions, RunOptions.synopsis),
    ]


def main(reactor, args):
    options = Options()
    options.parseOptions(args[1:])
    return defer.succeed('hey')


def run():
    import sys
    task.react(main, [sys.argv])
