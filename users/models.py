from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, cedula, telefono, carrera, semestre, categoria, password=None):
        if not email:
            raise ValueError('El usuario debe tener una dirección de correo electrónico')

        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono=telefono,
            carrera=carrera,
            semestre=semestre,
            categoria=categoria,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, cedula, telefono, carrera, semestre, categoria, password=None):
        user = self.create_user(
            email=email,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono=telefono,
            carrera=carrera,
            semestre=semestre,
            categoria=categoria,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    nombre = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el nombre.')]
    )
    apellido = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para el apellido.')]
    )
    email = models.EmailField(unique=True)  # Hace que el correo electrónico sea único
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener exactamente 10 dígitos y solo números.')]
    )
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'El teléfono debe tener exactamente 10 dígitos y solo números.')]
    )
    carrera = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Ingrese solo letras para la carrera.')]
    )
    semestre = models.IntegerField(
        validators=[MinValueValidator(0, "El semestre debe ser un número entre 0 y 10"), MaxValueValidator(10, "El semestre debe ser un número entre 0 y 10")]
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    categoria = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='user', blank=True)

    objects = CustomUserManager()  # Asociar el manager con el modelo

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cedula', 'telefono', 'carrera', 'semestre', 'categoria']

    def __str__(self):
        return self.email  

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
