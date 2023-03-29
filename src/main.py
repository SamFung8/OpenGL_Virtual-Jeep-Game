#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time, random, csv, datetime, os
import ImportObject
import PIL.Image as Image
import jeep, cone, star
import GameSetting
import RankingTable

jeepSpeed = 0.02

windowSizeWidth = 800
windowSizeHeight = 600
windowSizeRatio = float(windowSizeWidth/windowSizeHeight)
fullScreen = False
helpWindow = False
helpWin = 0
mainWin = 0
centered = False

beginTime = 0
countTime = 0
startTime = 0
score = 0
finalScore = 0
StarScore = 0
playerName = 0
canStart = False
canPlay = False
overReason = ""

#for wheel spinning
tickTime = 0

#creating objects
objectArray = []
jeep1Obj = jeep.jeep('p')
jeep2Obj = jeep.jeep('g')
jeep3Obj = jeep.jeep('r')
jeepObjZ = 0
jeepObjY = 0
jeepObjX = 0

allJeeps = [jeep1Obj, jeep2Obj, jeep3Obj]
jeepNum = 0
jeepObj = allJeeps[jeepNum]
#personObj = person.person(10.0,10.0)

#concerned with camera
eyeX = 0.0
eyeY = 10.0
eyeZ = -10.0
midDown = False
topView = False
behindView = False
cameraView = True

#concerned with panning
nowX = 0.0
nowY = 0.0

angle = 0.0
radius = 10.0
phi = 0.0

#concerned with scene development
land = 20
gameEnlarge = 10

#concerned with obstacles (cones) & rewards (stars)
coneAmount = 10
starAmount = 5 #val = -10 pts
diamondAmount = 1 #val = deducts entire by 1/2
# diamondObj = diamond.diamond(random.randint(-land, land), random.randint(10.0, land*gameEnlarge))
usedDiamond = False

allcones = []
allstars = []
obstacleCoord = []
rewardCoord = []
ckSense = 4.0

#                           right-down              right-top           left-top            left-down
acceleratingRibbonList = [[[land-10, 0.1, 60], [land-10, 0.1, 50], [-land+10, 0.1, 50], [-land+10, 0.1, 60]], 
                          [[land-5, 0.1, 100], [land-5, 0.1, 90], [-land+15, 0.1, 90], [-land+15, 0.1, 100]],
                          [[land-15, 0.1, 150], [land-15, 0.1, 140], [-land+5, 0.1, 140], [-land+5, 0.1, 150]],
                          [[land-20, 0.1, 190], [land-20, 0.1, 180], [-land, 0.1, 180], [-land, 0.1, 190]]]

#concerned with lighting#########################!!!!!!!!!!!!!!!!##########
applyLighting = True
drawSun = False
currentlight = -1
sunAngle=0

sunX=0.5
sunY=30
sunZ=80

fov = 30.0
attenuation = 1.0

light0_Position = [0.0, 1.0, 1.0, 1.0]
light0_Intensity = [0.75, 0.75, 0.75, 0.25]

light1_Position = [0.0, 0.0, 0.0, 0.0]
light1_Intensity = [0.25, 0.25, 0.25, 0.25]

matAmbient = [0.05375, 0.05, 0.06625, 0.82]
matDiffuse = [0.18275, 0.17, 0.22525, 0.82]
matSpecular = [0.332741, 0.328634, 0.346435, 0.82]
matShininess  = 38.4



