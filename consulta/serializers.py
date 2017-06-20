from .models import Consulta
from rest_framework import serializers


# Serializers define the API representation.
class ConsultaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consulta
        fields = ('nombre_consulta', 'activa')