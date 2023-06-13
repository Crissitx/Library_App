from datetime import date, timedelta
from django.shortcuts import render
import MongoConnection
from django.shortcuts import redirect
from bson.objectid import ObjectId


def add_days(date_value, days):
    return date_value + timedelta(days=days)
    
def prestamo(request):
    today = date.today()
    max_days = 7
    conexion = MongoConnection.ConnectToMongo()
    db = conexion.Biblioteca
    collection = db['libro']

    libros = collection.find({}, {'_id': 1, 'Titulo_libro': 1})

    nombres = []
    ids = []

    for libro in libros:
        nombres.append(libro['Titulo_libro'])
        ids.append(libro['_id'])
    
    lib_data = zip(ids, nombres)
    max_days = add_days(today, max_days)
    context = {'libros': lib_data,
               'today': today,
               'max_days': max_days,}
    
    if request.method == 'POST':
        nuevo_id = ObjectId()
        estudiante_id = request.session['estudiante_id'][0]
        fecha_in = request.POST.get('fecha_in')
        fecha_fin = request.POST.get('fecha_fin')
        print(fecha_in)
        print(fecha_fin)            
        dias =MongoConnection.calcular_dias_transcurridos(fecha_fin)
        print(dias)
        if  dias < 0 : 
            multa = 0 
        else : 
            col = db['estudiantes']
            col2 = db['PROGRAMAS']
            id_pro = col.find_one({'id_estudiante': int(estudiante_id) })
            id_programa =  id_pro['programa'] if id_pro else 0
            resultado = col2.find_one({'PROGRAMA': id_programa})
            yesno = resultado['MULTA'] if id_pro else "no"
            if yesno == "no":
                multa = 0
            else:
                multa = resultado['valor_multa_dia']
               
        document = {"_id": nuevo_id,
                    "estudiante_id": int(estudiante_id),
                    "libro_id": int(request.POST.get('libro')),
                    "fecha_incio": fecha_in,
                    "fecha_final": fecha_fin,
                    "multa": multa}
        
        MongoConnection.AddDocument(conexion, "Biblioteca", "Multas", document)
        return redirect('prestamo_url')
    
    return render(request, 'prestamos.html', context)

def login(request):
    client = MongoConnection.ConnectToMongo()
    if client:
        if request.method == 'POST':
            name = request.POST.get('name')
            doc = request.POST.get('password')
            filter_ = {
                "$and": [
                    {"documento": {"$regex": doc}},
                    {"nombre": {"$regex": name, "$options": "i"}}
                ]
            }

            results = MongoConnection.SearchDocuments(client, "Biblioteca", "estudiantes", filter_)
            resultsList = list(results)

            if len(resultsList) > 0:
                print("Conexion exitosa, bienvenid@:", name)
                results = MongoConnection.SearchDocuments(client, "Biblioteca", "estudiantes", filter_)
                estudiante_ids = [str(estudiante["_id"]) for estudiante in results]
                id_estudiante = estudiante_ids if estudiante_ids else 0
                request.session['estudiante_id'] = id_estudiante
                return redirect('menu_url')
            else:
                print("Tuki, no existe persona con ese nombre/documento")

            return render(request, "login.html")
        else:
            print("Error, no hubo method post(?)")
            return render(request, "login.html")
    else:
        #No hubo conexion :d
        print("Error conectandose a la db")
        return render(request, "login.html")

def registro(request):        
    conexion = MongoConnection.ConnectToMongo()

    db = conexion['Biblioteca']
    collection = db['PROGRAMAS']

    id_programas = db.PROGRAMAS.distinct('PROGRAMA')

    nombres = []

    for id_programa in id_programas:
        result = collection.find_one({'PROGRAMA': id_programa}, {'NOMBRE': 1})
        nombres.append(result['NOMBRE'])
    
    programas_data = zip(id_programas, nombres)

    context = {'programas_data': programas_data}
    
    if request.method == 'POST':
        db = conexion.Biblioteca
        last_document = db.estudiantes.find().sort("_id", -1).limit(1)
        doc_list = list(last_document)
        last_id = doc_list[0]["_id"] if len(doc_list) > 0 else 0
        new_id = last_id + 1
        document = {
            "_id": new_id,
            "id_estudiante": new_id,
            "documento": request.POST.get('doc_type') + "-" + request.POST.get('password'),
            "nombre": request.POST.get('name'),
            "direccion": request.POST.get('dir'),
            "programa": int(request.POST.get('programa')),
            "edad": int(request.POST.get('edad'))
        }
        MongoConnection.AddDocument(conexion, "Biblioteca", "estudiantes", document)
        return redirect('/')
    return render(request, 'register.html', context)

def menu(request):
    client = MongoConnection.ConnectToMongo()
    loggedStudentId = int(request.session['estudiante_id'][0])

    filter = {'id_estudiante': loggedStudentId}

    results = MongoConnection.SearchDocuments(client, "Biblioteca", "estudiantes", filter)

    context = {'student_name': results[0]['nombre'],}

    return render(request, 'menu.html', context)

def historial(request):
    estudiante_id = request.session['estudiante_id'][0]      
    client = MongoConnection.ConnectToMongo()
    db = client['Biblioteca']
    collection = db['Multas']
    collection2 = db['libro']
    prestados = collection.find()
    libros = []
    fechaInicial = []
    fechafinal = []
    multa = []
    for p in prestados:
        print("hola fooor")
        libros.append(p['libro_id'])
        fechaInicial.append(p['fecha_incio'])
        fechafinal.append(p['fecha_final'])
        multa.append(p['multa_id'])
                    
                
    print(fechafinal)           
                                
    libros_nombres = []
    for libro in libros:
            result = collection2.find_one({'ID:libro': libro}, {'NOMBRE': 1})
            libros.append(result['NOMBRE'])
                         
    data = zip((libros_nombres, fechaInicial, fechafinal, multa))     
    contex = {'data': data}

    return render(request, 'historial.html', contex)