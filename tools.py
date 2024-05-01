class ToolSettings:
    def __init__(self):
        self._tool = "pen"
        self._color = "#000"

        self._pen_size = 2
        self._figure_size = 2
        self._eraser_size = 10

    @property
    def tool(self):
        return self._tool
    @tool.setter
    def tool(self, value):
        self._tool = value

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value

    @property
    def pen_size(self):
        return self._pen_size
    @pen_size.setter
    def pen_size(self, value):
        self._pen_size = value

    @property
    def pen_size(self):
        return self._pen_size
    @pen_size.setter
    def pen_size(self, value):
        self._pen_size = value

    @property
    def figure_size(self):
        return self._figure_size
    @figure_size.setter
    def figure_size(self, value):
        self._figure_size = value

    @property
    def eraser_size(self):
        return self._eraser_size
    @eraser_size.setter
    def eraser_size(self, value):
        self._eraser_size = value