#--------------------------------------developing scene---------------
class Scene:
    axisColor = (0.5, 0.5, 0.5, 0.5)
    axisLength = 50   # Extends to positive and negative on all axes
    landColor = (.47, .53, .6, 0.5) #Light Slate Grey
    landLength = land  # Extends to positive and negative on x and y axis
    landW = 1.0
    landH = 0.0
    cont = gameEnlarge
    
    def draw(self):
        #self.drawAxis()
        self.drawLand()
        self.drawAcceleratingRibbon()

    def drawAxis(self):
        glColor4f(self.axisColor[0], self.axisColor[1], self.axisColor[2], self.axisColor[3])
        glBegin(GL_LINES)
        glVertex(-self.axisLength, 0, 0)
        glVertex(self.axisLength, 0, 0)
        glVertex(0, -self.axisLength, 0)
        glVertex(0, self.axisLength, 0)
        glVertex(0, 0, -self.axisLength)
        glVertex(0, 0, self.axisLength)
        glEnd()

    def drawLand(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, roadTextureID)

        glBegin(GL_POLYGON)

        glTexCoord2f(self.landH, self.landH)
        glVertex3f(self.landLength, 0, self.cont * self.landLength)

        glTexCoord2f(self.landH, self.landW)
        glVertex3f(self.landLength, 0, -self.landLength)

        glTexCoord2f(self.landW, self.landW)
        glVertex3f(-self.landLength, 0, -self.landLength)

        glTexCoord2f(self.landW, self.landH)
        glVertex3f(-self.landLength, 0, self.cont * self.landLength)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        
    def drawAcceleratingRibbon(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, acceleratingRibbonID)
        
        global acceleratingRibbonList
        for ribbon in acceleratingRibbonList:
            glBegin(GL_POLYGON)
            #right-down
            glTexCoord2f(self.landH, self.landH)
            glVertex3f(ribbon[0][0], ribbon[0][1], ribbon[0][2])
            #right-top
            glTexCoord2f(self.landH, self.landW)
            glVertex3f(ribbon[1][0], ribbon[1][1], ribbon[1][2])
            #left-top
            glTexCoord2f(self.landW, self.landW)
            glVertex3f(ribbon[2][0], ribbon[2][1], ribbon[2][2])
            #left-down
            glTexCoord2f(self.landW, self.landH)
            glVertex3f(ribbon[3][0], ribbon[3][1], ribbon[3][2])
            glEnd()

        glDisable(GL_TEXTURE_2D)

#--------------------------------------populating scene----------------
def staticObjects():
    global objectArray
    objectArray.append(Scene())
    print "scene appended"


