from tkinter import *
import keyboard
import time

def on_destroy(event):
    global isPlaying
    if event.widget != window:
        return
    print("[Gamin]: Game Closed By User\n")
    isPlaying = False

if not __name__ == "__main__":
    window = Tk()
    window.title("Gamin Window")
    window.geometry("700x500")
    window.bind("<Destroy>", on_destroy)
    isPlaying = True
    canvas = Frame(window,width=700,height=500)
    canvas.place(x=0,y=0)

    commands = []
    creatingClass = "MAIN"

    gravity = 5
    movement = 10
    jumping = movement + 55
    camera = {'x':0,'y':0}

def addCommand(command):
    global window
    global commands
    global creatingClass
    #Preparing Line
    data = command.rstrip().split(" ")
    line = len(commands) + 1

    #Saving Command
    try:
        match data[0]:
            case "-"|"comment"|"comentar":
                print(f"____________________\n{data[1]}\n")
                commands.append({"type":"-","executed":"printed:","result":data[1]})
            case ":"|"data"|"dados":
                print(f"\n[Gamin: Line {line}]:")
                if len(data) == 1:
                    printResources()
                else:
                    printResources(data[1])
                commands.append({"type":"-","executed":"ShowData"})
            case ";"|"pause"|"pausar":
                if len(data) == 1:
                    pauseput = input("press enter to continue")
                else:
                    pauseput = input(data[1])
                commands.append({"type":"-","executed":"paused: ","result":pauseput})
            case "group"|"grupo":
                creatingClass = data[1]
                commands.append({"type":"-","executed":"class: ","result":"_"+data[1]})
            case "property"|"propriedade":
                changeData(data)
                commands.append({"type":"-","executed":"property","result":data[1]})
            case "config"|"configuration"|"configurar":
                changeData(data)
                commands.append({"type":"-","executed":"config","result":data[1]})
            case "block"|"bloco":
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=RAISED,borderwidth=4)
                    commands.append({"type":"block","x":data[1],"y":data[2],"object":thisObject,"class":creatingClass})
            case "character"|"personagem":
                    thisObject = Frame(canvas,width=data[4],height=data[5],bg=data[6],relief=SOLID,borderwidth=2)
                    commands.append({"type":"character","control":data[1],"x":data[2],"y":data[3],"object":thisObject,"class":creatingClass,"jumping":"ground"})
            case "background"|"plano":
                thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=FLAT,borderwidth=2)
                commands.append({"type":"background","x":data[1],"y":data[2],"object":thisObject,"class":creatingClass})
            case _:
                print(f"\n[Gamin ERR: Line {line}]: This command does not exist\n")
                commands.append({"type":"-","result":"ERROR"})
    except IndexError:
        print(f"\n[Gamin ERR: Line {line}]: Missing Parameter in command\n")
        commands.append({"type":"-","result":"ERROR"})
    except TclError:
        print(f"\n[Gamin ERR: Line {line}]: Invalid value for parameter\n")
        commands.append({"type":"-","result":"ERROR"})
    except ValueError:
        print(f"\n[Gamin ERR: Line {line}]: Invalid number for parameter\n")
        commands.append({"type":"-","result":"ERROR"})

def loadGame(fileName):
    with open(fileName + ".gmn","r") as sheet:
        itens = sheet.readlines()
        for item in itens:
            addCommand(item)
        

def getResource(line,property=""):
    if property == "":
        return commands[line-1]
    else:
        try:
            return commands[line-1][property]
        except KeyError:
            print(f"[Gamin ERR]: No property in {line}")
            return ""

def changeResource(line,property,edit):
    match property:
        case 'x'|'y'|'class'|'type':
            commands[line-1][property] = edit
        case _:
            commands[line-1]['object'][property] = edit

