import pymongo

def ConnectToMongo():
    try:
        client = pymongo.MongoClient("mongodb+srv://bibliotecario:bibliotecario123@biblioteca0.mglvdip.mongodb.net/?retryWrites=true&w=majority")
        print("Succesfully connected to MongoDB")
        return client
    except pymongo.errors.ConnectionError as e:
        print("Error connecting to MongoDB:", e)

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


# TEST
client = ConnectToMongo()
if client:
    filter = {"id_area": 1}
    results = SearchDocuments(client, "Biblioteca", "libro", filter)
    for document in results:
        print(document)