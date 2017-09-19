# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.forms
#
# Formulario correspondiente a la aplicación participación
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput
)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from base.fields import CedulaField
from base.functions import (
    cargar_entidad, cargar_municipios, cargar_parroquias,
    validate_cedula, validate_email
    )
from base.models import Municipio, Parroquia
from .models import Perfil
from captcha.fields import CaptchaField

from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    """!
    Clase del formulario de logeo

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-03-2017
    @version 1.0.0
    """
    ## Campo de la constraseña
    contrasena = CharField()

    ## Nombre del usuario
    usuario = CharField()

    ## Formulario de recordarme
    remember_me = BooleanField()

    ## Campo del captcha
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['contrasena'].widget = PasswordInput()
        self.fields['contrasena'].widget.attrs.update({'class': 'validate',
        'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'class': 'validate',
        'placeholder': 'Nombre de Usuario'})
        self.fields['remember_me'].label = "Recordar"
        self.fields['remember_me'].widget = CheckboxInput()
        self.fields['remember_me'].required = False
        self.fields['captcha'].label = "Captcha"
        self.fields['captcha'].widget.attrs.update({'class': 'validate'})

    def clean(self):
        """!
        Método que valida si el usuario a autenticar es valido

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 21-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con los errores
        """
        usuario = self.cleaned_data['usuario']
        contrasena = self.cleaned_data['contrasena']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verifique su usuario o contraseña"
            self.add_error('usuario', msg)

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me')


class UserRegisterForm(forms.ModelForm):
    """!
    Formulario de Registro

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        # Si se ha seleccionado un estado establece el listado de municipios y elimina el atributo disable
        if 'estado' in self.data and self.data['estado']:
            self.fields['municipio'].widget.attrs.pop('disabled')
            self.fields['municipio'].queryset=Municipio.objects.filter(entidad=self.data['estado'])

            # Si se ha seleccionado un municipio establece el listado de parroquias y elimina el atributo disable
            if 'municipio' in self.data and self.data['municipio']:
                self.fields['parroquia'].widget.attrs.pop('disabled')
                self.fields['parroquia'].queryset=Parroquia.objects.filter(municipio=self.data['municipio'])

        self.fields['estado'].choices = cargar_entidad()
        self.fields['municipio'].choices = cargar_municipios()
        self.fields['parroquia'].choices = cargar_parroquias()


    ## Nombre de usuario
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(),
        label="Nombre de Usuario"
        )

    ## Contraseña
    password = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Constraseña"
        )

    ## Repita la Contraseña
    password_repeat = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Repita su constraseña"
        )

    ## nombre
    nombre = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Nombre"
        )

    ## apellido
    apellido = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Apellido"
        )

    ## correo
    email = forms.EmailField(
        widget=forms.TextInput(),
        label="Correo"
        )

    ## cedula
    cedula = CedulaField()

    ## estado
    estado = forms.ChoiceField(widget=forms.Select(attrs={
        'onchange': "actualizar_combo(this.value,'base','Municipio','entidad','codigo','nombre','id_municipio');$('select').material_select();"}))

    ## municipio
    municipio = forms.ChoiceField(widget=forms.Select(attrs={'disabled':'disabled',
        'onchange': "actualizar_combo(this.value,'base','Parroquia','municipio','codigo','nombre','id_parroquia');$('select').material_select();"}))

    ## parroquia
    parroquia = forms.ChoiceField(widget=forms.Select(attrs={'disabled':'disabled'}))

    ## Campo del captcha
    captcha = CaptchaField()

    def clean_password_repeat(self):
        """!
        Método que valida si las contraseñas coinciden

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if(password_repeat!=password):
            raise forms.ValidationError("La contraseña no coincide")
        return password_repeat

    def clean_cedula(self):
        """!
        Método que valida si la cedula es única

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        cedula = self.cleaned_data['cedula']
        if(validate_cedula(cedula)):
            raise forms.ValidationError("La cédula ingresada ya existe")
        return cedula

    def clean_email(self):
        """!
        Método que valida si el correo es única

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        email = self.cleaned_data['email']
        if(validate_email(email)):
            raise forms.ValidationError("El correo ingresado ya existe")
        return email

    class Meta:
        model = User
        exclude = ['is_staff','is_active','date_joined']

class PerfilForm(forms.ModelForm):
    """!
    Formulario del perfil

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 24-04-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(PerfilForm, self).__init__(*args, **kwargs)

        self.fields['estado'].choices = cargar_entidad()
        self.fields['municipio'].choices = cargar_municipios()
        self.fields['parroquia'].choices = cargar_parroquias()

    ## cedula
    cedula = CedulaField()

    ## estado
    estado = forms.ChoiceField(widget=forms.Select(attrs={
        'onchange': "actualizar_combo(this.value,'base','Municipio','entidad','codigo','nombre','id_municipio');$('select').material_select();"}))

    ## municipio
    municipio = forms.ChoiceField(widget=forms.Select(attrs={
        'onchange': "actualizar_combo(this.value,'base','Parroquia','municipio','codigo','nombre','id_parroquia');$('select').material_select();"}))

    ## parroquia
    parroquia = forms.ChoiceField(widget=forms.Select())

    class Meta:
        model = Perfil
        exclude = ['user','parroquia']


class PasswordResetForm(PasswordResetForm):
    """!
    Clase del formulario de resetear contraseña

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 02-05-2017
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Correo'})

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get("email")

        if email:
            msg = "Error no existe el email"
            try:
                User.objects.get(email=email)
            except:
                self.add_error('email', msg)



class PasswordConfirmForm(SetPasswordForm):
    """!
    Formulario para confirmar la constraseña

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 15-05-2017
    @version 1.0.0
    """
    def __init__(self, *args, **kwargs):
        super(PasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'input-field',
                                                  'placeholder': 'Contraseña Nueva'})
        self.fields['new_password2'].widget.attrs.update({'class': 'input-field',
                                                  'placeholder': 'Repita su Contraseña'})

class UserForm(forms.Form):
    ## Nombre de usuario
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(),
        label="Nombre de Usuario"
        )

    ## Contraseña
    password = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Constraseña"
        )

    ## Repita la Contraseña
    password_repeat = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'type':'password'}),
        label="Repita su constraseña"
        )

    ## nombre
    nombre = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Nombre"
        )

    ## apellido
    apellido = forms.CharField(max_length=100,
        widget=forms.TextInput(),
        label="Apellido"
        )

    ## correo
    email = forms.EmailField(
        widget=forms.TextInput(),
        label="Correo"
        )

    cedula = forms.CharField(max_length=9,
        validators=[RegexValidator(
            regex='^[V|E][0-9]{7,8}',
            message='La cédula no está en el formato indicado'
            )],
        label="Cedula"
        )

    # validations
    def clean_password_repeat(self):
        """!
        Método que valida si las contraseñas coinciden

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        print("******clean_password_repeat")
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if(password_repeat!=password):
            raise forms.ValidationError("La contraseña no coincide")
        return password_repeat

    def clean_cedula(self):
        """!
        Método que valida si la cedula es única

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        cedula = self.cleaned_data['cedula']
        if(validate_cedula(cedula)):
            raise forms.ValidationError("La cédula ingresada ya existe")
        return cedula

    def clean_email(self):
        """!
        Método que valida si el correo es única

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        email = self.cleaned_data['email']
        if(validate_email(email)):
            raise forms.ValidationError("El correo ingresado ya existe")
        return email


    def validate(self, data):
        print(data)
        return data