def display():
    global jeepObj, canStart, score, beginTime, countTime, applyLighting, prevTime
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if drawSun:
        glPushMatrix()
        glColor3f(1.0,1.0,0.0)
        glTranslatef(sunX, sunY, sunZ)
        glutSolidSphere(5.0, 92, 38)
        glPopMatrix()
        
    if canPlay:
        #print score
        beginTime = 6-score
        countTime = score-6
        if (score <= 5):
            #prevTime = glutGet(GLUT_ELAPSED_TIME)
            canStart = False
            glColor3f(1.0,0.0,1.0)
            text3d("Begins in: "+str(beginTime), jeepObj.posX + 2, jeepObj.posY + 3.0, jeepObj.posZ)
        elif (score == 6):
            canStart = True
            glColor(1.0,0.0,1.0)
            text3d("GO!", jeepObj.posX + 0.5, jeepObj.posY + 3.0, jeepObj.posZ)
            prevTime = glutGet(GLUT_ELAPSED_TIME)
        else:
            canStart = True
            glColor3f(0.0,1.0,1.0)
            text3d("Time: "+str(countTime), jeepObj.posX + 0.5, jeepObj.posY + 3.0, jeepObj.posZ)
            text3d("Star: "+str(starAmount -len(allstars)), jeepObj.posX + 0.5, jeepObj.posY + 4.0, jeepObj.posZ)
    else:
        glColor3f(1.0,0.0,1.0)
        text3d("Please push 's' to start the game!", jeepObj.posX + 5, jeepObj.posY + 5.0, jeepObj.posZ)       

    for obj in objectArray:
        obj.draw()
    for cone in allcones:
        cone.draw()
    for star in allstars:
        star.draw()
    # if (usedDiamond == False):
    #     diamondObj.draw()
    
    #glClear(GL_DEPTH_BUFFER_BIT)
    
    jeepObj.draw()
    jeepObj.drawW1()
    jeepObj.drawW2()
    jeepObj.drawLight()
    
    #glClear(GL_COLOR_BUFFER_BIT)
    
    #personObj.draw()
    glutSwapBuffers()

    if (applyLighting == True):
        glPushMatrix()
        glLoadIdentity()
        #glViewport(0, 0, windowSizeWidth, windowSizeHeight)
        #gluLookAt(0.0, 3.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        #glEnable(GL_LIGHTING)
        #glClear(GL_COLOR_BUFFER_MASK | GL_DEPTH_BUFFER_MASK);
        #glLightfv(GL_LIGHT0, GL_POSITION, [jeep1Obj.posX, jeepObj.posY , jeepObj.posZ + 2, 1])
        #pointPosition = [0.0,-10.0,0.0]

        #glDisable(GL_LIGHTING)

        #glColor3f(light0_Intensity[0], light0_Intensity[1], light0_Intensity[2])
        
        #glColor3f(1.0 , 0.0 , 0.0)

        #glTranslatef(light0_Position[0], light0_Position[1], light0_Position[2])

        #glutSolidSphere(10.25, 36, 24)

        #glTranslatef(-light0_Position[0], -light0_Position[1], -light0_Position[2])
        #glEnable(GL_LIGHTING)
        #glMaterialfv(GL_FRONT, GL_AMBIENT, matAmbient)
        
        #for x in range(1,4):
            #for z in range(1,4):
                 #matDiffuse = [float(x) * 0.3, float(x) * 0.3, float(x) * 0.3, 1.0] 
                 #matSpecular = [float(z) * 0.3, float(z) * 0.3, float(z) * 0.3, 1.0]  
                 #matShininess = float(z * z) * 10.0
                 ## Set the material diffuse values for the polygon front faces. 
                 #glMaterialfv(GL_FRONT, GL_DIFFUSE, matDiffuse)

                 ## Set the material specular values for the polygon front faces. 
                 #glMaterialfv(GL_FRONT, GL_SPECULAR, matSpecular)

                 ## Set the material shininess value for the polygon front faces. 
                 #glMaterialfv(GL_FRONT, GL_SHININESS, matShininess)

                 ## Draw a glut solid sphere with inputs radius, slices, and stacks
                 #glutSolidSphere(10.25, 72, 64)
                 #glTranslatef(1.0, 0.0, 0.0)

            #glTranslatef(-3.0, 0.0, 1.0)
        
        #glClear(GL_COLOR_BUFFER_BIT)
        #glEnable(GL_LIGHTING)


        
        #glColorMaterial ( GL_FRONT, GL_AMBIENT_AND_DIFFUSE )
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, matAmbient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, matDiffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, matSpecular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, matShininess)
               
        # ---------spotlight--------------light 0
        glLightfv(GL_LIGHT0, GL_POSITION, [jeepObj.posX, jeepObj.posY + 2 , jeepObj.posZ + 40, 1])
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 45)
        glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION, [0,0,-1])
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 128)
        diffuseLight = [0.8, 0.8, 0.8, 1.0]      
        specularLight = [0.3, 0.8, 0.6, 1.0]
        ambientLight = [0.2, 0.2, 0.2, 1.0]
        glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE,diffuseLight)
        glLightfv(GL_LIGHT0,GL_SPECULAR,specularLight)
        glLightfv(GL_LIGHT0,GL_CONSTANT_ATTENUATION,0.5)

        
        
        #------------directional light------------light 1
        glLightfv(GL_LIGHT1, GL_POSITION, [sunX, sunY - 30, -sunZ, 0])
        diffuseLight = [0.8, 0.8, 0.8, 1.0]      
        specularLight = [0.3, 0.8, 0.6, 1.0]
        ambientLight = [0.2, 0.2, 0.2, 1.0]
        glLightfv(GL_LIGHT1,GL_AMBIENT,ambientLight)
        glLightfv(GL_LIGHT1,GL_DIFFUSE,diffuseLight)
        glLightfv(GL_LIGHT1,GL_SPECULAR,specularLight)
        
        
        #------------point light------------light 2
        glLightfv(GL_LIGHT2, GL_POSITION, [sunX, -sunY + 30, -sunZ, 1])
        diffuseLight = [0.8, 0.8, 0.8, 1.0]      
        specularLight = [0.3, 0.8, 0.6, 1.0]
        ambientLight = [0.2, 0.2, 0.2, 1.0]
        glLightfv(GL_LIGHT2,GL_AMBIENT,ambientLight)
        glLightfv(GL_LIGHT2,GL_DIFFUSE,diffuseLight)
        glLightfv(GL_LIGHT2,GL_SPECULAR,specularLight)
        
        
        
        glPopMatrix()
        setObjView()
        glFlush()
        glutSwapBuffers ()
        applyLighting = False

    
    #glutSolidSphere(10.25, 72, 64)
    glLightfv(GL_LIGHT0, GL_POSITION, [jeep1Obj.posX, jeepObj.posY + 2, jeepObj.posZ + 40, 1])
    #glutSolidSphere(2, 32, 18)

