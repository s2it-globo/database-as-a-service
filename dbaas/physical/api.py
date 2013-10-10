# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django_services.api import DjangoServiceAPI, register
from .service.node import NodeService
from .service.instance import InstanceService
from .service.plan import PlanService
from .service.engine import EngineService, EngineTypeService
from .serializers import NodeSerializer, InstanceSerializer, \
                        EngineSerializer, EngineTypeSerializer, PlanSerializer


class EngineTypeAPI(DjangoServiceAPI):
    serializer_class = EngineTypeSerializer
    service_class = EngineTypeService


class EngineAPI(DjangoServiceAPI):
    serializer_class = EngineSerializer
    service_class = EngineService


class PlanAPI(DjangoServiceAPI):
    serializer_class = PlanSerializer
    service_class = PlanService


class InstanceAPI(DjangoServiceAPI):

    serializer_class = InstanceSerializer
    service_class = InstanceService
    operations = ('list', 'retrieve', 'create', 'update', 'destroy')


class NodeAPI(DjangoServiceAPI):
    serializer_class = NodeSerializer
    service_class = NodeService


register('enginetype', EngineTypeAPI)
register('engine', EngineAPI)
register('plan', PlanAPI)
register('node', NodeAPI)
register('instance', InstanceAPI)
