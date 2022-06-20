from RSLib.CustomWorld import *

if __name__ == "__main__":
    world = CustomWorld() # World in cm
    world.addRobot("NeuroBip.json")
    world.run()