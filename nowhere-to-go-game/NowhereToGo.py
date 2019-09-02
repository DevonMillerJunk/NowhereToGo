###This is my version of Educational Insights "Nowhere To Go"
###By: Devon Miller-Junk

##imports
import pygame
import sys
import time
import random
#Random number seed based on clock to make it more random
random.seed(time.time())
import pygame.event
import pygame.font
import string
import math
##Functions
def GameBackGround():
    #This function draws the background behind the gameboard.
    screen.fill(DARKGREY)
    screen.blit(BlackSpyImage, (0,0))
    screen.blit(WhiteSpyImage, (screenx-BlackSpyImage.get_width(),0))
def CreateGrid(GameBoard):
    # This function converts a cartesian 2-D list into a 2-D hex grid with bridges and pads.
    Pads = []
    Bridges = []
    BridgeNum = []
    Blockers = []
    PadList = {}
    rownum = 0
    colnum = 0
    x = 0
    y = int(((screeny - (len(GameBoard))*87))/2)
    #Making a list of Pad coordinates and a dictionary of the created coordinates
    for row in GameBoard:
        x = 0
        for i in row:
            if i != " ":
                x += 1
        x = int(((screenx - (x)*100))/2)
        for col in row:
            if col == "B" or col == "O" or col == "T":
                padRect =(x+50,y+50)
                Pads.append(padRect)
                PadList[str(colnum)+","+str(rownum)] = len(Pads)
            if col != " ":
                x += 100
            colnum += 1
        y += 87
        rownum += 1
        colnum = 0
    rownum = 0
    colnum = 0
    #Making a list of bridge coordinates by referencing coordinates from the dictionary
    for row in GameBoard:
        for col in row:
            if col == "R" or col == "G":
                if rownum%2 == 0:
                    coordinate = str(int(colnum)-1)+","+str(int(rownum))
                    if coordinate in PadList:
                        startPos = PadList[coordinate] 
                    else:
                        raise Exception("coordinate %s not implemented" % coordinate)
                        
                    coordinate = str(int(colnum)+1)+","+str(int(rownum))
                    if coordinate in PadList:
                        endPos = PadList[coordinate] 
                    else:
                        raise Exception("coordinate %s not implemented" % coordinate)
                        
                elif rownum%2 == 1:
                    if colnum%2 == 0:
                        coordinate = str(int(colnum))+","+str(int(rownum)-1)
                        if coordinate in PadList:
                            startPos = PadList[coordinate] 
                        else:
                            raise Exception("coordinate %s not implemented" % coordinate)
                            
                        coordinate = str(int(colnum))+","+str(int(rownum)+1)
                        if coordinate in PadList:
                            endPos = PadList[coordinate] 
                        else:
                            raise Exception("coordinate %s not implemented" % coordinate) 
                            
                    elif colnum%2 == 1:
                        coordinate = str(int(colnum)-1)+","+str(int(rownum)-1)
                        if coordinate in PadList:
                            startPos = PadList[coordinate] 
                        else:
                            raise Exception("coordinate %s not implemented" % coordinate)
                            
                        coordinate = str(int(colnum)+1)+","+str(int(rownum)+1)
                        if coordinate in PadList:
                            endPos = PadList[coordinate] 
                        else:
                            raise Exception("coordinate %s not implemented" % coordinate)
                startPos = Pads[startPos-1]
                endPos = Pads[endPos-1]
                bridgeRect = (startPos,endPos)
                if col == "R":
                    Bridges.append(bridgeRect)
                    BridgeNum.append((colnum,rownum))
                if col == "G":
                    Blockers.append(bridgeRect)
            colnum +=1
        colnum = 0
        rownum += 1
    return Pads,Bridges,PadList,BridgeNum,Blockers
