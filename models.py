"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

sjg276
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute x: The horizontal coordinate of Ship object center
    # Invariant: x is a int or float and is between SHIP_WIDTH/2 and GAME_WIDTH-
    # SHIP_HEIGHT/2

    # Attribute y: The vertical coordinate of Ship object center
    # Invariant: y is a int or float in between SHIP_HEIGHT/2 and GAME_HEIGHT-
    # SHIP_HEIGHT/2

    # Attribute width: The width of an Ship
    # Invariant: width is SHIP_WIDTH

    # Attribute height: The height of an Ship
    # Invariant: height is SHIP_HEIGHT

    # Attribute source: The image source for an Ship
    # Invariant: source is one of the images inside SHIP_IMAGES

    def getX(self):
        """
        Returns the horizontal coordinate of the ship object's center
        """
        return self.x

    def setX(self,value):
        """
        Sets the horizontal coordinate of the ship object's center

        The _changeShip method in Wave should make sure that the ship never leaves
        the screen. The ship x coordinate is initialized in the __init__ method
        and has assert statements to make sure the initial value is within
        SHIP_WIDTH/2 and GAME_WIDTH-SHIP_WIDTH/2.

        Parameter: x is the horizontal coordinate of Ship object center
        Precondition: x is a float or int
        """
        assert type(value)== int or type(value)== float,repr(value)+' is not a'+\
        ' a valid type'

        self.x= value

    def getY(self):
        """
        Returns the vertical coordinate of the ship object's center
        """
        return self.y

    def __init__(self,x,y,width,height,source):
        """
        Initializes a ship object with a center coordinate (x,y), width, height,
        and source.

        Parameter: x is the horizontal coordinate of Ship object center
        Precondition: x is a float or int in between SHIP_WIDTH/2 and
        GAME_WIDTH-SHIP_WIDTH/2

        Parameter: y is the vertical coordinate of Ship object center
        Precondition: y is a float or int in between SHIP_HEIGHT/2 and
        GAME_HEIGHT-SHIP_HEIGHT/2

        Parameter: width is width of the Ship object
        Precondition: width is equal to SHIP_WIDTH

        Parameter: height is height of the Ship object
        Precondition: height is equal to SHIP_HEIGHT

        Parameter: source is image of Ship object
        Precondition: source is "ship.png"
        """
        assert type(x)== int or type(x)== float,repr(x)+' is not a float or int'
        assert x >= SHIP_WIDTH/2 and x <= GAME_WIDTH-SHIP_WIDTH/2,repr(x)+\
        ' is not a width that creates a valid ship'
        assert type(y)== int or type(y)== float,repr(y)+' is not a float or int'
        assert y >= SHIP_HEIGHT/2 and y <= GAME_HEIGHT-SHIP_HEIGHT/2,repr(x)+\
        ' is not a height that creates a valid ship'
        assert width==SHIP_WIDTH and height==SHIP_HEIGHT,repr(width)+' and '+\
        repr(height)+' are not the width and height constants'
        assert source == 'ship.png',repr(source)+' is not the correct image file'

        super().__init__(x=x,y=y,width=width,height=height,source=source)

    def collides(self,bolt):
        """
        Returns True if the alien bolt collides with the ship

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt),repr(bolt)+' is not a bolt instance'

        if self.contains([bolt.getX()-BOLT_WIDTH/2,
        bolt.getY()-BOLT_HEIGHT/2]) and not bolt.isPlayerBolt():

            return True
        elif self.contains([bolt.getX()+BOLT_WIDTH/2,
        bolt.getY()-BOLT_HEIGHT/2]) and not bolt.isPlayerBolt():

            return True
        elif self.contains([bolt.getX()-BOLT_WIDTH/2,
        bolt.getY()+BOLT_HEIGHT/2]) and not bolt.isPlayerBolt():

            return True
        elif self.contains([bolt.getX()+BOLT_WIDTH/2,
        bolt.getY()+BOLT_HEIGHT/2]) and not bolt.isPlayerBolt():

            return True
        else:
            return False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute x: The horizontal coordinate of Alien object center
    # Invariant: x is a int or float in between ALIEN_WIDTH/2 and GAME_WIDTH-
    # ALIEN_WIDTH/2

    # Attribute y: The vertical coordinate of Alien object center
    # Invariant: y is a int or float in between ALIEN_HEIGHT/2 and GAME_HEIGHT-
    # ALIEN_HEIGHT/2

    # Attribute width: The width of an alien
    # Invariant: width is ALIEN_WIDTH

    # Attribute height: The height of an alien
    # Invariant: height is ALIEN_HEIGHT

    # Attribute source: The image source for an alien
    # Invariant: source is one of the images inside ALIEN_IMAGES

    # Attribute _score: The score value for an alien
    # Invariant: _score is an integer >= 0

    def getX(self):
        """
        Returns the horizontal value of the alien object's center
        """
        return self.x

    def setX(self,value):
        """
        Sets the horizontal x coordinate of the alien object's center

        Parameter: x is the horizontal coordinate of Alien object center
        Precondition: x is a float or int in between ALIEN_WIDTH/2 and GAME_WIDTH-
        ALIEN_WIDTH/2
        """
        assert type(value) == int or type(value) == float,repr(value)+' is not'+\
        ' a valid type'
        assert value>=ALIEN_WIDTH/2 and value<=GAME_WIDTH-ALIEN_WIDTH/2,repr(value)+\
        ' is not a width that creates a valid alien'

        self.x = value

    def getY(self):
        """
        Returns the vertical value of the alien object's center
        """
        return self.y

    def setY(self,value):
        """
        Sets the vertical y coordinate of the alien object's center

        Parameter: y is the vertical coordinate of Alien object center
        Precondition: y is a float or int in between 0 and GAME_HEIGHT-
        ALIEN_HEIGHT/2
        """
        var = GAME_HEIGHT-ALIEN_HEIGHT/2
        assert type(value) == int or type(value) == float,repr(value)+' is not'+\
        ' a valid type'
        assert value >= ALIEN_HEIGHT/2 and value <= var,repr(value)+\
        ' is not a height that creates a valid alien'

        self.y = value

    def getScore(self):
        """
        Returns the score for an Alien object
        """
        return self._score

    def __init__(self,x,y,width,height,source,score):
        """
        Initializes an alien object with a center coordinate, width, height,
        and source.

        Parameter: x is the horizontal coordinate of Alien object center
        Precondition: x is a float or int in between ALIEN_WIDTH/2 and
        GAME_WIDTH-ALIEN_WIDTH/2

        Parameter: y is the vertical coordinate of Alien object center
        Precondition: y is a float or int in between ALIEN_HEIGHT/2 and
        GAME_HEIGHT-ALIEN_HEIGHT/2

        Parameter: width is width of the Alien object
        Precondition: width is equal to ALIEN_WIDTH

        Parameter: height is height of the Alien object
        Precondition: height is equal to ALIEN_HEIGHT

        Parameter: source is the image of the Alien object
        Precondition: source is an entry in ALIEN_IMAGES

        Parameter: _score is the alien's score value
        Precondition: _score is an integer greater than or equal to zero
        """
        assert type(x)== int or type(x)== float,repr(x)+' is not'+\
        ' a valid type'
        assert x >= ALIEN_WIDTH/2 and x <= GAME_WIDTH-ALIEN_WIDTH/2,repr(x)+\
        ' is not a width that creates a valid alien'
        assert type(y)== int or type(y)== float,repr(x)+' is not'+\
        ' a valid type'
        assert y >= ALIEN_HEIGHT/2 and y <= GAME_HEIGHT-ALIEN_HEIGHT/2,repr(x)+\
        ' is not a height that creates a valid alien'
        assert width==ALIEN_WIDTH and height==ALIEN_HEIGHT,repr(width)+' and '+\
        repr(height)+' are not the valid constants for width and height'
        assert source in ALIEN_IMAGES,repr(source)+' is not a correct alien image'
        assert type(score) == int and score >= 0,repr(score)+' is not a valid score'

        super().__init__(x=x,y=y,width=width,height=height,source=source)
        self._score = score

    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt),repr(bolt)+' is not a bolt object'

        if self.contains([bolt.getX()-BOLT_WIDTH/2,
        bolt.getY()-BOLT_HEIGHT/2]) and bolt.isPlayerBolt():
            return True
        elif self.contains([bolt.getX()+BOLT_WIDTH/2,
        bolt.getY()-BOLT_HEIGHT/2]) and bolt.isPlayerBolt():
            return True
        elif self.contains([bolt.getX()-BOLT_WIDTH/2,
        bolt.getY()+BOLT_HEIGHT/2]) and bolt.isPlayerBolt():
            return True
        elif self.contains([bolt.getX()+BOLT_WIDTH/2,
        bolt.getY()+BOLT_HEIGHT/2]) and bolt.isPlayerBolt():
            return True
        else:
            return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # Attribute x: The horizontal coordinate of Bolt object's center
    # Invariant: x is a int or float in between BOLT_WIDTH/2 and GAME_WIDTH-
    # BOLT_WIDTH/2 and the same x value as the ship

    # Attribute y: The vertical coordinate of Bolt object's center
    # Invariant: y is a int or float in between BOLT_HEIGHT/2 and GAME_HEIGHT-
    # BOLT_HEIGHT/2

    # Attribute width: The width of an alien
    # Invariant: width is BOLT_WIDTH

    # Attribute height: The height of an alien
    # Invariant: height is BOLT_HEIGHT

    def getVelocity(self):
        """
        Returns the velocity of a bolt object
        """
        return self._velocity

    def getX(self):
        """
        Returns the x coordinate of a bolt object's center
        """
        return self.x

    def setX(self,value):
        """
        Sets the x coordinate of bolt object's center

        Parameter: x is the horizontal coordinate of Bolt object center
        Precondition: x is a float or int in between BOLT_WIDTH/2 and
        GAME_WIDTH-BOLT_WIDTH/2
        """
        var = GAME_WIDTH-BOLT_WIDTH/2
        assert type(value)== int or type(value)== float,repr(value)+' is not a'+\
        ' valid type'
        assert value >= GAME_WIDTH/2 and value <= var,repr(value)+\
        ' is not a valid width for a bolt object'

        self.x= value

    def getY(self):
        """
        Returns the y coordinate of a bolt object's center
        """
        return self.y

    def setY(self,value):
        """
        Sets the y coordinate of bolt object's center

        Parameter: y is the vertical coordinate of Bolt object center
        Precondition: y is a float or int in between -2*BOLT_HEIGHT and
        GAME_HEIGHT+2*BOLT_HEIGHT

        The reason why the y value isn't in between BOLT_HEIGHT/2 and GAME_HEIGHT-
        BOLT_HEIGHT/2 is because of a small discrepancy in deleting the bolts.
        When had the preconditions as BOLT_HEIGHT/2 and GAME_HEIGHT-BOLT_HEIGHT/2,
        the program crashed because the frames were updating too quickly so a TA
        said we could tweak the preconditions to account for this
        """
        var = GAME_HEIGHT+2*BOLT_HEIGHT
        assert type(value)== int or type(value)== float,repr(value)+' is not a'+\
        ' valid type'
        assert value >= -2*BOLT_HEIGHT and value <= var,repr(value)+\
        ' is not a valid height for a bolt object'

        self.y= value

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,width,height,velocity):
        """
        Initializes a bolt objects with a center coordinate, width, height and
        velocity.

        Parameter: x is the horizontal coordinate of Bolt object center
        and is the same x value as the ship
        Precondition: x is a float or int in between BOLT_WIDTH/2 and
        GAME_WIDTH-BOLD_WIDTH/2

        Parameter: y is the vertical coordinate of Bolt object center
        Precondition: y is a float or int in between -2*BOLT_HEIGHT and
        GAME_HEIGHT+2*BOLT_HEIGHT

        Parameter: width is width of the Bolt object
        Precondition: width is equal to BOLT_WIDTH

        Parameter: height is heighst of the Bolt object
        Precondition: height is equal to BOLT_HEIGHT

        Parameter: _velocity: the velocity in y direction
        Precondition: _velocity is an int or float
        """
        assert type(x)== int or type(x)== float,repr(x)+' is not a valid type'
        assert x >= BOLT_WIDTH/2 and x <= GAME_WIDTH-BOLT_WIDTH/2,repr(x)+\
        ' is not a valid width for a bolt object'
        assert type(y)== int or type(y)== float,repr(y)+' is not a valid type'
        assert y >= -2*BOLT_HEIGHT and y <= GAME_HEIGHT+2*BOLT_HEIGHT,repr(y)+\
        ' is not a valid height for a bolt object'
        assert width==BOLT_WIDTH and height==BOLT_HEIGHT,repr(width)+' and '+\
        repr(height)+' are not the constants for width and height'
        assert type(velocity)==int or type(velocity)==float,repr(velocity)+\
        ' is not a valid type'

        super().__init__(x=x,y=y,width=width,height=height,linecolor='black',
        fillcolor='black')
        self._velocity = velocity

    def isPlayerBolt(self):
        """
        Returns whether or not the bolt is a player bolt(positive velocity)
        """
        return self._velocity > 0
