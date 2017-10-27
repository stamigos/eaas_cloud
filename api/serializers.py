from rest_framework import serializers
from api.models import Group, Node, AlarmLog


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'



class NodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Node
		fields = ('id', 'running_state', 'target_energy', 'run_command')

class NodeUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Node
		fields = ('running_state', 'target_energy', 
			'current_energy', 'accumulated_energy', 'max_accumulated_energy',
			'minimum_energy_allowed', 'output_actuator_valve_position', 
			'input_actuator_valve_position', 'node_io_state')

class AlarmLogSerializer(serializers.ModelSerializer):
	fields = '__all__'
	
	class Meta:
		model = AlarmLog
		fields = '__all__'
