import Gamin

Gamin.loadLevel("test")

Gamin.changeResource(3,"jumping","always")
Gamin.printResources()

while Gamin.isPlaying:
    #if Gamin.test_range(3,4,1,"top"):
    #    print("top")
    #if Gamin.test_range(3,4,1,"bottom"):
    #    print("bottom")
    #if Gamin.test_range(3,4,1,"left"):
    #    print("left")
    #if Gamin.test_range(3,4,1,"right"):
    #    print("right")
    if Gamin.test_range(3,4,1):
        print("touch")
    Gamin.gameUpdate()