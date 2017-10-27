import time
import json
from datetime import datetime

from rest_framework.exceptions import APIException, NotFound

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404


class BaseModel(models.Model):
	index = models.IntegerField(null=True)
	enabled = models.BooleanField(default=True)
	description = models.TextField(null=True)
	visible = models.BooleanField(default=True)
	send_to_influx_db = models.BooleanField(default=True)
	influx_db_retention_policy = models.TextField(null=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return '{model_name} (id={id})'.format(
			model_name=self.__class__.__name__, id=self.id
		)

	@classmethod
	def filter_user_group(cls, request, kwargs):
		"""
			Filter objects of model for
			particular group which belongs to current user
		"""
		return cls.objects.filter(group__id=kwargs['group_id'],
								  group__users__in=[request.user.id])

	# TODO: remove all to_dict(s)
	def to_dict(self):
		"""
		Convert object to dictonary where keys are names
		of attributes and values are values of attributes
		"""
		return dict((key, value) for key, value in self.__dict__.iteritems()
					if not callable(value)
					and not key.startswith('__')
					and not key.startswith('_s'))

	def serialize_to_dict(self):
		fields = json.loads(serialize('json', [self, ]))[0].get("fields")
		fields.update(dict(id=self.pk))
		return fields


class Group(BaseModel):
	users = models.ManyToManyField(User)


class Node(BaseModel):
	heartbeat_updated = models.DateTimeField()
	mac_address = models.CharField(max_length=255)
	public_ip = models.CharField(max_length=255)
	last_alarm = models.DateTimeField() 
	alarm_enable = models.BooleanField()
	timeout = models.IntegerField()
	group = models.ManyToManyField(Group)
	running_state = models.IntegerField()
	current_energy = models.FloatField()
	target_energy = models.FloatField()
	accumulated_energy = models.FloatField()
	max_accumulated_energy = models.FloatField()
	minimum_energy_allowed = models.FloatField()
	output_actuator_valve_position = models.FloatField()
	input_actuator_valve_position = models.FloatField()
	run_command = models.TextField(null=True)
	node_io_state = models.TextField(null=True)


class AlarmLog(BaseModel):
    last_alarm = models.DateTimeField()
    alarm_text = models.TextField()
    node = models.ForeignKey(Node)

    def to_dict(self):
        """
        Convert object to dictonary where keys are names
        of attributes and values are values of attributes
        """
        return dict((key, value) for key, value in self.__dict__.iteritems()
                    if not callable(value)
                    and not key.startswith('__')
                    and not key.startswith('_s'))

    def serialize_to_dict(self):
        fields = json.loads(serialize('json', [self, ]))[0].get("fields")
        fields.update(dict(id=self.pk))
        return fields


