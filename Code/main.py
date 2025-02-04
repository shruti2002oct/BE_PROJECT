import pygame
import sys
import random
import cv2
import numpy as np
from FindBalloon import *
from detectHit import *
from calbi import *
import calbi
# Initialize Pygame
pygame.init()

# # Constants for the screen width and height
SCREEN_WIDTH = 1540
SCREEN_HEIGHT = 820

# Colors
WHITE = (255, 255, 255)
# Use 0 for the default camera (usually webcam)
points = pickle.load(open('calibration.pkl','rb'))

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Moving Balloon")

# Load the balloon image
balloon_img = pygame.image.load("photos/b4.png")  # Replace "balloon.png" with your image file spath
balloon_img = pygame.transform.scale(balloon_img, (350, 400)) # change size of balloon
# Initial position of the balloons
balloon_x = SCREEN_WIDTH // 2 - balloon_img.get_width() // 2
balloon_y = SCREEN_HEIGHT + balloon_img.get_height()

pop_img = pygame.image.load("photos/pop.png")  # Replace "balloon.png" with your image file path
pop_img = pygame.transform.scale(pop_img, (250, 300))
# Initial position of the balloon



# Movement speed of the balloon
balloon_speed = 5


total_seconds = 30 # Total countdown time in seconds
clock = pygame.time.Clock()
countdown_timer = total_seconds * 60

hit_score = 0



class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 160
        self.height = 80

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 35)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
    
    def getText(self):
        return self.text

btns = [Button("Play",  (screen.get_width() // 2) - 80 , 300, (0,0,0)), Button("Calibrate", (screen.get_width() // 2) - 80, 420, (255,0,0)), Button("Quit", (screen.get_width() // 2) - 80, 540, (0,255,0))]

def pop_balloon():
    global hit_score
    screen.fill(WHITE)
    hit_score=hit_score + 1
    screen.blit(pop_img, (balloon_x, balloon_y))
    pygame.display.flip()
    pygame.time.delay(300)
    
def resetBallon():
    global balloon_x,balloon_y
    balloon_x = random.randint(0, SCREEN_WIDTH*0.8)
    balloon_y = SCREEN_HEIGHT  

def render_text(text, font_size, color):
    font = pygame.font.Font(None, font_size)  # You can specify a font file path instead of None
    text_surface = font.render(text, True, color)
    return text_surface

def calirateWindow():
    global points
    calbi.main()
    points = pickle.load(open('calibration.pkl','rb'))

    

def mainWindow():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(6,720)
    global countdown_timer,balloon_speed,balloon_img,hit_score,balloon_x,balloon_y
    clock = pygame.time.Clock()
    running = True
    while running:
        if not cap.isOpened():
            print("Error: Could not open camera.")
            running = False
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if countdown_timer > 0:
            countdown_timer -= 1
        elif countdown_timer == 0:
            running = False
            
        ret, frame = cap.read()

        if not ret:
                print("Error: Failed to capture frame.")
                running = False
                break
            
        frame = getBoard(frame,points)
        imgBalloons, bboxs = findBalloons(frame)
        # Detect hits on balloons
        hit = detectHit(frame, bboxs)
        
        if len(hit)> 0:
            print("hit")
            pop_balloon()
            
            resetBallon()
            
            continue
        # Move the balloon upward
        balloon_y -= balloon_speed  # Adjust this value to change the speed of the balloon
        
        # Check if the balloon has reached the top of the screen
        if (balloon_y + balloon_img.get_height()) <= 0:
            # Reset balloon to a random location at the top of the screen
            balloon_x = random.randint(0, SCREEN_WIDTH*0.8)
            balloon_y = SCREEN_HEIGHT  

        # Fill the screen with white color
        screen.fill(WHITE)

        # Calculate the position of "Time Left" text
        timer = f"Time Left: {countdown_timer // 60:02}:{countdown_timer % 60:02}"
        timer_surface = render_text(timer, 46, (255, 0, 0))
        timer_width, timer_height = timer_surface.get_size()
        timer_x = SCREEN_WIDTH - timer_width - 20  # Position on the right side
        timer_y = 20  # 20 pixels from the top

        # Blit the "Time Left" text surface onto the screen
        screen.blit(timer_surface, (timer_x, timer_y))

        # Calculate the position of "Score" text
        score = "Score : " + str(hit_score)
        score_surface = render_text(score, 36, (0, 255, 0))
        score_width, score_height = score_surface.get_size()
        score_x = SCREEN_WIDTH - score_width - 20  # Position on the right side
        score_y = timer_y + timer_height + 10  # 10 pixels below the "Time Left" text

        # Blit the "Score" text surface onto the screen
        screen.blit(score_surface, (score_x, score_y))
        
        # Draw the balloon at its current position
        screen.blit(balloon_img, (balloon_x, balloon_y))
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(60)  # You can adjust the frame rate (FPS) here
    cap.release()
    cv2.destroyAllWindows()
    menu_screen()

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill(WHITE)
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Pop Balloon", 1, (255,0,0))
        screen.blit(text, ((screen.get_width() // 2) - (text.get_width() // 2),100))
        for btn in btns:
            btn.draw(screen)
            
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        if(btn.text == "Play"):
                            run = False

                        if(btn.text == "Calibrate"):
                            calirateWindow()
                            
                        if(btn.text == "Quit"):
                            pygame.quit()
                            run = False
    mainWindow()


# Quit Pygame
while True:
    menu_screen()