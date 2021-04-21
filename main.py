import numpy as np
from scipy.stats import norm
from generateRandom import congruenciaLineal
from test import testAll


# Clase principal la cual recibe los promedios de tiempo que se van a manejar en cada estación.

class Queue_Guava:
    send_data = {}

    def __init__(self, nBoxPerDay, muState1, muState2, muState3, muState4, muState42, sigma, muState5):

        # Vector donde se guarda los tiempos de permanencia que tiene cada caja de guayabas en bodega.
        self.stack = []

        # Tiempo de producción por día en minuutos
        self.productionTime = 480  # min

        # Guarda la cantidad de cajas de guayabas que no pudieron ser procesadas
        self.dangerGuava = 0

        # Guarda la cola que queda de la estación i
        self.stackStation1 = []

        # Guarda las colas que se forman en cada dia en la estación i
        self.matrixStation1 = []

        # Guarda las colas que no se pudieron procesar por día en la estación i
        self.matrixStationWait1 = []

        self.stackStation2 = []
        self.matrixStation2 = []
        self.matrixStationWait2 = []
        self.stackStation3 = []
        self.matrixStation3 = []
        self.matrixStationWait3 = []
        self.stackStation4 = []
        self.matrixStationWait4 = []
        self.stackStation42 = []
        self.matrixStation42 = []
        self.matrixStationWait42 = []
        self.matrixStation4 = []
        self.stackStation5 = []
        self.matrixStation5 = []
        self.matrixStationWait5 = []

        # Guarda los tiempos(50000) normalizados con el promedio asignada a cada estación
        self.randomsStation1 = norm.ppf((generateRandoms(50000)), loc=muState1)
        self.randomsStation2 = norm.ppf((generateRandoms(50000)), loc=muState2)
        self.randomsStation3 = norm.ppf((generateRandoms(50000)), loc=muState3)
        self.randomsStation4 = norm.ppf((generateRandoms(50000)), loc=muState4)
        self.randomsStation42 = norm.ppf((generateRandoms(50000)), loc=muState42, scale=sigma)
        self.randomsStation5 = norm.ppf((generateRandoms(50000)), loc=muState5)

        # Índices con los que se recorren los tiempos anteriores
        self.indexR1 = 0
        self.indexR2 = 0
        self.indexR3 = 0
        self.indexR4 = 0
        self.indexR42 = 0
        self.indexR5 = 0

        # Número de día actual en la simulación
        self.day = 1

        # Guarda la cantidad de cajas de bocadillos que finalizaron
        self.nBocadillosFinish = 0

        # Guarda la cantidad de cajas de bocadillos que se han usado
        self.nGuavasUsed = 0

        # Recibe la cantidad de cajas por día que llegan a la bodega
        self.nBoxPerDay = nBoxPerDay

    # Método que agrega n cajas de guayabas a la bodega con permanencia inicial en 0

    def simulationInit(self):
        self.send_data["stock_init"] = len(self.stack)
        # print("Stock en bodega: ", len(self.stack))
        for x in range(self.nBoxPerDay):
            self.stack.append(0)
        # print("Han llegado 14 guayabas")
        self.send_data["guava"] = 14
        # print("Stock en bodega: ", len(self.stack))
        self.send_data["stock_store"] = len(self.stack)

    # Método que simula el proceso en la estación 1
    # Retorna la cola con las cajas que se pudieron procesar por día
    def station_1(self):
        lastGuava = None
        stack = []
        i = 0
        danger = 0
        while len(self.stack) != 0:
            actualGuava = self.stack[0]

            if actualGuava < 24:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation1[self.indexR1], self.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation1[self.indexR1], self.day)
                if lastGuava.exit >= self.productionTime:
                    listStack = np.array(self.stack) + 24
                    self.stack = listStack.tolist()
                    break
                self.nGuavasUsed += 1
                lastGuava.lastDayInStaiton = self.day
                self.stackStation1.append(lastGuava)
                stack.append(lastGuava)
                self.indexR1 += 1
                i += 1
                self.stack.pop(0)
            else:
                danger += 1
                self.stack.pop(0)
        self.dangerGuava += danger
        return stack

    # Método que simula el proceso en la estación 2
    # Retorna la cola con las cajas que se pudieron procesar por día
    def station_2(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation1) != 0:
            station1H = self.stackStation1[0]
            if station1H.lastDayInStaiton == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station1H.exit, station1H.exit, self.randomsStation2[self.indexR2],
                                               station1H.day)
                else:
                    lastGuava = Station1_Guava(station1H.exit, lastGuava.exit, self.randomsStation2[self.indexR2],
                                               station1H.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation2[self.indexR2], station1H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation2[self.indexR2], station1H.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation1.pop(0)
            lastGuava.lastDayInStaiton = self.day
            self.stackStation2.append(lastGuava)
            stack.append(lastGuava)
            self.indexR2 += 1
            i += 1

        return stack

    # Método que simula el proceso en la estación 3
    # Retorna la cola con las cajas que se pudieron procesar por día
    def station_3(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation2) != 0:
            station2H = self.stackStation2[0]
            if station2H.lastDayInStaiton == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station2H.exit, station2H.exit, self.randomsStation3[self.indexR3],
                                               station2H.day)
                else:
                    lastGuava = Station1_Guava(station2H.exit, lastGuava.exit, self.randomsStation3[self.indexR3],
                                               station2H.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation3[self.indexR3], station2H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation3[self.indexR3], station2H.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation2.pop(0)
            lastGuava.lastDayInStaiton = self.day
            lastGuava.dayMold = self.day
            self.stackStation3.append(lastGuava)
            stack.append(lastGuava)
            self.indexR3 += 1
            i += 1
        return stack

    # Método que simula el proceso en la estación 4
    # Retorna la cola con las cajas que se pudieron procesar por día
    def station_4(self):
        lastGuava = None
        stack = []
        i = 0

        while len(self.stackStation4) != 0:
            station4H = self.stackStation4[0]
            if self.day - station4H.dayCut >= 1:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation42[self.indexR42], station4H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation42[self.indexR42], station4H.day)
            else:
                break
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation4.pop(0)
            lastGuava.dayMold = station4H.dayMold
            lastGuava.dayCut = station4H.dayCut
            lastGuava.dayFinishCut = self.day
            lastGuava.lastDayInStaiton = self.day
            self.stackStation42.append(lastGuava)
            stack.append(lastGuava)
            self.indexR42 += 1
            i += 1

        self.printStation("42", stack, self.stackStation4)
        self.matrixStationWait42.append(self.stackStation4.copy())
        self.matrixStation42.append(stack)

        stack = []
        i = 0
        lastGuava = None

        while len(self.stackStation3) != 0:
            station3H = self.stackStation3[0]
            if self.day - station3H.dayMold >= 2:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation4[self.indexR4], station3H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation4[self.indexR4], station3H.day)
            else:
                break
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation3.pop(0)
            lastGuava.dayMold = station3H.dayMold
            lastGuava.dayCut = self.day
            self.stackStation4.append(lastGuava)
            stack.append(lastGuava)
            self.indexR4 += 1
            i += 1

        return stack

    # Método que simula el proceso en la estación 5
    # Retorna la cola con las cajas que se pudieron procesar por día
    def station_5(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation42) != 0:
            station5h = self.stackStation42[0]
            if station5h.dayFinishCut == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station5h.exit, station5h.exit, self.randomsStation5[self.indexR5],
                                               station5h.day)
                else:
                    lastGuava = Station1_Guava(station5h.exit, station5h.exit, self.randomsStation5[self.indexR5],
                                               station5h.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation5[self.indexR5], station5h.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation5[self.indexR5], station5h.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation42.pop(0)
            self.stackStation5.append(lastGuava)
            lastGuava.dayMold = station5h.dayMold
            lastGuava.dayCut = station5h.dayCut
            lastGuava.dayFinishCut = station5h.dayFinishCut
            lastGuava.lastDayInStaiton = self.day
            stack.append(lastGuava)
            self.indexR5 += 1
            i += 1

        return stack

    def printStation(self, nStation, stack, waitStack):
        info = {}
        # print("Estación " + nStation + "; día: ", self.day)
        for i in range(len(stack)):
            info["station_{}_day_{}_{}".format(nStation, self.day, i)] = stack[i].to_dic()
            # print(stack[i])
        self.send_data["station_{}_day_{}".format(nStation, self.day)] = {"station": len(waitStack), "info": info}

    # Método que inicia la simulación, recibe los días a simular.
    def start(self, days):
        for x in range(days):
            self.day = x
            self.simulationInit()
            stack = self.station_1()
            self.matrixStation1.append(stack)
            self.matrixStationWait1.append(self.stack.copy())
            self.printStation("1", stack, self.stack)

            stack = self.station_2()
            self.matrixStation2.append(stack)
            self.matrixStationWait2.append(self.stackStation1.copy())
            self.printStation("2", stack, self.stackStation1)

            stack = self.station_3()
            self.matrixStation3.append(stack)
            self.matrixStationWait3.append(self.stackStation2.copy())
            self.printStation("3", stack, self.stackStation2)

            stack = self.station_4()
            self.matrixStation4.append(stack)
            self.matrixStationWait4.append(self.stackStation3.copy())
            self.printStation("4", stack, self.stackStation3)

            stack = self.station_5()
            self.nBocadillosFinish += len(stack)
            self.matrixStation5.append(stack)
            self.matrixStationWait5.append(self.stackStation42.copy())
            self.printStation("5", stack, self.stackStation42)

        self.send_data["bocadillos_finish"] = self.nBocadillosFinish * 14
        self.send_data["guava_used"] = self.nGuavasUsed
        self.send_data["guava_fail"] = self.dangerGuava
        self.send_data["guava_store"] = len(self.stack)
        self.send_data["guava_production"] = self.nGuavasUsed - self.nBocadillosFinish
        # print("Cajas de bocadillos hechos = ", self.nBocadillosFinish * 14)
        # print("Cajas de guayabas usadas = ", self.nGuavasUsed)
        # print("Cajas de guayabas dañadas = ", self.dangerGuava)
        # print("Cajas de guayabas en bodega = ", len(self.stack))
        # print("Cajas de guayabas en producción = ", self.nGuavasUsed - self.nBocadillosFinish)


class Station1_Guava:
    lastDayInStaiton = -1
    dayMold = -1
    dayCut = -1
    dayFinishCut = -1

    def __init__(self, at, start, ri, day):
        self.at = at
        self.start = max(start, at)
        self.et = ri
        self.exit = abs(self.start + self.et)
        self.wt = self.start - at
        self.day = day

    def __str__(self):
        return str(self.at) + "," + str(self.start) + "," + str(self.et) + "," + str(self.exit) + "," + str(
            self.wt) + "," + str(self.day) + "," + str(self.dayMold) + "," + str(self.dayCut) + "," + str(
            self.dayFinishCut)

    def to_dic(self):
        return {"at": self.at, "start": self.start, "et": self.et, "exit": self.exit, "wt": self.wt, "day": self.day,
                "dayMold": self.dayMold, "dayCut": self.dayCut, "dayFinishCut": self.dayFinishCut}


# Retorna 'n' cantidad de números pseudoaleatorios (siempre y cuando pasen todas las pruebas)
# utilizando el método de congruencia lineal
def generateRandoms(n):
    randoms = congruenciaLineal(n)
    # while not testAll(randoms):
    # randoms = congruenciaLineal(n)
    return np.array(randoms)

# queue = Queue_Guava(14, 40, 65, 25, 25, 120, 20, 50)
# queue.start(25)
