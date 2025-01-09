"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in
the Planetoids game. Instances of Wave represent a single level, and should
correspond to a JSON file in the Data directory. Whenever you move to a new
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on
screen. These are model objects. Their classes are defined in models.py.

# Renee Gowda (rsg276) and Muskan Gupta (mg2479)
# December 9th 2024
"""
from game2d import *
from consts import *
from models import *
import random
import datetime
import math
import introcs

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    The Wave class controls the mechanics of a single level in the Planetoids game.

    Responsibilities include managing the ship, asteroids, bullets, and UFOs, as well as
    detecting collisions between game objects. The class ensures gameplay progression by
    handling events like destroying asteroids, reducing player lives, and advancing to
    new levels or ending the game.

    ATTRIBUTES:
    - _data: Stores the JSON data for the current wave, used for reloading the level.
    - _ship: The player's ship (an instance of the Ship class).
    - _asteroids: A list of active Asteroid objects on the screen.
    - _bullets: A list of active Bullet objects fired by the ship.
    - _lives: Integer representing the remaining lives of the player.
    - _firerate: Tracks the number of frames since the last bullet was fired.
    - _sound: Boolean indicating whether sound effects are enabled.
    - _UFO: Instance of the UFO class, representing the alien ship.
    - _UFOlives: Integer representing the remaining lives of the UFO.
    - _ufolivesimage: List of UFOLives objects, visually representing UFO lives.

    METHODS:
    - getLives: Returns the current number of player lives.
    - getUFOLives: Returns the current number of UFO lives.
    - __init__: Initializes the wave, creating the ship, asteroids, UFO, and other attributes.
    """

    # GETTERS AND SETTERS
    def getLives(self):
        """
        Returns the current number of player lives.

        This method allows external access to the player's remaining lives, which are
        represented as an integer between 0 and the maximum value defined by SHIP_LIVES.
        """
        return self._lives

    def getUFOLives(self):
        """
        Returns the current number of UFO lives.

        This method allows external access to the UFO's remaining lives, which are
        represented as an integer between 0 and the maximum value defined by UFO_LIVES.
        """
        return self._UFOlives

    # INITIALIZER
    def __init__(self, json):
        """
        Initializes the Wave instance by creating the ship, asteroids, bullets, UFO, and
        other gameplay elements.

        The initializer extracts data from the provided JSON file and uses it to configure
        the attributes of the Wave instance. It sets up the asteroids according to their
        size, position, and direction, initializes the player ship, and prepares the UFO
        with its corresponding lives and visual indicators.

        PARAMETERS:
        - json: A JSON file containing the configuration data for the current wave.
        """
        self._data = json  # Load JSON data for the wave configuration

        # Initialize the player's ship
        self._ship = self.newShip()

        # Initialize the list of asteroids using JSON data
        self._asteroids = []
        for i in range(len(self._data['asteroids'])):
            size_temp = self._data['asteroids'][i]['size']

            # Determine asteroid attributes based on size
            if size_temp == 'small':
                source_temp = SMALL_IMAGE
                radius = SMALL_RADIUS
            elif size_temp == 'medium':
                source_temp = MEDIUM_IMAGE
                radius = MEDIUM_RADIUS
            elif size_temp == 'large':
                source_temp = LARGE_IMAGE
                radius = LARGE_RADIUS

            # Create a new asteroid instance and add it to the list
            temp = Asteroid(
                x=self._data['asteroids'][i]['position'][0],
                y=self._data['asteroids'][i]['position'][1],
                size=size_temp,
                width=2 * radius, height=2 * radius,
                direction=self._data['asteroids'][0]['direction'],
                source=source_temp
            )
            self._asteroids.append(temp)

        # Initialize bullets, fire rate, and player lives
        self._bullets = []
        self._firerate = 0
        self._lives = SHIP_LIVES

        # Enable sound by default
        self._sound = True

        # Initialize the UFO and its attributes
        self._UFO = self.new_UFO()
        self._UFOlives = UFO_LIVES
        self._ufolivesimage = []

        # Generate visual indicators for UFO lives
        self.alienLives_image()


    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
