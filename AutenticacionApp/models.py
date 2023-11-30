from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ('', 'Selecciona el tipo de usuario'),  # Opción en blanco
        ('cliente_externo', 'Cliente externo'),
        ('comerciante_local', 'Comerciante local'),
        ('productor', 'Productor'),
        ('consultor', 'Consultor'),
        ('transportista', 'Transportista'),
        
    )

    tipo_usuario = models.CharField(
        max_length=50,
        choices=TIPO_USUARIO_CHOICES,
        default='',
        blank=True,
        verbose_name="Tipo de Usuario"
    )
    
    # Nuevo campo para la imagen de perfil
    profile_picture = models.ImageField(
        upload_to='usuarios/',  # Define la carpeta donde se guardarán las imágenes
        null=True,
        blank=True,
        verbose_name="Imagen de Perfil"
    )

    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superusuario"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario Personalizado"
        verbose_name_plural = "Usuarios Personalizados"
