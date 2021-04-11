# Copyright (C) 2021, Biren Patel
# MIT License
# Error handler unit tests

from src.error import ErrorHandler
from unittest import TestCase

class TestErrorHandler(TestCase):
    def test_initialized_handler_is_false(self):
        #arrange
        err = ErrorHandler()

        #assert
        self.assertFalse(bool(err))

    def test_non_empty_handler_is_true(self):
        #arrange
        err = ErrorHandler()

        #act
        err.push(1, "foo")

        #assert
        self.assertTrue(bool(err))

    def test_attempt_push_on_full_queue_is_false(self):
        #arrange
        err = ErrorHandler(1)

        #act
        err.push(1, "foo")
        status = err.push(2, "SUT")

        #assert
        self.assertFalse(status)

    def test_attempt_push_on_non_full_queue_is_true(self):
        #arrange
        err = ErrorHandler(2)

        #act
        err.push(1, "foo")
        status = err.push(2, "SUT")

        #assert
        self.assertTrue(status)

    def test_reset_results_in_false_handler(self):
        #arrange
        err = ErrorHandler(1)

        #act
        err.push(1, "foo")
        err.reset()

        #assert
        self.assertFalse(bool(err))

    def test_reset_then_push_results_in_true_handler(self):
        #arrange
        err = ErrorHandler(1)

        #act
        err.push(1, "foo")
        err.reset()
        err.push(1, "bar")

        #assert
        self.assertTrue(bool(err))

    def test_pushed_error_is_recovered_on_iteration(self):
        #arrange
        msg = "line 1: test error"
        err = ErrorHandler()

        #act
        err.push(1, "test error")

        #assert
        for i in err:
            self.assertEqual(msg, i)

    def test_pushed_mulitple_errors_are_recovered_on_iteration(self):
        #arrange
        msgs = ["line 1: test error 1", "line 2: test error 2"]
        err = ErrorHandler()

        #act
        err.push(1, "test error 1")
        err.push(2, "test error 2")

        #assert
        for i, val in enumerate(err):
            self.assertEqual(msgs[i], val)
