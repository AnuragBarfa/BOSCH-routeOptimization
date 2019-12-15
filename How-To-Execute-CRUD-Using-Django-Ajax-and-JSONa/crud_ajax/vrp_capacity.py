# [START import]
from __future__ import print_function
from functools import partial
from six.moves import xrange
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
# [END import]


# [START data_model]
def create_data_model(inputData):
    # datamatrix,psngr_no,buscap,num_vehicles
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix']=inputData['distance_matrix']
    data['demands']=inputData['passengerCount']
    # data['demands'][0]=0
    # data['demands'][1]=0
    data['vehicle_capacities']=inputData['busCapacity']
    data['num_vehicles'] = len(inputData['busCapacity'])
    data['time_per_demand_unit'] = .5 
    data['lower_stop']  = 1
    data['num_locations'] = len(inputData['distance_matrix'])
    data['starts'] = inputData['starts']
    data['ends'] = inputData['ends']
    data['time_windows'] = inputData['time_windows']
    data['soft_time_windows'] = inputData['soft_time_windows']
    data['max_allowed_time']  = inputData['max_allowed_time']
    data['vehicle_speed'] = 830  # Travel speed: 5km/h converted in m/min
    data['drop_penalty'] = 80000
    data['min_occ_penalty'] = 20000
    data['soft_time_penalty'] = 2000
    return data
    # [END data_model]

