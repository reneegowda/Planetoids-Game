"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that
you interact with on the screen is a model: the ship, the bullets, and the
planetoids.

# Renee Gowda (rsg276) and Muskan Gupta (mg2479)
# December 9th
"""
from consts import *
from game2d import *
from introcs import *
import random
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a
# parameter in your method, and Wave should pass it as an argument when it calls
# the method.

class Bullet(GEllipse):
    """
    A class representing a bullet from the ship.

    Bullets are typically just white circles (ellipses). The size of the bullet
    is determined by constants in consts.py. However, we MUST subclass GEllipse,
    because we need to add an extra attribute for the velocity of the bullet.

    The class Wave will need to look at this velocity, so you will need getters
    for the velocity components. However, it is possible to write this assignment
    with no setters for the velocities. That is because the velocity is fixed
    and cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GEllipse as a helper. This init will need a parameter to set the direction
    of the velocity.

    You also want to create a method to update the bolt. You update the bolt by
    adding the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _x: x coordinate of the Bullet
    # Invariant: _x is an int or float
    #
    # Attribute _y: y coordinate of the Bullet
    # Invariant: _y is an int or float
    #
    # Attribute _width: width of the Bullet
    # Invariant: _width is an int or float. In this case, _width is twice the
    #           BULLET_RADIUS
    #
    # Attribute _height: height of the Bullet
    # Invariant: _height is an int or float. In this case, _height is twice the
    #           BULLET_RADIUS
    #
    # Attribute _fillcolor: color of the Bullet
    # Invariant: _fillcolor is a string representing a color. In this case,
    #           _fillcolor is BULLET_COLOR
    #
    # Attribute _velocity: velocity of the Bullet
    # Invariant: _velocity is a Vector2 object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getvel_x(self):
        """
        Returns the x component of the Bullet's velocity.

        The x component can be an int or a float.

        Returns:
            float: The x component of the velocity.
        """
        return self._velocity.x

    def getvel_y(self):
        """
        Returns the y component of the Bullet's velocity.

        The y component can be an int or a float.

        Returns:
            float: The y component of the velocity.
        """
        return self._velocity.y

    def getBulletVel(self):
        """
        Returns the Bullet's velocity.

        Returns:
            Vector2: A vector containing the velocity components (x, y).
        """
        return self._velocity

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, x, y, vel_x, vel_y, fillcolor):
        """
        Initializes the Bullet object.

        This initializer sets the position, size, color, and velocity of the Bullet.

        Parameters:
            x (float): The x coordinate of the Bullet's starting position.
                       Must be an int or float.
            y (float): The y coordinate of the Bullet's starting position.
                       Must be an int or float.
            vel_x (float): The x component of the Bullet's velocity.
                           Must be an int or float.
            vel_y (float): The y component of the Bullet's velocity.
                           Must be an int or float.
            fillcolor (str): The color of the Bullet.
        """
        # Call the initializer of the GEllipse superclass
        super().__init__(x=x, y=y, width=2*BULLET_RADIUS,
                         height=2*BULLET_RADIUS, fillcolor=fillcolor)

        # Initialize the velocity as a Vector2 object
        self._velocity = introcs.Vector2(vel_x, vel_y)

