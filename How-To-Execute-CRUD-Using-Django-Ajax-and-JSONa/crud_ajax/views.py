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
    mySolver()
    return render(request,'base.html',{'users':users})

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
        route['bus']=[]
        route['type']="pickup/drop"
        #route['nodes']=[{'lat':22.2,'lng':77.7,'arr':12,'depa':32,'count':20},{'lat':32.2,'lng':87.7,'arr':12,'depa':32,'count':20}]
        route['nodes']=[]
        for i in range(0,len(locations)):
            route['nodes'].append(locations[i])
        
        for i in range(0,len(busdetails)):
            route['bus'].append(busdetails[i])
        
        data['routes']=route 
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