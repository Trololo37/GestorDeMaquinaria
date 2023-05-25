import oracledb
import getpass
from datetime import date
import datetime
from random import shuffle


class Conn():
    def __init__(self, **kwargs):
        self.oracle = oracledb.defaults.config_dir = "C:\app\leona\product\18.0.0\dbhomeXE\network\admin"
        self._user = "c##_proyectomau"
        self._pwd = "Ladoblet2808"
        self._port = '1521'
        self._host = "192.168.1.78" #lo cambie a "localhost" para la latitude, pero es mi ip "192.168.1.78"
        self._service = "xepdb1"
        self._sid = "xe"
        self._dsn = "localhost/xepdb1"
        self._cursor = None
        self._connection = None

    def establish_connection(self, **kwargs):
        oracledb.defaults.config_dir = self.oracle
        self._dsn = f'{self._user}/{self._pwd}@{self._host}:{self._port}/{self._sid}'
        self._connection = oracledb.connect(self._dsn)
        if True:
            print("Successfully established connection to %s" % (self._user))
        self._cursor = self._connection.cursor()
        """x = self._cursor.execute("select * from fabricantes")
        print(x)
        print()
        while True:
            row = self._cursor.fetchone()
            if row is None:
                break
            print(row)"""

    def establish_connection_m(self, **kwargs):
        oracledb.defaults.config_dir = "C:\app\leona\product\18.0.0\dbhomeXE\network\admin"
        userpwd = getpass.getpass("PYTHON_PASSWORD")
        self._connection = oracledb.connect(user="c##_proyectomau", password=userpwd, dsn="xe",
                                    config_dir="C:/app/leona/product/18.0.0/dbhomeXE/network/admin")
        self._cursor = self._connection.cursor()
        #x = self._cursor.execute("select * from carros")
        #print(x)

    def refresh_data(self):
        tablas = ["carros", "dueno_carro", "fabricantes", "historial_de_servicios", "mantenimiento_carro", "modelo_de_carro"]
        for tabla in tablas:
            statement = "refres table '%s'" % (tabla)
            cursor = self._cursor.execute(statement)


    def close_connection(self):
        self._connection.close()

    def commit_change(self):
        self._connection.commit() #comente esta linea para ir haciendo pruebas

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
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        res = []
        for value in values:
            res.append(value[0])
        return res

    def nombre_for_id(self, table, id_number):
        if table == "dueno_carro":
            statement = "SELECT nombre FROM %s WHERE dueno_id = %s" % (table, id_number)
        if table == "fabricantes":
            statement = "SELECT fabricante_nombre FROM %s WHERE fabricante_id = %s" % (table, id_number)
        if table == "modelo_de_carro":
            statement = "SELECT modelo_nombre FROM %s WHERE modelo_id = %s" % (table, id_number)
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        res = []
        for value in values:
            res.append(value[0])
        return res

    def query_column_data_pos(self, table, column, pos):
        statement = "SELECT %s FROM %s" % (column, table)
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        return values[pos]

    def query_column_data_5pos(self, table, column):
        statement = "SELECT %s FROM %s" % (column, table)
        cursor = self._cursor.execute(statement)
        #se puede utilizar .fetchmany(5) con 5 como parametro, pero hace exactamente
        #lo mismo, por lo que no es más rapido ni mas lento
        values = cursor.fetchall()
        values = list(dict.fromkeys(values))
        shuffle(values)
        values = values[:5]
        res = []
        for value in values:
            res.append(value[0])
        return res

    def query_column_data_5pos_years(self, table, column):
        statement = "SELECT %s FROM %s" % (column, table)
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        values = list(dict.fromkeys(values))
        shuffle(values)
        res = []
        #datetime.
        for value in values:
            #x = date.fromtimestamp(value)
            res.append(str(datetime.datetime.date(value[0]).year))
        res = list(dict.fromkeys(res))
        res = res[:5]
        return res

    def manual_query_5pos(self, statement):
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        values = values[:5]
        res = []
        for value in values:
            res.append(value[0])
        return list(dict.fromkeys(res))

    def manual_query(self, statement):
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        res = []
        for value in values:
            res.append(value[0])
        return res

    def raw_manual_query(self, statement):
        cursor = self._cursor.execute(statement)
        return cursor.fetchall()

    def query_for_id(self, table, ref_column, id_column, ref_value):
        statement = "SELECT %s FROM %s WHERE UPPER(%s) = UPPER('%s')" % (id_column, table, ref_column, ref_value)
        cursor = self._cursor.execute(statement)
        values = cursor.fetchall()
        return values[0]

    def insert_def(self, table, *args):
        if table == "carros":
            self.insert_carro(args)
        elif table == "dueno_carro":
            self.insert_dueno_carro(args)
        elif table == "modelo_de_carro":
            self.insert_modelo_de_carro(args)
        elif table == "fabricantes":
            self.insert_fabricante(args)
        elif table == "historial_de_servicios":
            self.insert_historial_de_servicio(args)
        elif table == "mantenimiento_carro":
            self.insert_mantenimiento_carro(args)

    def insert_carro(self, carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, image, dueno_id):
        entry = "insert into carros (carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, path_to_image, modelo_carro_id, dueno_id) "
        values = "VALUES (%s, TO_DATE('%s', 'YYYY-MM-DD'), '%s', %s, '%s', '%s', %s, %s)" % (carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, image, modelo_carro_id, dueno_id)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)

    def insert_dueno_carro(self, dueno_id, nombre, dueno_direccion):
        entry = "insert into dueno_carro (dueno_id, nombre, dueno_direccion) "
        values = "VALUES (%s, '%s', '%s')" % (dueno_id, nombre, dueno_direccion)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)

    def insert_modelo_de_carro(self, modelo_id, modelo_nombre, modelo_descripcion):
        entry = "insert into modelo_de_carro (modelo_id, modelo_nombre, modelo_descripcion) "
        values = "VALUES (%s, '%s', '%s')" % (modelo_id, modelo_nombre, modelo_descripcion)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)

    def insert_fabricante(self, fabricante_id, fabricante_nombre, fabricante_ubicacion, fabricante_detalles):
        entry = "insert into fabricantes (fabricante_id, fabricante_nombre, fabricante_ubicacion, fabricante_detalles) "
        values = "VALUES (%s, '%s', '%s', '%s')" % (fabricante_id, fabricante_nombre, fabricante_ubicacion, fabricante_detalles)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)

    def insert_historial_de_servicio(self, servicio_id, fecha_ultimo_servicio, detalles_ult_servicio, carro_id):
        entry = "insert into historial_de_servicios (servicio_id, fecha_ultimo_servicio, detalles_ult_servicio, carro_id) "
        values = "VALUES (%s, TO_DATE('%s', 'YYYY-MM-DD'), '%s', %s)" % (servicio_id, fecha_ultimo_servicio, detalles_ult_servicio, carro_id)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)

    def insert_mantenimiento_carro(self, mantenimiento_id, fecha_inicio, fecha_final, problema_carro, carro_id):
        entry = "insert into mantenimiento_carro (mantenimiento_id, fecha_inicio, fecha_final, problema_carro, carro_id) "
        values = "VALUES (%s, TO_DATE('%s', 'YYYY-MM-DD'), TO_DATE('%s', 'YYYY-MM-DD'), '%s', %s)" % (mantenimiento_id, fecha_inicio, fecha_final, problema_carro, carro_id)
        statement = entry + values
        print(statement)
        cursor = self._cursor.execute(statement)


    """# Ejecutar una consulta SQL "INSERT" para agregar los valores a la tabla de la base de datos
    consulta = "INSERT INTO nombre_de_tabla (columna1, columna2, columna3) VALUES (:1, :2, :3)"
    cursor.execute(consulta, (valor1, valor2, valor3))"""

"""connection = Conn()
connection.establish_connection()
statement = "SELECT COUNT(*) FROM dueno_carro WHERE UPPER(nombre) = UPPER('mau')"
datos = connection.insert_carro(5,2015)
#datos = connection.query_for_id('dueno_carro','nombre', 'dueno_direccion', 'leonardo trevizo herrera')
print(datos)"""
