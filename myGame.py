import Gamin

Gamin.loadGame("myGame")

time = 0

placed = False

def placeBlock():
    global placed
    if not placed:
        placed = True
        Gamin.addCommand("block 0 0 70 70 green")
        Gamin.printResources()

def passTime():
    global time
    if time > 1000:
        Gamin.changeData(["property", "background", "black"])
    if time > 2000:
        Gamin.changeData(["property", "background", "cyan"])
        time = 0
    time += 1

#Gamin.printResources()
while Gamin.isPlaying:
    passTime()
    Gamin.camera = {'x':Gamin.getResource(14,'x'),'y':Gamin.getResource(14,'y')}
    if Gamin.test_range(16,14,5) or Gamin.test_range(16,13,5):
        Gamin.changeResource(16,'bg','green')
        placeBlock()
    else:
        Gamin.changeResource(16,'bg','red')
    Gamin.gameUpdate()