### views.py
import requests
from django.shortcuts import render

def productos_aliados(request):
    query = request.GET.get('q', '')
    url = 'http://localhost:8001/courses/'
    if query:
        url += f'?search={query}'

    try:
        response = requests.get(url)
        cursos = response.json()
    except Exception as e:
        cursos = []
        print("Error al consumir API:", e)

    return render(request, 'productos_aliados.html', {'cursos': cursos, 'query': query})

def detalle_curso(request, id):
    try:
        response = requests.get(f'http://localhost:8001/courses/{id}/')
        curso = response.json()
    except Exception as e:
        curso = None
        print("Error al obtener el detalle del curso:", e)

    return render(request, 'curso_detalle.html', {'curso': curso})
