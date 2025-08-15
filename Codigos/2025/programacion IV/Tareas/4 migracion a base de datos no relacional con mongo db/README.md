## 📚 Biblioteca Personal con MongoDB

Aplicación de línea de comandos para gestionar una biblioteca personal utilizando **MongoDB** como base de datos no relacional y **pymongo** como cliente oficial.

---

## 🎯 Objetivo

Transformar una aplicación previamente basada en bases de datos relacionales (SQLite/MariaDB) para que funcione con documentos JSON en MongoDB, aprovechando las ventajas de las bases de datos NoSQL.

---

## 🛠️ Requisitos

- Python 3.8+
- MongoDB (local o Atlas)
- pymongo

---

## 📦 Instalación de dependencias

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt`:

```
pymongo
```

---

## 🧰 Instalación de MongoDB

### 🔹 Opción 1: MongoDB local

#### En Windows

1. Descargar desde [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Instalar MongoDB Server y MongoDB Compass (opcional)
3. Iniciar el servicio desde el Panel de Servicios o con:

```bash
net start MongoDB
```

#### En Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### En macOS

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### 🔹 Opción 2: MongoDB Atlas (remoto)

1. Crear cuenta en [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Crear un cluster gratuito
3. Configurar IP de acceso y usuario
4. Obtener la cadena de conexión (URI) y reemplazar en `config.py`:

```python
MONGO_URI = "mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

---

## ⚙️ Configuración

Archivo `config.py`:

```python
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "biblioteca_db"
COLLECTION_NAME = "libros"
```

---

## 🚀 Ejecución

```bash
python main.py
```

---

## 📋 Funcionalidades

- Agregar nuevo libro
- Actualizar información de un libro
- Eliminar libro existente
- Ver listado de libros
- Buscar libros por título, autor o género
- Salir del programa

---

## 📄 Estructura de documento (libro)

```json
{
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "genero": "Realismo mágico",
  "estado": "Leído"
}
```

---

## ⚠️ Manejo de errores

- Verificación de conexión a MongoDB
- Validación de ID al actualizar o eliminar
- Búsquedas sin resultados
- Documentos mal estructurados

---

## 🧠 Comparación con bases relacionales

| Relacional (MariaDB) | No Relacional (MongoDB) |
|----------------------|-------------------------|
| Tablas y filas       | Colecciones y documentos |
| Esquema rígido       | Esquema flexible         |
| SQL                  | JSON + filtros dinámicos |
| Integridad referencial | No aplica directamente |

---

## 📁 Estructura del proyecto

```
biblioteca_mongo/
├── main.py
├── operaciones.py
├── database.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 🧪 Ejemplo de uso

```
📚 Menú Biblioteca MongoDB
1. Agregar libro
2. Actualizar libro
3. Eliminar libro
4. Ver libros
5. Buscar libros
6. Salir
```

---

## 🧑‍💻 Autor

Desarrollado por Euris como parte de un ejercicio académico para comprender el uso de bases de datos NoSQL con Python.

```

