"""This is the game Snake.
There is a road with three lanes. Cars of various sizes, motorcycles and trucks are spawned randomly.
The player is a car. You can change the size of the car.
The other vehicles are going in the opposite direction.
The player has to avoid the other vehicles. The longer he can avoid them, the more points he gets and faster the other vehicles go.
When you hit a vehicle, the game is over.
The highest score is kept and changes if a new highscore is reached. The highscore depends on the size.

Pygame was used for the graphics."""
import pygame
import random


# Standard settings
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)




# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, setting):
        pygame.sprite.Sprite.__init__(self)
        self.images = ['imgs/RijdenAuto1.1.png', 'imgs/RijdenAuto1.2.png', 'imgs/RijdenAuto1.3.png', 'imgs/RijdenAuto1.4.png']
        self.size = [5, 20, 35, 50][setting]
        self.image = pygame.image.load(self.images[setting]).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
    def changespeed(self, x):
        self.change_x += x
    def update(self):
        self.rect.x += self.change_x
        if self.rect.x > 240 + 50 - self.size:
            self.rect.x = 240 + 50 - self.size
        if self.rect.x < 0:
            self.rect.x = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.random = int(random.randrange(0, 6))
        self.images = ['imgs/RijdenAuto2.1.png', 'imgs/RijdenAuto2.2.png', 'imgs/RijdenAuto2.3.png', 'imgs/RijdenAuto2.4.png', 'imgs/RijdenTruck1.png', 'imgs/RijdenMotor1.png']
        self.image = pygame.image.load(self.images[self.random]).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.accel = 0
    def givey(self):
        return self.rect.y
    def setaccel(self, accel):
        self.accel = accel
    def update(self):
        self.rect.y += 2 + self.accel



# Game mechanics
    # Initialiazing
def init(xdisplay, ydisplay, name):
    pygame.init()
    display = pygame.display.set_mode([xdisplay, ydisplay])
    pygame.display.set_caption(name)
    return display

    # Write text
def write(font, text, color, display, place):
    txt = font.render(text, True, color)
    display.blit(txt, place)

    # User moves settings
def usermovessetting(done, done2, done3, setting, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done, done2, done3 = False, False, False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                setting += 1
                if setting > 3:
                    setting = 0
            elif event.key == pygame.K_SPACE:
                done = False
            elif event.key == pygame.K_r:
                done, done2, done3 = False, False, False
                play(display)
    return done, done2, done3, setting

    # User moves game
def usermovesgame(done2, done3, state, player, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done2, done3 = False, False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-6)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(6)
            elif event.key == pygame.K_SPACE:
                if state == 1:
                    state = 0
                else:
                    state = 1
            elif event.key == pygame.K_r:
                done2, done3 = False, False
                play(display)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(6)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-6)
    return done2, done3, state

    # Display background
def backgrounddisplay(display, background, ybackground, accel):
    display.blit(background, [0, ybackground])
    display.blit(background, [0, ybackground - 430])
    ybackground += 2 + accel
    if ybackground > 430:
        ybackground = 0
    return ybackground

    # New blocks
def newblocks(block1, allblocks, blocks, block2):
    if block1.givey() > 50:
        rand = 20 + 100*int(random.randrange(0, 3))
        block1 = Block(rand, -150)
        allblocks.add(block1)
        blocks.add(block1)
        rand = 20 + 100*int(random.randrange(0, 3))
        block2 = Block(rand, -150)
        hits = pygame.sprite.spritecollide(block2, blocks, False)
        while len(hits) > 0:         
            rand = 20 + 100*int(random.randrange(0, 3))
            block2 = Block(rand, -150)
            hits = pygame.sprite.spritecollide(block2, blocks, False)
        blocks.add(block2)
        allblocks.add(block2)
    return block1, allblocks, blocks, block2

    # Accelerate
def accelerate(time, accel, blocks):
    if time%750 == 0:
        accel += 1
    for i in blocks:
        i.setaccel(accel)
    return accel

    # Die
def playerhit(player, blocks, done2):
    hits = pygame.sprite.spritecollide(player, blocks, True)
    if len(hits) > 0:
        done2 = False
    return blocks, done2

    # Read highscore
