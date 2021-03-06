# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from logical import models
from physical.models import Plan, Environment


class DatabaseSerializer(serializers.HyperlinkedModelSerializer):
    plan = serializers.HyperlinkedRelatedField(
        source='plan', read_only=True, view_name='plan-detail', queryset=Plan.objects)
    environment = serializers.HyperlinkedRelatedField(
        source='environment', read_only=True, view_name='environment-detail', queryset=Environment.objects)
    endpoint = serializers.Field(source='endpoint')
    quarantine_dt = serializers.Field(source='quarantine_dt')
    total_size_in_bytes = serializers.Field(source='total_size')
    used_size_in_bytes = serializers.Field(source='used_size')

    class Meta:
        model = models.Database
        fields = ('url', 'id', 'name', 'endpoint', 'plan', 'environment', 'project',
            'quarantine_dt', 'total_size_in_bytes', 'used_size_in_bytes', 'credentials')
        read_only = ('credentials',)

    def __init__(self, *args, **kwargs):
        super(DatabaseSerializer, self).__init__(*args, **kwargs)
        
        request = self.context.get('request', None)
        if request:
            creating = request.method == 'POST'

            # when database is created, user can't change plan, environment and name
            self.fields['plan'].read_only = not creating
            self.fields['environment'].read_only = not creating
            self.fields['name'].read_only = not creating
            self.fields['credentials'].read_only = True

        # quarantine is always readonly
        # self.fields['quarantine_dt'].read_only = True


class DatabaseAPI(viewsets.ModelViewSet):
    """
    *   ### __List databases__

        __GET__ /api/database/

    *   ### __To create a new database__

        __POST__ /api/database/

            {
                "name": "{name}",
                "plan": "{api_url}/plan/{plan_id}/",
                "environment": "{api_url}/environment/{environment_id}/",
                "project": "{api_url}/project/{project_id}/"
            }

    *   ### __Show details about a database__

        __GET__ /api/database/`database_id`/

    *   ### __To delete a database (will put it on quarantine)__

        __DELETE__ /api/database/`database_id`/

    *   ### __To change database project__

        __PUT__ /api/database/`database_id`/

            {
                "project": "{api_url}/project/{project_id}/"
            }

    """
    serializer_class = DatabaseSerializer
    queryset = models.Database.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            data = serializer.restore_fields(request.DATA, request.FILES)
            self.object = models.Database.provision(data['name'], data['plan'], data['environment'])
            data = serializer.to_native(self.object)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(data)
            return Response(data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