def idle():#--------------with more complex display items like turning wheel---
    global tickTime, prevTime, score, sunAngle, sunX, sunY, sunZ, canPlay, startTime
    jeepObj.rotateWheel(-0.1 * tickTime)    
    glutPostRedisplay()
    
    #print(startTime)
    if canPlay:
        curTime = glutGet(GLUT_ELAPSED_TIME)
        #tickTime =  curTime - prevTime
        prevTime = curTime
        score = curTime/1000 - startTime
        
    if canStart:
        #jeepObj.posZ = jeepObj.posZ + jeepSpeed
        curTime = glutGet(GLUT_ELAPSED_TIME)
        tickTime =  curTime - prevTime
        prevTime = curTime
        score = curTime/1000 - startTime
     
    if drawSun:            
        sunAngle = sunAngle + 0.05
        sunRx = sunZ * math.sin(math.radians(sunAngle)) + sunX * math.cos(math.radians(sunAngle))
        sunRz = sunZ * math.cos(math.radians(sunAngle)) - sunX * math.sin(math.radians(sunAngle))
        glLightfv(GL_LIGHT1, GL_POSITION, [sunRx, sunY - 30, -sunRz, 0])
        glutDisplayFunc(display)

    setObjView()
    collisionCheck()

#---------------------------------setting camera----------------------------
def setView():
    global eyeX, eyeY, eyeZ, windowSizeWidth, windowSizeHeight, windowSizeRatio
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, float(windowSizeRatio), float(0.01), float(100.0))
    if (topView == True):
        gluLookAt(jeepObj.posX, jeepObj.posY + 45 , jeepObj.posZ - 1.0, jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)
    elif (behindView ==True):
        gluLookAt(jeepObj.posX, jeepObj.posY + 6.0, jeepObj.posZ - 10.0, jeepObj.posX + jeepObjX, jeepObj.posY, jeepObj.posZ, 0, 1, 0) 
    elif (cameraView == True):
        gluLookAt(jeepObj.posX + eyeX,jeepObj.posY + eyeY ,jeepObj.posZ + eyeZ , jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    
    glutPostRedisplay()    

def setObjView():
    # things to do
    # realize a view following the jeep
    global eyeX, eyeY, eyeZ, windowSizeWidth, windowSizeHeight, windowSizeRatio
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, float(windowSizeRatio), float(0.1), float(100.0))
     
    if (topView == True):
        gluLookAt(jeepObj.posX, jeepObj.posY + 45 + radius, jeepObj.posZ - 1.0, jeepObj.posX, jeepObj.posY + jeepObjY, jeepObj.posZ + jeepObjZ, 0, 1, 0)
    elif (behindView ==True):
        gluLookAt(jeepObj.posX, jeepObj.posY + 8.0, jeepObj.posZ - radius, jeepObj.posX, jeepObj.posY + 8.0, jeepObj.posZ, 0, 1, 0) 
    elif (cameraView == True):
        gluLookAt(jeepObj.posX + eyeX,jeepObj.posY + eyeY ,jeepObj.posZ + eyeZ , jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)
       
        
    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()

#-------------------------------------------user inputs------------------
def mouseHandle(button, state, x, y):
    global midDown
    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        midDown = True
        # print "getting pushed"
    else:
        midDown = False    
        
