import pickle
import random
Instances={}
for i in range(0,3):
    Instance={}
    Instance['officeDetails']={
        'lat':random.random()*100,
        'lng':random.random()*100
    }
    Instance['busDetails']=[
        {
            'name':'MH123',
            'capacity':36
        },
        {
            'name':'MH143',
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
    Instance['CostMatrix']=[]
    for j in range(0,len(Instance['busStopDetails'])):
        distanceFromJ=[]
        for k in range(0,len(Instance['busStopDetails'])):
            distanceBetweenIJ=[]
            numRoutesBetweenIJ=random.randint(1,5)
            for l in range(0,numRoutesBetweenIJ):
                route={}
                route['distTotal']=random.randint(0,20)
                route['intermediateNodes']=[]
                numIntermidiate=random.randint(1,5)
                for m in range(0,numIntermidiate):
                    intermediateNode={}
                    intermediateNode['dist']=random.randint(0, 4)
                    intermediateNode['lat']=random.random()*100
                    intermediateNode['lng']=random.random()*100
                    route['intermediateNodes'].append(intermediateNode)
                distanceBetweenIJ.append(route)
            distanceFromJ.append(distanceBetweenIJ)
        Instance['CostMatrix'].append(distanceFromJ)    

    Instances[i]=Instance
dbfile = open('SimulationData', 'wb') 
# source, destination 
pickle.dump(Instances, dbfile)                      
dbfile.close() 