from direct.gui.DirectGui import DirectFrame, DirectButton


class Menu:
    def __init__(self, base):
        self.base = base

        self.ui = DirectFrame(
            frameColor=(0, 0, 0, 0),
            frameSize=(0, 0, 0, 0),
            pos=(-1.05, 0, 0.9)
        )