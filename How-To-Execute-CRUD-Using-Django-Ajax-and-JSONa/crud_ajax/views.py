from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CrudUser
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .RouteOptimization import mySolver
def FrontView(request):
    users=CrudUser.objects.all()
    # mySolver()
    return render(request,'front_page.html',{'users':users})

class RouteView(View):
    def post(self, request):
        print("in view")
        print(request.POST)
        locations=json.loads(request.POST['locations'])
        busdetails=json.loads(request.POST['busdetails'])
        # print(locations)
        print(busdetails)
        #print(x[0]["name"])
        #x[{},{}]

        # data={'lat':22.2,'lng':77.8,'arr':12,'depa':32,'count':20}
        routes=[]
        data={}
        route={}
        # route['bus']="NH123"
        # route['color']="red"
        # route['type']="pickup/drop"
        route['nodes']=[{"lat":12.9216579,"lng":77.55992140000001},
                        {"lat":12.930428,"lng": 77.53736},
                        {"lat":12.9021902,"lng": 77.51858199999992}]
                        # {"lat":12.929655,"lng": 77.551214},
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
        print(route['nodes'])               
        # routes.append(route)
        # for i in range(0,len(locations)):
        #     route['nodes'].append(locations[i])
        
        # for i in range(0,len(busdetails)):
        #     route['bus'].append(busdetails[i])
        
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
        # data['routes']=routes
        data['routes']=route['nodes'] 

        # print("ROUTES==================================")
        # print(routes)
        # print("ROUTES=============OVER=================")
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