"""RflysimUT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from source.air_road import url as air_road_url
from source.evaluation import url as evaluation_url
from source.flight_plan import url as flight_plan_url
from source.proposal import url as proposal_url
from source.road_control import url as road_control_url
from source.uav import url as uav_url
from source.uav_fault import url as uav_fault_url
from source.experiment import url as experiment_url
from source.mapapp import url as mapapp_url
#在urls.pyh中新增如下代码

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(air_road_url)),    
    path('', include(flight_plan_url)),
    path('', include(evaluation_url)),
    path('', include(proposal_url)),
    path('', include(road_control_url)),
    path('', include(uav_url)),
    path('', include(uav_fault_url)),
    path('', include(experiment_url)),
    path('', include(mapapp_url)),
    # path('docs/', include_docs_urls(title='平台接口文档',description='接口文档平台'))
]


