'''
Este código importa diferentes módulos y clases necesarios para el desarrollo de una aplicación Flask.

Flask: Es la clase principal de Flask, que se utiliza para crear instancias de la aplicación Flask.
jsonify: Es una función que convierte los datos en formato JSON para ser enviados como respuesta desde la API.
request: Es un objeto que representa la solicitud HTTP realizada por el cliente.
CORS: Es una extensión de Flask que permite el acceso cruzado entre dominios (Cross-Origin Resource Sharing), lo cual es útil cuando se desarrollan aplicaciones web con frontend y backend separados.
SQLAlchemy: Es una biblioteca de Python que proporciona una abstracción de alto nivel para interactuar con bases de datos relacionales.
Marshmallow: Es una biblioteca de serialización/deserialización de objetos Python a/desde formatos como JSON.
Al importar estos módulos y clases, estamos preparando nuestro entorno de desarrollo para utilizar las funcionalidades que ofrecen.

'''
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow
# ----------------

'''
En este código, se está creando una instancia de la clase Flask y se está configurando para permitir el acceso cruzado entre dominios utilizando el módulo CORS.

app = Flask(__name__): Se crea una instancia de la clase Flask y se asigna a la variable app. El parámetro __name__ es una variable que representa el nombre del módulo o paquete en el que se encuentra este código. Flask utiliza este parámetro para determinar la ubicación de los recursos de la aplicación.

CORS(app): Se utiliza el módulo CORS para habilitar el acceso cruzado entre dominios en la aplicación Flask. Esto significa que el backend permitirá solicitudes provenientes de dominios diferentes al dominio en el que se encuentra alojado el backend. Esto es útil cuando se desarrollan aplicaciones web con frontend y backend separados, ya que permite que el frontend acceda a los recursos del backend sin restricciones de seguridad del navegador. Al pasar app como argumento a CORS(), se configura CORS para aplicar las políticas de acceso cruzado a la aplicación Flask representada por app.

'''
# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

'''
En este código, se están configurando la base de datos y se están creando objetos para interactuar con ella utilizando SQLAlchemy y Marshmallow.

app.config["SQLALCHEMY_DATABASE_URI"]: Se configura la URI (Uniform Resource Identifier) de la base de datos. En este caso, se está utilizando MySQL como el motor de base de datos, el usuario y la contraseña son "root", y la base de datos se llama "proyecto". Esta configuración permite establecer la conexión con la base de datos.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: Se configura el seguimiento de modificaciones de SQLAlchemy. Al establecerlo en False, se desactiva el seguimiento automático de modificaciones en los objetos SQLAlchemy, lo cual mejora el rendimiento.

db = SQLAlchemy(app): Se crea un objeto db de la clase SQLAlchemy, que se utilizará para interactuar con la base de datos. Este objeto proporciona métodos y funcionalidades para realizar consultas y operaciones en la base de datos.

ma = Marshmallow(app): Se crea un objeto ma de la clase Marshmallow, que se utilizará para serializar y deserializar objetos Python a JSON y viceversa. Marshmallow proporciona una forma sencilla de definir esquemas de datos y validar la entrada y salida de datos en la aplicación. Este objeto se utilizará para definir los esquemas de los modelos de datos en la aplicación.

'''
# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
# siguiente linea para usar en local
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/proyecto"
# siguiente linea para usar db en python anywhere
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sebasrgomez90:DevilMayCry154274644@sebasrgomez90.mysql.pythonanywhere-services.com/sebasrgomez90$default'
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)


