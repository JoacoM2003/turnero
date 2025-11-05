from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Turno, Cancha, HorarioTurno
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from datetime import date, timedelta
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    """Vista principal con estadísticas si el usuario está autenticado"""
    context = {}
    if request.user.is_authenticated:
        # Obtener próximos turnos del usuario
        proximos_turnos = Turno.objects.filter(
            usuario=request.user,
            fecha__gte=date.today()
        ).select_related('cancha', 'horario').order_by('fecha', 'horario__hora_inicio')[:3]
        
        context['proximos_turnos'] = proximos_turnos
        context['total_reservas'] = Turno.objects.filter(usuario=request.user).count()
    
    return render(request, 'home.html', context)

def signup(request):
    """Registro de usuarios mejorado"""
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una sesión activa.")
        return redirect('home')
    
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Autenticar con el password sin hashear
        user = authenticate(
            username=form.cleaned_data['username'], 
            password=form.cleaned_data['password1']
        )
        if user:
            login(request, user)
            messages.success(request, f"¡Bienvenido {user.first_name}! Tu cuenta ha sido creada exitosamente.")
            return redirect('home')
    
    return render(request, 'sign/signup.html', {'form': form})

def signin(request):
    """Inicio de sesión mejorado"""
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una sesión activa.")
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f"¡Bienvenido de vuelta, {user.first_name or user.username}!")
            # Redirigir a la página que intentaba acceder o a home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Por favor, intenta de nuevo.")
    
    return render(request, 'sign/signin.html')

@login_required
def signout(request):
    """Cierre de sesión"""
    logout(request)
    messages.success(request, "Sesión cerrada correctamente. ¡Hasta pronto!")
    return redirect('home')

@login_required
def canchas(request):
    """Vista de canchas con búsqueda y filtros"""
    canchas_list = Cancha.objects.all().order_by('nombre')
    
    # Búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        canchas_list = canchas_list.filter(
            Q(nombre__icontains=search_query) | 
            Q(direccion__icontains=search_query)
        )
    
    # Filtro por tipo
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter:
        canchas_list = canchas_list.filter(tipo=tipo_filter)
    
    # Paginación
    paginator = Paginator(canchas_list, 9)  # 9 canchas por página
    page_number = request.GET.get('page')
    canchas = paginator.get_page(page_number)
    
    context = {
        'canchas': canchas,
        'search_query': search_query,
        'tipo_filter': tipo_filter,
    }
    return render(request, 'reservas/canchas.html', context)

@login_required
def agregar_cancha(request):
    """Agregar nueva cancha (solo superusuarios)"""
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para agregar canchas.")
        return redirect('home')
    
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            direccion = request.POST['direccion']
            tipo = request.POST['tipo']
            precio = request.POST['precio']
            imagen = request.FILES.get('imagen')
            
            cancha = Cancha.objects.create(
                nombre=nombre,
                direccion=direccion,
                tipo=tipo,
                precio=precio,
                imagen=imagen
            )
            messages.success(request, f"Cancha '{cancha.nombre}' agregada correctamente.")
            return redirect('canchas')
        except Exception as e:
            messages.error(request, f"Error al agregar la cancha: {str(e)}")
    
    return render(request, 'admin/agregar_cancha.html')

@login_required
def eliminar_cancha(request, cancha_id):
    """Eliminar cancha (solo superusuarios)"""
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar canchas.")
        return redirect('home')
    
    cancha = get_object_or_404(Cancha, id=cancha_id)
    nombre_cancha = cancha.nombre
    cancha.delete()
    messages.success(request, f"Cancha '{nombre_cancha}' eliminada correctamente.")
    return redirect('canchas')

