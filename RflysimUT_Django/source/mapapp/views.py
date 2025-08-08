from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClickAirportSerializer, ClickNodeSerializer, ClickEdgeSerializer
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from source.air_road.models import Airports, Nodes, Permissions, Layers, Edges
from django.shortcuts import render
from source.proposal.models import Proposals
from source.flight_plan.models import FlightRequirements


class ClickAirportAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        serializer = ClickAirportSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            try:
                proposal = Proposals.objects.get(name='proposal')
                permission = Permissions.objects.get(name='permission')
                layer = Layers.objects.get(name='layer')
                node_sample = Nodes(proposal=proposal, name=serializer.data['name'][:-1]+',-120)', gps=serializer.data['name'],
                                    radius=1, layer=layer, permission=permission)
                node_sample.save()
                if not Airports.objects.filter(name=serializer.data['name']).exists():
                    airport_sample = Airports(proposal=proposal, entrance_node=node_sample, exit_node=node_sample, capacity=10,
                                              gps=serializer.data['name'], radius=10, permission=permission,
                                              name=serializer.data['name'])
                    airport_sample.save()
                else:
                    return Response({"success": False, "error": "该位置机场已存在"})
                return Response({"success": True})
            except Exception as e:
                return Response({"success": False, "error": str(e)})
        return Response({"success": False, "error": serializer.errors})


def map_view(request):
    airports = Airports.objects.all()
    airport_coordinates = [
        {'x': airport.gps.strip('()').split(',')[0], 'y': airport.gps.strip('()').split(',')[1]} for airport in airports
    ]
    nodes = Nodes.objects.all()
    node_coordinates = [
        {'x': node.gps.strip('()').split(',')[0], 'y': node.gps.strip('()').split(',')[1]} for node in nodes
    ]
    edges = Edges.objects.all()
    edge_coordinates = [
        edge.name for edge in edges
    ]
    return render(request, 'mapapp.html',
                  {'airport': airport_coordinates, 'node': node_coordinates, 'edge': edge_coordinates})


class ClickNodeAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        serializer = ClickNodeSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            try:
                proposal = Proposals.objects.get(name='proposal')
                permission = Permissions.objects.get(name='permission')
                layer = Layers.objects.get(name='layer')
                if Nodes.objects.filter(name=serializer.data['name'][:-1]+',-120)').exists():
                    return Response({"success": False, "error": "此位置节点已存在"})
                node_sample = Nodes(proposal=proposal, name=serializer.data['name'][:-1]+',-120)', gps=serializer.data['name'],
                                    radius=1, layer=layer, permission=permission)
                node_sample.save()
                return Response({"success": True})
            except Exception as e:
                return Response({"success": False, "error": str(e)})
        return Response({"success": False, "error": serializer.errors})


class ClickEdgeAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        serializer = ClickEdgeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # serializer.save()
                proposal = Proposals.objects.get(name='proposal')
                permission = Permissions.objects.get(name='permission')
                start_node = Nodes.objects.get(name=serializer.data['node1'][:-1]+',-120)')
                end_node = Nodes.objects.get(name=serializer.data['node2'][:-1]+',-120)')
                if (Edges.objects.filter(name=f"{start_node.name}to{end_node.name}").exists()
                        or Edges.objects.filter(name=f"{end_node.name}to{start_node.name}").exists()):
                    return Response({"success": False, "error": "此航路已存在"})
                edge_sample = Edges(proposal=proposal, name=f"{start_node.name}to{end_node.name}",
                                    gps=f"{start_node.gps}to{end_node.gps}",
                                    start_node=start_node, end_node=end_node,
                                    nodes=f"{serializer.data['node1'][:-1]+',-120)'};{serializer.data['node2'][:-1]+',-120)'}",
                                    length=1, height=1, width=1, permission=permission, volume=1,
                                    junction=0, rule=0)
                edge_sample.save()
                mid = start_node
                start_node = end_node
                end_node = mid
                edge_sample = Edges(proposal=proposal, name=f"{start_node.name}to{end_node.name}",
                                    gps=f"{start_node.gps}to{end_node.gps}",
                                    start_node=start_node, end_node=end_node,
                                    nodes=f"{serializer.data['node2'][:-1] + ',-120)'};{serializer.data['node1'][:-1] + ',-120)'}",
                                    length=1, height=1, width=1, permission=permission, volume=1,
                                    junction=0, rule=0)
                edge_sample.save()
                return Response({"success": True})
            except Exception as e:
                return Response({"success": False, "error": str(e)})
        return Response({"success": True, "error": serializer.errors})


class DeleteAirportAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        try:
            delete_airport = request.data['airport']
            delete_node = delete_airport[:-1] + ',-120)'
            Airports.objects.get(name=delete_airport).delete()
            Nodes.objects.get(name=delete_node).delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, "error": str(e)})


class DeleteNodeAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        try:
            delete_nodes = request.data['nodes']
            for delete_node in delete_nodes:
                delete_node = delete_node[:-1]+',-120)'
                Nodes.objects.get(name=delete_node).delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, "error": str(e)})


class DeleteEdgeAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        node1 = request.data['node1'][:-1]+',-120)'
        node2 = request.data['node2'][:-1]+',-120)'
        try:
            Edges.objects.get(name=f"{node1}to{node2}").delete()
        except Edges.DoesNotExist:
            return Response({'success': False, "error": '无法删除不存在的航路'})
        try:
            Edges.objects.get(name=f"{node2}to{node1}").delete()
        except Edges.DoesNotExist:
            return Response({'success': False, "error": '无法删除不存在的航路'})
        return Response({'success': True})


class DeleteAllAPIView(APIView):
    renderer_classes = [JSONRenderer]
    template_name = "mapapp.html"

    def post(self, request):
        if request.data['command'] == 'delete_all':
            try:
                Airports.objects.all().delete()
                Edges.objects.all().delete()
                Nodes.objects.all().delete()
                FlightRequirements.objects.all().delete()
                return Response({'success': True, 'message': 'All data cleared'})
            except Exception as e:
                return Response({'success': False, "error": str(e)})
        else:
            return Response({'success': False, "error": "删除失败"})
