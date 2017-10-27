"""eaas_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^groups/$', views.GroupsListView.as_view(), name='groups_list'),
    url(r'^groups/(?P<group_id>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
    url(r'^nodes/$', views.NodesListView.as_view(), name='nodes_list'),
    url(r'^nodes/(?P<node_id>\d+)/$', views.NodeDetailView.as_view({'get': 'retrieve', 'put': 'put'}), name='node_detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
