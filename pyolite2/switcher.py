# -*- coding: utf-8 -*-

class ContextSwitcherError(Exception):
    pass

class ContextSwitcher(object):
    def __init__(self):
        self.contexts = dict()

    def command(self, context, command):
        def wrap(handler):
            if self.contexts.has_key(context) and self.contexts[context].has_key(command):
                raise ContextSwitcherError("Duplicate command '%s' in context '%s'" % (command, context))

            self.contexts.setdefault(context, {}).setdefault(command, handler)
            return handler
        return wrap

    def switch(self, context, command):
        if not self.contexts.has_key(context) or not self.contexts[context].has_key(command):
            raise ContextSwitcherError("Command '%s' not found in context '%s'" % (command, context))

        handler = self.contexts[context][command]
        if not handler:
            raise ContextSwitcherError("Handler error on context switching: '%s/%s'" % (context, command))

        return handler()

    __call__ = switch
