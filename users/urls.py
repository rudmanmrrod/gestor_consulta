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
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.0
from django.conf.urls import url
from django.contrib.auth.views import *
from .forms import PasswordResetForm, PasswordConfirmForm
from .views import *
from users import views

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name = "login"),
    url(r'^logout$', LogoutView.as_view(), name = "logout"),
    url(r'^register$', RegisterView.as_view(), name = "register"),
    url(r'^update/(?P<pk>\d+)$', PerfilUpdate.as_view(), name = "update"),
    url(r'^password/reset/$', password_reset,
        {'post_reset_redirect': '/password/done/',
         'template_name': 'user.reset.html', 'password_reset_form':PasswordResetForm}, name="reset"),
    url(r'^password/done/$', password_reset_done,
        {'template_name': 'user.passwordreset.done.html'},
        name='reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'user.passwordreset.confirm.html', 'set_password_form':PasswordConfirmForm,
         'post_reset_redirect': '/password/end/'},
        name='password_reset_confirm'),
    url(r'^password/end/$', password_reset_done,
        {'template_name': 'user.passwordreset.end.html'},
        name='reset_end'),
]
