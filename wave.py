"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _direction: the direction the aliens are moving
    # Invariant: _direction is a string for either left or right
    #
    # Attribute _newBolt: whether or not the player can fire a new bolt
    # Invariant: _newBolt is a boolean if the player is ready to fire a bolt
    #
    # Attribute _alienRate: how many steps until an alien shoots a bolt
    # Invariant: _alienRate is a int for how many steps until an alien fires
    #
    # Attribute _shooter: the alien in a row that will shoot a bolt
    # Invariant: _shooter is an alien object
    #
    # Attribute _stepaccum: counts the amount of steps an alien has taken
    # Invariant: _stepaccum is an int for how many steps have been taken
    #
    # Attribute _isPaused: an indicator if the game should be paused
    # Invariant: _isPaused is a boolean
    #
    # Attribute _gameDone: an indicator if the game is over
    # Invariant: _gameDone is a boolean
    #
    # Attribute _gameWon: an indicator if the game is won or lost(assume game is
    # already over)
    # Invariant: _gameWon is a boolean
    #
    # Attribute _score: the score value the player has
    # Invariant: _score is an int >= 0

    def getGameWon(self):
        """
        Returns whether or not the game has been won. This method assumes that
        the game has been completed and self._state in app.py is STATE_COMPLETE
        """
        return self._gameWon

    def getGameDone(self):
        """
        Returns whether or not the game is done and if the game should switch to
        STATE_COMPLETE
        """
        return self._gameDone

    def getIsPaused(self):
        """
        Returns whether or not the game is paused
        """
        return self._isPaused

    def setIsPaused(self,value):
        """
        Sets self._isPaused to follow whether or not the game is paused

        Parameter: value is whether or not the game is paused
        Precondition: value is a boolean
        """
        assert type(value) == bool,repr(value)+' is not a valid type'
        self._isPaused = value

    def getLives(self):
        """
        Returns self._lives, the current amount of lives the player has
        """
        return self._lives

    def getScore(self):
        """
        Returns self._score, the score value a player has
        """
        return self._score

    def __init__(self):
        """
        Initializes the Wave class

        Parameter _ship: the player ship to control
        Precondition: _ship is a Ship object or None

        Parameter _aliens: the 2d list of aliens in the wave
        Precondition: _aliens is a rectangular 2d list containing Alien objects
        or None

        Parameter _bolts: the laser bolts currently on screen
        Precondition: _bolts is a list of Bolt objects, possibly empty

        Parameter _dline: the defensive line being protected
        Precondition : _dline is a GPath object

        Parameter _lives: the number of lives left
        Precondition: _lives is an int >= 0

        Parameter _time: the amount of time since the last Alien "step"
        Precondition: _time is a float >= 0s

        Parameter _direction: the direction the aliens are moving
        Precondition: _direction is a string for either left or right

        Parameter _newBolt: whether or not the player can fire a new bolt
        Precondition: _newBolt is a boolean if the player is ready to fire a bolt

        Parameter _alienRate: how many steps until an alien shoots a bolt
        Precondition: _alienRate is a int for how many steps until an alien fires

        Parameter _shooter: the alien in a row that will shoot a bolt
        Precondition: _shooter is an alien object

        Parameter _stepaccum: counts the amount of steps an alien has taken
        Precondition: _stepaccum is an int for how many steps have been taken

        Parameter _isPaused: an indicator if the game should be paused
        Precondition: _isPaused is a boolean

        Parameter _gameDone: an indicator if the game is over
        Precondition: _gameDone is a boolean

        Parameter _gameWon: an indicator if the game is won or lost(assume game is
        alread over)
        Precondition: _gameWon is a boolean

        Parameter _score: the score value the player has
        Precondition: _score is an int >= 0
        """
        self._ship = Ship(GAME_WIDTH/2,SHIP_BOTTOM+SHIP_HEIGHT/2,
        SHIP_WIDTH,SHIP_HEIGHT,SHIP_IMAGE)
        self._aliens = self._createAliens(ALIENS_IN_ROW,ALIEN_ROWS)
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=2,linecolor='black')
        self._time=0
        self._direction = 'right'
        self._bolts = []
        self._newBolt = True
        self._alienRate = random.randint(1,BOLT_RATE)
        self._shooter = None
        self._stepaccum = 0
        self._lives = 3
        self._isPaused = False
        self._gameDone = False
        self._gameWon = None
        self._score = 0

    def update(self,input,dt):
        """
        Animates a single frame of the wave object.

        Parameter input: Allows functionality with user input
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._gameOver()
        self._changeShip(input)
        self._changeAlien(dt)
        self._verticalMove()
        self._createBolt(input)
        self._changeBolt()
        self._removeBolt()
        self._oneBolt()
        if self._stepaccum == 0:
            self._chooseAlien()
        self._alienBolt()
        self._collision()

    def draw(self, view):
        """
        Draws a single frame of the wave object.

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    def _gameOver(self):
        """
        Checks whether or not the game is over and whether or not the player won
        the game or lost it and returns booleans as required.

        The ways the player can lose the game is if the aliens reach the defense
        line or if the player runs out of lives. The player wins the game if they
        destroy all of the aliens on the screen.
        """
        aliencount = 0
        for row in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                if self._aliens[row][alien] is None:
                    aliencount+= 1
                if self._aliens[row][alien] is not None and self._aliens[row][alien].getY()-ALIEN_HEIGHT/2 <= DEFENSE_LINE:
                    self._gameDone = True
                    self._gameWon = False
        if self._lives == 0:
            self._gameDone = True
            self._gameWon = False
        elif aliencount == ALIEN_ROWS*ALIENS_IN_ROW:
            self._gameDone = True
            self._gameWon = True

    def createShip(self):
        """
        Creates a ship object with the necessary constants
        """
        self._ship = Ship(GAME_WIDTH/2,SHIP_BOTTOM+SHIP_HEIGHT/2,
        SHIP_WIDTH,SHIP_HEIGHT,SHIP_IMAGE)

    def _collision(self):
        """
        Checks whether or not an alien collides with a ship bolt and whether or
        not a ship collides with an alien bolt. If it does collide, the ship/alien
        as well as the bolt is deleted from the list(with the case of the alien,
        it becomes a None value). If the ship is hit by an alien bolt, the player
        loses a life.
        """
        for row in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                for bolt in range(len(self._bolts)):
                    if self._aliens[row][alien] is not None:
                        if self._aliens[row][alien].collides(self._bolts[bolt]):
                            self._score += self._aliens[row][alien].getScore()
                            self._aliens[row][alien] = None
                            del self._bolts[bolt]
                            self._newBolt = True
        for bolt in range(len(self._bolts)):
            if self._ship is not None:
                if self._ship.collides(self._bolts[bolt]):
                    self._ship = None
                    del self._bolts[bolt]
                    self._newBolt = True
                    self._lives -= 1
                    if self._lives >= 1:
                        self._isPaused = True

    def _changeBolt(self):
        """
        A method to update and move the alien and ship bolts in their corresponding
        directions.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt()==True:
                bolt.setY(bolt.getY()+BOLT_SPEED)
            else:
                bolt.setY(bolt.getY()-BOLT_SPEED)

    def _changeShip(self,input):
        """
        A method to move the ship left or right. If the ship is at the sides of
        the screen, the ship is not allowed to move further left or right. If a
        ship doesn't exist, the method doesn't not update anything.

        Parameter input: Allows functionality with user input to move ship
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        da = 0
        if input.is_key_down('left'):
            if self._ship is not None and min(self._ship.getX(),
            SHIP_WIDTH/2)==self._ship.getX():
                da=0
            else:
                da -= SHIP_MOVEMENT
        if input.is_key_down('right'):
            if self._ship is not None and max(self._ship.getX(),
            GAME_WIDTH-SHIP_WIDTH/2)==self._ship.getX():

                da=0
            else:
                da += SHIP_MOVEMENT
        if self._ship is not None:
            self._ship.setX(self._ship.getX()+da)

    def _changeAlien(self, dt):
        """
        A method to move the alien wave either to the right or the left by the
        amount ALIEN_H_WALK.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        if self._time >= ALIEN_SPEED:
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    alienvar = self._aliens[row][alien]
                    if self._direction == 'right' and alienvar is not None:
                        alienvar.setX(alienvar.getX()+ALIEN_H_WALK)
                    elif self._direction == 'left' and alienvar is not None:
                        alienvar.setX(alienvar.getX()-ALIEN_H_WALK)
            self._stepaccum += 1
            self._time = 0

    def _verticalMove(self):
        """
        A method to move the alien wave down ALIEN_V_WALK when it reaches the edge
        of the screen. It checks whether or not the furthest alien on the left
        or right is too close to move the aliens
        """
        leftAlien = self._verticalMoveHelperLeft()
        rightAlien = self._verticalMoveHelperRight()
        if rightAlien is not None and leftAlien is not None:
            rightBoundary = GAME_WIDTH-rightAlien.getX()-ALIEN_WIDTH//2
            leftBoundary = leftAlien.getX()-ALIEN_WIDTH//2

        if rightAlien is not None and ALIEN_H_SEP > rightBoundary:
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    alienvar = self._aliens[row][alien]
                    if self._aliens[row][alien] is not None:
                        alienvar.setY(alienvar.getY()-ALIEN_V_WALK)
                        alienvar.setX(alienvar.getX()-ALIEN_H_WALK)
            self._direction = 'left'
        if leftAlien is not None and leftBoundary < ALIEN_H_SEP:
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    alienvar = self._aliens[row][alien]
                    if self._aliens[row][alien] is not None:
                        alienvar.setY(alienvar.getY()-ALIEN_V_WALK)
                        alienvar.setX(alienvar.getX()+ALIEN_H_WALK)
            self._direction = 'right'

    def _verticalMoveHelperRight(self):
        """
        A helper method to find the most right column in the alien wave that still
        has an alien.
        """
        rightcolumn = ALIENS_IN_ROW-1
        rightrow = ALIEN_ROWS-1
        flag1 = False
        while not flag1:
            if self._aliens[rightrow][rightcolumn] is not None:
                rightAlien = self._aliens[rightrow][rightcolumn]
                flag1 = True
            elif rightcolumn == 0 and rightrow == 0:
                rightAlien = None
                flag1 = True
            elif rightrow == 0:
                rightcolumn -= 1
                rightrow = ALIEN_ROWS-1
            else:
                rightrow -= 1
        return rightAlien

    def _verticalMoveHelperLeft(self):
        """
        A helper method to find the most right column in the alien wave that still
        has an alien.
        """
        leftcolumn = 0
        leftrow = ALIEN_ROWS-1
        flag2 = False
        while not flag2:
            if self._aliens[leftrow][leftcolumn] is not None:
                leftAlien = self._aliens[leftrow][leftcolumn]
                flag2 = True
            elif leftcolumn == ALIENS_IN_ROW-1 and leftrow == 0:
                leftAlien = None
                flag2 = True
            elif leftrow == 0:
                leftcolumn += 1
                leftrow = ALIEN_ROWS-1
            else:
                leftrow -= 1
        return leftAlien

    def _createBolt(self,input):
        """
        When given user input, a ship bolt is created and added onto the list
        self._bolts and when a ship exists.

        Parameter input: Allows functionality with user input to create a bolt
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        if self._ship is not None:
            xbolt = self._ship.getX()
            ybolt = self._ship.getY()+SHIP_HEIGHT/2+BOLT_HEIGHT/2
            if input.is_key_down('up') and self._newBolt == True:
                self._bolts.append(Bolt(xbolt,ybolt,BOLT_WIDTH,
                BOLT_HEIGHT,BOLT_SPEED))

        return self._bolts

    def _chooseAlien(self):
        """
        This method determines a random column of aliens to fire a bolt as well
        as the lowest alien in that random column to fire. It makes sure that
        a None value Alien doesn't fire and crash the program.
        """
        flag = False
        while flag == False:
            noneind = 0
            column = random.randint(0,ALIENS_IN_ROW-1)
            for row in range(ALIEN_ROWS):
                if self._aliens[row][column] is None:
                    noneind += 1
            if ALIEN_ROWS != noneind:
                flag = True
        for row in range(ALIEN_ROWS-1,-1,-1):
            if self._aliens[row][column] is not None:
                self._shooter=self._aliens[row][column]

    def _alienBolt(self):
        """
        This method fires a bolt from the alien that was choosen from the method
        _chooseAlien. It creates a bolt with negative velocity to differentiate
        it from a ship bolt and then appends the newly created bolt to self._bolts.
        It also resets self._stepaccum to make sure there is a delay between
        the next alien firing.
        """
        if self._stepaccum == self._alienRate:
            boltYCoor = self._shooter.getY()-ALIEN_HEIGHT//2
            self._bolts.append(Bolt(self._shooter.getX(),boltYCoor,BOLT_WIDTH,
            BOLT_HEIGHT,-BOLT_SPEED))
            self._stepaccum = 0
            self._alienRate = random.randint(1,BOLT_RATE)

    def _oneBolt(self):
        """
        A method to check if there is only one player bolt on the screen. If there
        is one bolt, then the player cannot fire again until the bolt goes off
        the screen.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt()==True:
                self._newBolt = False

    def _removeBolt(self):
        """
        Removes bolts from the screen once they are out of bounds. For player bolts,
        it then allows the player to fire another bolt.
        """
        boltPos = []
        for bolt in range(len(self._bolts)):
            if self._bolts[bolt].getY()-BOLT_HEIGHT/2 >= GAME_HEIGHT:
                if self._bolts[bolt].isPlayerBolt():
                    self._newBolt = True
                boltPos.append(bolt)
            elif self._bolts[bolt].getY()+BOLT_HEIGHT/2 <= 0:
                boltPos.append(bolt)
        for pos in boltPos:
            del self._bolts[pos]

    def _createAliens(self,row,col):
        """
        This method initializes a wave of aliens and then appends them to
        self._aliens in the wave object.

        Parameter: row is the amount of aliens in a rows
        Precondition: row is an integer equal to ALIENS_IN_ROW

        Parameter; col is the amount of alien rows
        Precondition: col is an integer equal to ALIEN_ROWS
        """
        assert type(row) == int and row == ALIENS_IN_ROW,repr(row)+ 'is not a '+\
        'valid type and does not equal the correct constant'
        assert type(col) == int and col == ALIEN_ROWS,repr(col)+' is not a valid type '+\
        ' and does not equal the correct constant'
        accum = []
        noSpace=ALIEN_ROWS-0.5

        bottom = ALIEN_CEILING+ALIEN_HEIGHT*(noSpace)+ALIEN_V_SEP*(ALIEN_ROWS-1)
        bottombegin = GAME_HEIGHT-bottom
        rowcounter = 0
        alienimage = 0
        for col in range(0,col):
            variable = []
            if alienimage == len(ALIEN_IMAGES):
                alienimage = 0
            leftbegin = ALIEN_H_SEP+ALIEN_WIDTH//2
            for alien in range(0,row):
                variable.append(Alien(leftbegin,bottombegin,ALIEN_WIDTH,
                ALIEN_HEIGHT,ALIEN_IMAGES[alienimage],self._setAlienScore(col)))
                leftbegin +=ALIEN_H_SEP+ALIEN_WIDTH
            bottombegin +=ALIEN_V_SEP+ALIEN_HEIGHT
            rowcounter += 1
            if rowcounter == 2:
                rowcounter =0
                alienimage +=1
            accum.append(variable)
        return accum

    def _setAlienScore(self,row):
        """
        Returns a score value for the aliens in the given row. For every higher
        alien, the score value should increase by 20 points.

        Parameter: row is the row to which assign a score to
        Precondition: row is an int >= 0 and <= to ALIEN_ROWS
        """
        assert type(row) == int and row >= 0 and row <= ALIEN_ROWS,repr(row)+\
        ' is not a valid type or valid row'
        isEven = None
        score = 20
        if row % 2 == 0:
            tracker = row // 2
        else:
            tracker = row // 2
        for value in range(tracker):
            score += 20
        return score
