import simpy

class Railway(object):
    def __init__(self, env, name, time_to_travel):
        self.env = env
        self.name = name
        self.track = simpy.Resource(env)
        self.time_to_travel = time_to_travel
        
    def transport(self, train):
        yield self.env.timeout(self.time_to_travel)
        
    def get_name(self):
        return self.name
        
        
class Train(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        
    def ride(self,track):
        print('%s arrives at %s at %.2f.' % (self.name, track.get_name(), env.now))
        
        with track.track.request() as request:
            yield request
    
            print('%s begins on %s at %.2f.' % (self.name, track.get_name(), env.now))
            yield env.process(track.transport(self))
    
            print('%s leaves %s at %.2f.' % (self.name, track.get_name(), env.now))
            
    def recrew(self, station):
        new_crew = yield station.get_crew_store().get()
        print ('%s gets %s at %.2f' % (self.name, new_crew, env.now))
        yield env.timeout(1)
        
            
class Station(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.crew_store = simpy.Store(env)
        
    def call_crew(self):
        crew_num = 0
        while True:
            yield env.timeout(5)
            self.crew_store.put('Crew %i: arrived at %.2f' % (crew_num, env.now))
            print 'Current crew inventory at station:' + str(self.crew_store.items)
            crew_num += 1
            
    def get_crew_store(self):
        return self.crew_store
            
print('Railroad Simulation \n')

env = simpy.Environment()

railway_a = Railway(env, "track_A", 1)
railway_b = Railway(env, "track_B", 2)
railway_c = Railway(env, "track_C", 10)
railway_d = Railway(env, "track_D", 2)
railway_e = Railway(env,"track_E", 3)

train_west = Train(env,"Train_W")
train_east = Train(env,"Train_E")

grand_central = Station(env, "Grand Central")
    
def train_west_path(env):
    while True:
        yield env.process(train_west.ride(railway_a))
        yield env.process(train_west.ride(railway_b))
        yield env.process(train_west.recrew(grand_central))
        yield env.process(train_west.ride(railway_c))
        
def train_east_path(env):
    while True:
        yield env.process(train_east.ride(railway_d))
        yield env.process(train_east.ride(railway_e))
        yield env.process(train_east.ride(railway_c))
        yield env.process(train_east.recrew(grand_central))
     
env.process(grand_central.call_crew())   
env.process(train_west_path(env))
env.process(train_east_path(env))


env.run(until=20)