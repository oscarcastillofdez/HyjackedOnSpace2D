class pState(object):
    def __init__(self):
        self.animation = None
        self.next_state = None
        self.done =  False
        self.sprite_index = 0
        self.persist = {}
    
    def startup(self, persistent):
        self.persist = persistent

    def get_initial(self):
        return self.animation[0]
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        return self.animation[self.sprite_index]

    def update(self, dt):
        pass