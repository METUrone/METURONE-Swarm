import datetime
import math

M_PI = math.pi
def FloorAngle(angle):

    angle = angle*180/M_PI;
    after_point = angle - (int(angle));
    remainder = (int(angle))%360;
    
    return (remainder+after_point)*M_PI/180;

def FloorAngle2(angle):
    while angle > 360:
        angle-=360
    return angle

if __name__ == "__main__":
    x = datetime.datetime.now()
    for i in range(1000):
        z = FloorAngle2(540)
    print(datetime.datetime.now()-x)
    