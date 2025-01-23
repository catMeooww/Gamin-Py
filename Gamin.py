from tkinter import *
import keyboard
import time

window = False
isPlaying = False
canvas = False
commands = []
creatingClass = ""
gravity = 5
movement = 10
jumping = 15
camera = {}

def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage

def on_destroy(event):
    global isPlaying
    if event.widget != window:
        return
    print("[Gamin]: Level closed\n")
    isPlaying = False

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
                if data[5].startswith("img:"):
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=canvas['bg'])
                    objImage = PhotoImage(file=data[5].replace("img:",""))
                    objImage = resizeImage(objImage,int(data[3])+4,int(data[4])+4)
                    extraObject = Label(thisObject,image=objImage,width=data[3],height=data[4])
                    extraObject.image = objImage
                    extraObject.pack()
                else:
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=RAISED,borderwidth=4)
                commands.append({"type":"block","x":data[1],"y":data[2],"object":thisObject,"class":creatingClass})
            case "character"|"personagem":
                if data[5].startswith("img:"):
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=canvas['bg'])
                    objImage = PhotoImage(file=data[5].replace("img:",""))
                    objImage = resizeImage(objImage,int(data[3])+4,int(data[4])+4)
                    extraObject = Label(thisObject,image=objImage,width=data[3],height=data[4])
                    extraObject.image = objImage
                    extraObject.pack()
                else:
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=SOLID,borderwidth=2)
                commands.append({"type":"character","control":data[6],"x":data[1],"y":data[2],"object":thisObject,"class":creatingClass,"jumping":"ground","velX":0,"velY":0})
            case "background"|"plano":
                if data[5].startswith("img:"):
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=canvas['bg'])
                    objImage = PhotoImage(file=data[5].replace("img:",""))
                    objImage = resizeImage(objImage,int(data[3])+4,int(data[4])+4)
                    extraObject = Label(thisObject,image=objImage,width=data[3],height=data[4])
                    extraObject.image = objImage
                    extraObject.pack()
                else:
                    thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=FLAT,borderwidth=2)
                commands.append({"type":"background","x":data[1],"y":data[2],"object":thisObject,"class":creatingClass})
            case "label"|"txt"|"texto":
                thisObject = Frame(canvas,width=data[3],height=data[4],bg=data[5],relief=FLAT,borderwidth=2)
                extraObject = Label(thisObject,text=data[6].replace("_"," "),font=("Arial",data[4]),bg=data[5])
                extraObject.pack()
                commands.append({"type":"txt","x":data[1],"y":data[2],"object":thisObject,"class":creatingClass})
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

def loadLevel(fileName):
    global window
    global isPlaying
    global canvas
    global commands
    global creatingClass
    global gravity
    global movement
    global jumping
    global camera
    #prep
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
    jumping = 15
    camera = {'x':0,'y':0}

    #level
    if fileName != False:
        with open(fileName + ".gmn","r") as sheet:
            itens = sheet.readlines()
            for item in itens:
                addCommand(item)
        
def closeLevel():
    window.destroy()

def getResource(line,property=""):
    if property == "":
        return commands[line-1]
    else:
        try:
            return commands[line-1][property]
        except KeyError:
            try:
                return commands[line-1]['object'][property]
            except KeyError:
                print(f"[Gamin ERR]: No property in {line}")
                return ""

def changeResource(line,property,edit):
    match property:
        case 'x'|'y'|'class'|'type'|'jumping'|'control':
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
        elif values[1] == "icon":
            window.iconbitmap(values[2].replace("img:",""))
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

def test_range(object1,object2,inrange,direction='all'):
    obj1 = commands[object1 -1]
    obj2 = commands[object2 -1]
    try:
        if direction == "top":
            return (int(obj1['y']) + int(obj1["object"]['height']) > int(obj2['y']) - inrange and int(obj1['y']) + int(obj1["object"]['height']) < int(obj2['y']) + inrange) and (int(obj1['x']) < int(obj2['x']) + inrange + int(obj2["object"]['width'])) and (int(obj1['x']) + int(obj1["object"]['width']) > int(obj2['x']) - inrange)
        elif direction == "bottom":
            return (int(obj1['y']) < int(obj2['y']) + inrange + int(obj2["object"]['height']) and int(obj1['y']) > int(obj2['y']) - inrange + int(obj2["object"]['height'])) and (int(obj1['x']) < int(obj2['x']) + inrange + int(obj2["object"]['width'])) and (int(obj1['x']) + int(obj1["object"]['width']) > int(obj2['x']) - inrange)
        elif direction == "left":
            return (int(obj1['x']) + int(obj1["object"]['width']) > int(obj2['x']) - inrange and int(obj1['x']) + int(obj1["object"]['width']) < int(obj2['x']) + inrange) and (int(obj1['y']) < int(obj2['y']) + inrange + int(obj2["object"]['height'])) and (int(obj1['y']) + int(obj1["object"]['height']) > int(obj2['y']) - inrange)
        elif direction == "right":
            return (int(obj1['x']) < int(obj2['x']) + inrange + int(obj2["object"]['width']) and int(obj1['x']) > int(obj2['x']) - inrange + int(obj2["object"]['width'])) and (int(obj1['y']) < int(obj2['y']) + inrange + int(obj2["object"]['height'])) and (int(obj1['y']) + int(obj1["object"]['height']) > int(obj2['y']) - inrange)
        else:
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
                if command['velY'] != 0 or command['velX'] != 0:
                    move(loop+1,command['velX'],command['velY'],["block"])
                    if command['velY'] > 0:
                        command['velY'] -= 1
                    elif command['velY'] < 0:
                        command['velY'] += 1
                    if command['velX'] > 0:
                        command['velX'] -= 1
                    elif command['velX'] < 0:
                        command['velX'] += 1
                if command["control"] == "wasd":
                    if keyboard.is_pressed("w"):
                        if command['jumping'] == 'ground':
                            bloop = 0
                            for block in commands:
                                bloop += 1
                                if block['type'] == 'block':
                                    if test_range(bloop,loop+1,5,'bottom'):
                                        command['velY'] = -jumping
                        else:
                           move(loop+1,0,-movement,["block"]) 
                    if keyboard.is_pressed("s"):
                        move(loop+1,0,movement,["block"])
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
                                    if test_range(bloop,loop+1,5,'bottom'):
                                        command['velY'] = -jumping
                        else:
                           move(loop+1,0,-movement,["block"]) 
                    if keyboard.is_pressed("down"):
                        move(loop+1,0,movement,["block"])
                    if keyboard.is_pressed("left"):
                        move(loop+1,-movement,0,["block"])
                    if keyboard.is_pressed("right"):
                        move(loop+1,movement,0,["block"])

            elif command["type"] == "background":
                command["object"].place(x=int(command["x"])-int(camera['x'])+canvas["width"]//2,y=int(command["y"])-int(camera['y'])+canvas["height"]//2)
            
            elif command["type"] == "txt":
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
            pyfile.write(f"import Gamin\nGamin.loadLevel('{username}')\n\nwhile Gamin.isPlaying:\n    Gamin.gameUpdate()")
        with open(username+".gmn","a") as gmnfile:
            gmnfile.write(f"- {username}_project")
    elif useroption == "2":
        import webbrowser
        webbrowser.open("https://catmeooww.github.io/Index-Dev/page.html?-ODNvVVaLs_twwGHgJ7Q!0")