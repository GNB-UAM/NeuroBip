from Box2D.examples.framework import Framework
from Box2D import b2EdgeShape
from NeuroBip import *
from RSLib.UnitTransform import *
import threading
import time
from GA import GA

class CustomWorld (Framework):

    name = "NeuroBip"
    listening = True
    mode = 2 # 0 = Playground, 1 = Genetic Algorithm, 2 = Experiment
    experiment = 1 # 1 = respawn when fall, 2 = respawn when both fall
    numRobots = 100
    generations = 60
    timePerGen = 60
    recordedData = [[], []]
    deadRobots = 0

    def __init__(self):
        super(CustomWorld, self).__init__()
        self.world.gravity = (0, acceleration(-9.81, "m"))
        self.createFlatGround(10000)
        self.robots = []
        self.resetRobots = None
        #[0.6, 0.31303179479404736, -0.4282281750577982, -0.26993822831925085, 1.2892845847027137]#
        self.genes = [0.5, 0.31303179479404734, -0.4282281750577982, -0.26993822831925085, -0.21149889395959587]#0.5, 0.2617993877991494, -0.3490658503988659, -0.6802877826717444, -0.21149889395959587]#[0.5, 15*pi/180, 20*pi/180, -pi/2, -pi/2]#[0.6133845515398813, 0.17453292519943295, -0.17590314901826792, -1.5707963267948966, -1.5707963267948966]#[0.25, 10*pi/180, 20*pi/180, -pi/2, -pi/2]
        self.geneticAlgortihm = GA(self.generations, self.timePerGen, self.numRobots, self.generation_func, self.fitness_func, initial_genes=self.genes)
        self.communication = threading.Thread(target=self.listener)
        self.communication.start()
        self.time = time.time()
        
        if self.mode == 0:
            self.numRobots = 1
        
        if self.mode == 2:
            self.numRobots = 1
        
        self.robots = [self.createRobot(5000 + i) for i in range(self.numRobots)]
        
    def Step(self, settings):
        super(CustomWorld, self).Step(settings)
        if self.mode == 1:
            self.geneticAlgortihm.run()
            self.mode = 0
        
        if self.resetRobots is not None:
            maxDistance = 0
            maxIndex = 0
            if len(self.robots) > 0:
                for index, robot in enumerate(self.robots):
                    if max(robot.getPosition()[0], robot.maxDistance) > maxDistance:
                        maxDistance = max(robot.getPosition()[0], robot.maxDistance)
                        maxIndex = index
                #print("Best genes id({}): {} with distane {}".format(maxIndex, self.robots[maxIndex].getParams(), max(self.robots[maxIndex].getPosition()[0], self.robots[maxIndex].maxDistance)))
            self.resetRobotsWithParams(self.resetRobots)
        
        currentTime = time.time()

        for index, robot in enumerate(self.robots):
            robot.update(currentTime - self.time)
            if not robot.dead and robot.checkDead() and self.mode == 2:
                self.recordedData[index].append((robot.livingTime, robot.maxDistance, robot.port))
                robot.communication.close()
                if self.experiment == 1:
                    time.sleep(5)
                    self.robots[index] = self.createRobot(5000 + index)
                elif self.experiment == 2:
                    self.deadRobots += 1
        if self.experiment == 2 and self.deadRobots == self.numRobots:
            time.sleep(5)
            self.deadRobots = 0
            for index in range(len(self.robots)):
                self.robots[index] = self.createRobot(5000 + index)

        self.time = currentTime
        
        if self.viewCenter[0] - self.robots[0].getPosition()[0] > 10:
            self.viewCenter = (10 + self.robots[0].getPosition()[0], 20)
        elif self.viewCenter[0] - self.robots[0].getPosition()[0] < -10:
            self.viewCenter = (-10 + self.robots[0].getPosition()[0], 20)
        
    
    def resetRobotsWithParams(self, params):
        if len(self.robots) > 0:
            for robot in self.robots:
                robot.remove()
            self.robots = []
        
        for index, member in enumerate(params):
            self.robots.append(
                NeuroBip(
                    self.world,
                    index,
                    member[0],
                    member[1],
                    member[2],
                    member[3],
                    member[4],
                    offset = (0, 0)
                )
                )
        
        self.resetRobots = None
    
    def fitness_func(self, solution, solution_idx):
        return max(self.robots[solution_idx].getPosition()[0], self.robots[solution_idx].maxDistance)
    
    def generation_func(self, instance):
        solution, solution_fitness, solution_idx = instance.best_solution()
        correctSolution = [x for x in solution]
        print("Generation {} best ({}) : {} with distance {}".format(instance.generations_completed, solution_idx, correctSolution, solution_fitness))

        self.resetRobots = instance.population
    
    def checkEvents(self):
        superReturn = super(CustomWorld, self).checkEvents()
        if not superReturn:
            self.listening = False
            if self.mode == 2 and len(self.recordedData[0]) > 0:
                for index in range(len(self.recordedData)):
                    with open("Results/data/data{}_{}_mode{}.csv".format(time.strftime("%Y%m%d-%H%M%S"), index, self.experiment), "w") as f:
                        for data in self.recordedData[index]:
                            f.write("{},{},{}\n".format(data[0], data[1], data[2]))
            print("Exiting")
            self.communication.join()
        
        return superReturn


    def createFlatGround(self, width):
        groundCoords = [(-width, 0), (width, 0)]
        ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=groundCoords)
        )

        ground.CreateEdgeFixture(
            vertices=groundCoords,
            density=0,
            friction=2,
        )

        """
        wallCoords = [(0, 20), (0, 0)]
        wall = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=wallCoords)
        )

        wall.CreateEdgeFixture(
            vertices=wallCoords,
            density=0,
            friction=2,
        )
        """

    def addRobot(self, robot):
        pass

    def createRobot(self, port):
        return NeuroBip(
            self.world,
            0,
            self.genes[0],
            self.genes[1],
            self.genes[2],
            self.genes[3],
            self.genes[4],
            port if self.mode != 1 else None,
            offset = (0, 0)
        )

    def listener(self):
        while self.listening:
            """
            for i in range(-89, 89, 5):
                self.robot.sendMessage(i)
                sleep(0.01)
            for i in range(89, -89, -5):
                self.robot.sendMessage(i)
                sleep(0.01)
            """