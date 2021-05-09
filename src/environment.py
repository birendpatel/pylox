# Copyright (C) 2021 Biren Patel
# MIT License
# Environment data structure for associating variable names with their values.
# To enable lexical scoping, all environment instances exists within a cactus
# stack structure. Since python does not have explicit pointers, a parent
# attribute contains the reference to the immediate parent environment. When the
# attribute is None, then the environment must be the global environment.

class Environment():
    def __init__(self, parent):
        self.parent = parent
        self.map = {}

    def insert(self, key, val):
        """/
        insert a k-v pair into the environment. if the key already exists, the
        environment overrides the current value. This allows the user to declare
        a variable multiple times within the same scope.
        """
        self.map[key] = val

    def search(self, key):
        """\
        access a k-v pair from the environment. if it does not exist, search
        the parent environments. if it does not exist in the entire environment
        chain, the python KeyError propogates back to the calling tree node.
        """
        try:
            return self.map[key]
        except KeyError as err:
            if self.parent:
                return self.parent.search(key)
            else:
                raise err

    def modify(self, key, val):
        """\
        modify a k-v pair in the environment only if it exists. modifications
        are not allowed to trigger insertions. If the pair does not exist in
        this environment, check the parent environment.
        """
        if key in self.map:
            self.map[key] = val
        else:
            if self.parent:
                self.parent.modify(key, val)
            else:
                raise KeyError