@login_required
def detalle_cancha(request, cancha_id):
    """Vista detallada de cancha con turnos disponibles"""
    cancha = get_object_or_404(Cancha, id=cancha_id)
    fecha_str = request.GET.get('fecha', date.today().isoformat())
    
    try:
        fecha = parse_date(fecha_str)
        if not fecha:
            raise ValueError
    except:
        messages.error(request, "Fecha inválida.")
        return redirect('detalle_cancha', cancha_id=cancha_id)

    # No permitir fechas pasadas
    if fecha < date.today():
        messages.error(request, "No se pueden ver fechas anteriores a la actual.")
        return redirect('detalle_cancha', cancha_id=cancha_id)
    
    # Límite de 30 días en el futuro
    if fecha > date.today() + timedelta(days=30):
        messages.warning(request, "Solo puedes reservar turnos con hasta 30 días de anticipación.")
        fecha = date.today() + timedelta(days=30)
        fecha_str = fecha.isoformat()

    horarios = HorarioTurno.objects.all().order_by('hora_inicio')
    turnos_reservados = Turno.objects.filter(
        cancha=cancha, 
        fecha=fecha
    ).select_related('horario', 'usuario')
    
    horarios_reservados = [turno.horario.id for turno in turnos_reservados]
    horarios_reservados_usuario = [
        turno.horario.id 
        for turno in turnos_reservados 
        if turno.usuario == request.user
    ]
    
    # Crear diccionario de turnos reservados con información del usuario
    turnos_info = {
        turno.horario.id: {
            'usuario': turno.usuario.get_full_name() or turno.usuario.username,
            'es_mio': turno.usuario == request.user
        }
        for turno in turnos_reservados
    }

    context = {
        'cancha': cancha,
        'fecha': fecha_str,
        'fecha_obj': fecha,
        'horarios': horarios,
        'horarios_reservados': horarios_reservados,
        'horarios_reservados_usuario': horarios_reservados_usuario,
        'turnos_info': turnos_info,
    }
    return render(request, 'reservas/detalle_cancha.html', context)

@login_required
def reservar_turno(request):
    """Reservar turno con validaciones mejoradas"""
    if request.method == 'POST':
        try:
            cancha_id = request.POST.get('cancha_id')
            fecha_str = request.POST.get('fecha')
            horario_id = request.POST.get('horario_id')
            
            # Validaciones
            cancha = get_object_or_404(Cancha, id=cancha_id)
            horario = get_object_or_404(HorarioTurno, id=horario_id)
            fecha = parse_date(fecha_str)
            
            if fecha < date.today():
                messages.error(request, "No puedes reservar turnos en fechas pasadas.")
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Verificar si el turno ya está reservado
            if Turno.objects.filter(cancha=cancha, fecha=fecha, horario=horario).exists():
                messages.error(request, "Este turno ya está reservado. Por favor, elige otro.")
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Verificar si el usuario ya tiene una reserva en ese horario
            reserva_existente = Turno.objects.filter(
                usuario=request.user,
                fecha=fecha,
                horario=horario
            ).first()
            
            if reserva_existente:
                messages.warning(
                    request, 
                    f"Ya tienes una reserva para este horario en {reserva_existente.cancha.nombre}."
                )
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Crear la reserva
            turno = Turno.objects.create(
                cancha=cancha,
                fecha=fecha,
                horario=horario,
                usuario=request.user
            )
            
            messages.success(
                request, 
                f"¡Turno reservado exitosamente! {cancha.nombre} - {fecha} - {horario}"
            )
            
        except Exception as e:
            messages.error(request, f"Error al reservar el turno: {str(e)}")
        
        return redirect('detalle_cancha', cancha_id=cancha_id)
    
    return redirect('canchas')

@login_required
def cancelar_turno(request):
    """Cancelar turno reservado"""
    if request.method == 'POST':
        try:
            cancha_id = request.POST.get('cancha_id')
            fecha_str = request.POST.get('fecha')
            horario_id = request.POST.get('horario_id')
            
            fecha = parse_date(fecha_str)
            
            turno = Turno.objects.filter(
                cancha_id=cancha_id,
                fecha=fecha,
                horario_id=horario_id,
                usuario=request.user  # Solo puede cancelar sus propios turnos
            ).first()
            
            if turno:
                cancha_nombre = turno.cancha.nombre
                turno.delete()
                messages.success(
                    request, 
                    f"Turno cancelado correctamente en {cancha_nombre}."
                )
            else:
                messages.error(request, "No se encontró el turno o no tienes permiso para cancelarlo.")
            
        except Exception as e:
            messages.error(request, f"Error al cancelar el turno: {str(e)}")
        
        return redirect('detalle_cancha', cancha_id=cancha_id)
    
    return redirect('canchas')

@login_required
def mis_turnos(request):
    """Vista de turnos del usuario"""
    hoy = date.today()
    
    # Turnos próximos
    turnos_proximos = Turno.objects.filter(
        usuario=request.user,
        fecha__gte=hoy
    ).select_related('cancha', 'horario').order_by('fecha', 'horario__hora_inicio')
    
    # Historial (turnos pasados)
    turnos_pasados = Turno.objects.filter(
        usuario=request.user,
        fecha__lt=hoy
    ).select_related('cancha', 'horario').order_by('-fecha', '-horario__hora_inicio')[:10]
    
    context = {
        'turnos_proximos': turnos_proximos,
        'turnos_pasados': turnos_pasados,
    }
    return render(request, 'reservas/mis_turnos.html', context)