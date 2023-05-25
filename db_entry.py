    #Es una clase que contioene todos los atributos de un carro en la base de datos.
    #Nos va a servir para reutilizar la clase para agregar nuevas self.modelo_nombres a la base de datos

#...Esta en revision

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


    def id_gen(self, table):
        statement = "SELECT COUNT(*) FROM %s" % (table)
        res = connection.manual_query(statement)
        res = res[0]
        return int(res) + 1

    def insert(self,fabricante_nombre,modelo_nombre,fecha_de_creacion,carro_detalles,color,dueno_nombre,dueno_direccion):
        self.fabricante_nombre = fabricante_nombre
        self.modelo_nombre = modelo_nombre
        self.fecha_de_creacion = fecha_de_creacion
        self.carro_detalles = carro_detalles
        self.color = color
        self.nombre = dueno_nombre
        self.dueno_direccion = dueno_direccion
        if not (self.id_dueno_in_sys()):
            id_dueno = self.id_gen("dueno_carro")
            self.dueno_id = id_dueno
        id_carro = self.id_gen("carros")
        self.carro_id = id_carro
        

    def id_dueno_in_sys(self):
        statement = "SELECT COUNT(*) FROM dueno_carro WHERE UPPER(nombre) = UPPER(%s)" % (self.nombre)
        res = connection.manual_query(statement)
        if res[0] > 0:
            return True
        else:
            return False