def changeData(values):
    global camera
    if values[0] == "property":
        if values[1] == "title":
            window.title(values[2].replace("_"," "))
        elif values[1] == "size":
            window.geometry(f"{values[2]}x{values[3]}")
            canvas["width"] = int(values[2])
            canvas["height"] = int(values[3])
            camera = {'x': int(values[2])//2, 'y':int(values[3])//2}
        elif values[1] == "background":
            canvas["bg"] = values[2]
        elif values[1] == "offset":
            canvas.place(x=int(values[2]),y=int(values[3]))
            canvas['width'] -= int(values[2])*2
            canvas['height'] -= int(values[3])*2
    elif values[0] == "config":
        if values[1] == "gravity":
            global gravity
            gravity = int(values[2])
        elif values[1] == "movement" or values[1] == "velocity":
            global movement
            movement = int(values[2])
        elif values[1] == "jumping":
            global jumping
            jumping = int(values[2])
        elif values[1] == "camera":
            camera = {'x':values[2],'y':values[3]}

def printResources(resource_group="MAIN"):
    for item in range(len(commands)):
        if resource_group == "MAIN":
            print(f"{item+1}: {commands[item]}")
        else:
            try:
                if resource_group == commands[item]["class"]:
                    print(f"{item+1}: {commands[item]}")
            except KeyError:
                pass
    print()

def test_range(object1,object2,inrange):
    obj1 = commands[object1 -1]
    obj2 = commands[object2 -1]
    try:
        return (int(obj1['x']) < int(obj2['x']) + inrange + int(obj2["object"]['width'])) and (int(obj1['x']) + int(obj1["object"]['width']) > int(obj2['x']) - inrange) and (int(obj1['y']) < int(obj2['y']) + inrange + int(obj2["object"]['height'])) and (int(obj1['y']) + int(obj1["object"]['height']) > int(obj2['y']) - inrange)
    except KeyError:
        print("\n[Gamin ERR]: Class has non object resources")

def move(object,x,y,collide=[]):
    blockedWay = False
    objX = int(commands[object -1]["x"])
    objY = int(commands[object -1]["y"])
    objWidth = int(commands[object -1]["object"]["width"])
    objHeight = int(commands[object -1]["object"]["height"])
    for command in commands:
        try:
            if command['type'] in collide or command['class'] in collide:
                try:
                    if (int(command['x']) < objX + x + objWidth) and (int(command['x']) + int(command["object"]['width']) > objX + x) and (int(command['y']) < objY + y + objHeight) and (int(command['y']) + int(command["object"]['height']) > objY + y):
                        blockedWay = True
                except KeyError:
                    print("\n[Gamin ERR]: Class has non object resources")
        except KeyError:
            pass
    if not blockedWay:
        commands[object -1]["x"] = str(objX+x)
        commands[object -1]["y"] = str(objY+y)

def infiniteLoop():
    while isPlaying:
        gameUpdate()

def gameUpdate():
    global window
    global isPlaying
    global movement
    if isPlaying:
        time.sleep(0.05)
        loop = 0
        for command in commands:
            if command["type"] == "block":
                command["object"].place(x=int(command["x"])-int(camera['x'])+canvas["width"]//2,y=int(command["y"])-int(camera['y'])+canvas["height"]//2)

            elif command["type"] == "character":
                command["object"].place(x=int(command["x"])-int(camera['x'])+canvas["width"]//2,y=int(command["y"])-int(camera['y'])+canvas["height"]//2)
                move(loop+1,0,gravity,["block"])
                if command["control"] == "wasd":
                    if keyboard.is_pressed("w"):
                        if command['jumping'] == 'ground':
                            bloop = 0
                            for block in commands:
                                bloop += 1
                                if block['type'] == 'block':
                                    if test_range(bloop,loop+1,5):
                                        move(loop+1,0,-jumping,["block"])
                        else:
                           move(loop+1,0,-jumping,["block"]) 
                    if keyboard.is_pressed("s"):
                        move(loop+1,0,jumping,["block"])
                    if keyboard.is_pressed("a"):
                        move(loop+1,-movement,0,["block"])
                    if keyboard.is_pressed("d"):
                        move(loop+1,movement,0,["block"])
                if command["control"] == "arrows":
                    if keyboard.is_pressed("up"):
                        if command['jumping'] == 'ground':
                            bloop = 0
                            for block in commands:
                                bloop += 1
                                if block['type'] == 'block':
                                    if test_range(bloop,loop+1,5):
                                        move(loop+1,0,-jumping,["block"])
                        else:
                           move(loop+1,0,-jumping,["block"]) 
                    if keyboard.is_pressed("down"):
                        move(loop+1,0,jumping,["block"])
                    if keyboard.is_pressed("left"):
                        move(loop+1,-movement,0,["block"])
                    if keyboard.is_pressed("right"):
                        move(loop+1,movement,0,["block"])

            elif command["type"] == "background":
                command["object"].place(x=int(command["x"])-int(camera['x'])+canvas["width"]//2,y=int(command["y"])-int(camera['y'])+canvas["height"]//2)
            
            loop += 1

        window.update()

#Beggining
if __name__ == "__main__":
    print("1- Start Project")
    print("2- Open Documentation")
    useroption = input("-")
    if useroption == "1":
        username = input("Project Name: ")
        with open(username+".py","a") as pyfile:
            pyfile.write(f"import Gamin\nGamin.loadGame('{username}')\n\nwhile Gamin.isPlaying:\n    Gamin.gameUpdate()")
        with open(username+".gmn","a") as pyfile:
            pyfile.write(f"- {username}_project")
    elif useroption == "2":
        import webbrowser
        webbrowser.open("https://github.com/catMeooww/Gamin-Py")