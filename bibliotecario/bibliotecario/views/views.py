from django.shortcuts import render
from django.http import HttpResponse
import pymongo

def ConnectToMongo():
    try:
        client = pymongo.MongoClient("mongodb+srv://bibliotecario:bibliotecario123@biblioteca0.mglvdip.mongodb.net/?retryWrites=true&w=majority")
        print("Succesfully connected to MongoDB")
        return client
    except pymongo.errors.ConnectionError as e:
        print("Error connecting to MongoDB:", e)


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
    
    
    
def index(request):
    return HttpResponse("¡Hola, mundo!")

def login(request):
    conexion = ConnectToMongo()
    val = True
    val2 = False
    if conexion:
        variable1 = val
    else:
        variable1 = val2
    context = {'test1': variable1}
    
    return render(request, 'login.html', context)

def contact(request):
  
    return render(request, 'contact.html')