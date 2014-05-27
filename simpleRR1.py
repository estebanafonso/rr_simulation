import simpy

class Railway(object):
    def __init__(self, env, name, time_to_travel):
        self.env = env
        self.name = name
        self.track = simpy.Resource(env)
        self.time_to_travel = time_to_travel
        
    def transport(self, train):
        yield self.env.timeout(self.time_to_travel)
        
    def getName(self):
        return self.name
        
        
class Train(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        
    def ride(self,track):
        print('%s arrives at %s at %.2f.' % (self.name, track.getName(), env.now))
        
        with track.track.request() as request:
            yield request
    
            print('%s begins on track %s at %.2f.' % (self.name, track.getName(), env.now))
            yield env.process(track.transport(self))
    
            print('%s leaves the track %s at %.2f.' % (self.name, track.getName(), env.now))
            
            
print('Railroad Simulation \n')

env = simpy.Environment()

railway_a = Railway(env, "track_A", 1)
railway_b = Railway(env, "track_B", 2)
railway_c = Railway(env, "track_C", 10)
railway_d = Railway(env, "track_D", 2)
railway_e = Railway(env,"track_E", 3)

train_west = Train(env,"Train_W")
train_east = Train(env,"Train_E")
    
def train_west_path(env):
    while True:
        yield env.process(train_west.ride(railway_a))
        yield env.process(train_west.ride(railway_b))
        yield env.process(train_west.ride(railway_c))
        
def train_east_path(env):
    while True:
        yield env.process(train_east.ride(railway_d))
        yield env.process(train_east.ride(railway_e))
        yield env.process(train_east.ride(railway_c))
        
env.process(train_west_path(env))
env.process(train_east_path(env))

env.run(until=20)