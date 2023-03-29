from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time
import ImportObject


class star:
    obj = 0
    displayList = 0
    
    posX = 0.0
    posY = 1.75
    posZ = 0.0

    sizeX = 2
    sizeY = 2
    sizeZ = 2

    rotation = 0.0
    
    def __init__(self, x, z):
        self.obj = ImportObject.ImportedObject("../objects/star")
        self.posX = x
        self.posZ = z
        
    def makeDisplayLists(self):
        self.obj.loadOBJ()

        self.displayList = glGenLists(1)
        glNewList(self.displayList, GL_COMPILE)
        self.obj.drawObject()
        glEndList()
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.posX,self.posY,self.posZ)
        #glRotatef(self.rotation,0.0,1.0,0.0)
        glScalef(self.sizeX,self.sizeY,self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()

            
        
