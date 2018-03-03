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
        except:
            raise ConnectionError('Could not connect to the datebase {}'.format(
                self.dbname))

    def retrieve(self, query):
        if not self._connection:
            self._connect()
        return self 
