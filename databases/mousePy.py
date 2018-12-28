import time
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseUp
from Quartz.CoreGraphics import kCGMouseButtonRight
from Quartz.CoreGraphics import kCGHIDEventTap
def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)
def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);
def mouseclick(posx,posy,down=kCGEventLeftMouseDown,up=kCGEventLeftMouseUp):
        #mouseEvent(kCGEventMouseMoved, posx,posy); #uncomment this line if you want to force the mouse to MOVE to the click location first (i found it was not necesary).
        mouseEvent(down, posx,posy);
        mouseEvent(up, posx,posy);
        #time.sleep(.1)        
        #mouseEvent(kCGEventLeftMouseDown, posx+10,posy+20);
        #mouseEvent(kCGEventLeftMouseUp, posx+10,posy+20);
def rightclick(posx,posy):
        mouseclick(posx,posy,kCGEventRightMouseDown,kCGEventRightMouseUp)
def leftclick(posx,posy):
        mouseclick(posx,posy)

'''time.sleep(delay);
mouseclick(xclick, yclick);
print("done.")'''