def update(self, input, dt, sound):
    """
    Updates the models for the next animation frames.

    Moves the position of everything for just one animation step and
    resolves collisions (potentially deleting objects).

    Parameter input: What keys are pressed by the player
    Precondition: Any key on the keyboard

    Parameter dt: Time in seconds since the last call to update
    Precondition: dt is an int

    Parameter sound: Whether the player has sound on or not.
    Precondition: sound is a boolean
    """
    # Increment the frame counter for bullet firing rate
    self._firerate += 1
    # Update the sound setting based on the input parameter
    self._sound = sound

    # --- UPDATE THE SHIP'S MOVEMENT ---
    # Ensure the ship exists before applying movement updates
    if not self._ship == None:
        # Rotate the ship left when the 'left' key is held
        if input.is_key_down('left'):
            self._ship.turn_left()
        # Rotate the ship right when the 'right' key is held
        if input.is_key_down('right'):
            self._ship.turn_right()
        # Apply thrust to the ship when the 'up' key is held
        if input.is_key_down('up'):
            self._ship.apply_thrust()

        # Update the ship's position by adding velocity to its coordinates
        self._ship.x += self._ship.getShipVel_x()
        self._ship.y += self._ship.getShipVel_y()

        # Ensure the ship wraps around the screen edges
        self._ship.x_wrap()
        self._ship.y_wrap()

        # --- UPDATE THE ASTEROIDS ---
        # Iterate through each asteroid and update its position
        for ast in self._asteroids:
            ast.x += ast.getAstVel_x()  # Add velocity to the x-coordinate
            ast.y += ast.getAstVel_y()  # Add velocity to the y-coordinate
            ast.x_wrap()  # Handle x-coordinate wrapping
            ast.y_wrap()  # Handle y-coordinate wrapping

            # Check for collision between the asteroid and the ship
            if ast.collision_check(self._ship):
                # Decrement player lives and break the colliding asteroid
                self._lives -= 1
                self.breaking_asteroids(ast, self._ship)
                # Remove the asteroid from the list and set the ship to None
                self._asteroids.remove(ast)
                self._ship = None
                return

        # Handle collisions between the UFO and the ship if the UFO exists
        if self._UFO != None:
            if self.collision_UFO(self._UFO, self._ship):
                # Decrement player lives and UFO lives on collision
                self._lives -= 1
                self._ship = None
                self._UFOlives -= 1
                return

    # --- UPDATE BULLETS ---
    self.bullet_update(input)

    # --- UPDATE UFO ---
    if self._UFO != None:
        self._UFO.update_UFO()  # Update the UFO's movement and behavior
        self.update_UFOLives()  # Update the UFO's lives display
        if self._UFOlives < 1:
            self._UFO = None  # Remove the UFO if it has no lives left


# DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
def draw(self, view):
    """
    Method to draw all models to the screen.
    This method call instructs Python to draw in the window.

    Parameter view: Reference to the window
    Precondition: an instance of GameApp
    """
    # Draw the ship if it exists
    if self._ship != None:
        self._ship.draw(view)

    # Iterate through all asteroids and draw each one
    for i in range(len(self._asteroids)):
        if i < len(self._asteroids):
            self._asteroids[i].draw(view)

    # Iterate through all bullets and draw each one
    for j in range(len(self._bullets)):
        self._bullets[j].draw(view)

    # Draw the UFO if it exists
    if self._UFO != None:
        self._UFO.draw(view)

    # Draw the UFO's lives display
    for l in range(len(self._ufolivesimage)):
        self._ufolivesimage[l].draw(view)


