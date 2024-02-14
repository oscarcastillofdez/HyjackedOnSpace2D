class Global_Vars():
    def __init__(self) -> None:
        self.INERTIA = 20
        self.MAX_VELOCITY = 500
        self.GRAVITY = 1
        self.MIN_JUMP_HEIGHT = 20
        self.MAX_JUMP_HEIGHT = 30
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGTH = 720
        self.TILE_SIZE = 45
        self.GAME_OVER = False
        self.world_data = [[0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                          [1,1,1,1,1,1,1,1,1],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                          [0,0,0,0,0,0,0,0,0,0,0,2,0,0,2],
                          [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1]]
        self.CAMERA_OFFSET_X = 0