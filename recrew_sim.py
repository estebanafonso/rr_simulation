import simpy

class Train(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.time_of_last_recrew = env.now
        self.time_since_last_recrew = 0.0
        self.no_of_recrews = 0
        
    def ride(self,railway):
        #print('%s arrives at %s at %.2f.' % (self.name, track.get_name(), env.now))
        
        with railway.track.request() as request:
            yield request
    
            print('%s begins on %s at %.2f.' % (self.name, railway.get_name(), env.now))
            yield env.process(railway.transport(self))
            print('%s leaves %s at %.2f.' % (self.name, railway.get_name(), env.now))

            self.check_crew_status()


    def check_crew_status(self):
        self.time_since_last_recrew = env.now - self.time_of_last_recrew
        print "Time since last recrew for %s: %.2f" % (self.name,self.time_since_last_recrew)
        if self.time_since_last_recrew > 10.0:
            print "%s RECREW at %.2f" % (self.name,env.now)
            self.time_of_last_recrew = env.now
            self.time_since_last_recrew = 0.0
            self.no_of_recrews += 1
            print "%s Cumulative Recrews: %i " % (self.name,self.no_of_recrews)
        
    
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
        
        
print('Railroad Simulation \n')

env = simpy.Environment()

railway_nw = Railway(env, "track nw", 1)
railway_sw = Railway(env, "track sw", 5)
railway_ns = Railway(env, "track ns", 3)
railway_ne = Railway(env, "track ne", 2)
railway_se = Railway(env, "track se", 2)

train_west = Train(env,"West Train")

def train_west_path(env):
    while True:
        yield env.process(train_west.ride(railway_nw))
        yield env.process(train_west.ride(railway_ns))
        yield env.process(train_west.ride(railway_sw))
        
env.process(train_west_path(env))

env.run(until=40)