import math

Instance={}
Instance['officeDetails']={
    'lat' : 0,
    'lng': 0
}
Instance['startDetails']={
    'lat':random.random()*100,
    'lng':random.random()*100
}
Instance['busDetails']=[
    {
        'name':'VOLVO1',
        'capacity':20
    },
    {
        'name':'VOVLO4',
        'capacity':15
    },
    {
        'name':'VOVLO2',
        'capacity':26
    },
    {
        'name':'VOLVO3',
        'capacity':36
    }
]
Instance['busStopDetails']=[
    {
        'passengerCount':16,
        'lat':random.random()*100,
        'lng':random.random()*100,
    },
    {
        'passengerCount':10,
        'lat':random.random()*100,
        'lng':random.random()*100,
    },
    {
        'passengerCount':15,
        'lat':random.random()*100,
        'lng':random.random()*100,
    },
    {
        'passengerCount':20,
        'lat':random.random()*100,
        'lng':random.random()*100,
    },
    {
        'passengerCount':26,
        'lat':random.random()*100,
        'lng':random.random()*100,
    }
]
Instance['durationMatrix']=[]
Instance['CostMatrix']=[]
for j in range(0,len(Instance['busStopDetails'])):
    distanceFromJ=[]
    for k in range(0,len(Instance['busStopDetails'])):
        distanceBetweenIJ=[]
        numRoutesBetweenIJ=random.randint(1,3)
        for l in range(0,numRoutesBetweenIJ):
            route={}
            distTotal=0
            route['intermediateNodes']=[]
            numIntermidiate=random.randint(0,2)
            prev = [Instance['busStopDetails'][j]['lat'] , Instance['busStopDetails'][j]['lng']]
            for m in range(0,numIntermidiate):
                intermediateNode={}
                x1 = Instance['busStopDetails'][j]['lat']
                x1 += Instance['busStopDetails'][k]['lat']
                x1 /= 2

                y1 = Instance['busStopDetails'][j]['lng']
                y1 += Instance['busStopDetails'][k]['lng']
                y1 /= 2

                offset = 0.05

                costhe = random.random()
                sinthe = math.sqrt(1 - costhe*costhe)

                radius = random.random() * offset

                newX = x1 + costhe*radius
                newY = y1 + sinthe*radius
                D = (newX - prev[0])**2 + (newY-prev[1])**2
                distTotal += math.sqrt(D)
                prev = [newX, newY]


                # intermediateNode['dist']=random.randint(0, 4)
                intermediateNode['lat']= newX
                intermediateNode['lng']= newY
                route['intermediateNodes'].append(intermediateNode)
            route['distTotal']=distTotal   
            distanceBetweenIJ.append(route)
        distanceFromJ.append(distanceBetweenIJ)
    Instance['CostMatrix'].append(distanceFromJ)    
# import pickle
# import random
# Instances={}
# for i in range(0,3):
#     Instance={}
#     Instance['officeDetails']={
#         'lat':random.random()*100,
#         'lng':random.random()*100
#     }
#     Instance['startDetails']={
#         'lat':random.random()*100,
#         'lng':random.random()*100
#     }
#     Instance['busDetails']=[
#         {
#             'name':'MH123',
#             'capacity':36
#         },
#         {
#             'name':'MH143',
#             'capacity':36
#         }
#     ]
#     Instance['busStopDetails']=[
#         {
#             'passengerCount':16,
#             'lat':random.random()*100,
#             'lng':random.random()*100,
#         },
#         {
#             'passengerCount':10,
#             'lat':random.random()*100,
#             'lng':random.random()*100,
#         },
#         {
#             'passengerCount':15,
#             'lat':random.random()*100,
#             'lng':random.random()*100,
#         },
#         {
#             'passengerCount':20,
#             'lat':random.random()*100,
#             'lng':random.random()*100,
#         },
#         {
#             'passengerCount':26,
#             'lat':random.random()*100,
#             'lng':random.random()*100,
#         }
#     ]
#     Instance['CostMatrix']=[]
#     for j in range(0,len(Instance['busStopDetails'])):
#         distanceFromJ=[]
#         for k in range(0,len(Instance['busStopDetails'])):
#             distanceBetweenIJ=[]
#             numRoutesBetweenIJ=random.randint(1,5)
#             for l in range(0,numRoutesBetweenIJ):
#                 route={}
#                 route['distTotal']=random.randint(0,20)
#                 route['intermediateNodes']=[]
#                 numIntermidiate=random.randint(1,5)
#                 for m in range(0,numIntermidiate):
#                     intermediateNode={}
#                     intermediateNode['dist']=random.randint(0, 4)
#                     intermediateNode['lat']=random.random()*100
#                     intermediateNode['lng']=random.random()*100
#                     route['intermediateNodes'].append(intermediateNode)
#                 distanceBetweenIJ.append(route)
#             distanceFromJ.append(distanceBetweenIJ)
#         Instance['CostMatrix'].append(distanceFromJ)    

#     Instances[i]=Instance
# dbfile = open('SimulationData', 'wb') 
# # source, destination 
# pickle.dump(Instances, dbfile)                      
# dbfile.close() 