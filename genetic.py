import csv
import random

##Matriz para conseguir los tiempos de cada movimiento
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
            #self.printFile(matriz)
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
        print(len(llistSku))
        self.rackLogic.sortListSkuWeight(llistSku)

        cont1 = 0
        cont2 = 0
        while llistSku[cont1].weight > 180:
            cont1 += 1
        while llistSku[cont1 + cont2].weight > 100:
            cont2 += 1
        l1 = llistSku[0:cont1]
        l2 = llistSku[cont1:cont2+cont1]
        l3 = llistSku[cont2+cont1::]

        return (l1,l2,l3)
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
    def __init__(self,name = "none",rotation = 0,weight = 0,popularity = 0):
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
        
    def setRack(self,newRack):
        self.rack = newRack
        
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
                
            elif Sku.weight <= 180 and Sku.weight > 100 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
                
            elif Sku.weight <= 100 and not self.isFullRow(1):
                self.rack[self.y2Fill][1] = Sku
                self.y2Fill += 1
                
            elif Sku.weight <= 100 and not self.isFullRow(0):
                self.rack[self.y1Fill][0] = Sku
                self.y1Fill += 1
                
            elif Sku.weight <= 180 and not self.isFullRow(0):
                self.rack[self.y1Fill][0] = Sku
                self.y1Fill += 1
            else:
                self.rack[self.y3Fill][2] = Sku
                self.y3Fill += 1


    ##Sort highest to lowest
    def sortListSku(self,x):
        for j in range(len(x)-1):
            for i in range(len(x) - 1):
                if x[i].popularity < x[i + 1].popularity:
                    x[i],x[i + 1] = x[i + 1], x[i]
                
                
        return x
    
    def sortListSkuWeight(self,x):
        for j in range(len(x)-1):
            for i in range(len(x) - 1):
                if x[i].weight < x[i + 1].weight:
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
    def calculateTime(self,tupl):
        global matTime
        time = 0
        
        if tupl[0] == "A":
            time = matTime[0][tupl[1]][tupl[2]]
        elif tupl[0] == "B":
            time = matTime[1][tupl[1]][tupl[2]]
        elif tupl[0] == "C":
            time = matTime[2][tupl[1]][tupl[2]]
        elif tupl[0] == "D":
            time = matTime[3][tupl[1]][tupl[2]]
        return time


class Fitness():
    def __init__(self):
        self.name = "fitnessClass"
    def calculateFitness(self,Rack):
        fitness = 0
        for i in range(len(Rack.rack)):
            for j in range(len(Rack.rack[0])):
                fitness += Rack.rack[i][j].popularity
        return fitness


