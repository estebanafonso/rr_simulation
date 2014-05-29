import simpy

class Crew_Homebase(object):
    '''
    This class represents the crew's homebase.  When a crew member is not working,
    either waiting at the station, or working on the train, he is at home.
    '''
    def __init__(self, env, crew_list, name, min_sleep_time):
        self.env = env
        self.crew_at_home = simpy.Store(env)
        self.name = name
        self.min_sleep_time = min_sleep_time
        for crew in crew_list:
            self.crew_at_home.put(crew)
        print "Initialized crews at home: %s" % self.crew_at_home.items
        
    def put_crew_home(self, crew):
        print "%s gets home at %.2f.  Sleeps for %i hours." % (crew, self.env.now, self.min_sleep_time)
        yield self.env.timeout(self.min_sleep_time)
        print "%s wakes up at %.2f.  He is now available for work." % (crew, self.env.now)
        self.crew_at_home.put(crew)
        
    def get_crew_from_home(self):
        return self.crew_at_home.get()
        
    def view_crew_at_home(self):
        return self.crew_at_home.items
        
        
        
class Station(object):
    def __init__(self, env, name, call_frequency):
        self.env = env
        self.name = name
        self.crew_at_station = simpy.Store(env)
        self.call_frequency = call_frequency
        
    def call_crew_to_station(self,homebase):
        while True:
            yield self.env.timeout(self.call_frequency)
            crew = yield homebase.get_crew_from_home()
            self.crew_at_station.put(crew)
            print "Calling %s to station at %.2f." % (crew, env.now)
            print "Crew at station at %.2f: %s" % (env.now,self.view_crew_at_station())
            
    def get_crew_at_station(self):
        return self.crew_at_station.get()
        
    def view_crew_at_station(self):
        return self.crew_at_station.items
        
    def send_crew_home(self,homebase):
        crew = yield self.get_crew_at_station()
        env.process(homebase.put_crew_home(crew))
        

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
        self.crew_on_train = simpy.Store(env)
        
    def initialize_crew(self, homebase):
        crew = yield homebase.get_crew_from_home()
        self.crew_on_train.put(crew)
        print "Initialized %s with %s." % (self.name,crew)
        print "Crews at home: %s." % homebase.view_crew_at_home()
        
        
    def ride(self,track):
        #print('%s arrives at %s at %.2f.' % (self.name, track.get_name(), env.now))
        
        with track.track.request() as request:
            yield request
    
            print('%s begins on %s at %.2f.' % (self.name, track.get_name(), env.now))
            yield env.process(track.transport(self))
            print('%s leaves %s at %.2f.' % (self.name, track.get_name(), env.now))
            
    def get_crew_on_train(self):
        return self.crew_on_train.get()
        print "TEST"
        
    def view_crew_on_train(self):
        return self.crew_on_train.items
            
    def recrew(self, station, homebase):
        print "%s RECREW" % self.name
        print "Crew on %s before recrew: %s" % (self.name, self.view_crew_on_train())
        print "Crew at %s before recrew: %s" % (station.name, station.view_crew_at_station())
        print "Crew at %s before recrew: %s" % (homebase.name, homebase.view_crew_at_home())
        old_crew = yield self.get_crew_on_train()
        env.process(homebase.put_crew_home(old_crew))
        new_crew = yield station.get_crew_at_station()
        self.crew_on_train.put(new_crew)
        print ('%s gets %s at %.2f' % (self.name, new_crew, env.now))
        

            
            
NUM_OF_CREWS = 3 
MIN_SLEEP_TIME = 10
CALL_FREQUENCY = 5          
            
print('Railroad Simulation \n')

env = simpy.Environment()

crew_list = ['Crew %s' % i for i in range(NUM_OF_CREWS)]

denver = Crew_Homebase(env, crew_list, "Denver", MIN_SLEEP_TIME)

railway_a = Railway(env, "track A", 1)
railway_b = Railway(env, "track B", 2)
railway_c = Railway(env, "track C", 10)
railway_d = Railway(env, "track D", 2)
railway_e = Railway(env,"track E", 3)

grand_central = Station(env, "Grand Central", CALL_FREQUENCY)

train_west = Train(env,"Train West")
train_east = Train(env,"Train East")


    
def train_west_path(env):
    yield env.process(train_west.initialize_crew(denver))
    while True:
        yield env.process(train_west.ride(railway_a))
        yield env.process(train_west.ride(railway_b))
        yield env.process(train_west.recrew(grand_central,denver))
        yield env.process(train_west.ride(railway_c))
        
def train_east_path(env):
    yield env.process(train_east.initialize_crew(denver))
    while True:
        yield env.process(train_east.ride(railway_d))
        yield env.process(train_east.ride(railway_e))
        yield env.process(train_east.ride(railway_c))
        yield env.process(train_east.recrew(grand_central,denver))
     
env.process(grand_central.call_crew_to_station(denver))   
env.process(train_west_path(env))
env.process(train_east_path(env))


env.run(until=30)