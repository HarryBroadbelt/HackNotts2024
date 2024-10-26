class Enemy():
    def __init__(self, velocity, x, y, aggression):
        print('shimmy yeah shimmy yeah shimmy yah')
        self.__velocity = velocity
        self.__x = x
        self.__y = y
        self.__aggression = aggression


    def set_velocity(self, velocity):
        self.__velocity = velocity
    
    def get_velocity(self):
        return self.__velocity
    
    def set_x(self, x):
        self.__x = x
    
    def get_x(self):
        return self.__x
    
    def set_y(self, y):
        self.__y = y
    
    def get_y(self):
        return self.__y
    
    def set_aggression(self, aggression):
        self.__aggression = aggression
    
    def get_aggression(self):
        return self.__aggression
    
