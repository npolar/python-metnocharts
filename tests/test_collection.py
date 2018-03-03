import unittest
from unittest import TestCase

from metnocharts.collection import ChartsCollection

class TestCollection(TestCase):
    def setUp(self):
        dbname = 'foo'
        username = 'bar'
        password = 'charts'
        dbtype = 'postgres'
        self.charts_collection = ChartsCollection(dbname,
                                             username,
                                             password,
                                             dbtype=dbtype)
    
    def test_connection(self):
        self.charts_collection._connect()
        self.assertIsNotNone(self.charts_collection._connection)
        
    @unittest.skip('skip')
    def test_retrieves_collection(self):
        result = self.charts_collection.retrieve()
        self.assertIsInstance(result, ChartsCollection)

    def test_connect_to_postgres(self):
        self.charts_collection._connect_to_posgres()
        self.assertIsNotNone(self.charts_collection._connection)
