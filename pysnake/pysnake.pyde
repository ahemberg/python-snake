
import random
import copy
import time

class SnakeSegment:
    def __init__(self, x, y, s):
        self.xpos = x
        self.ypos = y
        self.s = s
    
    def set_pos(self, xy):
        self.xpos = xy[0]
        self.ypos = xy[1]
        
    def get_pos(self):
        return [self.xpos, self.ypos]
        
    def show(self):
        stroke(255,0,0)
        fill(220,50,0)
        rect(self.xpos, self.ypos, self.s, self.s)

class Food:
    def __init__(self,s):
        x = random.randint(0,width)    
        y = random.randint(0,height)
        self.xpos = x - (x % s)     
        self.ypos = y - (y % s)
        self.s = s
        self.age = 0.0
                
        valselector = random.randint(0,70)
        
        if valselector <= 40:
            self.value = 1
            self.col = [0, 255, 0]
            self.ttl = float(random.randint(100,400))  # Time To Live in frames
        elif 40 < valselector <= 60:
            self.value = 4
            self.col = [0, 0, 255]
            self.ttl = float(random.randint(50,200))  # Time To Live in frames
        else:
            self.value = 10
            self.col = [255, 0, 0]
            self.ttl = float(random.randint(10,100))  # Time To Live in frames

    def show(self):
        stroke(0,0,255)
        fill(self.col[0], self.col[1], self.col[2])        
        rect(self.xpos, self.ypos, self.s, self.s)
        self.age +=1
        
        #Fade food color according to age:
        old = self.col[self.col.index(max(self.col))]
        self.col[self.col.index(max(self.col))] = (1 - self.age/self.ttl)*255 
        
        
    def get_pos(self):
        return [self.xpos, self.ypos]


    
snake = []
food = []
score = 0
grow = False
crash = False
sx = 800
block_size = sx/20 
for i in range(0,50,10):
    snake.insert(0,SnakeSegment(i,0,block_size))
velocity = [block_size,0]

def setup():
    frameRate(10)
    size(sx,sx)
    background(0)
    
       
def draw():
    clear()
    global grow, score, crash, snake, food, block_size
    
    text('Score '+str(score), sx-len('Score '+str(score)*100), 10)
    
    # Add food if needed
    if len(food) <= 2:
        food.append(Food(block_size))
    
    # Draw Food and remove food if its age exceeds ttl.
    for i, goodie in enumerate(food):
        if goodie.age >= goodie.ttl:
            food.pop(i)
        else:
            goodie.show()
        
    # Draw the Python
    for segment in snake:
        segment.show()
    
    #Move and grow Snake    
    if grow:
        endsegment = copy.deepcopy(snake[-1])
    
    i = len(snake)
    for segment in reversed(snake[1::]):        
        segment.set_pos(snake[i-2].get_pos())
        i -= 1
        
    if grow:
        snake.append(endsegment)
        grow = False
    
    snake[0].set_pos([(snake[0].xpos + velocity[0]), snake[0].ypos + velocity[1]])    
    

    if snake[0].xpos >= width:
        snake[0].xpos = 0
    if snake[0].xpos < 0:
        snake[0].xpos = width-block_size
        
    if snake[0].ypos >= height:
        snake[0].ypos = 0
    if snake[0].ypos < 0:
        snake[0].ypos = height-block_size
        
    #Check if the snake crashed into itself
    headpos = snake[0].get_pos()
    
    for segment in snake[1::]:
        if segment.get_pos() == headpos:
            crash = True
    
    if crash:
        text('GAME OVER! Press R to restart!', width/2-120, height/2)       
        noLoop()
        
        
    #Check if eaten    
    for i, goodie in enumerate(food):
        if headpos == goodie.get_pos():
            score += goodie.value
            food.pop(i)
            grow = True
            break 
                     
def reset_game():
    """
    Resets game variables
    """
    global snake, food, score, grow, crash, sx, block_size, velocity
    
    snake = []
    food = []
    score = 0
    grow = False
    crash = False
    block_size = sx/20 
    for i in range(0,50,10):
        snake.insert(0,SnakeSegment(i,0,block_size))
    velocity = [block_size,0]
    
    loop()
               
def keyPressed():
    """
    Handles movements of the snake. If the game is over it resets all variables and restarts
    """
    global velocity, food, block_size
    
    if key == 'r':
        reset_game()       
    if key == 'f':
        # Undocumented feature: Spawn more food
        food.append(Food(block_size))
        
    if keyCode == UP and velocity[1] == 0:
        velocity[1] = -block_size
        velocity[0] = 0
    if keyCode == DOWN and velocity[1] == 0:
        velocity[1] = block_size
        velocity[0] = 0
    if keyCode == LEFT and velocity[0] == 0:
        velocity[1] = 0
        velocity[0] = -block_size
    if keyCode == RIGHT and velocity[0] == 0:
        velocity[1] = 0
        velocity[0] = block_size