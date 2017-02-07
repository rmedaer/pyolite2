# -*- coding: utf-8 -*-

class Bundle(list):
    def __init__(self, names):
        super(Bundle, self).__init__()
        self.names = names

    def drop_name(self, name):
        if not name in self.names:
            return

        self.names.remove(name)

    def __str__(self):
        def dump_entry(entry): return entry.__str__()

        if not self.names:
            return ''

        return 'repo ' + ' '.join(self.names) + ('\n' if self else '') + '\n'.join(map(dump_entry, self))