def create_time_evaluator(data):
    """Creates callback to get total times between locations."""

    def service_time(data, node):
        """Gets the service time for the specified location."""
        return data['lower_stop'] + data['demands'][node] * data['time_per_demand_unit']

    def travel_time(data, from_node, to_node):
        """Gets the travel times between two locations."""
        if from_node == to_node:
            travel_time = 0
        else:
            # travel_time = manhattan_distance(data['locations'][from_node], data[
            #     'locations'][to_node]) / data['vehicle_speed']
            travel_time = data['distance_matrix'][from_node][to_node]/data['vehicle_speed']
        return travel_time

    _total_time = {}
    # precompute total time to have time callback in O(1)
    for from_node in xrange(data['num_locations']):
        _total_time[from_node] = {}
        for to_node in xrange(data['num_locations']):
            if from_node == to_node:
                _total_time[from_node][to_node] = 0
            else:
                _total_time[from_node][to_node] = int(
                    service_time(data, from_node) + travel_time(
                        data, from_node, to_node))

    def time_evaluator(manager, from_node, to_node):
        """Returns the total time between the two nodes"""
        return _total_time[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return time_evaluator

def add_time_window_constraints(routing, manager, data, time_evaluator_index):
    """Add Global Span constraint"""
    time = 'Time'
<<<<<<< HEAD
    horizon = data['max_allowed_time']
=======
    horizon = 3000
>>>>>>> 2fd7728e151029bff14c7c36778472e2a6ef72cf
    routing.AddDimension(
        time_evaluator_index,
        horizon,  # allow waiting time
        horizon,  # maximum time per vehicle
        False,  # don't force start cumul to zero since we are giving TW to start nodes
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for location_idx, time_window in enumerate(data['time_windows']):
        index = manager.NodeToIndex(location_idx)
        if index == -1:
            continue
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
    

    # Add time window constraints for each vehicle start node
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][data['starts'][vehicle_id]][0],
                                                data['time_windows'][data['starts'][vehicle_id]][1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
        # Warning: Slack var is not defined for vehicle's end node
        #routing.AddToAssignment(time_dimension.SlackVar(self.routing.End(vehicle_id)))
    
    ## soft constraint
    soft_time_penalty = data['soft_time_peanlty']
    for location_idx,soft_time_window in enumerate(data['soft_time_windows']):
        index = manager.NodeToIndex(location_idx)
        if index == -1:
            continue
        time_dimension.SetCumulVarSoftLowerBound(index, time_window[0], soft_time_penalty)
        time_dimension.SetCumulVarSoftUpperBound(index, time_window[1], soft_time_penalty)
        


def print_solution(data, manager, routing, assignment):  # pylint:disable=too-many-locals
    """Prints assignment on console"""
    # Display dropped nodes.
    dropped_nodes1=[]
    Objective1=[]
    routes=[]
    empty_vehicle =[]
    dropped_nodes = []
    status = routing.status()
    route=[]
    total={}
    total['total_distance']=[]
    total['total_load']=[]
    total['total_time']=[]

    plan_output1={}
    plan_output1['vehicle_id']=[]
    
    plan_output1['index']=[]
    plan_output1['load_var']=[]

    plan_output1['time_var']={}
    plan_output1['time_var']['max_time_var']=[]
    plan_output1['time_var']['min_time_var']=[]
    
    plan_output1['slack_var']={}
    plan_output1['slack_var']['max_slack_var']=[]
    plan_output1['slack_var']['min_slack_var']=[]
    

    
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
            dropped_nodes1.append(manager.IndexToNode(node))
    print(dropped_nodes)
    print("Dropped Nodes=================")
    print(dropped_nodes1)
    
    print('Objective: {}'.format(assignment.ObjectiveValue()))
    Objective1.append(assignment.ObjectiveValue())

    total_distance = 0
    total_load = 0
    total_time = 0
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    time_dimension = routing.GetDimensionOrDie('Time')
    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        distance = 0
        no_of_nodes = 0
        while not routing.IsEnd(index):
            no_of_nodes = no_of_nodes + 1
            load_var = capacity_dimension.CumulVar(index)
            time_var = time_dimension.CumulVar(index)
            slack_var = time_dimension.SlackVar(index)
            plan_output += ' {0} Load({1}) Time({2},{3}) Slack({4},{5}) ->'.format(
                manager.IndexToNode(index),
                assignment.Value(load_var),
                assignment.Min(time_var),
                assignment.Max(time_var),
                assignment.Min(slack_var), assignment.Max(slack_var))

            ###DECLARED VARIABLES
            
            ###OVER DECLARE

            plan_output1['index'].append(manager.IndexToNode(index))
            plan_output1['load_var'].append(assignment.Value(load_var))       
            plan_output1['time_var']['min_time_var'].append(assignment.Min(time_var))
            plan_output1['time_var']['max_time_var'].append(assignment.Max(time_var))
            plan_output1['slack_var']['min_slack_var'].append(assignment.Min(slack_var))
            plan_output1['slack_var']['max_slack_var'].append(assignment.Max(slack_var))
            plan_output1['vehicle_id'].append(vehicle_id)


            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            distance += routing.GetArcCostForVehicle(previous_index, index,  vehicle_id)

        if no_of_nodes == 1:
            empty_vehicle.append(vehicle_id)                                           
        load_var = capacity_dimension.CumulVar(index)
        time_var = time_dimension.CumulVar(index)
        slack_var = time_dimension.SlackVar(index)
        plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(
            manager.IndexToNode(index),
            assignment.Value(load_var),
            assignment.Min(time_var), assignment.Max(time_var))

        plan_output += 'Distance of the route: {0}m\n'.format(distance)
        plan_output += 'Load of the route: {}\n'.format(
            assignment.Value(load_var))
        plan_output += 'Time of the route: {}\n'.format(
            assignment.Value(time_var))
        print(plan_output)
        total_distance += distance
        total_load += assignment.Value(load_var)
        total_time += assignment.Value(time_var)
        total['total_distance'].append(total_distance)
        total['total_load'].append(total_load)
        total['total_time'].append(total_time)
        route2={}
        route2['index']=[]
        route2['load_var']=[]
        route2['max_time_var']=[]
        route2['min_time_var']=[]

        if len(plan_output1['index'])>1:
            for i in range(0,len(plan_output1['index'])):
                route2={}    
                route2['index']=plan_output1['index'][i]
                route2['load_var']=plan_output1['load_var'][i]
                route2['max_time_var']=plan_output1['time_var']['max_time_var'][i]
                route2['min_time_var']=plan_output1['time_var']['min_time_var'][i]
                route2['max_slack_var']=plan_output1['slack_var']['max_slack_var'][i]
                route2['min_slack_var']=plan_output1['slack_var']['min_slack_var'][i]
                route.append(route2)
            routes.append(route)
        print("WORK1")      
        
        print("WORK2")

        total={}
        total['total_distance']=[]
        total['total_load']=[]
        total['total_time']=[]

        plan_output1={}
        plan_output1['vehicle_id']=[]
        
        plan_output1['index']=[]
        plan_output1['load_var']=[]

        plan_output1['time_var']={}
        plan_output1['time_var']['max_time_var']=[]
        plan_output1['time_var']['min_time_var']=[]
        
        plan_output1['slack_var']={}
        plan_output1['slack_var']['max_slack_var']=[]
        plan_output1['slack_var']['min_slack_var']=[]

        print("SAVED NEW ROUTES==========================")
        print(routes)
        print("OVER NEW ROUTES==========================")

    print('Total Distance of all routes: {0}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))
    print('Total Time of all routes: {0}min'.format(total_time))
    route=[]
    output = {}
    output['routes'] = routes
    output['empty_vehicle'] = empty_vehicle
    output['dropped_nodes'] = dropped_nodes1
    output['status'] = status
    return output    
    
    #return data['routes']=[{"Bus no",[{},{},{}]},{}]
    #route['Bus_no']=3 route['nodes']=[{},{},{}]
    #route['Total']=
    #route['Total']=
    #route['Total']=
    #route['nodes'][0]={'stop':0,'load':2,'windows':}


def solver(inputData):
    # datamatrix,psngr_no,buscap,num_vehicles
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    # [START data]
    data = create_data_model(inputData)

    # [END data]
    print("in solver")
    # Create the routing index manager.
    # [START index_manager]
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'],
                                        #    data['depot'],
                                           data['starts'],
                                           data['ends']
                                        )
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
    routing = pywrapcp.RoutingModel(manager)

    # [END routing_model]

    # Create and register a transit callback.
    # [START transit_callback]
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # [END arc_cost]

 #  Add Distance constraint.
#     dist_dimension_name = 'Distance'
#     routing.AddDimension(
#         transit_callback_index,
#         0,  # no slack
#         3000,  # vehicle maximum travel distance
#         True,  # start cumul to zero
#         dist_dimension_name)
#     # distance_dimension = routing.GetDimensionOrDie(dist_dimension_name)
#     # distance_dimension.SetGlobalSpanCostCoefficient(100)    


    # distance_dimension.SetCumulVarSoftUpperBound(index, time_window[1], soft_time_penalty)            
    
    
    # Add Capacity constraint.
    # [START capacity_constraint]
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    # [END capacity_constraint]

    demand_dimension = routing.GetDimensionOrDie('Capacity')
    
    soft_min_occ_penalty = data['soft_min_occ_penalty']
    index = manager.NodeToIndex(data['ends'][0])
    for vehicle_id in range(data['num_vehicles']):
        index = routing.End(vehicle_id)
        demand_dimension.SetCumulVarSoftLowerBound(index,data['soft_min_occupancy'][vehicle_id], soft_min_occ_penalty)

    # Add Time Window constraint
    time_evaluator_index = routing.RegisterTransitCallback(
        partial(create_time_evaluator(data), manager))
    add_time_window_constraints(routing, manager, data, time_evaluator_index)

    drop_penalty = data['drop_penalty']
    for node in range(0, len(data['distance_matrix'])):
        if manager.NodeToIndex(node) == -1:
            continue
        routing.AddDisjunction([manager.NodeToIndex(node)], drop_penalty)



    # Setting first solution heuristic.
    # [START parameters]
    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)  # pylint: disable=no-member
    search_parameters.time_limit.seconds = 100
    # [END parameters]

    # Solve the problem.
    # [START solve]
    assignment = routing.SolveWithParameters(search_parameters)
    # [END solve]
    data['previous_solution'] = assignment
    # Print solution on console.
    # [START print_solution]
    print(assignment)
    if assignment:
        return print_solution(data, manager, routing, assignment)
    # [END print_solution]

    print('\n\n\n')
    ### Running new instance ####
    # data['demands'][14] = 0
    
    # new_solution = routing.SolveFromAssignmentWithParameters(data['previous_solution'] , search_parameters)
    
    # if new_solution:
    #     print('New solution from previous one : ')
    #     print_solution(data, manager , routing, new_solution)
        

# if __name__ == '__main__':
#     # print(":jias")
#     main()
# [END program]
