import csv
import random
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

##Clase que maneja los archivos csv
class FileController:
    def __init__(self):
        self.name = "controler"
        self.rackLogic = Rack()
    ##Funcion para leer la matriz desde el archivo csv
    def init(self):
        
        matriz = []
        with open('Skus.csv') as File:
            reader = csv.reader(File, delimiter=';', quotechar=';',
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if len(row) != 0:
                    matriz += [row]
                    
            for i in range(len(matriz)):
                for j in range(len(matriz[0])):
                    if self.isFloat(matriz[i][j]):
                        matriz[i][j] = float(matriz[i][j])
            self.printFile(matriz)
            return matriz
    def printFile(self,mat):
        for i in mat:
            print(i)
    def isFloat(self,word):
        nums = "1234567890. "
        for i in word:
            if i not in nums:
                return False
        return True
    def makeListSku(self,mat):
        llistSku = []
        for i in range(len(mat)):
            s = Sku(mat[i][0],mat[i][1],mat[i][2],mat[i][3])
            llistSku += [s]
        self.rackLogic.sortListSku(llistSku)
        ##MAKE TUPLA CON TRES LISTAS CON LOS TRES RANGOS DE PESO
        ##LUEGO DISTRIBUIR CADA LISTA DE MANERA ALEATORIA
        return llistSku
    def printListSkuName(self,l):
        print(" SKU NAMES ")
        for i in l:
            print(i.name)
    def printListSkuRotation(self,l):
        print(" SKU ROTATION ")
        for i in l:
            print(i.rotation)
    def printListSkuWeight(self,l):
        print(" SKU WEIGHT ")
        for i in l:
            print(i.weight)
    def printListSkuPopularity(self,l):
        print(" SKU POPULARITY ")
        for i in l:
            print(i.popularity)
        

class Sku:
    def __init__(self,name = "",rotation = 0,weight = 0,popularity = 0):
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
        self.y3Fill = 0
        
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
            if Sku.weight > 180 and not self.isFullRow(0):
                
                self.rack[self.y1Fill][0] = Sku
                self.y1Fill += 1
                
            elif Sku.weight <= 100 and not self.isFullRow(2):
                self.rack[self.y3Fill][2] = Sku
                self.y3Fill += 1
                
            elif Sku.weight <= 180 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
                
            elif Sku.weight <= 100 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
                
            elif Sku.weight <= 180 and not self.isFullRow(0):
                self.rack[self.y1Fill][0] = Sku
                self.y1Fill += 1


    def addNum(self,num):
        if not self.isFull():
            ##Condicionales de peso
            if num > 180 and not self.isFullRow(0):
                
                self.rack[self.y1Fill][0] = num
                self.y1Fill += 1

            elif num <= 100 and not self.isFullRow(2):
                self.rack[self.y3Fill][2] = num
                self.y3Fill += 1
                
            elif num <= 180 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = num
                self.y2Fill += 1
                
            elif num <= 100 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = num
                self.y2Fill += 1

                
            elif num <= 180 and not self.isFullRow(0):
                self.rack[self.y1Fill][0] = num
                self.y1Fill += 1

    ##Sort highest to lowest
    def sortListSku(self,x):
        for j in range(len(x)-1):
            for i in range(len(x) - 1):
                if x[i].popularity < x[i + 1].popularity:
                    x[i],x[i + 1] = x[i + 1], x[i]
                
        return x
    
    def sortRack(self):
        sortRack = []
        l1 = []
        l2 = []
        l3 = []
        for i in range(5):
            l1 += [self.rack[i][0]]
            l2 += [self.rack[i][1]]
            l3 += [self.rack[i][2]]

        l1 = self.sortListSku(l1)
        l2 = self.sortListSku(l2)
        l3 = self.sortListSku(l3)

        for j in range(5):
            row = []
            row += [l1[j]]
            row += [l2[j]]
            row += [l3[j]]
            sortRack += [row]
        
        self.rack = sortRack

        
        
    def initRack(self):
        for i in range(5):
            l = []
            for j in range(3):
                s = Sku()
                l+=[s]
            self.rack += [l]
    def showRack(self):
        mat = []
        for i in self.rack:
            row = []
            for j in i:
                row += [j.popularity]
            mat += [row]
        for k in mat:
            print(k)
            
    def showRackNAMES(self):
        mat = []
        for i in self.rack:
            row = []
            for j in i:
                row += [j.name]
            mat += [row]
        for k in mat:
            print(k)
                
    def isFull(self):
        for i in self.rack: 
            for j in i:
                if j.popularity == 0:
                    return False
        return True
    def isFullRow(self,row):
        for i in self.rack:
            if i[row].popularity == 0:
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
        self.timeControll = TimeController()
        self.rackA = Rack("A")
        self.rackB = Rack("B")
        self.rackC = Rack("C")
        self.rackD = Rack("D")
    def addRack(self,Rack):
        self.population += [Rack]
    def finTime(self):
        t = self.findSku()
        time = self.timeControll.CalculateTime(t[0],t[1],t[2])
    def findSku(self,name):
        for i in self.population:
            for j in i:
                for k in j:
                    if k.name == name:
                        slot = "ABCD"
                        return (slot[i],j,k)
    def printRacks(self):
        print(" RACK A ")
        self.rackA.showRackNAMES()
        print(" RACK B ")
        self.rackB.showRackNAMES()
        print(" RACK C ")
        self.rackC.showRackNAMES()
        print(" RACK D ")
        self.rackD.showRackNAMES()
                    
    def makePopulation(self,l):
        listRacks = [self.rackA,self.rackB,self.rackC,self.rackD]
        for j in range(4):
            
            for i in range(15):
                randSKU =  random.randint(0,len(l)-1)
                if randSKU == 0:
                    listRacks[j].addSku(l[randSKU])
                    l = l[1::]
                elif randSKU == len(l)-1:
                    listRacks[j].addSku(l[randSKU])
                    l = l[0:len(l)-1]
                else:
                    listRacks[j].addSku(l[randSKU])
                    l = l[0:randSKU] + l[randSKU+1::]
        self.printRacks()
        
                
        
    
        
        
            
        


class Fitness():
    def __init__(self):
        self.name = "fitnessClass"
    def calculateFitness(self,Rack):
        fitness = 0
        for i in Rack.rack:
            fitness += i.popularidad









##Productos

fileC = FileController()
matData = fileC.init()

listSkus = fileC.makeListSku(matData)

population = Population()

population.makePopulation(listSkus)



            



#l = [1,2,3,4,5]
#l[1::]
#[2, 3, 4, 5]
#l[0:len(l)-1]
#[1, 2, 3, 4]
#l[0:1] + l[2::]
#[1, 3, 4, 5]

        
            
        
        
        
