
#Constantes
timex = 0.25
timey = 0.25
timez = 0.15

global matTime
matTime = [[[35.5,50.1,64.8],
            [44.3,58.9,73.6],
            [53.1,67.7,82.4],
            [61.9,76.5,91.2],
            [70.7,85.3,100]],
           [[40.0,74.1,88.8],
            [68.3,82.9,97.6],
            [77.1,91.7,106.4],
            [85.9,100.5,115.2],
            [94.7,109.3,124.0]],
           [[83.5,98.1,112.8],
            [92.3,106.9,121.6],
            [101.1,115.7,130.4],
            [109.9,124.5,139.2],
            [118.7,133.3,148.0]],
           [[107.5,122.1,136.8],
            [116.3,130.9,145.6],
            [125.1,139.7,154.4],
            [133.9,148.5,163.2],
            [142.7,157.3,172.0]],
           ]



#Posiciones sin limite de peso
#A[n][0]

#Posiciones restriccion de 180
#A[n][1]

#Posiciones con restriccion de 100
#A[n][2]



##Sort highest to lowest
def sort(x):
    for j in range(len(x)-1):
        for i in range(len(x) - 1):
            if x[i] < x[i + 1]:
                x[i],x[i + 1] = x[i + 1], x[i]
    print (x)


class Sku:
    def __init__(self,name,popularity = 0,rotation = 0,weight = 0):
        self.name = name
        self.popularity = popularity
        self.rotation = rotation
        self.weight = weight

        
class Rack:
    def __init__(self,name = "None"):
        self.name = name
        self.fitness = 0
        self.rack = []

        ##Contador para cada fila del Rack
        self.y1Fill = 0
        self.y2Fill = 0
        self.y3.Fill = 0
        
        self.zFill = 0
        self.initRack()
    def fillRack(self,llist):
        cont = 0
        for i in range(5):
            l = []
            for j in range(3):
                l += [llist[cont]]
                cont += 1
            self.rack[i] = l
    def addSku(self,Sku):
        if not self.isFull():
            ##Condicionales de peso
            if Sku.wight > 180 and not self.isFullRow(0):
                
                self.rack[self.y1Fill][0] = Sku
                self.y1Fill += 1
            elif Sku.weight <= 180 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
                
            elif Sku.weight <= 100 and not self.isFullRow(2):
                self.rack[self.y3Fill][2] = Sku
                self.y3Fill += 1
                
            elif Sku.weight <= 180 and not self.isFullRow(0):
                self.rack[self.y2Fill][0] = Sku
                self.y1Fill += 1

            elif Sku.weight <= 100 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
    
            if self.yFill > 4:
                self.yFill = 0
                self.zFill += 1
        
        
    def initRack(self):
        for i in range(5):
            l = []
            for j in range(3):
                l+=[0]
            self.rack += [l]
    def showRack(self):
        for i in self.rack:
            print(i)
    def isFull(self):
        for i in self.rack:
            for j in i:
                if j==0:
                    return False
        return True
    def isFullRow(self,row):
        for i in self.rack:
            if i[row] == 0:
                return False
        return True


class TimeController:
    def __init__(self):
        self.name = "name"
    def CalculateTime(self,rackName,col,row):
        global matTime
        time = 0
        if rackName == "A":
            time = matTime[0][col][row]
        elif rackName == "B":
            time = matTime[1][col][row]
        elif rackName == "C":
            time = matTime[2][col][row]
        elif rackName == "D":
            time = matTime[3][col][row]
        return time


class Population:
    def __init__(self):
        self.population = []
    def addRack(self,Rack):
        self.population += [Rack]
    def findSku(self,name):
        for i in self.population:
            for j in i:
                for k in j:
                    if k.name == name:
                        return (i,j,k)
    
        
        
            
        


class Fitness():
    def __init__(self):
        self.name = "fitnessClass"
    def calculateFitness(self,Rack):
        fitness = 0
        for i in Rack.rack:
            fitness += i.popularidad
        
            
        
        
        
