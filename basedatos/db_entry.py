    #Es una clase que contioene todos los atributos de un carro en la base de datos.
    #Nos va a servir para reutilizar la clase para agregar nuevas self.modelo_nombres a la base de datos

import datetime

class db_entry():
    def __init__(self, connection):
        #connection to db data
        self._connection = connection
        #CARROS table
        self.carro_id = None
        self.fecha_de_creacion = None
        self.color = None
        self.carro_detalles = None
        self.modelo_carro_id = None
        self.path_to_image = None
        #DUEÑO_CARRO table
        self.dueno_id = None
        self.nombre = None
        self.dueno_dirreccion = None
        #FABRICANTES table
        self.fabricante_id = None
        self.fabricante_nombre = None
        self.fabricante_ubicacion = None
        self.fabricante_detalles = None
        #HISTORIAL_DE_SERVICIOS table
        self.servicio_id = None
        self.fecha_ultimo_servicio = None
        self.detalles_ult_servicio = None
        #MANTENIMIENTO_CARRO table
        self.mantenimiento_id = None
        self.fecha_inicio = None
        self.fecha_final = None
        self.problema_carro = None
        #FABRICANTES table
        self.fabricante_nombre = None
        self.fabricante_ubicacion = None
        self.fabricante_detalles = None
        #MODELO_CARRO table
        self.modelo_id = None
        self.modelo_nombre = None
        self.modelo_descricpcion = None
        #PROVEEDORES table
        self.proveedor_id = None
        self.proveedor_nombre = None
        self.proveedor_dirreccion = None
        self.proveedor_detalles = None
        self.image = None


    def id_gen(self, table):
        statement = "SELECT COUNT(*) FROM %s" % (table)
        res = self._connection.manual_query(statement)
        res = res[0]
        return int(res) + 1

    def insert(self):
        self.datetime_gen()
        self.fabricante_id = self.id_in_sys("fabricantes", "fabricante_nombre", "fabricante_id",  self.fabricante_nombre)
        self.dueno_id = self.id_in_sys("dueno_carro", "nombre", "dueno_id", self.nombre)
        self.modelo_carro_id = self.id_in_sys("modelo_de_carro", "modelo_nombre", "modelo_id", self.modelo_nombre)
        self.carro_id = self.id_gen("carros")
            #se comunica con la base de datos para insertar los datos del carro
        self._connection.insert_carro(self.carro_id, self.fecha_de_creacion, self.color, self.fabricante_id, self.carro_detalles, self.modelo_carro_id, self.image, self.dueno_id)
        self._connection.commit_change()
        #entry = "insert into carros (carro_id, fecha_de_creacion, color, fabricante_id, carro_detalles, modelo_carro_id, path_to_image, dueno) VALUES (%s, TO_DATE('%s', 'YYYY-MM-DD'), %s, %s, %s, 10, BFILENAME('imagenes_carros','%s'))" % (self.carro_id, self.fecha_de_creacion, self.color, self.fabricante_id, self.carro_detalles, self.modelo_carro_id, self.image, self.dueno_id)
        #self._connection.manual_query(entry)



    def id_in_sys(self, table, column, id_column, ref_value):
        statement = "SELECT COUNT(*) FROM %s WHERE UPPER(%s) = UPPER('%s')" % (table, column, ref_value)
        res = self._connection.manual_query(statement)
        if res[0] > 0:
            return self.query_for_id(table, column, id_column, ref_value)
        else:
            nuevo_id = self.id_gen(table)
            if table == "dueno_carro":
                self.dueno_id = nuevo_id
                self._connection.insert_dueno_carro(self.dueno_id, self.nombre, self.dueno_dirreccion)
            elif table == "modelo_de_carro":
                self.modelo_carro_id = nuevo_id
                self.modelo_id = nuevo_id
                self._connection.insert_modelo_de_carro(self.modelo_id, self.modelo_nombre, self.modelo_descricpcion)
            elif table == "fabricantes":
                self.fabricante_id = nuevo_id
                self._connection.insert_fabricante(self.fabricante_id, self.fabricante_nombre, self.fabricante_ubicacion, self.fabricante_detalles)
            elif table == "historial_de_servicios":
                self.servicio_id = nuevo_id
                self._connection.insert_historial_de_servicio(self.servicio_id, self.fecha_ultimo_servicio, self.detalles_ult_servicio, self.carro_id)
            elif table == "mantenimiento_carro":
                self.mantenimiento_id = nuevo_id
                self._connection.insert_mantenimiento_carro(self.mantenimiento_id, self.fecha_inicio, self.fecha_final, self.problema_carro, self.carro_id)
            return nuevo_id


    def id_dueno_in_sys(self):
        statement = "SELECT COUNT(*) FROM dueno_carro WHERE UPPER(nombre) = UPPER(%s)" % (self.nombre)
        res = self._connection.manual_query(statement)
        if res[0] > 0:
            self.dueno_id = self.query_for_id("dueno_carro", "nombre", "dueno_id", self.nombre)
        else:
            self.dueno_id = self.id_gen("dueno_carro")

    def query_for_id(self, table, ref_column, id_column, ref_value):
        statement = "SELECT %s FROM %s WHERE UPPER(%s) = UPPER('%s')" % (id_column, table, ref_column, ref_value)
        res = self._connection.manual_query(statement)[0]
        return res

    def datetime_gen(self):
        date = datetime.date.fromisoformat("%s-01-01"%(str(self.fecha_de_creacion)))
        self.fecha_de_creacion = date

