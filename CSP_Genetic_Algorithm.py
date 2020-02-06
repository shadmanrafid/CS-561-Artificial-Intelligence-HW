import random
import time

class Plane:

    def __init__(self, hoverTime, landingTime, changingTime, takeOffTime, maxWaitTime):
        self.hoverTime = hoverTime
        self.landingTime = landingTime
        self.changingTime = changingTime
        self.takeOffTime = takeOffTime
        self.maxWaitTime = maxWaitTime

    def getHoverTime(self):
        return self.hoverTime

    def getMinReadyTime(self):
        return self.landingTime + self.changingTime

class probableSchedule:

    def __init__(self,numberOfPlanes,problemInstance):
        self.numberOfPlanes = numberOfPlanes
        self.problemInstance = problemInstance
        self.solutionList =[]
        self.createSolutionList()

    def createSolutionList(self):
        for i in range(self.numberOfPlanes):
            plane = self.problemInstance.listOfPlanes[i]
            minReadyTime = plane.getMinReadyTime()
            landingTime = random.randint(0,plane.getHoverTime())

            if(plane.maxWaitTime - minReadyTime > 0):
                takeOffTime = landingTime + minReadyTime + random.randint(0,plane.maxWaitTime - minReadyTime - 1)
            else:
                takeOffTime = landingTime + minReadyTime

            self.solutionList.append((landingTime,takeOffTime))



    def getTimesOfBoardings(self):
        timesOfBoardings = []
        for i in range(self.numberOfPlanes):
            plane = self.problemInstance.listOfPlanes[i]
            ele = self.solutionList[i][0] + plane.landingTime
            if ele not in timesOfBoardings:
                timesOfBoardings.append(ele)
            ele = self.solutionList[i][1]
            if ele not in timesOfBoardings:
                timesOfBoardings.append(ele)
        return timesOfBoardings


    def getTimesOfTakeOffs(self):
        timesOfTakeOffs = []
        for i in range(self.numberOfPlanes):
            plane = self.problemInstance.listOfPlanes[i]
            ele = self.solutionList[i][1]
            if ele not in timesOfTakeOffs:
                timesOfTakeOffs.append(ele)
            ele = self.solutionList[i][1] + plane.takeOffTime
            if ele not in timesOfTakeOffs:
                timesOfTakeOffs.append(ele)
        return timesOfTakeOffs



    def getTimesOfLandings(self):
        timesOfLandings = []
        for i in range(self.numberOfPlanes):
            plane = self.problemInstance.listOfPlanes[i]
            ele = self.solutionList[i][0]
            if ele not in timesOfLandings:
                timesOfLandings.append(ele)
            ele = self.solutionList[i][0] + plane.landingTime
            if ele not in timesOfLandings:
                timesOfLandings.append(ele)
        return timesOfLandings



    def calculateCost(self):
        timesOfLandings = self.getTimesOfLandings()
        timesOfBoardings = self.getTimesOfBoardings()
        timesOfTakeOffs = self.getTimesOfTakeOffs()

        hardPenalty = 10
        self.cost = 0

        for i in range(len(timesOfLandings)):
            planeLandingCount = 0
            for j in range(self.numberOfPlanes):
                plane = self.problemInstance.listOfPlanes[j]
                if self.solutionList[j][0] <= timesOfLandings[i] and (self.solutionList[j][0] + plane.landingTime > timesOfLandings[i]):
                    planeLandingCount = planeLandingCount + 1

            if planeLandingCount > self.problemInstance.landingStrips:
                self.cost+= (planeLandingCount - self.problemInstance.landingStrips)*hardPenalty

        for i in range(len(timesOfBoardings)):
            planeBoardingCount = 0
            for j in range(self.numberOfPlanes):
                plane = self.problemInstance.listOfPlanes[j]
                if self.solutionList[j][0] + plane.landingTime <= timesOfBoardings[i] and (self.solutionList[j][1]  > timesOfBoardings[i]):
                    planeBoardingCount = planeBoardingCount + 1

            if planeBoardingCount > self.problemInstance.gates:
                self.cost+= (planeBoardingCount - self.problemInstance.gates)*hardPenalty

        for i in range(len(timesOfTakeOffs)):
            planesTakingOff = 0
            for j in range(self.numberOfPlanes):
                plane = self.problemInstance.listOfPlanes[j]
                if self.solutionList[j][1] <= timesOfTakeOffs[i] and (self.solutionList[j][1] + plane.takeOffTime > timesOfTakeOffs[i]):
                    planesTakingOff = planesTakingOff + 1

            if planesTakingOff > self.problemInstance.takeOffStrips:
                self.cost+= (planesTakingOff - self.problemInstance.takeOffStrips)*hardPenalty


