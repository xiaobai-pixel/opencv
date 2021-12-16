import numpy as np
import cv2

from pip._vendor.certifi.__main__ import  args

class Sketcher:
    def __init__(self,windowname,dests,colors_func):
        self.prevpt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname,self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname,self.dests[0])
        cv2.imshow(self.windowname+":mask", self.dests[1])

    #使用鼠标把掩膜画出来也就是第二幅图的白色线条
    def on_mouse(self,event,x,y,flags,param):
        pt = (x,y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prevpt = pt
        elif event == cv2.EVENT_RBUTTONUP:
            self.prevpt = None

        if self.prevpt and flags & cv2.EVENT_FLAG_LBUTTON:#左键拖曳
            for dst,color in zip(self.dests,self.colors_func()):
                cv2.line(dst,self.prevpt,pt,color,5)

            self.dirty =True
            self.prevpt = pt
            self.show()


def main():
    img = cv2.imread("Lincoln.jpg",cv2.IMREAD_COLOR)

    img_mask = img.copy()
    inpaintMask = np.zeros(img.shape[:2],np.uint8)

    sketch = Sketcher("img",[img_mask,inpaintMask],lambda :((255,255,255),255))

    while True:
        ch = cv2.waitKey()
        if ch == 27:
            break
        if ch == ord("t"):
            res = cv2.inpaint(src=img_mask,inpaintMask=inpaintMask,inpaintRadius=3,flags=cv2.INPAINT_TELEA)
            cv2.imshow("Inpaint output using FMM",res)


        if ch == ord("n"):
            res = cv2.inpaint(src=img_mask,inpaintMask=inpaintMask,inpaintRadius=3,flags=cv2.INPAINT_NS)
            cv2.imshow("Inpaint output using Technique",res)

        if ch == ord("r"):
            img_mask[:] = img
            inpaintMask = 0
            sketch.show()

    print("completed")

if __name__ == "__main__":
    main()