def DrawGrid(Bridges,Blockers,Pads):
    #Drawing Bridges and Pads
    for i in range (len(Bridges)):
        (coordinateStart,coordinateEnd) = (Bridges[i])
        pygame.draw.line(screen,ORANGE,coordinateStart,coordinateEnd,15)
    for pad in Pads:
        pygame.draw.circle(screen,ORANGE,(pad),50,0)
    for i in range(len(Blockers)):
        (coordinateStart,coordinateEnd) = (Blockers[i])
        pygame.draw.line(screen,ORANGE,coordinateStart,coordinateEnd,15)
        (startx,starty) = coordinateStart
        (endx,endy) = coordinateEnd
        BlockerRect = (((startx + endx)/2),((starty + endy)/2))
        pygame.draw.circle(screen,LGREY,(BlockerRect),15,0)
def InitialRandDestroy(GameBoard):
    #This function finds 8 random bridges to destroy and removes them from the array. (It won't destroy some select bridges)
    for i in range(8):
        DestroyBridge = random.randint(1,34-i)
        score = 1
        Destroying = True
        while Destroying:
            rownum = 0
            colnum = 0
            for row in GameBoard:
                for col in row:
                    if col == "R":
                        coordinate = (colnum,rownum)
                        if coordinate != (0,3):
                            if coordinate != (7,3):
                                if coordinate != (1,4):
                                    if coordinate != (7,4):
                                        if coordinate != (1,5):
                                            if coordinate != (8,5):
                                                if coordinate != (1,3):
                                                    if coordinate != (2,5):
                                                        if coordinate != (3,6):
                                                            if coordinate != (5,7):
                                                                if score == DestroyBridge:
                                                                    GameBoard[rownum] = (GameBoard[rownum])[:colnum]+"G"+(GameBoard[rownum])[colnum+1:]
                                                                    Destroying = False
                                                                score += 1
                    colnum += 1
                colnum = 0
                rownum += 1
    return GameBoard
def ConvertHexCart(Pos):
    #This function takes in the coordinate for a circle on the screen and finds the cartesian coordiante on my graph.
    for j in range(len(Pads)):
        if Pos == Pads[j]:
            Posi = j+1
    #Getting Key from Value taken from Stack Overflow on June 6, 2017
    for coord, PosNum in PadList.items():
        if PosNum == Posi:
            Place = coord
    try:
        Place = Place.split(',')
    except:
        pass
    return Place
