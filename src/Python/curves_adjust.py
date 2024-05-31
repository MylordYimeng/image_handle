import sys, os
os.chdir(os.path.dirname(__file__))
sys.path.append('../../include')
import curves as curves # type: ignore
import numpy as np

class Curves:
    def __init__(self, mainwindow, src, small_src, label1, label2, label3, label4):
        self.C = curves.Curves()
        self.src = src
        self.small_src = small_src
        self.curves_mat = np.ones((256, 256, 3), dtype=np.uint8)
        self.label1 = label1 # label1 is the label for curves
        self.label2 = label2 # label2 is the label for the image
        self.label3 = label3 # label3 is the label for the histogram
        self.label4 = label4 # label4 is the label for preview
        self.mainwindow = mainwindow
        
    def update(self, is_prev=True, wanna_return = False):
        chan = self.mainwindow.ui.cbox_curv_channel.currentText()
        self.chan_cho(chan)
        self.C.draw(self.curves_mat)
        self.mainwindow.display_image(self.label1, self.curves_mat)  # 通用
        if is_prev:
            #self.small_src = self.mainwindow.small_img
            temp_img = self.C.adjust(self.small_src)  # 区别之处
            self.mainwindow.display_single_channel(temp_img)
        else:
            temp_img = self.C.adjust(self.src)
            self.mainwindow.display_image(self.label2, temp_img)

        self.mainwindow.display_image(self.label3, self.mainwindow.funcs.display_histogram(self.label3, chan, temp_img))
        P = self.get_points()
        print(P)
        if wanna_return:
            return temp_img
    def chan_cho(self, s):
        if s == "R":
            self.C.channel_chose(1)
        elif s == "G":
            self.C.channel_chose(2)
        elif s == "B":
            self.C.channel_chose(3)
        else:
            self.C.channel_chose(4)
        
    def get_points(self):
        return self.C.get_points()
    def set_points(self, pointsRGB = [(0, 0), (255, 255)], pointsR = [(0, 0), (255, 255)], pointsG = [(0, 0), (255, 255)], pointsB = [(0, 0), (255, 255)]):
        self.C.set_points(pointsRGB, pointsR, pointsG, pointsB)
        self.update()
    def callbackMouseEvent(self, mouseEvent, pos):
        if self.mainwindow.ui.cbox_function.currentText() == "调整曲线":
            if mouseEvent == "press":
                self.C.mouseDown(pos[0], pos[1])
            elif mouseEvent == "move":
                self.C.mouseMove(pos[0], pos[1])
            elif mouseEvent == "up":
                self.C.mouseUp(pos[0], pos[1])
            self.update()


    
        