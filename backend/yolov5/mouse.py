class Mouse:
    def __init__(self):
        self.center = (0, 0)
        self.left_front = (0,0,0,0)
        self.left_front_size = 0
        self.right_front = (0,0,0,0)
        self.right_front_size = 0
        self.left_hind = (0,0,0,0)
        self.left_hind_size = 0
        self.right_hind = (0,0,0,0)
        self.right_hind_size = 0
        self.left_front_up = True
        self.right_front_up = True
        self.left_hind_up = True
        self.right_hind_up = True

        # self.left_front_up_time = 0 
        # self.right_front_up_time = 0 
        # self.left_hind_up_time = 0 
        # self.right_hind_up_time = 0 

        # self.left_front_down_time = 0 
        # self.right_front_down_time = 0 
        # self.left_hind_down_time = 0 
        # self.right_hind_down_time = 0 


        self.direction = -1
        self.velocity = 0
        self.pos = [0,0,0,0]