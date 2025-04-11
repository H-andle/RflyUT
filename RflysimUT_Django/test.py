from django.conf import settings
import os
import django

# 设置环境变量，指向你的 Django 配置文件（例如 RflysimUT.settings）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RflysimUT.settings")

# 初始化 Django
django.setup()

from source.mapapp.models import ClickAirport, ClickNode, ClickEdge
from source.air_road.models import Airports, Edges, Nodes
from source.proposal.models import Proposals
from source.flight_plan.models import FlightRequirements

