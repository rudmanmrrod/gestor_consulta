from rest_framework.routers import DefaultRouter
from consulta.rest import ConsultaViewSet

router = DefaultRouter()
# ------------------------------------------
router.register(r'consulta', ConsultaViewSet, 'consulta')
