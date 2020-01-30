import math 

tan22_5 = math.tan(math.pi/4)
tan67_5 = math.tan(3*math.pi/4)

def decision(position,room):

    nearestExit = getNearestExit(position,room)
    y_distant = y_nearestExit - y_position
    x_distant = x_nearestExit - x_position
    y_absDistant = abs(y_distant)
    x_absDistant = abs(x_distant)
    tanPosition2Exit = (y_absDistant/x_absDistant)
    xORy = 0 # 0 --> x 1 --> y 2 --> xy
    if tanPosition2Exit <= tan22_5:
        xORy = 0
    if tanPosition2Exit >= tan67_5:
        xORy = 1
    else:
        xORy = 2

    if xORy = 0:
        if x_distant <= 0:
            direction.x = position.x - 1
        else:
            direction.x = position.x + 1
    elif xORy = 1 :
        if y_distant <= 0:
            direction.y = position.y - 1
        else:
            direction.y = position.y + 1
    else:
        if x_distant <= 0:
            direction.x = position.x - 1
        else:
            direction.x = position.x + 1
            
        if y_distant <= 0:
            direction.y = position.y - 1
        else:
            direction.y = position.y + 1
    return direction

class room:
    def __init__(length,wideth,numofpeople):
        self.numofpeople = numofpeople
        createNewRoom(length,wideth)

    def createNewRoom(length,wideth):
        
