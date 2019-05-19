# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from datetime import datetime, date, timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from django.db.models import Q
from .. import models, filter
from ..permissions import workorder as workoder_permission
from ..permissions import comment as comment_permission
from ..serializers import workorder as workoder_serializer
from ..serializers import comment as comment_serializer
from deveops.api import WebTokenAuthentication
from timeline.models import WorkOrderHistory
from timeline.decorator import decorator_base
from timeline.serializers.workorder import WorkOrderHistorySerializer
from django.conf import settings

__all__ = [
    'SceneWorkOrderCommentAPI', 'SceneWorkOrderCreateAPI',
    'SceneWorkOrderListAPI', 'SceneWorkOrderUpdateAPI', 'SceneWorkOrderMobileDetailAPI',
    'SceneWorkOrderActiveAPI', 'SceneWorkOrderAppointAPI', 'SceneWorkOrderDetailAPI', 'SceneWorkOrderDoneAPI'
]


class WorkOrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 60
    page_size_query_param = 'pageSize'
    page_query_param = 'current'


class SceneWorkOrderMobileDetailAPI(WebTokenAuthentication, generics.ListAPIView):
    permission_classes = [workoder_permission.WorkOrderListRequiredMixin, IsAuthenticated]
    queryset = models.WorkOrder.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user

        now = timezone.now().date()
        start_day = now - timedelta(days=1)
        end_day = now - timedelta(days=1)

        return Response(
            {
                'workorder_total_count': 36,
                'workorder_undone_count': 2,
                'full_name': user.full_name,
            }
            , status.HTTP_200_OK
        )


class SceneWorkOrderListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderSerializer
    queryset = models.WorkOrder.objects.all().order_by('create_time')
    permission_classes = [workoder_permission.WorkOrderListRequiredMixin, IsAuthenticated]
    pagination_class = WorkOrderPagination
    filter_class = filter.WorkOrderFilter


class SceneWorkOrderCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderSerializer
    permission_classes = [workoder_permission.WorkOrderCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.SceneWorkOrderCreateAPI

    @decorator_base(WorkOrderHistory, timeline_type=settings.TIMELINE_KEY_VALUE['WORKORDER_CREATE'])
    def create(self, request, *args, **kwargs):
        response = super(SceneWorkOrderCreateAPI, self).create(request, *args, **kwargs)
        obj = models.WorkOrder.objects.get(id=response.data['id'], uuid=response.data['uuid'])
        return [obj, ], self.msg.format(
            USER=request.user.full_name,
        ), response


class SceneWorkOrderUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderSerializer
    queryset = models.WorkOrder.objects.all()
    permission_classes = [workoder_permission.WorkOrderUpdateRequiredMixin, IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "pk"
    msg = settings.LANGUAGE.SceneWorkOrderUpdateAPI

    @decorator_base(WorkOrderHistory, timeline_type=settings.TIMELINE_KEY_VALUE['WORKORDER_UPDATE'])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.duty_user.id != request.user.id:
            return None, '', Response({'detail': settings.LANGUAGE.SceneWorkOrderNotAccept}, status=status.HTTP_406_NOT_ACCEPTABLE)
        response = super(SceneWorkOrderUpdateAPI, self).update(request, *args, **kwargs)
        return [obj, ], self.msg.format(
            USER=request.user.full_name,
        ), response


class SceneWorkOrderActiveAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderActiveSerializer
    queryset = models.WorkOrder.objects.all()
    permission_classes = [workoder_permission.WorkOrderUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.SceneWorkOrderActiveAPI

    @decorator_base(WorkOrderHistory, timeline_type=settings.TIMELINE_KEY_VALUE['WORKORDER_ACTIVE'])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super(SceneWorkOrderActiveAPI, self).update(request, *args, **kwargs)
        return [obj, ], self.msg.format(
            USER=request.user.full_name,
        ), response


class SceneWorkOrderAppointAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderAppointSerializer
    queryset = models.WorkOrder.objects.all()
    permission_classes = [workoder_permission.WorkOrderUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.SceneWorkOrderAppointAPI

    @decorator_base(WorkOrderHistory, timeline_type=settings.TIMELINE_KEY_VALUE['WORKORDER_APPOINT'])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.duty_user.id != request.user.id:
            return None, '', Response({'detail': settings.LANGUAGE.SceneWorkOrderNotAccept}, status=status.HTTP_406_NOT_ACCEPTABLE)
        new_duty_user = models.ExtendUser.objects.get(id=request.data['appoint'])
        response = super(SceneWorkOrderAppointAPI, self).update(request, *args, **kwargs)
        return [obj, ], self.msg.format(
            USER1=request.user.full_name,
            USER2=new_duty_user.full_name,
        ), response


class SceneWorkOrderDoneAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderDoneSerializer
    queryset = models.WorkOrder.objects.all()
    permission_classes = [workoder_permission.WorkOrderUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.SceneWorkOrderDoneAPI

    @decorator_base(WorkOrderHistory, timeline_type=settings.TIMELINE_KEY_VALUE['WORKORDER_DONE'])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.duty_user.id != request.user.id:
            return None, '', Response({'detail': settings.LANGUAGE.SceneWorkOrderNotAccept }, status=status.HTTP_406_NOT_ACCEPTABLE)
        response = super(SceneWorkOrderDoneAPI, self).update(request, *args, **kwargs)
        return [obj, ], self.msg.format(
            USER=request.user.full_name,
        ), response


class SceneWorkOrderDetailAPI(WebTokenAuthentication, generics.ListAPIView):
    permission_classes = [workoder_permission.WorkOrderListRequiredMixin, IsAuthenticated]
    queryset = models.WorkOrder.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "pk"

    def list(self, request, *args, **kwargs):
        obj = self.get_object()

        timeline_queryset = WorkOrderHistory.objects.filter(
            instances=obj
        ).order_by('-id')

        timeline_serializer = WorkOrderHistorySerializer(timeline_queryset, many=True)

        com_serializer = comment_serializer.CommentSerializer(obj.comments.order_by('create_time'), many=True)

        current_serializer = workoder_serializer.WorkOrderSerializer(obj,)

        order_queryset = models.WorkOrder.objects.filter(
            (~Q(phone='') & Q(phone=obj.phone))
            | (~Q(user='') & Q(user=obj.user))
            | (~Q(serial_number='') & Q(serial_number=obj.serial_number))
        ).exclude(id=obj.id).exclude(user='', phone='')[:10]

        order_serializer = workoder_serializer.WorkOrderSerializer(order_queryset, many=True)
        return Response(
            {
                'current': current_serializer.data,
                'timeline': timeline_serializer.data,
                'order': order_serializer.data,
                'comment': com_serializer.data,
            }, status.HTTP_200_OK
        )


class SceneWorkOrderCommentAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.WorkOrder
    serializer_class = workoder_serializer.WorkOrderCommentSerializer
    queryset = models.WorkOrder.objects.all()
    permission_classes = [comment_permission.CommentListRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'