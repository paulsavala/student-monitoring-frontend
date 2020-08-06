#!/usr/bin/env python
import unittest
from app import create_app, db
from flask import current_app
from config import StEdwardsTestConfig


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(StEdwardsTestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main(verbosity=2)