def shoot_bullet(self, x, y, facing, rate):
    """
    Method to create a new bullet.

    Calculates the starting position of the bullet (the front tip of
    the ship) by adding the ship's current position to the facing multiplied
    by the ship's radius (treating the ship as a circle).
    Calculates the new velocity of the bullet by multiplying the
    BULLET_SPEED constant by the direction the ship is facing.
    Each calculation is done by breaking the position or velocity into
    x and y components.

    The bullet is only created if it has been more than or equal to the
    allowed number of seconds.

    Parameter x: Current x of the ship
    Precondition: x is an int or float value

    Parameter y: Current y of the ship
    Precondition: y is an int or float value

    Parameter facing: The direction the ship is facing
    Precondition: facing is a Vector2 object

    Parameter rate: The number of seconds the object needs to wait before
    firing a bullet.
    Precondition: rate is an int
    """
    # Check if enough time has passed to allow firing a new bullet
    if self._firerate >= rate:
        self._firerate = 0  # Reset the firing rate counter

        # Calculate the bullet's starting position
        new_x = x + facing.x * SHIP_RADIUS
        new_y = y + facing.y * SHIP_RADIUS

        # Calculate the bullet's velocity based on its direction
        new_vel_x = facing.x * BULLET_SPEED
        new_vel_y = facing.y * BULLET_SPEED

        # Create a new bullet object and add it to the bullets list
        new_bullet = Bullet(
            x=new_x,
            y=new_y,
            vel_x=new_vel_x,
            vel_y=new_vel_y,
            fillcolor=BULLET_COLOR
        )
        self._bullets.append(new_bullet)

        # Play the bullet sound effect if sound is enabled
        if self._sound:
            pewSound = Sound('pew1.wav')
            pewSound.play()

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

    def new_asteroid(self, size, radius, vel, x_old, y_old, source):
    """
    Method to create a new asteroid

    Calculates the center for the asteroid after it was broken off of a
    bigger asteroid. Uses the old center and adds it to the components
    of the resultant vector multiplied by the radius of the new asteroid.
    The direction of the new asteroid is the same as the direction of the
    given resultant vector.

    Parameter size: Size of the new asteroid
    Precondition: one size smaller than the asteroid before it and is a
    valid asteroid size ('small', 'medium', or 'large')

    Parameter radius: Radius of the new asteroid
    Precondition: radius is an int that is a valid asteroid radius
    (SMALL_RADIUS, MEDIUM_RADIUS, LARGE_RADIUS)

    Parameter vel: Resultant vector of an object colliding with an asteroid
    Precondition: vel is a Vector2 object

    Parameter x_old: X coordinate of the center of the asteroid that is
    being broken
    Precondition: x is an int or float

    Parameter y_old: Y coordinate of the center of the asteroid that is
    being broken
    Precondition: y is an int or float

    Parameter source: The image name for the associated object
    Precondition: source is a valid Asteroid image (SMALL_IMAGE,
    MEDIUM_IMAGE, LARGE_IMAGE)
    """
    # Creates a new Asteroid object with the specified parameters
    return Asteroid(
        # Calculate the new x-coordinate using the radius and velocity's x-component
        x = (radius * vel.x) + x_old,
        # Calculate the new y-coordinate using the radius and velocity's y-component
        y = (radius * vel.y) + y_old,
        # Set the size of the new asteroid
        size = size,
        # The width is twice the radius (diameter of the asteroid)
        width = 2 * radius,
        # The height is also twice the radius
        height = 2 * radius,
        # The direction is defined by the velocity components
        direction = [vel.x, vel.y],
        # The image source for the asteroid is passed as a parameter
        source = source
    )

def rotate_vector(self, vector, angle):
    """
    Method to rotate vector by angle.

    The vector result is the resultant vector for the asteroids that
    are a result of an asteroid being broken.

    Parameter vector: Vector to be rotated
    Precondition: vector is a Vector2 object

    Parameter angle: The angle the vector needs to be rotated by
    Precondition: angle is an int or float
    NOTE: angle should be in radians
    """
    # Calculate the cosine and sine of the angle
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    # Return the rotated vector using the standard 2D rotation formula
    return introcs.Vector2(
        vector.x * cos_theta - vector.y * sin_theta,  # x' = x*cosθ - y*sinθ
        vector.x * sin_theta + vector.y * cos_theta   # y' = x*sinθ + y*cosθ
    )

def breaking_asteroids(self, asteroid, object):
    """
    Method to split the given asteroid into three smaller asteroids. If the
    asteroid is already the smallest size, nothing happens.

    Add the new asteroids to the _asteroids attribute of the wave object.
    Position of each new asteroid is calculated using the collision vector.
    If the collision is with the ship, then the collision vector is the
    unit vector for the ship velocity, unless the ship is standing still;
    then we use the facing vector instead. If the collision is with a
    bullet, then it is the unit vector for the bullet velocity.

    Parameter asteroid: The Asteroid involved in the collision
    Precondition: asteroid is an Asteroid object in the wave object's
    attribute _asteroids

    Parameter object: The object the asteroid collided with
    Precondition: object is either a Bullet object in the wave object's
    attribute _bullets or is wave's Ship object
    """
    # Store the old coordinates of the asteroid
    x_old = asteroid.x
    y_old = asteroid.y

    # Determine the collision vector based on the object type
    if isinstance(object, Ship):  # If the object is a Ship
        velocity = object.getShipVel()  # Get the ship's velocity
        if velocity == Vector2(0.0, 0.0):  # If the ship is stationary
            velocity = self._ship.getFacing()  # Use the ship's facing direction
    if isinstance(object, Bullet):  # If the object is a Bullet
        velocity = object.getBulletVel()  # Get the bullet's velocity

    # Normalize the collision vector to get a unit vector
    velocity.normalize()
    angle = math.radians(120)  # Define the angle for splitting (120 degrees)

    # Rotate the velocity vector to create the directions for the new asteroids
    v1 = self.rotate_vector(velocity, angle)  # First direction
    v1.normalize()
    v2 = self.rotate_vector(velocity, 2 * angle)  # Second direction
    v2.normalize()
    v3 = velocity  # Third direction remains unchanged

    # Determine the size, radius, and image of the new asteroids based on the original size
    if asteroid.getSize() == 'large':
        new_size = 'medium'
        new_radius = MEDIUM_RADIUS
        new_image = MEDIUM_IMAGE
    elif asteroid.getSize() == 'medium':
        new_size = 'small'
        new_radius = SMALL_RADIUS
        new_image = SMALL_IMAGE
    else:
        return  # Small asteroids do not break further

    # Create three new asteroids with the calculated attributes
    new_asteroids = [
        self.new_asteroid(new_size, new_radius, v1, x_old, y_old, new_image),
        self.new_asteroid(new_size, new_radius, v2, x_old, y_old, new_image),
        self.new_asteroid(new_size, new_radius, v3, x_old, y_old, new_image)
    ]

    # Add the new asteroids to the wave's list of asteroids
    self._asteroids.extend(new_asteroids)

