import math

G = 6.67430e-11 # gravitational constant 
M_EARTH = 5.9742e24 # kg 

class Satellite: 
    def __init__(self, position, velocity, mass): 
        self.position = position # [x, y, z] 
        self.velocity = velocity # [vx, vy, vz] 
        self.mass = mass 
    
    def acceleration(self, thrust=None): 
        """Compute gravitational + optional thrust acceleration""" 
        x, y, z = self.position 
        r = math.sqrt(x*x + y*y + z*z) # Gravity toward Earth's center 
        a_grav = [-G*M_EARTH*x/r**3, -G*M_EARTH*y/r**3, -G*M_EARTH*z/r**3] 
        if thrust: # thrust = [ax, ay, az] in m/s^2 
            return [a_grav[i] + thrust[i] for i in range(3)] 
        return a_grav 
    
    def step(self, dt, thrust=None): 
        """Update position and velocity based on acceleration""" 
        a = self.acceleration(thrust) 
        self.velocity = [self.velocity[i] + a[i]*dt for i in range(3)] 
        self.position = [self.position[i] + self.velocity[i]*dt for i in range(3)] 
        return self.position, self.velocity, a 
    
    

    
