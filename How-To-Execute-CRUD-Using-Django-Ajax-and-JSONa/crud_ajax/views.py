from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CrudUser
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .RouteOptimization import mySolver
import requests
import json
import urllib
from urllib.request import urlopen


def FrontView(request):
    users=CrudUser.objects.all()
    # mySolver()
    return render(request,'front_page.html',{'users':users})
def create_data(datakac):
    print("DATA['addresses']")
    print(datakac['addresses'])
    print(datakac)
    return datakac

def create_distance_matrix(data,datakac):
    data = create_data(datakac)  
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
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
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
    request = request + '&origins=' + origin_address_str + '&destinations=' + dest_address_str + '&key=' + API_key
    html = urlopen(request).read()
    # jsonResult = urllib.urlopen(request).read()
    response = json.loads(html)
    return response


def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix  

def main(datakac):
    data = create_data(datakac)
    addresses = data['addresses']
    API_key = data['API_key']
    distance_matrix = create_distance_matrix(data,datakac)
    print(distance_matrix)


class RouteView(View):
    def post(self, request):
        buscap=[]
        count=[]
        print("in view")
        print(request.POST)
        locations=json.loads(request.POST['locations'])
        busdetails=json.loads(request.POST['busdetails'])
        # print(locations)
        print("BUS=====================")
        print(busdetails)
        #print(x[0]["name"])
        #x[{},{}]

        # data={'lat':22.2,'lng':77.8,'arr':12,'depa':32,'count':20}
        routes=[]
        data={}
        route={}
        route['bus']="NH123"
        route['color']="red"
        route['type']="pickup/drop"
        route['nodes']=[]
        # route['nodes']=[{"lat":12.9216579,"lng":77.55992140000001},
        # #                 {"lat":12.930428,"lng": 77.53736}]
        #                 # {"lat":12.9021902,"lng": 77.51858199999992}]
                        # # {"lat":12.929655,"lng": 77.551214},
                        # {"lat":12.9233054,"lng":77.55334479999999},
                        # {"lat":12.859117,"lng":77.66167799999994},
                        # {"lat":12.9252588,"lng":77.5477436}]
                        # {"lat":17.4940497,"lng":78.40006399999993},
                        # {"lat":12.924475,"lng":77.5396084},
                        # {"lat":12.9304185,"lng":77.5149308},
                        # {"lat":12.928443,"lng":77.54591200000004},
                        # {"lat":12.9571219,"lng":77.5904727},
                        # {"lat":12.9149751,"lng":77.5185754},
                        # {"lat":12.9355867,"lng":77.5593574},
                        # {"lat":12.9292117,"lng":77.5696025},
                        # {"lat":12.916499,"lng":77.5603895},
                        # {"lat":12.9364473,"lng":77.58721119999996},
                        # {"lat":12.9039598,"lng":77.52598590000002},
                        # {"lat":12.9100928,"lng":77.48686399999997}]
        # print(route['nodes'])               
        # routes.append(route)
        for i in range(0,len(locations)):
            route['nodes'].append(locations[i])
            count.append(int(locations[i]['count']))
        print("PSNGR NO ================")    
        print(count)
        for i in range(0,len(busdetails)):
            # route['bus'].append(busdetails[i])
            buscap.append(int(busdetails[i]['buscapacity']))
        print("buscapacity================")    
        print(buscap)
        routes.append(route)
        # route2={}    
        # route2['bus']="NK324"
        # route2['color']="green"
        # route2['type']="pickup/drop"
        # route2['nodes']=[{'name': "k1", 'count': "20",'arr':"1",'depa':"1", 'lat': 22, 'lng': 79},{'name': "d1", 'count': "30",'arr':"1",'depa':"1", 'lat': 24, 'lng': 83},{'name': "M1", 'count': "20",'arr':"1",'depa':"1", 'lat': 21, 'lng': 81}]
        
        # routes.append(route2)

        # route3={}    
        # route3['bus']="NK324"
        # route3['color']="black"
        # route3['type']="pickup/drop"
        # route3['nodes']=[{'name': "k2", 'count': "20",'arr':"1",'depa':"1", 'lat': 12, 'lng': 77},{'name': "d2", 'count': "30",'arr':"1",'depa':"1", 'lat': 13, 'lng': 80}]
        
        # routes.append(route3)

        # route4={}
        # route4['bus']="NH123"
        # route4['color']="red"
        # route4['type']="pickup/drop"
        # route4['nodes']=[{'name': "k", 'count': "20",'arr':"1",'depa':"1", 'lat': 22.6018382, 'lng': 88.38306550000004},{'name': "d", 'count': "30",'arr':"1",'depa':"1", 'lat': 28.7040592, 'lng': 77.10249019999992},{'name': "M", 'count': "20",'arr':"1",'depa':"1", 'lat': 19.0759837, 'lng': 72.87765590000004}]
        # routes.append(route4)
        data['routes']=routes
        # data['routes']=route['nodes'] 

        print("ROUTES==================================")
        # print(routes[len(routes)]['nodes'][len(routes[0]['nodes'])]['name'])
        print(routes[0]['nodes'][0]['name'])
        print(routes[0]['nodes'][0]['name'].replace(", ", "+"))
        print("ROUTES=============OVER=================")   

        datakac = {}
        datakac['API_key'] = 'AIzaSyDmwBs8dSuwg56fTWsbJyMdrvXYU3_Pim4'
        datakac['addresses']=[]
        for i in range(0,len(routes[0]['nodes'])):
            x=routes[0]['nodes'][i]['name'].replace(", ", "+").replace(" ","+").replace(".","+")
            datakac['addresses'].append(x)
        datakac['addresses']=list(set(datakac['addresses']))    
        print(datakac)   
        main(datakac)
        # data['name']='anurag'       
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