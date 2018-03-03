import geopandas as gpd


class ChartsCollection(object):
    def __init__(self, dbname, username, password, dbtype=None):
        self.collection = None
        self.dbname = dbname
        self.username = username
        self.password = password
        self.dbtype = dbtype
        self._connection = None
        self._make_connection_str()

    def _make_connection_str(self):
        self._conn_str = "host='localhost' dbname='{}' user='{}' password='{}' port='5433'".format(
                self.dbname,
                self.username,
                self.password)

    def _connect_to_posgres(self):
        '''
        self._connection must be set at the end
        '''
        import psycopg2
        try:
            connection = psycopg2.connect(self._conn_str)
        except:
            raise
        if not self._connection:
            self._connection = connection

    def _connect(self):
        '''
        self._connection must be set at the end
        '''
        try:
            if self.dbtype == 'postgres':
                 self._connect_to_posgres()
            elif self.dbtype is None:
                raise TypeError('Database type is None')
            else:
                raise TypeError("Don't know which database type to connect to")
        except:
            raise ConnectionError('Could not connect to the datebase {}'.format(
                self.dbname))

    def retrieve_query(self, query):
        if not self._connection:
            self._connect()
        cur = self._connection.cursor()
        cur.execute(query)
        return cur.fetchall()

    def _retrieve_table_stats(self, tablename):
        self.cursor = self._connection.cursor()
        query = ' '.join(("SELECT attname, n_distinct FROM pg_stats",
                 "WHERE tablename='{}' and".format(tablename),
                 "attname='gid'"))
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def to_gpd(self, query, crs=None, geom_col=None):
        if geom_col == None:
            geom_col = 'geom'
        df = gpd.GeoDataFrame.from_postgis(query,
                                           self._connection,
                                           geom_col=geom_col)
        if df.crs is None:
            crs = {'init':'epsg:4326'}
            df.crs = crs

        if crs != df.crs:
            df[geom_col] = df[geom_col].to_crs(crs)
        return df
