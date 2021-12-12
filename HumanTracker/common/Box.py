class Box:
    start_x = None
    start_y = None
    end_x = None
    end_y = None
    width = None
    height = None
    
    def __init__(self, start_x, start_y, end_x, end_y) -> None:
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.width = end_x - start_x
        self.height = end_y - start_y
    
    def __init__(self, frame, f, padding) -> None:
        self.start_x = max(0, f[0]-padding)
        self.start_y = max(0, f[1]-padding)
        self.end_x = min(frame.shape[1]-1, f[2]+padding)
        self.end_y = min(frame.shape[0]-1, f[3]+padding)
        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y
    
    def __init__(self, image, bBox) -> None:
        image_height, image_width, _ = image.shape
        self.start_x = int(bBox.xmin * image_width)
        self.start_y = int(bBox.ymin * image_height)
        self.end_x = self.start_x + int(bBox.width * image_width)
        self.end_y = self.start_y + int(bBox.height * image_height)
        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y
        pass

    def add_offset(self, x, y):
        self.start_x += x
        self.start_y += y
        self.end_x += x
        self.end_y += y

    @property
    def start(self):
        return (self.start_x, self.start_y)

    @property
    def end(self):
        return (self.end_x, self.end_y)

    @property
    def area(self):
        return self.width * self.height
    
    @property
    def center(self):
        return ((self.start_x + self.end_x) // 2, (self.start_y + self.end_y) // 2)