class Asteroid(GImage):
    """
    A class to represent a single asteroid.

    Asteroids are typically are represented by images. Asteroids come in three
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that
    determine the choice of image and asteroid radius. We MUST subclass GImage,
    because we need extra attributes for both the size and the velocity of the
    asteroid.

    The class Wave will need to look at the size and velocity, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for either of these. That is because they are fixed and cannot
    change when the asteroid is created.

    In addition to the getters, you need to write the __init__ method to set the
    size and starting velocity. Note that the SPEED of an asteroid is defined in
    const.py, so the only thing that differs is the velocity direction.

    You also want to create a method to update the asteroid. You update the
    asteroid by adding the velocity to the position. While it is okay to add a
    method to detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """

    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _x: x coordinate of the Asteroid
    # Invariant: _x is an int or float
    #
    # Attribute _y: y coordinate of the Asteroid
    # Invariant: _y is an int or float
    #
    # Attribute _width: width of the Asteroid
    # Invariant: _width is an int or float
    #
    # Attribute _height: height of the Asteroid
    # Invariant: _height is an int or float.
    #
    # Attribute _size: the size of the Asteroid
    # Invariant: _size is a str of a valid Asteroid size ('small', 'medium', 'large')
    #
    # Attribute _velocity: velocity of the Asteroid
    # Invariant: _velocity is a Vector2 object
    #
    # Attribute _direction: direction the Asteroid is moving in
    # Invariant: _direction is a list

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getSize(self):
        """
        Returns the size of the Asteroid
        """
        return self._size

    def getAstVel_x(self):
        """
        Returns the x component of the Asteroid's velocity

        The x component can be an int or a float
        """
        return self._velocity.x

    def getAstVel_y(self):
        """
        Returns the y component of the Asteroid's velocity

        The y component can be an int or a float
        """
        return self._velocity.y

    def getAstVel(self):
        """
        Returns the Asteroid's velocity
        """
        return self._velocity

    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, x, y, size, width, height, direction, source):
        """
        Initializes the Asteroid object.

        Parameter x: x coordinate of the Asteroid's starting position
        Precondition: x is an int or float

        Parameter y: y coordinate of the Asteroid's starting position
        Precondition: y is an int or float

        Parameter size: size of the Asteroid
        Precondition: size is a str ('small', 'medium', or 'large')

        Parameter width: width of the image of the Asteroid
        Precondition: width is an int or float

        Parameter height: height of the image of the Asteroid
        Precondition: width is an int or float

        Parameter direction: direction the Asteroid is moving in
        Precondition: direction is a list

        Parameter source: The image name for the associated object
        Precondition: source is a valid Asteroid image
        (SMALL_IMAGE, MEDIUM_IMAGE, and LARGE_IMAGE)
        """
        # Call the initializer of the superclass (GImage)
        super().__init__(x = x, y = y, size = size, width = width, height = height,
                         source = source)
        # Store position, size, and dimensions
        self._x = x
        self._y = y
        self._size = size
        self._width = width
        self._height = height
        self._direction = direction
        self._source = source

        # Initialize velocity: if no direction, set velocity to zero
        if direction[0] == 0 and direction[1] == 0:
            self._velocity = introcs.Vector2(0, 0)
        else:
            # Determine speed based on asteroid size
            if size == 'small':
                speed = SMALL_SPEED
            elif size == 'medium':
                speed = MEDIUM_SPEED
            else:
                speed = LARGE_SPEED

            # Normalize direction vector and scale by speed
            self._velocity = introcs.Vector2(direction[0], direction[1])
            self._velocity = self._velocity.normalize()
            self._velocity.x *= speed
            self._velocity.y *= speed

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def x_wrap(self):
        """
        Method to wrap the x component of the Asteroid so it stays onscreen.

        When the Asteroid goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the left, it should
        come back around on the right.
        """
        # Check if the x-coordinate is out of bounds and wrap accordingly
        if self.x < -DEAD_ZONE:
            self.x += GAME_WIDTH + 2 * DEAD_ZONE
        elif self.x > GAME_WIDTH + DEAD_ZONE:
            self.x -= GAME_WIDTH + 2 * DEAD_ZONE

    # WRAP METHOD FOR Y AXIS
    def y_wrap(self):
        """
        Method to wrap the y component of the Asteroid so it stays onscreen.

        When the Asteroid goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the top, it should come
        back around on the bottom.
        """
        # Check if the y-coordinate is out of bounds and wrap accordingly
        if self.y < -DEAD_ZONE:
            self.y += GAME_HEIGHT + 2 * DEAD_ZONE
        elif self.y > GAME_HEIGHT + DEAD_ZONE:
            self.y -= GAME_HEIGHT + 2 * DEAD_ZONE

    def collision_check(self, object):
        """
        Method to check whether the Asteroid collided with the object.

        Calculates the distance between the Asteroid and object and compares it
        to the sum of the radii of the Asteroid and object. If the distance is
        smaller than the sum of the radii, then the collision occurred; this
        returns True. Otherwise, returns False

        Parameter object: object being checked whether it collided with the Asteroid
        Precondition: object is a Ship or Bullet
        """
        # Calculate the distance between the asteroid and the object
        x_diff = self.x - object.x
        y_diff = self.y - object.y
        distance = math.sqrt(x_diff**2 + y_diff**2)

        # Determine asteroid radius based on size
        if self._size == 'small':
            radius_ast = SMALL_RADIUS
        elif self._size == 'medium':
            radius_ast = MEDIUM_RADIUS
        else:
            radius_ast = LARGE_RADIUS

        # Check for collision with Ship or Bullet
        if isinstance(object, Ship):
            return distance < (radius_ast + SHIP_RADIUS)
        elif isinstance(object, Bullet):
            return distance < (radius_ast + BULLET_RADIUS)

        # Return False if no collision detected
        return False