def newShip(self):
    """
    Method to create a new Ship object.

    Creates ship using data from wave object's _data attribute
    NOTE: The given angle in _data is in degrees. Convert the angle to degrees
    to radians.
    """
    # Create a new Ship object with the provided position, angle, and dimensions
    return Ship(
        x = self._data['ship']['position'][0],  # X-coordinate from data
        y = self._data['ship']['position'][1],  # Y-coordinate from data
        angle = math.radians(self._data['ship']['angle']),  # Convert angle to radians
        width = 2 * SHIP_RADIUS,  # Set the ship's width
        height = 2 * SHIP_RADIUS,  # Set the ship's height
        source = SHIP_IMAGE  # Use the ship's image source
    )

def checkAsteroids(self):
    """
    Method to check if there are any asteroids left in the wave.

    Returns False if there are no asteroids left. Returns True otherwise.
    """
    # Return False if the list of asteroids is empty, True otherwise
    if self._asteroids == []:
        return False
    return True

def checkShip(self):
    """
    Method to check if there is a Ship left in the wave.

    Returns False is there is no Ship. Returns True otherwise.
    """
    # Return False if the ship object is None, True otherwise
    if self._ship == None:
        return False
    return True

def checkUFO(self):
    """
    Method to check if the UFO exists.

    Returns False if there is no UFO. Returns True otherwise.
    """
    # Return False if the UFO object is None, True otherwise
    if self._UFO == None:
        return False
    return True

    def bullet_update(self, input):
    """
    Method to move and update Bullet.

    Parameter input: What keys are pressed by the player
    Precondition: Any key on the keyboard
    """
    if self._ship != None:  # Ensure the ship exists before updating bullets
        if input.is_key_down('spacebar'):  # Check if the spacebar is pressed
            facing = self._ship.getFacing()  # Get the ship's current facing direction
            # Shoot a new bullet from the ship's current position in the facing direction
            self.shoot_bullet(self._ship.x, self._ship.y, facing, BULLET_RATE)
        # Update the position of each bullet based on its velocity
        for i in range(len(self._bullets)):
            self._bullets[i].x += self._bullets[i].getvel_x()  # Update x-coordinate
            self._bullets[i].y += self._bullets[i].getvel_y()  # Update y-coordinate
    i = 0
    while i < len(self._bullets):  # Loop through the bullets to check for collisions
        bullet = self._bullets[i]  # Get the current bullet
        # Check if the bullet is outside the game area (dead zone)
        if (bullet.x < -DEAD_ZONE or bullet.x > GAME_WIDTH + DEAD_ZONE or
            bullet.y < -DEAD_ZONE or bullet.y > GAME_HEIGHT + DEAD_ZONE):
            del self._bullets[i]  # Remove the bullet if it's out of bounds
        else:
            coll = False  # Initialize collision flag as False
            # Check for collisions between the bullet and asteroids
            for asteroid in self._asteroids:
                if asteroid.collision_check(bullet):  # Collision detected
                    self._asteroids.remove(asteroid)  # Remove the collided asteroid
                    self._bullets.remove(bullet)  # Remove the bullet
                    self.breaking_asteroids(asteroid, bullet)  # Break the asteroid into smaller ones
                    coll = True  # Set collision flag to True
                    break  # Exit the asteroid loop since collision occurred
            # Check for collisions between the bullet and the UFO
            if self._UFO != None:
                if self.collision_UFO(self._UFO, bullet):  # Collision detected with UFO
                    self._bullets.remove(bullet)  # Remove the bullet
                    self._UFOlives -= 1  # Decrease UFO's lives by 1
                    if self._UFOlives >= 0:  # If UFO still has lives left
                        del self._ufolivesimage[-1]  # Remove one life image
                    coll = True  # Set collision flag to True
            if not coll:  # If no collision occurred, move to the next bullet
                i += 1