class Mascota(db.Model):  # mascota hereda de db.Model
    """
    Definición de la tabla mascota en la base de datos.
    La clase mascota hereda de db.Model.
    Esta clase representa la tabla "mascota" en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    id_especie = db.Column(db.String(100))
    peso = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre, id_especie, peso, imagen):
        """
        Constructor de la clase mascota.

        Args:
            nombre (str): Nombre del mascota.
            id_especie (int): id_especie del mascota.
            peso (int): Cantidad en peso del mascota.
            imagen (str): URL o ruta de la imagen del mascota.
        """
        self.nombre = nombre
        self.id_especie = id_especie
        self.peso = peso
        self.imagen = imagen

    # Se pueden agregar más clases para definir otras tablas en la base de datos


with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase mascota


class MascotaSchema(ma.Schema):
    """
    Esquema de la clase mascota.

    Este esquema define los campos que serán serializados/deserializados
    para la clase mascota.
    """
    class Meta:
        fields = ("id", "nombre", "id_especie", "peso", "imagen")


mascota_schema = MascotaSchema()  # Objeto para serializar/deserializar un mascota
# Objeto para serializar/deserializar múltiples mascotas
mascotas_schema = MascotaSchema(many=True)

'''
Este código define un endpoint que permite obtener todos los mascotas de la base de datos y los devuelve como un JSON en respuesta a una solicitud GET a la ruta /mascotas.
@app.route("/mascotas", methods=["GET"]): Este decorador establece la ruta /mascotas para este endpoint y especifica que solo acepta solicitudes GET.
def get_mascotas(): Esta es la función asociada al endpoint. Se ejecuta cuando se realiza una solicitud GET a la ruta /mascotas.
all_mascotas = mascota.query.all(): Se obtienen todos los registros de la tabla de mascotas mediante la consulta mascota.query.all(). Esto se realiza utilizando el modelo mascota que representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza para obtener todos los registros de la tabla.
result = mascotas_schema.dump(all_mascotas): Los registros obtenidos se serializan en formato JSON utilizando el método dump() del objeto mascotas_schema. El método dump() heredado de ma.Schema se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''


@app.route("/mascotas", methods=["GET"])
def get_Mascotas():
    """
    Endpoint para obtener todos los mascotas de la base de datos.

    Retorna un JSON con todos los registros de la tabla de mascotas.
    """
    all_mascotas = Mascota.query.all()  # Obtiene todos los registros de la tabla de mascotas
    # Serializa los registros en formato JSON
    result = mascotas_schema.dump(all_mascotas)
    # Retorna el JSON de todos los registros de la tabla
    return jsonify(result)


'''
El código que sigue a continuación termina de resolver la API de gestión de mascotas, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de mascotas:
get_mascota(id):
    # Obtiene un mascota específico de la base de datos
    # Retorna un JSON con la información del mascota correspondiente al ID proporcionado
delete_mascota(id):
    # Elimina un mascota de la base de datos
    # Retorna un JSON con el registro eliminado del mascota correspondiente al ID proporcionado
create_mascota():
    # Crea un nuevo mascota en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de mascota
    # Retorna un JSON con el nuevo mascota creado
update_mascota(id):
    # Actualiza un mascota existente en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del mascota con el ID especificado
    # Retorna un JSON con el mascota actualizado

'''


@app.route("/mascotas/<id>", methods=["GET"])
def get_mascota(id):
    """
    Endpoint para obtener un mascota específico de la base de datos.

    Retorna un JSON con la información del mascota correspondiente al ID proporcionado.
    """
    mascota = Mascota.query.get(
        id)  # Obtiene el mascota correspondiente al ID recibido
    return mascota_schema.jsonify(mascota)  # Retorna el JSON del mascota


@app.route("/mascotas/<id>", methods=["DELETE"])
def delete_mascota(id):
    """
    Endpoint para eliminar un mascota de la base de datos.

    Elimina el mascota correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    mascota = Mascota.query.get(
        id)  # Obtiene el mascota correspondiente al ID recibido
    # Elimina el mascota de la sesión de la base de datos
    db.session.delete(mascota)
    db.session.commit()  # Guarda los cambios en la base de datos
    # Retorna el JSON del mascota eliminado
    return mascota_schema.jsonify(mascota)


@app.route("/mascotas", methods=["POST"])  # Endpoint para crear un mascota
def create_mascota():
    """
    Endpoint para crear un nuevo mascota en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de mascota en la base de datos.
    Retorna un JSON con el nuevo mascota creado.
    """
    nombre = request.json["nombre"]  # Obtiene el nombre del mascota del JSON proporcionado
    # Obtiene el id_especie del mascota del JSON proporcionado
    id_especie = request.json["id_especie"]
    # Obtiene el peso del mascota del JSON proporcionado
    peso = request.json["peso"]
    # Obtiene la imagen del mascota del JSON proporcionado
    imagen = request.json["imagen"]
    # Crea un nuevo objeto mascota con los datos proporcionados
    new_mascota = Mascota(nombre, id_especie, peso, imagen)
    # Agrega el nuevo mascota a la sesión de la base de datos
    db.session.add(new_mascota)
    db.session.commit()  # Guarda los cambios en la base de datos
    # Retorna el JSON del nuevo mascota creado
    return mascota_schema.jsonify(new_mascota)


# Endpoint para actualizar un mascota
@app.route("/mascotas/<id>", methods=["PUT"])
def update_mascota(id):
    """
    Endpoint para actualizar un mascota existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del mascota con el ID especificado.
    Retorna un JSON con el mascota actualizado.
    """
    mascota = Mascota.query.get(
        id)  # Obtiene el mascota existente con el ID especificado

    # Actualiza los atributos del mascota con los datos proporcionados en el JSON
    mascota.nombre = request.json["nombre"]
    mascota.id_especie = request.json["id_especie"]
    mascota.peso = request.json["peso"]
    mascota.imagen = request.json["imagen"]

    db.session.commit()  # Guarda los cambios en la base de datos
    # Retorna el JSON del mascota actualizado
    return mascota_schema.jsonify(mascota)


'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal

if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)
