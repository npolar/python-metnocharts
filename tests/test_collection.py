import unittest
from unittest import TestCase

from metnocharts.collection import ChartsCollection

class TestCollection(TestCase):
    def setUp(self):
        dbname = 'foo'
        username = 'user'
        password = 'charts'
        dbtype = 'postgres'
        self.charts_collection = ChartsCollection(dbname,
                                             username,
                                             password,
                                             dbtype=dbtype)

        self.test_query = ' '.join(("SELECT * FROM",
                          "merged_charts",
                          "where dates = '2017-01-30'"))

    def tearDown(self):
        self.charts_collection = None

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

    def test_get_table_stats(self):
        self.charts_collection._connect()
        self.charts_collection._retrieve_table_stats('merged_charts')

    def test_database_type_not_known(self):
        self.charts_collection.dbtype = None
        with self.assertRaises(ConnectionError):
            self.charts_collection._connect()

    def test_database_type_is_known(self):
        self.charts_collection.dbtype = 'postgres'
        self.charts_collection._connect()
        self.assertIsNotNone(self.charts_collection._connection)

    def test_retrieve_all(self):
        query = ' '.join(("SELECT * FROM",
                          "merged_charts",
                          "where dates = '2017-01-30'"))

        self.charts_collection.retrieve_query(query)

    def test_to_geodataframe(self):
        self.charts_collection._connect()
        df = self.charts_collection.to_gpd(self.test_query, crs={"init":"epsg:3411"})
