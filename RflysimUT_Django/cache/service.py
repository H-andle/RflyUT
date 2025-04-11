from source.proposal.models import Proposals
from source.flight_plan.models import FlightRequirements
from source.flight_plan.serializers import FlightRequirementsSerializer
from source.air_road.models import Edges, Nodes, Airports
from source.air_road.serializers import EdgesSerializer, NodesSerializer, AirportsSerializer
from source.uav.models import Drones
from source.uav.serializers import DronesSerializer
from source.experiment.models import Experiments
from constant import *
from cache_utils import *
import datetime

def simulation_luanch(proposal_id):
    try:
        proposal = Proposals.objects.get(id=proposal_id)        
    
    except Proposals.DoesNotExist:
        return f"Proposal with id {proposal_id} does not exist."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    if not proposal.status == PROPOSAL_STATUS_STOP:
        return f"Proposal {proposal.id} is already running."

    proposal.status = PROPOSAL_STATUS_LAUNCHING
    proposal.save()
    # logger.log(f"Proposal {proposal_id} start luanching.")
    
    simulation_luanch_cache(proposal)

    create_experiment(proposal)

def create_experiment(proposal:Proposals):
    experiment = Experiments()
    time_date = str(datetime.time)
    experiment.name = f'{proposal.name}:{time_date}'
    experiment.proposal = proposal
    experiment.save()

def simulation_end(proposal_id):
    proposal = Proposals.objects.get(id=proposal_id)
    if proposal.status == PROPOSAL_STATUS_STOP or proposal.status == PROPOSAL_STATUS_STOPING:
        return f"Proposal {proposal.id} is already stopped."
    
    experiment = Experiments.objects.filter(proposal=proposal).latest('start_time')
    save_expriment_data(experiment)
    simulation_end_cache(proposal_id)
    evaluation_calculate(experiment)

def evaluation_calculate(experiment):
    pass

############################ cache操作部分 #########################
def simulation_luanch_cache(proposal:Proposals):    
     
    load_proposal_cache(proposal.id,proposal.time)
    
def simulation_end_cache(proposal_id):
    empty_proposal_cache(proposal_id)


def load_proposal_cache(proposal_id, ex):
    
    load_airway_network(proposal_id=proposal_id,expire_time=ex)
    load_airports(proposal_id=proposal_id,expire_time=ex)
    load_drones(proposal_id=proposal_id,expire_time=ex)
    load_fligth_requirements(proposal_id=proposal_id,expire_time=ex)
    load_network_control(proposal_id=proposal_id,expire_time=ex)
    load_faults(proposal_id=proposal_id,expire_time=ex)

    # logger.log(f"Proposal {proposal_id} successfully loaded.")

def empty_proposal_cache(proposal_id):
    '''
        功能：清空redis中对应仿真实验的所有仿真数据
    '''
    pass

def load_airway_network(proposal_id, expire_time):
    try:
        airways = Edges.objects.filter(id=proposal_id)
                
        for airway in airways:        
            serializer = EdgesSerializer(airway,context={'redis_flag': True})
            data = serializer.data
            set_airway_to_cache(proposal_id=id, airway_id= airway.id, data = data, ex = expire_time)
    
    except Proposals.DoesNotExist:
        return f"Airway with proposal id {proposal_id} does not exist."
    
    try:
        nodes = Nodes.objects.filter(id=proposal_id)
                
        for node in nodes:
            serializer = NodesSerializer(node,context={'redis_flag': True})
            data = serializer.data
            set_node_to_cache(proposal_id=id, node_id= airway.id, data = data, ex = expire_time)
    
    except Proposals.DoesNotExist:
        return f"Node with proposal id {proposal_id} does not exist."
    

def load_airports(proposal_id, expire_time):
    try:
        airports = Airports.objects.filter(id=proposal_id)
        
        for uav in airports:
            serializer = AirportsSerializer(uav)
            data = serializer.data
            
            set_airport_to_cache(proposal_id=id, airport_id= uav.id, data = data, ex = expire_time)
    
    except Proposals.DoesNotExist:
        return f"Airport with proposal id {proposal_id} does not exist."

def load_drones(proposal_id, expire_time):
    try:
        uavs = Drones.objects.filter(id=proposal_id)
        
        for uav in uavs:
            serializer = DronesSerializer(uav,context={'redis_flag': True})
            data = serializer.data
            set_drone_to_cache(proposal_id=id, drone_id= uav.id, data = data, ex = expire_time)
    
    except Proposals.DoesNotExist:
        return f"UAV with proposal id {proposal_id} does not exist."
    
def load_fligth_requirements(proposal_id, expire_time):
    try:
        requirements = FlightRequirements.objects.filter(id=proposal_id)
        
        for requirement in requirements:
            serializer = FlightRequirementsSerializer(requirement,context={'redis_flag': True})
            data = serializer.data
            set_requirement_to_cache(proposal_id=id, requirement_id= requirement.id, data = data, ex = expire_time)
    
    except Proposals.DoesNotExist:
        return f"Requirement with proposal id {proposal_id} does not exist."

def load_network_control(proposal_id, expire_time):
    pass

def load_faults(proposal_id, expire_time):
    pass


def update_airway():
    pass

def update_uav():
    pass

def timing_to_terminate():
    pass
    
def save_expriment_data(experiment:Experiments):
    # save_airway_log()
    # save_uav_log()
    # save_system_log()
    pass