class Population:
    def __init__(self):
        self.population = []
        self.timeControll = TimeController()
        self.fit = Fitness()
        self.rackA = Rack("A")
        self.rackB = Rack("B")
        self.rackC = Rack("C")
        self.rackD = Rack("D")
        self.fillPopulation()
    def fillPopulation(self):
        
        self.addRack(self.rackA)
        self.addRack(self.rackB)
        self.addRack(self.rackC)
        self.addRack(self.rackD)

        
    def addRack(self,Rack):
        self.population += [Rack]
    def findTime(self):
        t = self.findSku()
        time = self.timeControll.CalculateTime(t[0],t[1],t[2])
    def findSku(self,name):
        name = name.replace(" ","")
        for i in range(len(self.population)):
            for j in range(len(self.population[i].rack)):
                for k in range(len(self.population[i].rack[0])):
                    n = self.population[i].rack[j][k].name.replace(" ","")
                    if n == name:
                        slot = "ABCD"
                        return (slot[i],j,k)
    def printRacks(self):
        print("\n EJES ")
        print("------> Z")
        print("|        ")
        print("|        ")
        print("|        ")
        print("v        ")
        print("Y       \n")

        print(" RACK A ")
        self.population[0].showRackNAMES()
        print(" RACK B ")
        self.population[1].showRackNAMES()
        print(" RACK C ")
        self.population[2].showRackNAMES()
        print(" RACK D ")
        self.population[3].showRackNAMES()
        print("\n")
                    
    def makePopulation(self,l):
        
        cont = 0
        while l != []:
            #listRacks[cont].addSku(l[0])
            #l = l[1::]
            randSKU = random.randint(0,len(l)-1)
            if randSKU == 0 and not self.population[cont].isFull() and self.verifySKUWEIGHT(self.population[cont],l[randSKU]):
                self.population[cont].addSku(l[randSKU])
                l = l[1::]
            elif randSKU == len(l)-1 and not self.population[cont].isFull() and self.verifySKUWEIGHT(self.population[cont],l[randSKU]):
                self.population[cont].addSku(l[randSKU])
                l = l[0:len(l)-1]
            elif randSKU != 0 and randSKU != len(l)-1 and not self.population[cont].isFull() and self.verifySKUWEIGHT(self.population[cont],l[randSKU]):
                self.population[cont].addSku(l[randSKU])
                l = l[0:randSKU] + l[randSKU+1::]
            
            cont+=1
            if cont == 4:
                cont = 0
        self.printRacks()
        
    def verifySKUWEIGHT(self,rack,skuW):
        if skuW.weight > 100 and rack.isFullRow(0) and rack.isFullRow(1):
            return False
        else:
            return True
        
    def getGeneration(self,generation):
        for i in range(generation):
            self.crossover()
        
    def crossover(self):

        for k in self.population:
            k.sortRack()

        for j in range(len(self.population)-1):
            for i in range(len(self.population) - 1):
                if self.fit.calculateFitness(self.population[i]) < self.fit.calculateFitness(self.population[i + 1]):
                    self.population[i],self.population[i + 1] = self.population[i + 1], self.population[i]

        newR1 = []
        newR2 = []
        newR3 = []
        newR4 = []
        
        r1 = self.population[0]
        r2 = self.population[1]
        r3 = self.population[2]
        r4 = self.population[3]

        for i in range(5):
            row = [r1.rack[i][0] , r2.rack[i][1] , r1.rack[i][2]]
            newR1 += [row]
        for j in range(5):
            row = [r2.rack[j][0] , r1.rack[j][1] , r2.rack[j][2]]
            newR2 += [row]

        for ii in range(5):
            row = [r3.rack[ii][0] , r4.rack[ii][1] , r3.rack[ii][2]]
            newR3 += [row]
            
        for jj in range(5):
            row = [r4.rack[jj][0] , r3.rack[jj][1] , r4.rack[jj][2]]
            newR4 += [row]
            
        nr1 = Rack("A")
        nr1.setRack(newR1)
        nr2 = Rack("B")
        nr2.setRack(newR2)
        nr3 = Rack("C")
        nr3.setRack(newR3)
        nr4 = Rack("D")
        nr4.setRack(newR4)
        self.rackA = nr1
        self.rackB = nr2
        self.rackC = nr3
        self.rackD = nr4
        self.population = [nr1,nr2,nr3,nr4]



##Productos

fileC = FileController()
matData = fileC.init()
listSkus = fileC.makeListSku(matData)



population = Population()
population.makePopulation(listSkus[0])
population.makePopulation(listSkus[1])
population.makePopulation(listSkus[2])


##PRUEBA ANTES DE APLICAR CRUCE

find = "SKU 23" #SLOT A BUSCAR
print("\nGENERATION 0")
print("\nFIND: " + find)
local = population.findSku(find)
print(local)
print("time: " + str(population.timeControll.calculateTime(local)))

#fit = Fitness()

##MIDIENDO LOS FITNESS DE CADA RACK5
#print("Fitness")
#print(fit.calculateFitness(population.population[0]))
#print(fit.calculateFitness(population.population[1]))
#print(fit.calculateFitness(population.population[2]))
#print(fit.calculateFitness(population.population[3]))


#DESPUES DE GENERACIONES

i = 2 #NUMERO DE GENERACION A BUSCAR
population.getGeneration(i)

print("\n -RACKS- ")
population.printRacks()

print("\nGENERATION " + str(i))
print("\nFIND: " + find)
local = population.findSku(find)
print(local)
print("time: " + str(population.timeControll.calculateTime(local)))
















#l = [1,2,3,4,5]
#l[1::]
#[2, 3, 4, 5]
#l[0:len(l)-1]
#[1, 2, 3, 4]
#l[0:1] + l[2::]
#[1, 3, 4, 5]

        
            
        
        
        
