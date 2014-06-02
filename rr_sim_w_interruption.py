import simpy
import random

class Train(object):
    def __init__(self, env, name, max_recrew_period,MTTF):
        self.env = env
        self.name = name
        self.max_recrew_period = max_recrew_period
        self.time_of_last_recrew = env.now
        self.time_since_last_recrew = 0.0
        self.no_of_recrews = 0
        self.old_time = env.now
        self.new_time = env.now
        
    def ride(self,railway):
        #print('%s arrives at %s at %.2f.' % (self.name, track.get_name(), env.now))
        
        with railway.track.request() as request:
            yield request
    
            print('%s begins on %s at %.2f.' % (self.name, railway.get_name(), env.now))
            yield self.env.timeout(railway.get_distance())
            print('%s leaves %s at %.2f.' % (self.name, railway.get_name(), env.now))
            

    def check_for_recrew(self, next_railway):
        self.time_since_last_recrew = env.now - self.time_of_last_recrew
        print "Time since last recrew for %s: %.2f" % (self.name,self.time_since_last_recrew)
        print "Estimated crew time at next recrew point: %i" % (self.time_since_last_recrew + next_railway.get_distance())
        if self.time_since_last_recrew + next_railway.get_distance() > self.max_recrew_period:
            yield env.process(self.recrew())
            
            
    def recrew(self):
        print "%s RECREW at %.2f" % (self.name,env.now)
        #yield(self.env.timeout(0))
        yield env.event().succeed()
        self.time_of_last_recrew = env.now
        self.time_since_last_recrew = 0.0
        self.no_of_recrews += 1
        print "%s Cumulative Recrews: %i " % (self.name,self.no_of_recrews)
        
    def time_to_failure(self):
        return random.expovariate(1/self.MTTF)
        
    def breakdown(self):
        while True:
            yield self.env.timeout(self.time_to_failure())
            if not self.broken:
                # breaking machine
    
        
        
        
    
class Railway(object):
    def __init__(self, env, name, distance):
        self.env = env
        self.name = name
        self.track = simpy.Resource(env)
        self.distance = distance
        
    def get_distance(self):
        return self.distance
        
    def get_name(self):
        return self.name
        
        
print('Railroad Simulation \n')

MAX_RECREW_PERIOD = 10
MEAN_TIME_TO_FAILURE = 15

env = simpy.Environment()

railway_nw = Railway(env, "track nw", 1)
railway_sw = Railway(env, "track sw", 5)
railway_ns = Railway(env, "track ns", 8)
railway_ne = Railway(env, "track ne", 2)
railway_se = Railway(env, "track se", 2)

train_west = Train(env, "West Train", MAX_RECREW_PERIOD,MEAN_TIME_TO_FAILURE)
train_east = Train(env, "East Train", MAX_RECREW_PERIOD)

def train_west_path(env):
    while True:
        yield env.process(train_west.ride(railway_nw))
        yield env.process(train_west.check_for_recrew(railway_ns))
        yield env.process(train_west.ride(railway_ns))
        yield env.process(train_west.check_for_recrew(railway_sw))
        yield env.process(train_west.ride(railway_sw))
        yield env.process(train_west.check_for_recrew(railway_nw))
        
def train_east_path(env):
    while True:
        yield env.process(train_east.ride(railway_ne))
        yield env.process(train_east.check_for_recrew(railway_se))
        yield env.process(train_east.ride(railway_se))
        yield env.process(train_east.check_for_recrew(railway_ns))
        yield env.process(train_east.ride(railway_ns))
        yield env.process(train_east.check_for_recrew(railway_ne))
        
env.process(train_west_path(env))
#env.process(train_east_path(env))


env.run(until=30)