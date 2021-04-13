# Copyright (C) 2021, Biren Patel
# MIT License
# Error handler to queue errors found during lox source interpretation

class ErrorHandler():
    def __init__(self, limit: int = 10) -> None:
        """\
        @limit: maximum capacity, negative indicates no threshold
        @queue: FIFO via self.push() and self.__iter__()
        """
        self.__limit = limit
        self.__queue = []

    def push(self, line: int, error: str) -> bool:
        """\
        load an error onto the queue formated as 'line x: description'
        @line: offending line number
        @error: description
        returns: False if queue is already at maximum capacity
        """
        if len(self.__queue) == self.__limit:
            return False

        msg = "line {}: {}".format(line, error)
        self.__queue.append(msg)
        return True

    def grow(self, inc: int) -> bool:
        if inc > 0:
            self.__limit = self.__limit + inc
            return True

        return False

    def reset(self) -> None:
        self.__queue = []

    def __bool__(self):
        return bool(self.__queue)

    def __iter__(self):
        return iter(self.__queue)