def new_UFO(self):
    """
    Method that creates a new UFO object.

    Detects whether self._data says that the UFO has an alien or not.
    Sets the source accordingly.
    The starting x and y coordinates for the position of the UFO is random.
    If there is no UFO in self._data, then the method returns None.
    """
    if "UFO" in self._data:  # Check if UFO data exists
        alien = bool(self._data['UFO']['alien'])  # Determine if the UFO has an alien
        print(alien)  # Debug: Print alien status
        if alien == False:  # UFO without alien
            print('no alien')  # Debug: Print message
            return UFO(
                x = random.randrange(GAME_WIDTH),  # Random x-coordinate
                y = random.randrange(GAME_HEIGHT),  # Random y-coordinate
                source = UFO_IMAGE  # Use non-alien UFO image
            )
        elif alien == True:  # UFO with alien
            print(self._data['UFO']['alien'])  # Debug: Print alien data
            print('alien')  # Debug: Print message
            return AlienUFO(
                x = random.randrange(GAME_WIDTH),  # Random x-coordinate
                y = random.randrange(GAME_HEIGHT),  # Random y-coordinate
                source = UFOalien_IMAGE  # Use alien UFO image
            )
    else:
        return None  # No UFO data found

def collision_UFO(self, ufo, object):
    """
    Method that detects whether there has been a collision between a UFO and
    another object.

    Calculates the distance between the UFO and object and compares it
    to the sum of the radii of the UFO and object. If the distance is
    smaller than the sum of the radii, then the collision occurred; this
    returns True. Otherwise, returns False

    Parameter object: object being checked whether it collided with the UFO
    Precondition: object is a Ship or Bullet
    """
    # Calculate the x and y differences between the UFO and the object
    x_diff = ufo.x - object.x
    y_diff = ufo.y - object.y
    # Calculate the Euclidean distance between the UFO and the object
    distance = math.sqrt(x_diff**2 + y_diff**2)
    if isinstance(object, Ship):  # Check collision with a Ship
        if distance < UFO_RADIUS + SHIP_RADIUS:  # Check if distance is less than combined radii
            return True
    elif isinstance(object, Bullet):  # Check collision with a Bullet
        if distance < UFO_RADIUS + BULLET_RADIUS:  # Check if distance is less than combined radii
            return True
    return False  # No collision occurred

def alienLives_image(self):
    """
    Method that creates the objects representing the UFO Lives.

    Creates the objects with the given details and adds them to the attribute
    that stores them.
    """
    if self._UFO != None:  # Ensure the UFO exists
        # Set the initial y-coordinate for the lives icons
        y_val = self._UFO.getUFO_y() + UFO_RADIUS + 15
        for i in range(UFO_LIVES):  # Create icons for the number of UFO lives
            life = UFOLives(
                x = self._UFO.getUFO_x() - 20 + 20*(i),  # Set x-coordinate for each life
                y = y_val,  # Set y-coordinate
                vel_x = self._UFO.getUFOVel_x(),  # Set x-velocity
                vel_y = self._UFO.getUFOVel_y(),  # Set y-velocity
                fillcolor = 'green',  # Set the color of the life icon
                width = 6,  # Set the width of the icon
                height = 6  # Set the height of the icon
            )
            self._ufolivesimage.append(life)  # Add the life icon to the list

def update_UFOLives(self):
    """
    Method to updates the objects representing the UFO lives.

    The objects' new positions are calculates and are wrapped to make sure
    they do not go on forever.
    """
    for i in range(self._UFOlives):  # Loop through the remaining UFO lives
        # Update the x and y positions of the life icons based on UFO's velocity
        self._ufolivesimage[i].x += self._UFO.getUFOVel_x()
        self._ufolivesimage[i].y += self._UFO.getUFOVel_y()
        self._ufolivesimage[i].x_wrap()  # Wrap the x-coordinate if out of bounds
        self._ufolivesimage[i].y_wrap()  # Wrap the y-coordinate if out of bounds
