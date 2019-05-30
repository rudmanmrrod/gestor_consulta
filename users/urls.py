# -*- coding: utf-8 -*-
"""
Sistema de Consulta Pública

Copyleft (@) 2017 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/wiki/ModeladoTopicos_2017
"""
## @package participacion.urls
#
# Urls de la aplicación participacion
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
# @version 1.0
from django.urls import path
from django.contrib.auth.views import *
from .forms import PasswordResetForm, PasswordConfirmForm
from .views import *
from users import views

urlpatterns = [
    path('login', LoginView.as_view(), name = "login"),
    path('logout', LogoutView.as_view(), name = "logout"),
    path('register', RegisterView.as_view(), name = "register"),
    path('update/<int:pk>', PerfilUpdate.as_view(), name = "update"),
]
"""path('password/reset/', password_reset,
    {'post_reset_redirect': '/password/done/',
     'template_name': 'user.reset.html', 'password_reset_form':PasswordResetForm}, name="reset"),
path('password/done/', password_reset_done,
    {'template_name': 'user.passwordreset.done.html'},
    name='reset_done'),
path('password/reset/<slug:uidb64>-<slug:token>/',
    password_reset_confirm,
    {'template_name': 'user.passwordreset.confirm.html', 'set_password_form':PasswordConfirmForm,
     'post_reset_redirect': '/password/end/'},
    name='password_reset_confirm'),
path('password/end/', password_reset_done,
    {'template_name': 'user.passwordreset.end.html'},
    name='reset_end'),"""
