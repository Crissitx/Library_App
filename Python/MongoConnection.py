import pymongo

def ConnectToMongo():
    try:
        client = pymongo.MongoClient("mongodb+srv://bibliotecario:bibliotecario123@biblioteca0.mglvdip.mongodb.net/?retryWrites=true&w=majority")
        print("Succesfully connected to MongoDB")
        return client
    except pymongo.errors.ConnectionError as e:
        print("Error connecting to MongoDB:", e)

def AddDocument(client: pymongo.MongoClient, db_name: str, collection_name: str, document):
    try:
        # Acceder a la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]

        # Agregar el documento
        result = collection.insert_one(document)

        print("Documento agregado exitosamente. ID:", result.inserted_id)
        return True

    except pymongo.errors.CollectionInvalid as e:
        print("Error al acceder a la colección:", e)
        return False
    except pymongo.errors.WriteError as e:
        print("Error al agregar el documento:", e)
        return False

def RemoveDocuments(client: pymongo.MongoClient, db_name: str, collection_name: str, filter):
    try:
        # Acceder a la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]

        # Eliminar los documentos que coinciden con el filtro
        result = collection.delete_many(filter)

        print("Documentos eliminados exitosamente. Total:", result.deleted_count)
    except pymongo.errors.CollectionInvalid as e:
        print("Error al acceder a la colección:", e)
    except pymongo.errors.WriteError as e:
        print("Error al eliminar los documentos:", e)

def SearchDocuments(client: pymongo.MongoClient, db_name: str, collection_name: str, filter):
    try:
        # Acceder a la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]
        # Realizar la búsqueda
        results = collection.find(filter)

        return results
    
    except pymongo.errors.CollectionInvalid as e:
        print("Error triying to access to Collection:", collection_name, ":", e)

def UpdateDocument(client: pymongo.MongoClient, db_name: str, collection_name: str, filter, new_data):
    try:
        # Acceder a la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]
        
        collection.update_one(filter, {"$set": new_data})

        print("Documento actualizado exitosamente.")
        return True
    except pymongo.errors.CollectionInvalid as e:
        print("Error al acceder a la colección:", e)
        return False
    except pymongo.errors.WriteError as e:
        print("Error al actualizar el documento:", e)
        return False
    
def UpdateDocuments(client: pymongo.MongoClient, db_name: str, collection_name: str, filter, new_data):
    try:
        # Acceder a la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]
        
        collection.update_many(filter, {"$set": new_data})

        print("Documentos actualizado exitosamente.")
        return True
    except pymongo.errors.CollectionInvalid as e:
        print("Error al acceder a la colección:", e)
        return False
    except pymongo.errors.WriteError as e:
        print("Error al actualizar los documentos:", e)
        return False
    
client = ConnectToMongo()

# UPDATE TEST
#if client:
#    filter = {"id_area": 1}
#    update = {"DESCRIPCION_AREA": "Literatura"}
#    UpdateDocument(client, "Biblioteca", "area", filter, update)

# ADD TEST
#if client:
#    document = {"id_area": 12, "DESCRIPCION_AREA": "Artistica"}
#    AddDocument(client, "Biblioteca", "area", document)

#REMOVE TEST
#if client:
#    filter = {"id_area": 12}
#    RemoveDocuments(client, "Biblioteca", "area", filter)