class UFO(GImage):
    """
    A class to represent a single UFO

    UFOs are represented by a UFO image. We subclass GImage for it to be able
    to draw the image correctly.
    """
    # Attribute _x: x coordinate of the AlienUFO
    # Invariant: _x is an int or float
    #
    # Attribute _y: y coordinate of the AlienUFO
    # Invariant: _y is an int or float
    #
    # Attribute _velocity: velocity of the AlienUFO
    # Invariant: _velocity is a Vector2 object

    def getUFOVel_x(self):
        """
        Returns the x component of the UFO's velocity

        The x component can be an int or a float
        """
        return self._velocity.x

    def getUFOVel_y(self):
        """
        Returns the y component of the UFO's velocity

        The y component can be an int or a float
        """
        return self._velocity.y

    def getUFOVel(self):
        """
        Returns the UFO's velocity

        Velocity is a Vector2 object.
        """
        return self._velocity

    def getUFO_x(self):
        """
        Returns UFO's x position.

        X is an int or float.
        """
        return self.x

    def getUFO_y(self):
        """
        Returns UFO's y position.

        Y is an int or float.
        """
        return self.y

    def __init__(self, x, y, source):
        """
        Initializes a new UFO object.

        Parameter x: x is the x component of the position.
        Preconditon: x is an int or float

        Parameter y: y is the y component of the position.
        Precondtion: y is an int or float

        Parameter source: source is the image name.
        Precondition: source is a string
        """
        # Call the superclass initializer to set up the image.
        super().__init__(x = x, y = y, width = UFO_RADIUS*2,
            height = UFO_RADIUS*2, source = source)

        # Generate random directions for velocity components.
        x_dir = random.random()
        y_dir = random.random()

        # Create a velocity vector and normalize it to get direction.
        self._velocity = introcs.Vector2(x_dir, y_dir)
        self._velocity = self._velocity.normalize()

        # Scale the normalized vector by UFO speed.
        self._velocity.x = self._velocity.x * UFO_SPEED
        self._velocity.y = self._velocity.y * UFO_SPEED

    def x_wrap(self):
        """
        Method to wrap the x component of the UFO so it stays onscreen.

        When the UFO goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the left, it should
        come back around on the right.
        """
        if self.x < -DEAD_ZONE:
            self.x += GAME_WIDTH + 2 * DEAD_ZONE
        elif self.x > GAME_WIDTH + DEAD_ZONE:
            self.x -= GAME_WIDTH + 2 * DEAD_ZONE

    def y_wrap(self):
        """
        Method to wrap the y component of the UFO so it stays onscreen.

        When the UFO goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the top, it should come
        back around on the bottom.
        """
        if self.y < -DEAD_ZONE:
            self.y += GAME_HEIGHT + 2 * DEAD_ZONE
        elif self.y > GAME_HEIGHT + DEAD_ZONE:
            self.y -= GAME_HEIGHT + 2 * DEAD_ZONE

    def update_UFO(self):
        # Move the UFO by updating its position based on velocity.
        self.x += self.getUFOVel_x()
        self.y += self.getUFOVel_y()

        # Wrap the UFO position around the screen.
        self.x_wrap()
        self.y_wrap()

class AlienUFO(UFO):
    """
    A class to represent a single UFO with an alien inside.
    """
    def __init__(self, x, y, source):
        """
        Initializes a new UFO object with an alien inside.

        Parameter x: x is the x component of the position.
        Preconditon: x is an int or float

        Parameter y: y is the y component of the position.
        Precondtion: y is an int or float

        Parameter source: source is the image name.
        Precondition: source is a string
        """
        # Call the parent class initializer to set up the AlienUFO.
        super().__init__(x = x, y = y, source = source)

        # Generate random directions for velocity components.
        x_dir = random.random()
        y_dir = random.random()

        # Create and normalize a velocity vector.
        self._velocity = introcs.Vector2(x_dir, y_dir)
        self._velocity = self._velocity.normalize()

        # Scale the normalized vector by UFO speed.
        self._velocity.x = self._velocity.x * UFO_SPEED
        self._velocity.y = self._velocity.y * UFO_SPEED

class UFOLives(GEllipse):
    """
    A class to represent the objects that represent the UFO's lives.
    """
    def __init__(self, x, y, vel_x, vel_y, fillcolor, width, height):
        """
        Initializes a new UFOLives object.

        Parameter x: the x coordinate of the UFOLives's starting position
        Precondition: x is an int or float

        Parameter y: the y coordinate of the UFOLives's starting position
        Precondition: y is an int or float

        Parameter vel_x: the x component of the UFOLives's velocity
        Precondition: vel_x is an int or float

        Parameter vel_y: the y component of the UFOLives's velocity
        Precondition: vel_y is an int or float

        Preconditon fillcolor: the color of the UFOLives
        Precondition: fillcolor is a string

        Parameter width: width of the object
        Precondition: width is an int or float

        Parameter height: height of the object
        Preconditon: height is an int or float
        """
        # Call the superclass initializer to set up the ellipse.
        super().__init__(x = x, y = y, fillcolor = fillcolor, width = width, height = height)

        # Set the velocity using the provided components.
        self._velocity = introcs.Vector2(vel_x, vel_y)

    def x_wrap(self):
        """
        Method to wrap the x component of the UFO so it stays onscreen.

        When the UFO goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the left, it should
        come back around on the right.
        """
        if self.x < -DEAD_ZONE:
            self.x += GAME_WIDTH + 2 * DEAD_ZONE
        elif self.x > GAME_WIDTH + DEAD_ZONE:
            self.x -= GAME_WIDTH + 2 * DEAD_ZONE

    def y_wrap(self):
        """
        Method to wrap the y component of the UFO so it stays onscreen.

        When the UFO goes offscreen, it should be wrapped back around to the
        other side. For example, when going offscreen to the top, it should come
        back around on the bottom.
        """
        if self.y < -DEAD_ZONE:
            self.y += GAME_HEIGHT + 2 * DEAD_ZONE
        elif self.y > GAME_HEIGHT + DEAD_ZONE:
            self.y -= GAME_HEIGHT + 2 * DEAD_ZONE