def Moveable(GameBoard,Position):
    #This function makes a list of all possible pads a player could move to from their current location
    (x,y) = Position
    Place = PadList[str(int(x))+","+str(int(y))]
    Position = Pads[Place-1]
    MoveList = [Position]
    for i in range(29):
        for Pos in MoveList:
            (x,y) = ConvertHexCart(Pos)
            coordinate = str(int(x))+","+str(int(y))
            if coordinate in PadList:
                StartPos = PadList[coordinate]
                StartPos = Pads[StartPos-1]
                coordinate = str(int(x)+2)+","+str(int(y))
                try:
                    if (GameBoard[int(y)])[int(x)+2] != "T" and (GameBoard[int(y)])[int(x)+2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
                coordinate = str(int(x)-2)+","+str(int(y))
                try:
                    if (GameBoard[int(y)])[int(x)-2] != "T" and (GameBoard[int(y)])[int(x)-2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
                coordinate = str(int(x))+","+str(int(y)+2)
                try:
                    if (GameBoard[int(y)+2])[int(x)] != "T" and (GameBoard[int(y)+2])[int(x)] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
                coordinate = str(int(x))+","+str(int(y)-2)
                try:
                    if (GameBoard[int(y)-2])[int(x)] != "T" and (GameBoard[int(y)-2])[int(x)] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
                coordinate = str(int(x)+2)+","+str(int(y)+2)
                try:
                    if (GameBoard[int(y)+2])[int(x)+2] != "T" and (GameBoard[int(y)+2])[int(x)+2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
                coordinate = str(int(x)-2)+","+str(int(y)-2)
                try:
                    if (GameBoard[int(y)-2])[int(x)-2] != "T" and (GameBoard[int(y)-2])[int(x)-2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    MoveListRepeat = False
                                    for j in range(len(MoveList)):
                                        if MoveList[j] == EndPos:
                                            MoveListRepeat = True
                                    if MoveListRepeat == False:
                                        MoveList.append(EndPos)
                except:
                    pass
    return MoveList
def DrawCharacter(PlyrPos,Plyr):
    #Takes in Cartesian coordinates of the character and draw it on the screen
    (x,y) = PlyrPos
    PosNum = PadList[str(int(x))+","+str(int(y))]
    (x,y) = Pads[PosNum-1]
    #Images taken from Ali Express on June 8, 2017
    if Plyr == "O":
        screen.blit(GameCharacter1,(int(x)-25,int(y)-85))
    else:
        screen.blit(GameCharacter2,(int(x)-25,int(y)-85))
def ShortestRoute(Movement):
    #Uses Dijkstra's algorithm to make a list of the coordinates that the player must move through to get to the desired coordinate
    #Dijkstra's algorithm taken on June 3,2017
    RoutDict = {}
    for Pad in Pads:
        (x,y) = Pad
        RoutDict[str(int(x))+","+str(int(y))] = 31
    (Start,End) = Movement
    (w,x) = Start
    (y,z) = End
    Place = PadList[str(int(w))+","+str(int(x))]
    Position = Pads[Place-1]
    (w,x) = Position
    RoutDict[str(int(w))+","+str(int(x))] = 0
    Place = PadList[str(int(y))+","+str(int(z))]
    Position = Pads[Place-1]
    (q,z) = Position
    DistValue = 0
    #This while loop sets a distance value to each coordinate that can be moved too.
    #The distance value is the number of bridges that you have to cross to reach the coordinate with a distance value of 0.
    while RoutDict[str(int(q))+","+str(int(z))] == 31:
        #Getting Key from Value taken from Stack Overflow on June 6, 2017
        DistList = []
        for coord, PosNum in RoutDict.items():
            if PosNum == DistValue:
                DistList.append(coord)
        DistValue += 1
        for item in range(len(DistList)):
            Place = DistList[item]
            try:
                Place = Place.split(',')
            except:
                pass
            (x,y) = Place
            (x,y) = (int(x),int(y))
            (x,y) = ConvertHexCart((x,y))
            coordinate = str(int(x))+","+str(int(y))
            if coordinate in PadList:
                StartPos = PadList[coordinate]
                StartPos = Pads[StartPos-1]
                coordinate = str(int(x)+2)+","+str(int(y))
                try:
                    if (GameBoard[int(y)])[int(x)+2] != "T" and (GameBoard[int(y)])[int(x)+2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
                coordinate = str(int(x)-2)+","+str(int(y))
                try:
                    if (GameBoard[int(y)])[int(x)-2] != "T" and (GameBoard[int(y)])[int(x)-2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
                coordinate = str(int(x))+","+str(int(y)+2)
                try:
                    if (GameBoard[int(y)+2])[int(x)] != "T" and (GameBoard[int(y)+2])[int(x)] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
                coordinate = str(int(x))+","+str(int(y)-2)
                try:
                    if (GameBoard[int(y)-2])[int(x)] != "T" and (GameBoard[int(y)-2])[int(x)] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
                coordinate = str(int(x)+2)+","+str(int(y)+2)
                try:
                    if (GameBoard[int(y)+2])[int(x)+2] != "T" and (GameBoard[int(y)+2])[int(x)+2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
                coordinate = str(int(x)-2)+","+str(int(y)-2)
                try:
                    if (GameBoard[int(y)-2])[int(x)-2] != "T" and (GameBoard[int(y)-2])[int(x)-2] != "O":
                        if coordinate in PadList:
                            EndPos = PadList[coordinate]
                            EndPos = Pads[EndPos-1]
                            for Place in Bridges:
                                if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                                    (a,b) = EndPos
                                    if RoutDict[str(int(a))+","+str(int(b))] > DistValue:
                                        RoutDict[str(int(a))+","+str(int(b))] = DistValue
                except:
                    pass
    Route = [(q,z)]
    for i in range(RoutDict[str(int(q))+","+str(int(z))]):
        skip = True
        (x,y) = Route[0]
        (x,y) = ConvertHexCart((x,y))
        coordinate = str(int(x))+","+str(int(y))
        if coordinate in PadList:
            StartPos = PadList[coordinate]
            StartPos = Pads[StartPos-1]
            (a,b) = StartPos
            coordinate = str(int(x)+2)+","+str(int(y))
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            coordinate = str(int(x)-2)+","+str(int(y))
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            coordinate = str(int(x))+","+str(int(y)+2)
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            coordinate = str(int(x))+","+str(int(y)-2)
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            coordinate = str(int(x)+2)+","+str(int(y)+2)
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            coordinate = str(int(x)-2)+","+str(int(y)-2)
            try:
                if coordinate in PadList:
                    EndPos = PadList[coordinate]
                    EndPos = Pads[EndPos-1]
                    for Place in Bridges:
                        if(StartPos,EndPos) == Place or (EndPos,StartPos) == Place:
                            if skip:
                                (m,n) = EndPos
                                if RoutDict[str(int(m))+","+str(int(n))] == (RoutDict[str(int(a))+","+str(int(b))])-1:
                                    skip = False
                                    Route.insert(0,EndPos)
            except:
                pass
            if skip == True:
                raise Exception("coordinate %s not implemented" % coordinate)
    return Route
def PlyrPosition(Plyr):
    #This function gives cartesian coordinates for the player position when given the letter
    colnum = 0
    rownum = 0
    for row in GameBoard:
        for col in row:
            if col == Plyr:
                PlyrPos = (colnum, rownum)
            colnum += 1
        colnum = 0
        rownum += 1
    return PlyrPos
def AnimateRoute(StartPos,EndPos,Plyr):
    #This function takes two positions and animates the characters movement between the two values.
    (a,b) = StartPos
    (c,d) = EndPos
    if Plyr == "O":
        GameCharacter = GameCharacter1
    else:
        GameCharacter = GameCharacter2
    for i in range (60):
        dx = int((c-a)/float(60-i))
        dy = int((d-b)/float(60-i))
        a += dx
        b += dy
        GameBackGround()
        DrawGrid(Bridges,Blockers,Pads)
        if Plyr == "O":
            PlyrPos2 = PlyrPosition("T")
            DrawCharacter(PlyrPos2,"T")
        else:
            PlyrPos1 = PlyrPosition("O")
            DrawCharacter(PlyrPos1,"O")
        screen.blit(GameCharacter,(a-25,b-85))
        pygame.display.update()
        clock.tick(45)
    GameBackGround()
    DrawGrid(Bridges,Blockers,Pads)
    if Plyr == "O":
        PlyrPos2 = PlyrPosition("T")
        DrawCharacter(PlyrPos2,"T")
    else:
        PlyrPos1 = PlyrPosition("O")
        DrawCharacter(PlyrPos1,"O")
    screen.blit(GameCharacter,(c-25,d-85))
    pygame.display.update()
    (a,b) = ConvertHexCart(StartPos)
    (c,d) = ConvertHexCart(EndPos)
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    GameBoard[b] = (GameBoard[b])[:a]+"B"+(GameBoard[b])[(a+1):]
    if Plyr == "O":
        GameBoard[d] = (GameBoard[d])[:c]+"O"+(GameBoard[d])[(c+1):]
    elif Plyr == "T":
        GameBoard[d] = (GameBoard[d])[:c]+"T"+(GameBoard[d])[(c+1):]
##Screen and initial variables

    #Pygame Screen
pygame.init()
screenx = 1000
screeny = 900
##screeny = 600
screenSize = (screenx,screeny)
screen = pygame.display.set_mode((screenSize),0)
pygame.display.set_caption("NowhereToGo")

    #Colours
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
PURPLE = (175,0,175)
YELLOW = (175,175,0)
CYAN = (0,175,175)
ORANGE = (255,155,55)
BLACK = (32,32,32)
DARKGREY = (64,64,64)
MAGENTA = (255,0,127)
DARKORANGE = (255,140,0)
LORANGE = (255,165,0)
LGREY = (211,211,211)

    #Font and Sizes
Bebas60 = pygame.font.SysFont("bebas",60)
Bebas30 = pygame.font.SysFont("bebas",30)

    #Variables
clock = pygame.time.Clock()
Lost = "NoOne"

##Initial Log in Screen
screen.fill(WHITE)
    #Image taken from Educational Insights, May 28, 2017
TitleImage = pygame.image.load("Images\TitleScreen.png").convert()
    #Images Taken from Mad Magazine, May 28, 2017
BlackSpyImage = pygame.image.load("Images\BlackSpyBackGround.png")
WhiteSpyImage = pygame.image.load("Images\WhiteSpyBackGround.png")
GameCharacter1 = pygame.image.load("Images\GameCharacter1.png")
GameCharacter2 = pygame.image.load("Images\GameCharacter2.png")
    #Image Taken from Mad Magazine, June 14, 2017
WinScreen1 = pygame.image.load("Images\BSpyWin.png").convert()
WinScreen2 = pygame.image.load("Images\WSpyWin.png").convert()
Playbox = Bebas60.render("Play Game",True,DARKORANGE)
OnPlyrbox = Bebas60.render("1 Player",True,DARKORANGE)
TwPlyrbox = Bebas60.render("2 Player",True,DARKORANGE)
Instrbox = Bebas60.render("Instructions",True,DARKORANGE)
Exitbox = Bebas60.render("Exit Game",True,DARKORANGE)
Backbox = Bebas60.render("Back to Main Menu",True,DARKORANGE)
Tilebox1 = Bebas30.render("Black Player, Choose a Tile to Move to",True,DARKORANGE)
Tilebox2 = Bebas30.render("White Player, Choose a Tile to Move to",True,DARKORANGE)
Bridgebox1 = Bebas30.render("Black Player, Choose a bridge to block",True,DARKORANGE)
Bridgebox2 = Bebas30.render("White Player, Choose a bridge to block",True,DARKORANGE)
PlayRect = pygame.Rect(50,550,Playbox.get_width(),Playbox.get_height())
OnPlyrRect = pygame.Rect(50,550,OnPlyrbox.get_width(),OnPlyrbox.get_height())
TwPlyrRect = pygame.Rect(50,550 + OnPlyrbox.get_height()+35,TwPlyrbox.get_width(),TwPlyrbox.get_height())
InstrRect = pygame.Rect(50,550 + Playbox.get_height()+35,Instrbox.get_width(),Instrbox.get_height())
ExitRect = pygame.Rect(50,550 + Playbox.get_height()+70 + Instrbox.get_height(),Exitbox.get_width(),Exitbox.get_height())
BackRect = pygame.Rect(50,550 + OnPlyrbox.get_height()+70 + TwPlyrbox.get_height(),Backbox.get_width(),Backbox.get_height())
EndBackRect = pygame.Rect(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height())
Game = True
while Game == True:
    playing = True
    PlyrLost = False
    PlayOptions = False
    Exit = False
    Instructions = False
    height = 0
    iy = 50
    diy = 0
    while playing:
        if Instructions == False:
            screen.fill(WHITE)
            screen.blit(TitleImage, (((screenx-TitleImage.get_width())/2),((screeny-TitleImage.get_height())/2)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    Exit = True
                    Game = False
                    Turns = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        if PlayOptions:
                            ################if OnPlyrRect.collidepoint(mousePos):
                            if TwPlyrRect.collidepoint(mousePos):
                                playing = False
                            if BackRect.collidepoint(mousePos):
                                PlayOptions = False
                        else:
                            if ExitRect.collidepoint(mousePos):
                                Exit = True
                                playing = False
                                Game = False
                                Turns = False
                                break
                            if PlayRect.collidepoint(mousePos):
                                PlayOptions = True
                            if InstrRect.collidepoint(mousePos):
                                Instructions = True
                                height = 0
                                iy = 50
                                diy = 0
                                break
            mousePos = pygame.mouse.get_pos()
            if PlayOptions:
                if OnPlyrRect.collidepoint(mousePos):
                    OnPlyrbox = Bebas60.render("1 Player",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550,OnPlyrbox.get_width(),OnPlyrbox.get_height()),0)
                else:
                    OnPlyrbox = Bebas60.render("1 Player",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550,OnPlyrbox.get_width(),OnPlyrbox.get_height()),0)
                if TwPlyrRect.collidepoint(mousePos):
                    TwPlyrbox = Bebas60.render("2 Player",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550 + OnPlyrbox.get_height()+35,TwPlyrbox.get_width(),TwPlyrbox.get_height()),0)
                else:
                    TwPlyrbox = Bebas60.render("2 Player",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550 + OnPlyrbox.get_height()+35,TwPlyrbox.get_width(),TwPlyrbox.get_height()),0)
                if BackRect.collidepoint(mousePos):
                    Backbox = Bebas60.render("Back to Main Menu",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550 + OnPlyrbox.get_height()+70 + TwPlyrbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                else:
                    Backbox = Bebas60.render("Back to Main Menu",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550 + OnPlyrbox.get_height()+70 + TwPlyrbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                screen.blit(OnPlyrbox, (50,550))
                screen.blit(TwPlyrbox, (50,550 + OnPlyrbox.get_height()+35))
                screen.blit(Backbox, (50,550 + OnPlyrbox.get_height()+70 + TwPlyrbox.get_height()))
            else:
                if PlayRect.collidepoint(mousePos):
                    Playbox = Bebas60.render("Play Game",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550,Playbox.get_width(),Playbox.get_height()),0)
                else:
                    Playbox = Bebas60.render("Play Game",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550,Playbox.get_width(),Playbox.get_height()),0)
                if InstrRect.collidepoint(mousePos):
                    Instrbox = Bebas60.render("Instructions",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550 + Playbox.get_height()+35,Instrbox.get_width(),Instrbox.get_height()),0)
                else:
                    Instrbox = Bebas60.render("Instructions",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550 + Playbox.get_height()+35,Instrbox.get_width(),Instrbox.get_height()),0)
                if ExitRect.collidepoint(mousePos):
                    Exitbox = Bebas60.render("Exit Game",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,550 + Playbox.get_height()+70 + Instrbox.get_height(),Exitbox.get_width(),Exitbox.get_height()),0)
                else:
                    Exitbox = Bebas60.render("Exit Game",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,550 + Playbox.get_height()+70 + Instrbox.get_height(),Exitbox.get_width(),Exitbox.get_height()),0)    
                screen.blit(Playbox, (50,550))
                screen.blit(Instrbox, (50,550 + Playbox.get_height()+35))
                screen.blit(Exitbox, (50,550 + Playbox.get_height()+70 + Instrbox.get_height()))
            pygame.display.update()
            clock.tick(60)
            
        #Displaying Instructions    
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Exit = True
                    playing = False
                    Game = False
                    Turns = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if EndBackRect.collidepoint(mousePos):
                        Instructions = False
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        diy = 5
                    if event.key == pygame.K_UP:
                        diy = -5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        diy = 0
                    if event.key == pygame.K_UP:
                        diy = 0
            iy += diy
            if iy > screeny-100-Backbox.get_height():
                iy = screeny-100-Backbox.get_height()
            if Instructions:
                GameBackGround()
                newFile = open("Documents\Instructions.txt", 'r')
                height = 0
                for line in newFile:
                    linestr = line
                    linestr = linestr.rstrip('\n')
                    Instrbox = Bebas60.render(linestr,True,DARKORANGE)
                    a = ((screenx-Instrbox.get_width())/2)
                    b = height + iy
                    if b + Instrbox.get_height() < screeny-50-Backbox.get_height() and b-Instrbox.get_height() > 0:
                        screen.blit(Instrbox,(a,b))
                    height += Instrbox.get_height()+10
                mousePos = pygame.mouse.get_pos()
                if EndBackRect.collidepoint(mousePos):
                    Backbox = Bebas60.render("Back to Main Menu",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                else:
                    Backbox = Bebas60.render("Back to Main Menu",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                screen.blit(Backbox,(50,screeny-50-Backbox.get_height()))
                pygame.display.update()
                clock.tick(120)
                newFile.close()
            #Instructions = False
    ##Making Grid
    GameBoard = [
    "BRBRB    " ,
    "RRRRRR   " ,
    "BRBRBRB  " ,
    "RRRRRRRR " ,
    "ORBRBRBRT" ,
    " RRRRRRRR" ,
    "  BRBRBRB" ,
    "   RRRRRR" ,
    "    BRBRB" ,
    ]
    if Exit == False:
        GameBackGround()
        #Destroying Random bridges
        GameBoard = InitialRandDestroy(GameBoard)
        #Drawing Hex Grid
        (Pads,Bridges,PadList,BridgeNum,Blockers) = CreateGrid(GameBoard)
        DrawGrid(Bridges,Blockers,Pads)
        pygame.display.update()
    ##Individual Turns
        PlyrPos2 = PlyrPosition("T")
        PlyrPos1 = PlyrPosition("O")
        TurnScore = 0
        Turns = True
        while Turns:
            TurnScore += 1
            if TurnScore%2 == 1:
                TurnPlyr1 = True
            else:
                TurnPlyr1 = False
            if TurnPlyr1:
                PlyrPos = PlyrPos1
            else:
                PlyrPos = PlyrPos2
        #Determine all possible tiles play can move to
            MoveList = Moveable(GameBoard,PlyrPos)
            #Determine if a player has lost
            playing = True
            if len(MoveList)<2:
                Turns = False
                if TurnPlyr1:
                    Lost = "Plyr1"
                    #print "Player 2 Won"
                else:
                    Lost = "Plyr2"
                    #print "Player 1 Won"
            while playing and Lost == "NoOne":
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        playing = False
                        Exit = True
                        Turns = False
                        Game = False
                        break
        #Recieve input of tile choice
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        (Mx,My) = pygame.mouse.get_pos()
                        for i in range (len(MoveList)-1):
                            (x,y) = MoveList[i+1]
                            dist = int(math.sqrt(((float(x)-float(Mx))**2)+((float(y)-float(My))**2)))
                            if dist <= 50:
                                (x,y) = ConvertHexCart((x,y))
                                Movement = (PlyrPos,(int(x),int(y)))
                                playing = False                
                #Drawing Everything
                GameBackGround()
                DrawGrid(Bridges,Blockers,Pads)
                PlyrPos2 =  PlyrPosition("T")
                PlyrPos1 = PlyrPosition("O")
                #Character Images
                DrawCharacter(PlyrPos1,"O")
                DrawCharacter(PlyrPos2,"T")
                if TurnPlyr1:
                    screen.blit(Tilebox1,((screenx-(Tilebox1.get_width()))/2,10))
                else:
                    screen.blit(Tilebox2,((screenx-(Tilebox2.get_width()))/2,10))
                pygame.display.update()
                (Mx,My) = pygame.mouse.get_pos()
                for i in range (len(MoveList)-1):
                    (x,y) = MoveList[i+1]
                    dist = int(math.sqrt(((float(x)-float(Mx))**2)+((float(y)-float(My))**2)))
                    if dist <= 45:
                        pygame.draw.circle(screen,BLUE,(x,y),45,0)
                        pygame.display.update()

            #Determine best path to chosen tile
            if Exit == False and Lost == "NoOne":
                Route = ShortestRoute(Movement)
                #Animation of path
                for i in range(len(Route)-1):
                    if TurnPlyr1:
                        AnimateRoute(Route[i],Route[i+1],"O")
                    else:
                        AnimateRoute(Route[i],Route[i+1],"T")
        #Destroying Bridge
                Playing = True
                while Playing:
                    clock.tick(60)
                    GameBackGround()
                    DrawGrid(Bridges,Blockers,Pads)
                    PlyrPos2 =  PlyrPosition("T")
                    PlyrPos1 = PlyrPosition("O")
                    DrawCharacter(PlyrPos1,"O")
                    DrawCharacter(PlyrPos2,"T")
                    if TurnPlyr1:
                        screen.blit(Bridgebox1,((screenx-(Bridgebox1.get_width()))/2,10))
                    else:
                        screen.blit(Bridgebox2,((screenx-(Bridgebox2.get_width()))/2,10))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Playing = False
                            playing = False
                            Exit = True
                            Turns = False
                            Game = False
                            break
            #Choosing Bridge to destroy
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            (Mx,My) = pygame.mouse.get_pos()
                            for i in range (len(Bridges)):
                                ((a,b),(c,d)) = Bridges[i]
                                x = (a+c)/2.0
                                y = (b+d)/2.0
                                dist = int(math.sqrt(((float(x)-float(Mx))**2)+((float(y)-float(My))**2)))
                                if dist <= 25:
                                    (x,y) = BridgeNum[i]
                                    GameBoard[y] =  (GameBoard[y])[:x]+"G"+(GameBoard[y])[(x+1):]
                                    (Pads,Bridges,PadList,BridgeNum,Blockers) = CreateGrid(GameBoard)
                                    Playing = False
                                    break
                    (Mx,My) = pygame.mouse.get_pos()
                    for i in range (len(Bridges)):
                        ((a,b),(c,d)) = Bridges[i]
                        x = (a+c)/2.0
                        y = (b+d)/2.0
                        dist = int(math.sqrt(((float(x)-float(Mx))**2)+((float(y)-float(My))**2)))
                        if dist <= 25:
                            pygame.draw.circle(screen,BLUE,(int(x),int(y)),25,0)
                            pygame.display.update()
    ##Finish Screen
        if Exit == False and Lost != "NoOne":
            screen.fill(WHITE)
            #Display Screen
            if Lost == "Plyr1":
                screen.blit(WinScreen2,(0,0))
            elif Lost == "Plyr2":
                screen.blit(WinScreen1,(0,0))
            Playing = True
            pygame.display.update()
            clock.tick(100)
            while Playing:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        playing = False
                        Exit = True
                        Turns = False
                        Game = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        if EndBackRect.collidepoint(mousePos):
                            Playing = False
                            break
                screen.fill(DARKGREY)
                if Lost == "Plyr1":
                    screen.blit(WinScreen2,(0,0))
                elif Lost == "Plyr2":
                    screen.blit(WinScreen1,(0,0))
                mousePos = pygame.mouse.get_pos()
                if EndBackRect.collidepoint(mousePos):
                    Backbox = Bebas60.render("Back to Main Menu",True,LORANGE)
                    pygame.draw.rect(screen, DARKGREY,(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                else:
                    Backbox = Bebas60.render("Back to Main Menu",True,DARKORANGE)
                    pygame.draw.rect(screen, BLACK,(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height()),0)
                screen.blit(Backbox,(50,screeny-50-Backbox.get_height()))
                pygame.display.update()
        Lost = "NoOne"
        PlayRect = pygame.Rect(50,550,Playbox.get_width(),Playbox.get_height())
        OnPlyrRect = pygame.Rect(50,550,OnPlyrbox.get_width(),OnPlyrbox.get_height())
        TwPlyrRect = pygame.Rect(50,550 + OnPlyrbox.get_height()+35,TwPlyrbox.get_width(),TwPlyrbox.get_height())
        InstrRect = pygame.Rect(50,550 + Playbox.get_height()+35,Instrbox.get_width(),Instrbox.get_height())
        ExitRect = pygame.Rect(50,550 + Playbox.get_height()+70 + Instrbox.get_height(),Exitbox.get_width(),Exitbox.get_height())
        BackRect = pygame.Rect(50,550 + OnPlyrbox.get_height()+70 + TwPlyrbox.get_height(),Backbox.get_width(),Backbox.get_height())
        EndBackRect = pygame.Rect(50,screeny-50-Backbox.get_height(),Backbox.get_width(),Backbox.get_height())
    ##Revert back to beginning
pygame.quit()
sys.exit()