class landingSchedule:

    def __takeInput(self):
        f = open("input.txt", "r")

        lines = f.readlines()

        values = lines[0].split(" ")

        self.landingStrips = int(values[0])
        self.gates = int(values[1])
        self.takeOffStrips= int(values[2])
        self.numberOfPlanes = int(lines[1])
        self.listOfPlanes = []

        for i in range(1, self.numberOfPlanes + 1):
            values = lines[i + 1].split(" ")
            hoverTime = int(values[0])
            landingTime = int(values[1])
            changingTime = int(values[2])
            takeOffTime = int(values[3])
            maxWaitTIme = int(values[4])

            plane = Plane(hoverTime,landingTime,changingTime,takeOffTime,maxWaitTIme)
            self.listOfPlanes.append(plane)


    def __generateRandomPopulation(self, populationSize):
        randomPopulation = []
        for i in range(populationSize):
            sampleSolution = probableSchedule(len(self.listOfPlanes),self)
            sampleSolution.calculateCost()

            randomPopulation.append(sampleSolution)

        return randomPopulation

    def __selectBestSamples(self,initialPopulation, rate):
        selectedPopulation = []
        initialPopulation.sort(key=lambda x: x.cost, reverse=False)
        selectedPopulationSize = rate * len(initialPopulation)
        for i in range(int(selectedPopulationSize)):
            selectedPopulation.append(initialPopulation[i])
        return selectedPopulation


    def __performCrossOver(self,selectedPopulation,rate):
        crossOverPopulation = []
        initialSize = len(selectedPopulation)
        numberOfCrossOvers = int(rate*initialSize)
        for i in range(numberOfCrossOvers):
            firstParent = selectedPopulation[random.randint(0,initialSize-1)]
            secondParent = selectedPopulation[random.randint(0,initialSize-1)]
            child = probableSchedule(len(self.listOfPlanes),self)
            del child.solutionList[:]
            newlist = []
            dividingIndex = random.randint(0,len(self.listOfPlanes)-2)
            for j in range(dividingIndex+1):
                landingTime = firstParent.solutionList[j][0]
                gateFinishTime = firstParent.solutionList[j][1]
                newlist.append((landingTime,gateFinishTime))
            for j in range(dividingIndex+1,len(self.listOfPlanes)):
                landingTime = secondParent.solutionList[j][0]
                gateFinishTime = secondParent.solutionList[j][1]
                newlist.append((landingTime, gateFinishTime))
            child.solutionList = newlist
            child.calculateCost()
            selectedPopulation.append(child)
        selectedPopulation.sort(key=lambda x: x.cost, reverse=False)
        for i in range(initialSize):
                crossOverPopulation.append(selectedPopulation[i])

        return crossOverPopulation

    def __getMutatedChild(self,parent):
        child = probableSchedule(len(self.listOfPlanes),self)
        mutationIndex = random.randint(0,len(self.listOfPlanes)-1)
        del child.solutionList[:]
        newList = []
        for i in range(len(self.listOfPlanes)):
            if i == mutationIndex:
                plane = self.listOfPlanes[i]
                minReadyTime = plane.getMinReadyTime()
                landingTime = random.randint(0, plane.getHoverTime())

                if (plane.maxWaitTime - minReadyTime > 0):
                    takeOffTime = landingTime + minReadyTime + random.randint(0, plane.maxWaitTime - minReadyTime - 1)
                else:
                    takeOffTime = landingTime + minReadyTime
                newList.append((landingTime,takeOffTime))
            else:
                landingTime = parent.solutionList[i][0]
                takeOffTime = parent.solutionList[i][1]
                newList.append((landingTime,takeOffTime))
        child.solutionList = newList
        child.calculateCost()
        return child

    def __performMutation(self,crossOverPopulation,rate):
        mutatedPopulation = []
        initialSize = len(crossOverPopulation)
        numberOfMutations = int(initialSize*rate)
        for i in range(numberOfMutations):
            parent = crossOverPopulation[random.randint(0,initialSize-1)]
            child = self.__getMutatedChild(parent)
            crossOverPopulation.append(child)
        crossOverPopulation.sort(key=lambda x: x.cost, reverse=False)
        for i in range(initialSize):
            mutatedPopulation.append(crossOverPopulation[i])
        return mutatedPopulation



    def __simulateGeneticAlgorithm(self):
        initialPopulation = self.__generateRandomPopulation(1000)
        selectedPopulation = self.__selectBestSamples(initialPopulation,0.5)

        if selectedPopulation[0].cost == 0:
             return selectedPopulation[0].solutionList
        else:
            for i in range(200000):

                crossOverPopulation = self.__performCrossOver(selectedPopulation, 0.4)
                mutatedPopulation = self.__performMutation(crossOverPopulation, 0.3)


                if mutatedPopulation[0].cost == 0:
                    return mutatedPopulation[0].solutionList
                    break
                selectedPopulation = mutatedPopulation



    def main(self):
        start = time.time()
        schedule = landingSchedule()
        schedule.__takeInput()
        result = schedule.__simulateGeneticAlgorithm()
        f2 = open("output.txt", "w")
        for i in range(len(result)):
            if i == len(result) -1:
                f2.write('%d %d' % (result[i][0], result[i][1]))
            else:
                f2.write('%d %d\n' % (result[i][0], result[i][1]))

        f2.close()
        end = time.time()
        print(format(end - start, '.10f'))

if __name__ == '__main__':
 landingSchedule().main()