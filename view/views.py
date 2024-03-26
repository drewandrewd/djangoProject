# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from model.models import Position, Employee
import json


def positions_list(request):
    positions = Position.objects.all()
    data = [{'id': pos.id, 'name': pos.name, 'category': pos.category} for pos in positions]
    return JsonResponse(data, safe=False)


@csrf_protect
def add_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        category = data.get('category')
        if name and category:
            position = Position.objects.create(name=name, category=category)
            return JsonResponse({'id': position.id, 'name': position.name, 'category': position.category})
    return JsonResponse({'error': 'Invalid data'})


@csrf_protect
def edit_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)

    if request.method == 'POST':
        # Получаем данные из POST-запроса
        name = request.POST.get('name')
        category = request.POST.get('category')

        if name and category:
            # Обновляем поля должности
            position.name = name
            position.category = category
            position.save()
            # Возвращаемся на страницу с деталями должности
            return redirect('position_detail', position_id=position.id)
    else:
        # Если это GET-запрос, просто отображаем форму редактирования
        return render(request, 'position_detail.html', {'position': position})
# def edit_position(request, position_id):
#     position = Position.objects.get(id=position_id)
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         name = data.get('name')
#         category = data.get('category')
#         if name and category:
#             position.name = name
#             position.category = category
#             position.save()
#             return JsonResponse({'id': position.id, 'name': position.name, 'category': position.category})
#     return JsonResponse({'error': 'Invalid data'})


def delete_position(request, position_id):
    position = Position.objects.get(id=position_id)
    position.delete()
    return JsonResponse({'success': True})


def employees_list(request):
    employees = Employee.objects.all()
    data = [
        {'id': emp.id, 'full_name': emp.full_name, 'gender': emp.gender, 'age': emp.age, 'position': emp.position.name,
         'category': emp.position.category} for emp in employees]
    return JsonResponse(data, safe=False)


@csrf_protect
def add_employee(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('full_name')
        gender = data.get('gender')
        age = data.get('age')
        position_id = data.get('position_id')
        if full_name and gender and age and position_id:
            position = Position.objects.get(id=position_id)
            employee = Employee.objects.create(full_name=full_name, gender=gender, age=age, position=position)
            return JsonResponse(
                {'id': employee.id, 'full_name': employee.full_name, 'gender': employee.gender, 'age': employee.age,
                 'position': employee.position.name, 'category': employee.position.category})
    return JsonResponse({'error': 'Invalid data'})


# @csrf_protect
# def edit_employee(request, employee_id):
#     employee = Employee.objects.get(id=employee_id)
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         full_name = data.get('full_name')
#         gender = data.get('gender')
#         age = data.get('age')
#         position_id = data.get('position_id')
#         if full_name and gender and age and position_id:
#             position = Position.objects.get(id=position_id)
#             employee.full_name = full_name
#             employee.gender = gender
#             employee.age = age
#             employee.position = position
#             employee.save()
#             return JsonResponse(
#                 {'id': employee.id, 'full_name': employee.full_name, 'gender': employee.gender, 'age': employee.age,
#                  'position': employee.position.name, 'category': employee.position.category})
#     return JsonResponse({'error': 'Invalid data'})


def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return JsonResponse({'success': True})


def position_detail(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    return render(request, 'position_detail.html', {'position': position})


@csrf_protect
def view_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'GET':
        return JsonResponse(
            {'id': employee.id, 'full_name': employee.full_name, 'gender': employee.gender, 'age': employee.age,
             'position': employee.position.name, 'category': employee.position.category})
    elif request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('full_name')
        gender = data.get('gender')
        age = data.get('age')
        position_id = data.get('position_id')
        if full_name and gender and age and position_id:
            position = Position.objects.get(id=position_id)
            employee.full_name = full_name
            employee.gender = gender
            employee.age = age
            employee.position = position
            employee.save()
            return JsonResponse(
                {'id': employee.id, 'full_name': employee.full_name, 'gender': employee.gender, 'age': employee.age,
                 'position': employee.position.name, 'category': employee.position.category})
    return JsonResponse({'error': 'Invalid data'})


# Шаблоны и отображения интерфейса:
def index(request):
    employees = Employee.objects.all()  # Получаем список всех сотрудников
    return render(request, 'index.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    positions = Position.objects.all()
    return render(request, 'employee_detail.html', {'employee': employee, 'positions': positions})

def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    positions = Position.objects.all()  #Все должности для выпадающего списка
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        position_id = request.POST.get('position_id')
        if full_name and gender and age and position_id:
            position = get_object_or_404(Position, id=position_id)
            employee.full_name = full_name
            employee.gender = gender
            employee.age = age
            employee.position = position
            employee.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        #Отображение формы редактирования
        return render(request, 'employee_detail.html', {'employee': employee, 'positions': positions})
