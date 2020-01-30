import sys
import pygame
import random
import numpy
import time
import matplotlib
import matplotlib.pyplot as pyplot

game_name = "Simulation of Virus"

# refresh speed
FPS = 2



class People(object):
    def __init__(self):
            # status
        self.DEAD = 99
        self.NORMAL = 0
        self.IMMNUITY = 2
        self.SICK = 4
        self.INFECTED = 3
        self.RECOVERED = 1

        
        self.status = self.NORMAL
        self.transmission = 200 #probability self condition
        self.recover = 2 # self healing
        self.incubation = random.randint(7,14) # incubation period
        self.deadrate = 2

    def setPosition(self,x,y):
        self.x = x
        self.y = y

    def getStatus(self):
        return [self.status,self.transmission,self.recover,self.incubation]

    def setStatus(self,status_list):
        self.status = status_list[0]
        self.transmission = status_list[1]
        self.recover = status_list[2]
        self.incubation = status_list[3]

    def updateStatus(self,neighbor_status_list):
        up_neighbor = neighbor_status_list[0]
        down_neighbor = neighbor_status_list[1]
        left_neighbor = neighbor_status_list[2]
        right_neighbor = neighbor_status_list[3]
        if self.status == self.DEAD:
           pass
        if self.status == self.RECOVERED:
            pass
        '''
            for h in neighbor_status_list:
                if (h == self.INFECTED or h == self.SICK) and random.randint(0,1000) <= self.transmission:
                    self.status = self.INFECTED
                    self.recover = 2
                    self.incubation = random.randint(7,14)
        '''  
        if self.status == self.NORMAL:
            for h in neighbor_status_list:
                if (h == self.INFECTED or h == self.SICK) and random.randint(0,1000) <= self.transmission:
                    self.status = self.INFECTED
                    self.recover = 2
                    self.incubation = random.randint(7,14)
                    
        if self.status == self.IMMNUITY:
            pass
        '''
            for h in neighbor_status_list:
                if (h == self.INFECTED or h == self.SICK) and random.randint(0,1000) <= self.transmission:
                    self.status = self.INFECTED
                    self.recover = 1
                    self.incubation = random.randint(7,14)
        '''
            
        
        if self.status == self.SICK:
            if random.randint(0,1000) <= self.recover:
                self.status = self.RECOVERED#or IMMNUITY
                self.recover = 0
                self.incubation = 0
            if random.randint(0,1000) <= self.deadrate:
                self.status = self.DEAD
            
        
        if self.status == self.INFECTED:
            if random.randint(0,1000) <= self.recover:
                self.status = self.RECOVERED#or IMMNUITY  or normal
                self.recover = 0
                self.incubation = 0
            if self.incubation == 0:
                self.status = self.SICK

            self.incubation -= 1
            
            
                
            


class World(object):
    
    def __init__(self):
        # size of window
        self.window_width = 800
        self.window_height = 600
        self.cell_size = 5
        if self.window_width % self.cell_size != 0 or self.window_width % self.cell_size != 0:
            print("window width and height should be the multiple of cell size!!")
            sys.exit()
        self.x_count = int(self.window_width / self.cell_size)
        self.y_count = int(self.window_height / self.cell_size)

        #color
        self.BLACK = (41,36,33) # dead
        self.WHITE = (255,255,255) # normal 
        self.GRAY = (128,138,135) # immunity
        self.RED = (227,23,13) # sick
        self.YELLOW = (255,227,132) # infected
        self.GREEN = (64,224,208) # recovered

       
        # init
        pygame.init()
        self.human0 = People()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([self.window_width,self.window_height])
        self.screen.fill(self.WHITE)
        self.world_map = [[]]
        self.drawWorld()
        # start infect
        self.createMotherHost()
        self.paintWorld()
        self.startWorld()

    def drawBoundary(self):
        for x in range(0,self.window_width,self.cell_size):
            pygame.draw.line(self.screen,self.GRAY,(x,0),(x,self.window_height))
        for y in range(0,self.window_height,self.cell_size):
            pygame.draw.line(self.screen,self.GRAY,(0,y),(self.window_width,y))
        pygame.display.update()

    def drawWorld(self):
        self.drawBoundary()
	
        world_map = []

        for x in range(self.x_count):#?
            row = []
            for y in range(self.y_count):
                human = People()
                human.setPosition(x,y)
                row.append(human)
            world_map.append(row)
        self.world_map = world_map


    def createMotherHost(self):
        x = random.randint(0,self.x_count-1)
        y = random.randint(0,self.y_count-1)
        self.world_map[x][y].status = self.human0.INFECTED
        print("virus appear")
        
    def startWorld(self):
        step = 0
        while True:
            #self.drawUpdateWorld()
            #self.updateWorld()
            self.updateCell()
            self.paintWorld()
            self.drawBoundary()
            pygame.display.update()
            self.clock.tick(FPS)
            step += 1
            print(step)
            
    def updateCell(self):
        for x in range(self.x_count):
            for y in range(self.y_count):
                neighbor_status_list = []
                try:#up
                    neighbor_status_list.append(self.world_map[x][y-1].status)
                except:
                    neighbor_status_list.append(None)
                try:#down
                    neighbor_status_list.append(self.world_map[x][y+1].status)
                except:
                    neighbor_status_list.append(None)
                try:#left
                    neighbor_status_list.append(self.world_map[x-1][y].status)
                except:
                    neighbor_status_list.append(None)
                try:#right
                    neighbor_status_list.append(self.world_map[x+1][y].status)
                except:
                    neighbor_status_list.append(None)
                    
                try:#up left
                    neighbor_status_list.append(self.world_map[x-1][y-1].status)
                except:
                    neighbor_status_list.append(None)
                try:#down left
                    neighbor_status_list.append(self.world_map[x-1][y+1].status)
                except:
                    neighbor_status_list.append(None)
                try:#up right
                    neighbor_status_list.append(self.world_map[x+1][y-1].status)
                except:
                    neighbor_status_list.append(None)
                try:#down right
                    neighbor_status_list.append(self.world_map[x+1][y+1].status)
                except:
                    neighbor_status_list.append(None)

                self.world_map[x][y].updateStatus(neighbor_status_list)
        
    def paintWorld(self):
        for x in range(self.x_count):
            for y in range(self.y_count):
                cellx = x*self.cell_size
                celly = y*self.cell_size
                if self.world_map[x][y].status == self.human0.DEAD:
                    pygame.draw.rect(self.screen,self.BLACK,(cellx,celly,self.cell_size,self.cell_size))
                if self.world_map[x][y].status == self.human0.NORMAL:
                    pygame.draw.rect(self.screen,self.WHITE,(cellx,celly,self.cell_size,self.cell_size))
                if self.world_map[x][y].status == self.human0.IMMNUITY:
                    pygame.draw.rect(self.screen,self.GRAY,(cellx,celly,self.cell_size,self.cell_size))
                if self.world_map[x][y].status == self.human0.SICK:
                    pygame.draw.rect(self.screen,self.RED,(cellx,celly,self.cell_size,self.cell_size))
                if self.world_map[x][y].status == self.human0.INFECTED:
                    pygame.draw.rect(self.screen,self.YELLOW,(cellx,celly,self.cell_size,self.cell_size))
                if self.world_map[x][y].status == self.human0.RECOVERED:
                    pygame.draw.rect(self.screen,self.GREEN,(cellx,celly,self.cell_size,self.cell_size))
        return None

if __name__=='__main__':

    world = World() 
