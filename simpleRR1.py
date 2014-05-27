import simpy


class Railway(object):
    def __init__(self, env, time_to_travel):
        self.env = env
        self.track = simpy.Resource(env)
        self.time_to_travel = time_to_travel
        
    def transport(self, train):
        yield self.env.timeout(self.time_to_travel)
        print("Transporting on track")
        
        
        
class Train(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        
    def ride(self,track):
        print('%s arrives at the track at %.2f.' % (self.name, env.now))
        
        with track.track.request() as request:
            yield request
    
            print('%s begins on track at %.2f.' % (self.name, env.now))
            yield env.process(track.transport(self))
    
            print('%s leaves the track at %.2f.' % (self.name, env.now))
            
            
            
            

print('Railroad Simulation \n')

env = simpy.Environment()

railway_a = Railway(env, 5)
railway_b = Railway(env, 7)
train_west = Train(env,"Train_W")
    

env.process(train_west.ride(railway_a))
env.process(train_west.ride(railway_b))

env.run(until=100)