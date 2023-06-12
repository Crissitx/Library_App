from django.shortcuts import render
from django.http import HttpResponse
from random import randint
import pymongo



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


def id_generator():
    return randint(1, 10000)
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
    
    
    return render(request, "login.html")


def registro(request):        
    conexion = ConnectToMongo()
    
    if request.method == 'POST':
        db = conexion.Biblioteca
        last_document = db.estudiantes.find().sort("_id", -1).limit(1)
        doc_list = list(last_document)
        last_id = doc_list[0]["_id"] if len(doc_list) > 0 else 0
        new_id = last_id + 1
        document = {
            "_id": new_id,
            "id_estudiante": new_id,
            "documento": request.POST.get('password'),
            "nombre": request.POST.get('name'),
            "direccion": request.POST.get('dir'),
            "programa": request.POST.get('Programa'),
            "edad": request.POST.get('edad')
        }
        AddDocument(conexion, "Biblioteca", "estudiantes", document)
        return render(request, 'login.html')
    return render(request, 'register.html')



def contact(request):
  
    return render(request, 'contact.html')