def motionHandle(x,y):
    global nowX, nowY, angle, eyeX, eyeY, eyeZ, phi
    if (midDown == True):
        pastX = nowX
        pastY = nowY 
        nowX = x
        nowY = y
        if (nowX - pastX > 0):
            angle -= 0.03
        elif (nowX - pastX < 0):
            angle += 0.03
        
        if (nowY - pastY > 0): #look into looking over and under object...
            phi += 0.03
        elif (nowY - pastY <0):
            phi -= 0.03            
        
        eyeZ = radius * math.cos(phi) * math.cos(angle)
        eyeX = radius * math.sin(angle) * math.cos(phi)
        eyeY = radius * math.sin(phi)            
        
        
    if centered == False:
        setView()
    elif centered == True:
        setObjView()
    #print eyeX, eyeY, eyeZ, nowX, nowY, radius, angle, phi
    #print "getting handled"

def mouseScroll(button, scroll, x, y):
    global eyeX, eyeY, eyeZ, radius
    
    if (scroll > 0): #zoom in
        radius -= 1
        #setView()
        print("zoom in!")
    elif (scroll < 0): #zoom out
        radius += 1
        #setView()
        print("zoom out!")
        
    eyeZ = radius * math.cos(phi) * math.cos(angle)
    #eyeZ = radius * math.cos(angle)
    eyeX = radius * math.sin(angle) * math.cos(phi)
    eyeY = radius * math.sin(phi)  
    
    setObjView()

def specialKeys(keypress, mX, mY):
    # things to do
    # this is the function to move the car
    #Move car object
    if canStart:
        if keypress == GLUT_KEY_UP:
            print "Up pushed!"
            jeepObj.posZ = jeepObj.posZ + 0.5
            # for cone in allcones:
            #     cone.posZ = cone.posZ - 0.5
            # for star in allstars:
            #     star.posZ = star.posZ - 0.5
        elif keypress == GLUT_KEY_LEFT:
            print "Left pushed!"
            jeepObj.posX = jeepObj.posX + 0.5
        elif keypress == GLUT_KEY_RIGHT:
            print "Right pushed!"
            jeepObj.posX = jeepObj.posX - 0.5
        
        # Refresh look at view
        setObjView()
       
    
def myKeyboard(key, mX, mY):
    global eyeX, eyeY, eyeZ, angle, radius, helpWindow, centered, helpWin, overReason, topView, behindView, windowSizeWidth, windowSizeHeight, canPlay, playerName, prevTime, startTime
    if key == "h":
        print "h pushed " + str(helpWindow)
        winNum = glutGetWindow()
        if helpWindow == False:
            helpWindow = True
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
            glutInitWindowSize(500,300)
            glutInitWindowPosition(600,0)
            helpWin = glutCreateWindow('Help Guide')
            glutDisplayFunc(showHelp)
            glutKeyboardFunc(myKeyboard)
            glutMainLoop()
        elif helpWindow == True and winNum!=1:
            helpWindow = False
            print glutGetWindow()
            glutHideWindow()
            #glutDestroyWindow(helpWin)
            glutMainLoop()
    elif key == '1':
        GameSetting.reopen_setting_window()
        GameSetting.run_setting()
        fullScreen ,windowSizeWidth, windowSizeHeight, playerName = GameSetting.get_setting_info()
        print("Changed screen size to: " + str(windowSizeWidth) + " x " + str(windowSizeHeight))
        GameSetting.close_setting_window()
        if (fullScreen):
            glutFullScreen()
               
        glutReshapeWindow(windowSizeWidth, windowSizeHeight)
        glutPostRedisplay()
    elif key == 's':
        if canPlay == False:
            startTime = glutGet(GLUT_ELAPSED_TIME)/ 1000
            print 'Start the Game!'
            #print startTime
            canPlay = True      

#-------------------------------------------------tools----------------------       
def drawTextBitmap(string, x, y): #for writing text to display
    glRasterPos2f(x, y)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def text3d(string, x, y, z):
    glRasterPos3f(x,y,z)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def dist(pt1, pt2):
    a = pt1[0]
    b = pt1[1]
    x = pt2[0]
    y = pt2[1]
    return math.sqrt((a-x)**2 + (b-y)**2)

def noReshape(newX, newY): #used to ensure program works correctly when resized
    global windowSizeWidth, windowSizeHeight, windowSizeRatio
    #windowSizeRatio = windowSizeWidth/windowSizeHeight
    glutReshapeWindow(windowSizeWidth,windowSizeHeight)
    
    setView()
    glViewport(0, 0, windowSizeWidth, windowSizeHeight)

