import oracledb

class Conn():
    def __init__(self, **kwargs):
        self._user = "c##_proyectomau"
        self._pwd = "Ladoblet2808"
        self._port = "1521"
        self._host = "192.168.1.78"
        self._service = "xepdb1"
        self._sid = "xe"
        self._dsn = "localhost/xepdb1"

    def establish_connection(self, **kwargs):
        self._dsn = f'{self._user}/{self._pwd}@{self._host}:{self._port}/{self._sid}'
        self._connection = oracledb.connect(self._dsn)
        if True:
            print("Successfully established connection to %s" % (self._user))
        self._cursor = self._connection.cursor()

    def close_connection(self):
        self._connection.close()

    def commit_change(self):
        self._connection.commit()

    def insert_entry(self, table, **kwargs):
        #for **kwargs specify column name and value
        #for inserting null state None as value
        columnas = []
        valores = []
        raw_values = []
        numeros_valores = []
        len_values = len(kwargs)
        i=0
        coma = ", "
        for column, value in kwargs.items():
            i+=1
            raw_values.append(value)
            numeros_valores.append(str(":")+str(i))
            columnas.append(column)
            valores.append(str(value))
            if(i != len_values):
                valores.append(coma)
                numeros_valores.append(coma)
        values_text = ""
        for valor in valores:
            values_text += valor
        numeros_valores_text = ""
        for numero in numeros_valores:
            numeros_valores_text += numero
        statement = "INSERT INTO %s VALUES (%s)" % (table, numeros_valores_text)
        self._cursor.execute(statement, raw_values)

    def _query(self, table, **kwargs):
        statement = "SELECT * FROM ", str(table)
        rows = []
        for row in self._cursor.execute(statement):
            rows.append(row)
        return rows

    def query_column_data(self, table, column):
        statement = "SELECT %s FROM %s" % (column, table)
        self._cursor.execute(statement)

    """# Ejecutar una consulta SQL "INSERT" para agregar los valores a la tabla de la base de datos
    consulta = "INSERT INTO nombre_de_tabla (columna1, columna2, columna3) VALUES (:1, :2, :3)"
    cursor.execute(consulta, (valor1, valor2, valor3))"""

