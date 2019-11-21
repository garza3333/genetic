class Individ:
    def __init__(self,popularidad = 0,rotacion = 0,peso = 0):
        
        self.popularidad = popularidad
        self.rotacion = rotacion
        self.peso = peso

timex = 1
timey = 2
timez = 1

class Controller:
    def __init__(self):
        self.name = "name"
    def CalculateTime(self,mat,pos,prod):
        lok = mat[pos]
        time = 0
        for i in lok:
            for j in lok:
                if lok[i][j] == prod:
                    time += pos*timex
                    time += j*timey
                    time += i*timez
                     
                    return time
class Population:
    def __init__(self):
        self.mat = []

    def fillMat(self,llist):
        
            
        


class Fitness()
        
        
        