#--------------------------------------------making game more complex--------
def addCone(x,z):
    allcones.append(cone.cone(x,z))
    obstacleCoord.append((x,z))
    
def addStar(x,z):
    allstars.append(star.star(x,z))
    rewardCoord.append((x,z))

def collisionCheck():
    global overReason, score, usedDiamond, countTime, StarScore, acceleratingRibbonList, jeepSpeed
    for obstacle in obstacleCoord:
        if dist((jeepObj.posX, jeepObj.posZ), obstacle) <= ckSense:
            print 'game over!'
            overReason = "You hit an obstacle!"
            glutIdleFunc(None)
            gameOver()
    if (jeepObj.posX >= land or jeepObj.posX <= -land):
        overReason = "You ran off the road!"
        glutIdleFunc(None)
        gameOver()
    for reward in rewardCoord:
        if dist((jeepObj.posX, jeepObj.posZ), reward) <= ckSense:
            print "Star bonus!"
            #StarScore+=1
            allstars.pop(rewardCoord.index(reward))
            rewardCoord.remove(reward)
            #countTime -= 10
    #if (dist((jeepObj.posX, jeepObj.posZ), (diamondObj.posX, diamondObj.posZ)) <= ckSense and usedDiamond ==False):
    #    print "Diamond bonus!"
    #    countTime /= 2
    #    usedDiamond = True
    if (jeepObj.posZ >= land*gameEnlarge):
        glutIdleFunc(None)
        gameSuccess()
        
    for item in acceleratingRibbonList:
        if (jeepObj.posZ > item[1][2] and jeepObj.posZ < item[0][2]) and (jeepObj.posX < item[0][0] and jeepObj.posX > item[2][0]):
            print 'Speed Up!'
            jeepObj.posZ = jeepObj.posZ + (jeepSpeed * 10)
            #acceleratingRibbonList.remove(item)
            
def mainMenuList(value):
    if value == 1:
        sys.exit()
            
def viewPointMenuList(value):
    global topView, behindView
    
    if value == 1:
        topView = True
        behindView = False
        cameraView = False
    if value == 2:
        topView = False
        behindView = True
        cameraView = False
    if value == 3:
        cameraView = True
        topView = False
        behindView = False
    
    setObjView()
    return 0
    
def lightingMenuList(value):
    global drawSun
    if value == 1:
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        drawSun=False
    if value == 2:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        drawSun=False
    if value == 3:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHT2)
        drawSun=True
    if value == 4:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        drawSun=True

             
    setObjView()
    return 0
    
def lightingColorMenuList(value):   
    if value == 1:
        diffuseLight = [ 0.0, 0.0, 1.0, 1.0 ]
        specularLight = [ 1.0, 1.0, 1.0, 1.0 ]
        ambientLight = [ 0.0, 0.0, 0.2, 1.0 ]
    if value == 2:
        diffuseLight = [0.8, 0.8, 0.8, 1.0]      
        specularLight = [0.3, 0.8, 0.6, 1.0]
        ambientLight = [0.2, 0.2, 0.2, 1.0]
    if value == 3:
        diffuseLight = [0.34615, 0.3143, 0.0903, 1.0]      
        specularLight = [0.797357, 0.723991, 0.208006, 1.0]
        ambientLight = [0.24725, 0.2245, 0.0645, 1.0]    


    glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLight)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,diffuseLight)
    glLightfv(GL_LIGHT0,GL_SPECULAR,specularLight)
    glLightfv(GL_LIGHT1,GL_AMBIENT,ambientLight)
    glLightfv(GL_LIGHT1,GL_DIFFUSE,diffuseLight)
    glLightfv(GL_LIGHT1,GL_SPECULAR,specularLight)
    glLightfv(GL_LIGHT2,GL_AMBIENT,ambientLight)
    glLightfv(GL_LIGHT2,GL_DIFFUSE,diffuseLight)
    glLightfv(GL_LIGHT2,GL_SPECULAR,specularLight)
           
    setObjView()
    return 0
        
