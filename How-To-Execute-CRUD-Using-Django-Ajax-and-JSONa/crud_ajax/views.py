from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CrudUser
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .RouteOptimization import mySolver
from .vrp_capacity import solver
import requests
import json
import urllib
from urllib.request import urlopen
import pandas as pd
import random 
buscap=[]
count=[]
num_vehicles=0
def FrontView(request):
    users=CrudUser.objects.all()
    # mySolver()
    return render(request,'front_page.html',{'users':users})

def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses) # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        # print("origin address###############")
        # print(i)
        print(origin_addresses)
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        print("origin address###############")
        # print(i)
        print(origin_addresses)
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix


def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    def build_address_str(addresses):
        # Build a pipe-separated string of addresses
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
                        dest_address_str + '&key=' + API_key
    print("request#####")
    print(request)
    jsonResult = urlopen(request).read()
    print("jsonresult")
    print(jsonResult)
    response = json.loads(jsonResult)
    return response


def build_distance_matrix(response):
    print("response#############")
    print(response)
    distance_matrix = []
    for row in response['rows']:
        print("row===================")
        print(row['elements'])
        row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix  


class RouteView(View):
    def post(self, request):
        locations=json.loads(request.POST['locations'])
        print("locations#####")
        print(locations)
        busdetails=json.loads(request.POST['busdetails'])
        starts = json.loads(request.POST['starts'])
        ends = json.loads(request.POST['ends'])
        # pickup = json.loads(request.POST['pickup'])
        pickup = 1
        print(locations)
        print("BUS=====================")
        print(busdetails)

        passengerPerStop=[]
        busCapacity=[]
        dataForSolver={}
        dataForDistanceMatrix = {}

        dataForDistanceMatrix['API_key'] = 'AIzaSyDmwBs8dSuwg56fTWsbJyMdrvXYU3_Pim4'
        dataForDistanceMatrix['addresses']=[]

        for i in range(0,len(locations)):
            x=locations[i]['name'].replace(", ", "+").replace(" ","+").replace(".","+").replace(")","+").replace("(","+").replace("\"","+")
            dataForDistanceMatrix['addresses'].append(x)
            passengerPerStop.append(int(locations[i]['count']))

        dataForDistanceMatrix['addresses']=list(dataForDistanceMatrix['addresses'])    
        print("dataForDistanceMatrix")
        print(dataForDistanceMatrix)
        
        distance_matrix = create_distance_matrix(dataForDistanceMatrix)   
        print(distance_matrix)

            
        
        for i in range(0,len(busdetails)):
            print("BUS ",i)
            print("======================")
            print(busdetails[i])
            print("=========COUNT=============")
            print(busdetails[i]['buscapacity'])
            busCapacity.append(int(busdetails[i]['buscapacity']))

        dataForSolver['distance_matrix']=distance_matrix
        dataForSolver['pickup'] = pickup
        dataForSolver['passengerCount']=passengerPerStop
        dataForSolver['busCapacity']=busCapacity
        dataForSolver['time_windows']=[(0,200)]*len(locations)
        dataForSolver['starts'] = starts
        dataForSolver['ends'] = ends
        dataForSolver['max_allowed_time'] = 100
        dataForSolver['soft_time_windows'] = dataForSolver['time_windows']
        dataForSolver['soft_min_occupancy'] = [85]*len(dataForSolver['starts'])
    #     dataForSolver['distance_matrix']=distance_matrix
    #     dataForSolver['distance_matrix'] = [
    #     [
    #         0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
    #         468, 776, 662
    #     ],
    #     [
    #         548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
    #         1016, 868, 1210
    #     ],
    #     [
    #         776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
    #         1130, 788, 1552, 754
    #     ],
    #     [
    #         696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
    #         1164, 560, 1358
    #     ],
    #     [
    #         582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
    #         1050, 674, 1244
    #     ],
    #     [
    #         274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
    #         514, 1050, 708
    #     ],
    #     [
    #         502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
    #         514, 1278, 480
    #     ],
    #     [
    #         194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
    #         662, 742, 856
    #     ],
    #     [
    #         308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
    #         320, 1084, 514
    #     ],
    #     [
    #         194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
    #         274, 810, 468
    #     ],
    #     [
    #         536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
    #         730, 388, 1152, 354
    #     ],
    #     [
    #         502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
    #         308, 650, 274, 844
    #     ],
    #     [
    #         388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
    #         536, 388, 730
    #     ],
    #     [
    #         354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
    #         342, 422, 536
    #     ],
    #     [
    #         468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
    #         342, 0, 764, 194
    #     ],
    #     [
    #         776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
    #         388, 422, 764, 0, 798
    #     ],
    #     [
    #         662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
    #         536, 194, 798, 0
    #     ],
    # ]

    #     dataForSolver['passengerCount']= [0, 0, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    #     dataForSolver['busCapacity']=[20, 5, 10, 35]
    #     dataForSolver['time_windows']=[(0,200)]*17
        results=solver(dataForSolver)
        print("printing optimal route")
        print(results)
        # main(datakac)
        #print(x[0]["name"])
        #x[{},{}]

        # data={'lat':22.2,'lng':77.8,'arr':12,'depa':32,'count':20}
        routes=[]
        for i in range(0,len(results)):
            route={}
            route['bus']="NH123"
            route['color']="red"
            route['type']="pickup/drop"
            route['nodes']=[]
            for j in range(0,len(results[i])):
                node={}
                stopIndex=results[i][j]['index']
                node['lat']=locations[stopIndex]['lat']
                node['lng']=locations[stopIndex]['lng']
                node['load']=results[i][j]['load_var']
                node['max_time']=results[i][j]['max_time_var']
                node['min_time']=results[i][j]['min_time_var']
                node['max_slack']=results[i][j]['max_slack_var']
                node['min_slack']=results[i][j]['min_slack_var']
                route['nodes'].append(node)    
            routes.append(route)
        print(routes)
        # route={}
        # route['bus']="NH123"
        # route['color']="red"
        # route['type']="pickup/drop"
        # route['nodes']=[]
        # for i in range(0,len(locations)):
        #     route['nodes'].append(locations[i])
        #     count.append(int(locations[i]['count']))
        # print("PSNGR NO ================")    
        # print(count)
        # for i in range(0,len(busdetails)):
        #     # route['bus'].append(busdetails[i])
        #     buscap.append(int(busdetails[i]['buscapacity']))
        # print("buscapacity================")    
        # print(buscap)
        # num_vehicles=len(buscap)
        # routes.append(route)
        # data['routes']=routes
        # # data['routes']=route['nodes'] 

        # print("ROUTES==================================")
        # # print(routes[len(routes)]['nodes'][len(routes[0]['nodes'])]['name'])
        # print(routes[0]['nodes'][0]['name'])
        # print(routes[0]['nodes'][0]['name'].replace(", ", "+"))
        # print("ROUTES=============OVER=================")   
        data={}
        data['routes']=routes
        data['empty_vehicle'] = results['empty_vehicle']
        data['dropped_routes'] = results['dropped_routes']
        data['status'] = results['status']
        data['pickup'] = results['pickup']      
        print("DATAROUTES++++++++=========================")
        print(data['routes'][0]['nodes'])
        return JsonResponse(data)


