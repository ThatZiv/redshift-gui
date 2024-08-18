import os
import unittest
import src.db as db

class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = db.DB('test.db')

    def test_db(self):
        self.db.set('test', 2)
        self.assertEqual(self.db.get('test2'), None)
        self.assertEqual(self.db.get('test'), 2)

    @classmethod
    def tearDownClass(cls):
        cls.db.conn.close()
        os.remove('test.db')