def createMenu():
    viewPointMenu = glutCreateMenu(viewPointMenuList)
    glutAddMenuEntry("Top View", 1)
    glutAddMenuEntry("Behind View", 2)
    glutAddMenuEntry("Camera View", 3)
    
    lightingMenu = glutCreateMenu(lightingMenuList)
    glutAddMenuEntry("Lighting Off", 1)
    glutAddMenuEntry("Spotlight", 2)
    glutAddMenuEntry("Directional Light", 3)
    glutAddMenuEntry("Point Light", 4)
    
    lightingColorMenu = glutCreateMenu(lightingColorMenuList)
    glutAddMenuEntry("Blue Color", 1)
    glutAddMenuEntry("White Color", 2)
    glutAddMenuEntry("Yellor Color", 3)
    
    mainMune = glutCreateMenu(mainMenuList)
    glutAddSubMenu("View Point Setting", viewPointMenu)
    glutAddSubMenu("Lighting Setting", lightingMenu)
    glutAddSubMenu("Material Color", lightingColorMenu)
    glutAddMenuEntry("Exit",1)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def gameConfig():
    global fullScreen, windowSizeWidth, windowSizeHeight, playerName

    GameSetting.run_setting()
    fullScreen ,windowSizeWidth, windowSizeHeight, playerName = GameSetting.get_setting_info()
    print("Changed screen size to: " + str(windowSizeWidth) + " x " + str(windowSizeHeight))
    print("Changed player name to: " + str(playerName))
    GameSetting.close_setting_window()
    glutInitWindowSize(windowSizeWidth, windowSizeHeight)
    #glutInitWindowPosition(0, 0)
    glutInitWindowPosition((glutGet(GLUT_SCREEN_WIDTH) - windowSizeWidth)/2, (glutGet(GLUT_SCREEN_HEIGHT) - windowSizeHeight)/2)
    mainWin = glutCreateWindow('CS4182')
    if (fullScreen):
        glutFullScreen()

#----------------------------------multiplayer dev (using tracker)-----------
def recordGame():
    global playerName, StarScore, finalScore

    table = []
    header=['Ranking', 'Player Name', 'Date Time', 'Star Gain', 'Time Needed']
    #playerName = 'player 000'

    with open('../gameRecord/ranking.csv', 'r+t') as csvfile:
        obj = csv.reader(csvfile)

        for row in obj:
            if row != header:
                row[0] = row[1]
                row[1] = row[2]
                row[2] = int(row[3])
                row[3] = int(row[4])
                table.append(row)

    os.remove('../gameRecord/ranking.csv')

    with open('../gameRecord/ranking.csv', 'w') as csvfile:   
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        currentRecord = []
        currentRecord.append(playerName)
        currentRecord.append(st)
        StarScore = starAmount - len(allstars)
        currentRecord.append(StarScore)
        currentRecord.append(finalScore)
        #print(currentRecord)
        table.append(currentRecord)

        #print(table)
        #print(len(table))
        if len(table) > 1:
            table.sort(key = lambda x: (x[2],-x[3]), reverse = True)
        
        table = table[:10]

        spamwriter.writerow(header)

        rankNum = 1
        for row in table:
            temp = row[:4]
            row[0] = rankNum
            row[1:5] = temp
            print(row)
            spamwriter.writerow(row)
            rankNum +=1

    
#-------------------------------------developing additional windows/options----
def gameOver():
    global finalScore
    print "Game completed!"
    finalScore = score-6
    recordGame() #add to excel
    #RankingTable.getTable()
    glutHideWindow()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(200,200)
    glutInitWindowPosition(600,100)
    overWin = glutCreateWindow("Game Over!")
    glutDisplayFunc(overScreen)
    glutMainLoop()
    #RankingTable.showTable()
    
def gameSuccess():
    global finalScore
    print "Game success!"
    finalScore = score-6
    recordGame() #add to excel
    glutHideWindow()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(200,200)
    glutInitWindowPosition(600,100)
    overWin = glutCreateWindow("Complete!")
    glutDisplayFunc(winScreen)
    glutMainLoop()

def winScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0,1.0,0.0)
    drawTextBitmap("Completed Trial!" , -0.6, 0.85)
    glColor3f(0.0,1.0,0.0)
    drawTextBitmap("Your score is: ", -1.0, 0.0)
    glColor3f(1.0,1.0,1.0)
    drawTextBitmap(str(finalScore), -1.0, -0.15)
    glutSwapBuffers()
    displayRanking()


def overScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0,0.0,1.0)
    drawTextBitmap("Incomplete Trial" , -0.6, 0.85)
    glColor3f(0.0,1.0,0.0)
    drawTextBitmap("Because you..." , -1.0, 0.5)
    glColor3f(1.0,1.0,1.0)
    drawTextBitmap(overReason, -1.0, 0.35)
    glColor3f(0.0,1.0,0.0)
    drawTextBitmap("Your score stopped at: ", -1.0, 0.0)
    glColor3f(1.0,1.0,1.0)
    drawTextBitmap(str(finalScore), -1.0, -0.15)
    glutSwapBuffers()
    displayRanking()

def showHelp():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0,0.0,0.0)
    drawTextBitmap("Help Guide" , -0.2, 0.85)
    glColor3f(0.0,0.0,1.0)
    drawTextBitmap("describe your control strategy." , -1.0, 0.7)
    glutSwapBuffers()
    
def displayRanking():
    RankingTable.getTable()
    #RankingTable.showTable()

#----------------------------------------------texture development-----------
def loadTexture(imageName):
    texturedImage = Image.open(imageName)
    try:
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw","RGBX",0,-1)#tostring("raw", "RGBX", 0, -1)
    except Exception:
        print "Error:"
        print "Switching to RGBA mode."
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw","RGB",0,-1)#tostring("raw", "RGBA", 0, -1)

    tempID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tempID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, imgX, imgY, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    return tempID

def loadSceneTextures():
    global roadTextureID, acceleratingRibbonID
    roadTextureID = loadTexture("../img/road2.png")
    acceleratingRibbonID = loadTexture("../img/road.png")
    
#-----------------------------------------------lighting work--------------
def initializeLight():
    #glEnable(GL_LIGHTING)                              
    glEnable(GL_DEPTH_TEST)              
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glDepthFunc(GL_LEQUAL)
    glClearColor(0, 0, 0, 0)

#~~~~~~~~~~~~~~~~~~~~~~~~~the finale!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    print "Start"
    glutInit()

    global prevTime, mainWin, windowSizeWidth, windowSizeHeight, fullScreen
    
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

    # things to do
    # change the window resolution in the game and player Name
    gameConfig()

    glutDisplayFunc(display)
    glutIdleFunc(idle)#wheel turn

    setView()
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)   

    glutMouseFunc(mouseHandle)
    glutMotionFunc(motionHandle)
    glutMouseWheelFunc(mouseScroll)
    glutSpecialFunc(specialKeys)
    glutKeyboardFunc(myKeyboard)
    glutReshapeFunc(noReshape)

    # things to do
    # add a menu
    createMenu()

    loadSceneTextures()
    jeep1Obj.makeDisplayLists()
    jeep2Obj.makeDisplayLists()
    jeep3Obj.makeDisplayLists()
    #personObj.makeDisplayLists()

    # things to do
    # add a automatic object
    for i in range(coneAmount):#create cones randomly for obstacles, making sure to give a little lag time in beginning by adding 10.0 buffer
        addCone(random.randint(-land+10, land-10), random.randint(15.0, land*gameEnlarge))

    # things to do
    # add stars
    i = 0
    while i < starAmount:
        x = random.randint(-land+10, land-10)
        z = random.randint(15.0, land*gameEnlarge)
        check = True
        for obstacle in obstacleCoord:
            if dist((x, z), obstacle) <= ckSense:
                check = False
        if check:        
            addStar(x, z)
            i= i + 1

    for cone in allcones:
        cone.makeDisplayLists()

    for star in allstars:
        star.makeDisplayLists()
   
    # diamondObj.makeDisplayLists()
    
    staticObjects()
    if (applyLighting == True):
        initializeLight()
    glutMainLoop()



    
main()

