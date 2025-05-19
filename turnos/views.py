from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Turno, Cancha, HorarioTurno
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from datetime import date
from django.utils.dateparse import parse_date

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(request, user)
        messages.success(request, "Te has registrado exitosamente.")
        return redirect('home')
    return render(request, 'sign/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, "Sesión iniciada correctamente.")
            return redirect('home')
        messages.error(request, "Usuario o contraseña inválidos.")
    return render(request, 'sign/signin.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('home')

@login_required
def canchas(request):

    canchas = Cancha.objects.all()
    return render(request, 'reservas/canchas.html', {'canchas': canchas})

@login_required
def agregar_cancha(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para agregar canchas.")
        return redirect('home')
    if request.method == 'POST':
        print(request.POST)
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        tipo = request.POST['tipo']
        precio = request.POST['precio']
        imagen = request.FILES.get('imagen')
        cancha = Cancha.objects.create(nombre=nombre, direccion=direccion, tipo=tipo, precio=precio, imagen=imagen)
        cancha.save()
        messages.success(request, "Cancha agregada correctamente.")
        return redirect('canchas')
    return render(request, 'admin/agregar_cancha.html')

@login_required
def eliminar_cancha(request, cancha_id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar canchas.")
        return redirect('home')
    cancha = get_object_or_404(Cancha, id=cancha_id)
    cancha.delete()
    messages.success(request, "Cancha eliminada correctamente.")
    return redirect('canchas')

@login_required
def detalle_cancha(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    fecha_str = request.GET.get('fecha', date.today().isoformat())
    fecha = parse_date(fecha_str)

    if fecha < date.today():
        messages.error(request, "No se pueden ver fechas anteriores a la actual.")
        return redirect('detalle_cancha', cancha_id=cancha_id)

    horarios = HorarioTurno.objects.all().order_by('hora_inicio')
    turnos_reservados = Turno.objects.filter(cancha=cancha, fecha=fecha)
    horarios_reservados = [turno.horario.id for turno in turnos_reservados]

    turnos_reservados_usuario = Turno.objects.filter(cancha=cancha, fecha=fecha, usuario=request.user)
    horarios_reservados_usuario = [turno.horario.id for turno in turnos_reservados_usuario]

    return render(request, 'reservas/detalle_cancha.html', {
        'cancha': cancha,
        'fecha': fecha_str,
        'horarios': horarios,
        'horarios_reservados': horarios_reservados,
        'horarios_reservados_usuario': horarios_reservados_usuario,
    })


@login_required
def reservar_turno(request):
    if request.method == 'POST':
        cancha_id = request.POST['cancha_id']
        fecha = request.POST['fecha']
        horario_id = request.POST['horario_id']
        user = request.user

        turno = Turno.objects.create(cancha_id=cancha_id, fecha=fecha, horario_id=horario_id, usuario=user)
        turno.save()
        messages.success(request, "Turno reservado correctamente.")
        return redirect('detalle_cancha', cancha_id=cancha_id)

    
@login_required
def cancelar_turno(request):
    if request.method == 'POST':
        cancha_id = request.POST['cancha_id']
        fecha = request.POST['fecha']
        horario_id = request.POST['horario_id']

        turno = Turno.objects.get(cancha_id=cancha_id, fecha=fecha, horario_id=horario_id)
        turno.delete()
        messages.success(request, "Turno cancelado correctamente.")
        return redirect('canchas')
    