class CrudView(TemplateView):
    template_name = 'crud_ajax/crud.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CrudUser.objects.all()
        return context


class CreateCrudUser(View):
    def  get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.create(
            name = name1,
            address = address1,
            age = age1
        )

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        print(user)
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        usr=CrudUser.objects.get(id=id1)
        location=usr.name
        print(location)
        usr.delete()

        print("STARTED INIT!!");
        data = {
            'deleted': True,
            'location':location
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.address = address1
        obj.age = age1
        obj.save()

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

def SimulationView(request):  
    data=pd.read_csv("data.csv",header=None)     
    df=pd.read_csv("data.csv", nrows=1,header=None)     
    print("INSIDE CSV:")
    print(data)     
    print("OFFSET:================")    
    offset=df[0][0]
    print(offset)
    return render(request,'simulation.html',)

class SimulatorView(View):
    def post(self, request):
        index=request.POST['index']
        print("in view")
        print(request.POST)
        #Displays ONE DATA contains how many rows
        data=pd.read_csv("data.csv")     
        # print(data)
        previndex=index
        x=random.choice([0,1])
        if x>0 :
            index=index+1
        
        print("index",index)
        # data=pd.read_csv("data.csv")
        # data=pd.read_csv("data.csv",usecols=[1])    
       
        #random>0.5
        #index0
        #offset1=>Memory
        data={}
        data['updated']=False
        data['name']='anurag'
        data['index']=index
        return JsonResponse(data)
