from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    monto_max= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # null si es categoría predeterminada
    es_predeterminada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Validar si es un gasto y supera el monto máximo de la categoría
        if self.tipo == 'gasto' and self.categoria.monto_max > 0:
            # Calcular el total de gastos actuales en la categoría
            gastos_actuales = Transaccion.objects.filter(
                usuario=self.usuario,
                categoria=self.categoria,
                tipo='gasto'
            ).aggregate(total=models.Sum('monto'))['total'] or 0

            # Verificar si el nuevo gasto supera el monto máximo
            if gastos_actuales + self.monto > self.categoria.monto_max:
                raise ValidationError(f"El gasto supera el monto máximo permitido para la categoría '{self.categoria.nombre}'.")

        # Guardar la transacción si pasa la validación
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.categoria})"

class Presupuesto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.IntegerField()  # 1-12
    anio = models.IntegerField()

    def __str__(self):
        return f"Presupuesto {self.categoria} - {self.mes}/{self.anio}"

# (opcional) Para datos adicionales del usuario
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moneda_predeterminada = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return self.user.username
    

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['monto', 'tipo', 'categoria', 'fecha', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
