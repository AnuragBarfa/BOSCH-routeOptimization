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
        route['bus']="NH123"
        route['color']="red"
        route['type']="pickup/drop"
        route['nodes']=[{'name': "k", 'count': "20", 'lat': 22.6018382, 'lng': 88.38306550000004},{'name': "d", 'count': "30", 'lat': 28.7040592, 'lng': 77.10249019999992},{'name': "M", 'count': "20", 'lat': 19.0759837, 'lng': 72.87765590000004}]
        routes.append(route)
        for i in range(0,len(locations)):
            route['nodes'].append(locations[i])
        
        for i in range(0,len(busdetails)):
            route['bus'].append(busdetails[i])
        
        route2={}    
        route2['bus']="NK324"
        route2['color']="green"
        route2['type']="pickup/drop"
        route2['nodes']=[{'name': "k1", 'count': "20", 'lat': 22, 'lng': 79},{'name': "d1", 'count': "30", 'lat': 24, 'lng': 83},{'name': "M1", 'count': "20", 'lat': 21, 'lng': 81}]
        
        routes.append(route2)

        route3={}    
        route3['bus']="NK324"
        route3['color']="black"
        route3['type']="pickup/drop"
        route3['nodes']=[{'name': "k2", 'count': "20", 'lat': 12, 'lng': 77},{'name': "d2", 'count': "30", 'lat': 13, 'lng': 80}]
        
        routes.append(route3)

        data['routes']=routes 
        print("ROUTES==================================")
        print(routes)
        print("ROUTES=============OVER=================")
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