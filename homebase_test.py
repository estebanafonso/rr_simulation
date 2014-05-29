import simpy

class Crew_Homebase(object):
    def __init__(self, env, crew_list, min_sleep_time):
        self.env = env
        self.crew_at_home = simpy.Store(env)
        self.min_sleep_time = min_sleep_time
        for crew in crew_list:
            self.crew_at_home.put(crew)
        print self.crew_at_home.items
        
    def put_crew_home(self, crew):
        print "%s gets home at %.2f.  Sleeps for 10 hours." % (crew, self.env.now)
        yield self.env.timeout(self.min_sleep_time)
        print "%s wakes up at %.2f.  He is now available for work." % (crew, self.env.now)
        self.crew_at_home.put(crew)
        
    def get_crew_from_home(self):
        return self.crew_at_home.get()
        
    def view_crew_at_home(self):
        return self.crew_at_home.items
        
        
NUM_OF_CREWS = 3
MIN_SLEEP_TIME = 10            
            
print('Railroad Simulation \n')

env = simpy.Environment()

crew_list = ['Crew %s' % i for i in range(NUM_OF_CREWS)]

denver = Crew_Homebase(env, crew_list, MIN_SLEEP_TIME)

def get_crew(env, city):
    crew = yield denver.get_crew_from_home()
    print('Received this at %.2f while %s' % (env.now, crew))
    print(city.view_crew_at_home())
    yield env.process(denver.put_crew_home(crew))
    print(city.view_crew_at_home())
    
env.process(get_crew(env,denver))

env.run(until=20)