def readhighscore(name, setting):
    with open(name, 'r') as file:
        z = list(file.read())
        try:
            lis = [[], [], [], []]
            e = 0
            for i in z:
                if i == ' ':
                    e += 1
                elif i == ',':
                    pass
                else:
                    lis[e].append(i)
            l = ''
            for i in lis[setting]:
                l += i
            highscore = int(l)
        except:
            highscore = 0
            lis = [['0'], ['0'], ['0'], ['0']]
    return lis, highscore

    # Improve highscore
def improvehighscore(name, time, highscore, lis, setting, newhighscore):
    with open(name, 'w') as file:
            if time > highscore:
                lis[setting] = [str(time)]
                newhighscore = True
            h = ''
            for i, j in enumerate(lis):
                for r in j:
                    h += r
                if i != 3:
                    h += ' ,'
            file.write(h)
    return lis, newhighscore




# Game loop
def play(display):
    # Names
    font = pygame.font.Font("C:/Windows/Fonts/FORTE.TTF", 20)
    font2 = pygame.font.Font("C:/Windows/Fonts/STENCIL.TTF", 40)
    allblocks = pygame.sprite.Group()
    background = pygame.image.load('imgs/RijdenAchtergrond.png').convert()
    blocks = pygame.sprite.Group()
    block1 = Block(20, 0)
    block2 = Block(120, 0)
    blocks.add(block1)
    blocks.add(block2)
    allblocks.add(block1)
    allblocks.add(block2)
    accel = 0
    setting = 3
    newhighscore = False
    ybackground = 0
    clock = pygame.time.Clock()
    time = 0
    done, done2, done3 = True, True, True
    state = 1

    # Settings
    while done:
        # User moves settings
        done, done2, done3, setting = usermovessetting(done, done2, done3, setting, display)

        # Display
        display.fill(black)
        versions = ['Mini', 'Small', 'Medium', 'Big']
        write(font, 'Size: ' + versions[setting], blue, display, [10, 150])
        write(font, 'Press arrow right to', white, display, [10, 10])
        write(font, 'change size', white, display, [10, 30])
        write(font, 'Press space to start', white, display, [10, 50])
        write(font, 'Press r to restart', white, display, [10, 70])

        # Flip display
        pygame.display.flip()

    # Make player
    player = Player(120, 350, setting)
    allblocks.add(player)

    # Game
    while done2:
        # User moves game
        done2, done3, state = usermovesgame(done2, done3, state, player, display)

        # When game plays
        if state == 1:
            
            time += 1

            # Main game mechanics
            block1, allblocks, blocks, block2 = newblocks(block1, allblocks, blocks, block2)
            accel = accelerate(time, accel, blocks)
            blocks, done2 = playerhit(player, blocks, done2)

            # Display
            display.fill(black)
            ybackground = backgrounddisplay(display, background, ybackground, accel)
            allblocks.update()
            allblocks.draw(display)
            write(font, 'Score: ' + str(time), green, display, [120, 10])
            write(font, 'Level ' + str(accel + 1), white, display, [120, 30])

            # Time between loops
            clock.tick(60)

        # When pause
        else:
            # Display
            display.fill(black)
            write(font2, 'Pause', white, display, [70, 150])
            write(font2, 'Level ' + str(accel + 1), green, display, [70, 210])
            write(font2, versions[setting], yellow, display, [70, 270])
            write(font, 'Press r to restart', white, display, [10, 10])

        # Flip display
        pygame.display.flip()

    # Highscore
    lis, highscore = readhighscore('HighscoreRijden.txt', setting)
    lis, newhighscore = improvehighscore('HighscoreRijden.txt', time, highscore, lis, setting, newhighscore)
                
    # Display end
    while done3:
        # User moves game
        done2, done3, state = usermovesgame(done2, done3, state, player, display)
        
        # Display
        display.fill(black)
        write(font2, 'Score: ' + str(time), green, display, [10, 150])
        write(font2, 'Level ' + str(accel + 1), green, display, [70, 210])
        write(font2, versions[setting], yellow, display, [70, 270])
        write(font, 'Press r to restart', white, display, [10, 70])
        write(font, 'Highscore: ' + str(highscore), white, display, [70, 10])
        if newhighscore:
            write(font, 'New highscore', green, display, [70, 30])
            
        # Flip display
        pygame.display.flip()




# Main loop        
def main():
    display = init(290, 430, 'Highway Rider')
    play(display)
    pygame.quit()


# Start game
if __name__ == '__main__':
    main()
