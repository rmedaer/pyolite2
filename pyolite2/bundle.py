# -*- coding: utf-8 -*-

class Bundle(list):
    def __init__(self, names):
        super(Bundle, self).__init__()
        self.names = names

    def __str__(self):
        def dump_entry(entry): return entry.__str__()

        return 'repo ' + ' '.join(self.names) + ('\n' if self else '') + '\n'.join(map(dump_entry, self))
