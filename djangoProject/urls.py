from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from view import views

urlpatterns = [
    path('positions/', views.positions_list, name='positions_list'),
    path('positions/add/', views.add_position, name='add_position'),
    path('positions/<int:position_id>/edit/', views.edit_position, name='edit_position'),
    path('positions/<int:position_id>/delete/', views.delete_position, name='delete_position'),
    #path('positions/<int:position_id>/', views.view_position, name='view_position'),
    path('positions/<int:position_id>/', views.position_detail, name='position_detail'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employees/<int:employee_id>/', views.view_employee, name='view_employee'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('', views.index, name='index'),  # пустой путь для главной страницы
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
