from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    tipo = models.PositiveSmallIntegerField(null=True, blank=True)
    precio = models.PositiveIntegerField(null=True, blank=True)
    imagen = models.ImageField(upload_to='canchas', null=True, blank=True)

    def __str__(self):
        return self.nombre


class HorarioTurno(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['hora_inicio']

    def __str__(self):
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"


class Turno(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha = models.DateField()
    horario = models.ForeignKey(HorarioTurno, on_delete=models.CASCADE, related_name='turnos', null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='confirmado')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ('cancha', 'fecha', 'horario')
        ordering = ['fecha', 'horario']

    def __str__(self):
        nombre_usuario = self.usuario.get_full_name() or self.usuario.username
        return f"{self.cancha} | {self.fecha} | {self.horario} - {nombre_usuario}"

    def clean(self):
        if Turno.objects.filter(
            cancha=self.cancha,
            fecha=self.fecha,
            horario=self.horario
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Este turno ya está reservado para esa cancha, fecha y horario.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
