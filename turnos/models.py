from django.db import models
from django.contrib.auth.models import User

class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class HorarioTurno(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"

from django.contrib.auth.models import User

class Turno(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha = models.DateField()
    horario = models.ForeignKey(HorarioTurno, on_delete=models.CASCADE, related_name='turnos', null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cancha', 'fecha', 'horario')

    def __str__(self):
        return f"{self.cancha} | {self.fecha} | {self.horario} - {self.usuario.get_full_name()}"
