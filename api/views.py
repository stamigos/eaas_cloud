from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework import viewsets

from api.models import Group, Node, AlarmLog
from api.serializers import GroupSerializer, NodeSerializer, NodeUpdateSerializer, AlarmLogSerializer


class GroupsListView(generics.ListAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)
	serializer_class = GroupSerializer

	def get_queryset(self):
		return get_list_or_404(Group.objects.filter(users__in=[self.request.user.id]))


class GroupDetailView(generics.RetrieveAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)
	serializer_class = GroupSerializer

	def retrieve(self, request, *args, **kwargs):
		instance = Group.objects.filter(users__in=[self.request.user.id],
									   pk=kwargs['group_id']).first()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)


class NodesListView(generics.ListAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)
	serializer_class = NodeSerializer

	def get_queryset(self):
		return get_list_or_404(Node.objects.all())


class NodeDetailView(viewsets.ModelViewSet):
	authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_serializer_class(self):
		if self.action == 'put':
			return NodeUpdateSerializer
		if self.action == 'retrieve':
			return NodeSerializer
		return NodeSerializer

	def retrieve(self, request, *args, **kwargs):
		instance = Node.objects.filter(pk=kwargs['node_id']).first()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def put(self, request, node_id, format=None):
		node = Node.objects.filter(pk=node_id).first()
		node.running_state = self._verify_field("running_state")
		node.current_energy = self._verify_field("current_energy")
		node.target_energy = self._verify_field("target_energy")
		node.accumulated_energy = self._verify_field("accumulated_energy")
		node.max_accumulated_energy = self._verify_field("max_accumulated_energy")
		node.minimum_energy_allowed = self._verify_field("minimum_energy_allowed")
		node.output_actuator_valve_position = self._verify_field("output_actuator_valve_position")
		node.input_actuator_valve_position = self._verify_field("input_actuator_valve_position")
		node.node_io_state = self._verify_field("node_io_state")
		node.save()

		serializer = NodeUpdateSerializer(node)
		return Response(serializer.data)

	def _verify_field(self, field):
		if not self.request.data.get(field):
			raise Exception("{} required".format(field))
		return self.request.data.get(field)




