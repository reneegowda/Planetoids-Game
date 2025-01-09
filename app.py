"""
Primary module for Alien Invaders

This module contains the main controller class for the Planetoids application.

# Renee Gowda (rsg276) and Muskan Gupta (mg2479)
# December 9th
"""
from consts import *
from game2d import *
from wave import *
import json

# PRIMARY RULE: Planetoids can only access attributes in wave.py via getters/setters
# Planetoids is NOT allowed to access anything in models.py

class Planetoids(GameApp):
    """
    The primary controller class for the Planetoids application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class. Any initialization should be done in
    the start method instead. This is only for this class. All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state. For a complete description of how the states work, see the
    specification for the method update().

    As a subclass of GameApp, this class has the following (non-hidden) inherited
    INSTANCE ATTRIBUTES:

    Attribute view: the game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView

    Attribute input: the user input, used to control the ship and change state
    Invariant: input is an instance of GInput

    This attributes are inherited. You do not need to add them. Any other attributes
    that you add should be hidden.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _state: the current state of the game as a value from consts.py
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE
    #
    # Attribute _wave: the subcontroller for a single wave, which manages the game
    # Invariant: _wave is a Wave object, or None if there is no wave currently active.
    #            _wave is only None if _state is STATE_INACTIVE.
    #
    # Attribute _title: the game title
    # Invariant: _title is a GLabel, or None if there is no title to display. It is None
    #            whenever the _state is not STATE_INACTIVE.
    #
    # Attribute _message: the currently active message
    # Invariant: _message is a GLabel, or None if there is no message to display. It is
    #            only None if _state is STATE_ACTIVE.
    # Attribute _paused: Whether or not the animation is paused
    # Invariant: _paused is a boolean
    #
    # Attribute _startmessage: message containing start message
    # Invariant: _startmessage is a GLabel
    #
    # Attribute _lives: the number of lives the ship has left
    # Invariant: _lives is an int
    #
    # Attribute _labelLives: the lives label to show the player how many lives
    #           they have left
    # Invariant: _labelLives is a GLabel, or None if there is no message to display.
    #           It is only None if _state is STATE_COMPLETE or STATE_INACTIVE
    #
    # Attribute _howto: message to display during STATE_WELCOME to introduce the
    #           instructions
    # Invariant: _howto is a GLabel, or None when the application is not in the
    #           STATE_WELCOME
    #
    # Attribute _instructions: message to display instructions to play the game
    # Invariant: _instructions is a GLabel, or None when the application is not in the
    #           STATE_WELCOME
    #
    # Attribute _soundLabel: message to tell player to turn sound on or off
    # Invariant: _instructions is a GLabel, or None when the application is not in the
    #           STATE_WELCOME
    #
    # Attribute _sound: whether the sound effects are on or off
    # Invariant: _sound is a boolean
    #
    # Attribute _labelLives: message to display the number of lives player has left
    # Invariant: _labelLives is a GLabel, or None when STATE_INACTIVE
    #
    # Attribute _livesUFO: number of lives the UFO has left
    # Invariant: _livesUFO is an int
    #

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and creates both
        the title (in attribute _title) and a message (in attribute _message) saying
        that the user should press a key to play a game.
        """
        # Initialize the game state to inactive
        self._state = STATE_INACTIVE
        # Wave object to handle game mechanics, set to None initially
        self._wave = None
        # Pause state for animations, default is not paused
        self._paused = False

        # Title screen label with game title and formatting
        self._title = GLabel(text = "Planetoids",
            font_name = TITLE_FONT, font_size = TITLE_SIZE)
        self._title.x = GAME_WIDTH/ 2
        self._title.y = GAME_HEIGHT / 2 + TITLE_OFFSET

        # Start game message displayed on the title screen
        self._startmessage = GLabel(text = "Press 'S' to start the game",
            font_name = MESSAGE_FONT, font_size = MESSAGE_SIZE)
        self._startmessage.x = GAME_WIDTH / 2
        self._startmessage.y = GAME_HEIGHT / 2 + MESSAGE_OFFSET
        self._message = self._startmessage

        # Welcome screen labels and flags (instructions, sound settings, etc.)
        self._howto = None
        self._instructions = None
        self._soundLabel = None
        self._sound = True

        # Check if the game is inactive and set title/message accordingly
        if self._state == STATE_INACTIVE:
            pass
        else:
            self._title = None
            if self._state == STATE_ACTIVE:
                self._message = None

        # Set player lives and corresponding label for display
        self._lives = SHIP_LIVES
        self._labelLives = GLabel(text = "Lives: " + str(self._lives),
            font_name = MESSAGE_FONT, font_size = MESSAGE_SIZE-20)
        self._labelLives.x = GAME_WIDTH - 85
        self._labelLives.y = GAME_HEIGHT - 25

        # Initialize UFO lives
        self._livesUFO = UFO_LIVES


    def update(self, dt):
    """
    Animates a single frame in the game.

    This method determines the current state of the game and performs the
    corresponding actions for each state. The primary states are described
    in the docstring. Helper methods are called for specific tasks such as
    loading the game, transitioning states, or handling specific game logic.

    Parameter dt: The time in seconds since last update
    Precondition: dt is a number (int or float)
    """
    # Check if 's' key is pressed and handle state transitions
    if self.input.is_key_pressed('s'):
        # Transition from inactive to welcome state
        if self._state == STATE_INACTIVE:
            self._state = STATE_WELCOME
            self.welcome()
        # Resume game from paused state
        elif self._paused:
            self._state = STATE_CONTINUE
            self._message = None
            self._paused = False
        # Handle welcome state logic
        elif self._state == STATE_WELCOME:
            self.welcome_state()

    # Toggle sound on/off with 'n' key in welcome state
    if self.input.is_key_pressed('n') and self._state == STATE_WELCOME:
        self._sound = not self._sound  # Toggle sound boolean
        self._soundLabel = None       # Clear sound label
        self.welcome()                # Update welcome screen

    # Exit early if game is complete or paused
    if self._state in {STATE_COMPLETE, STATE_PAUSED}:
        return

    # Transition from continue to active state
    if self._state == STATE_CONTINUE:
        self._state = STATE_ACTIVE

    # Handle loading state: initialize a new wave
    if self._state == STATE_LOADING:
        json = self.load_json(DEFAULT_WAVE)  # Load wave data from JSON
        self._wave = Wave(json)             # Create new Wave object
        self._state = STATE_ACTIVE          # Transition to active state

    # Update wave if it exists
    if self._wave is not None:
        self._wave.update(self.input, dt, self._sound)  # Update game logic
        # Check if all asteroids and UFOs are destroyed
        if not self._wave.checkAsteroids() and not self._wave.checkUFO():
            self.inactive_ast()
        # Check if the ship is destroyed
        elif not self._wave.checkShip():
            self.inactive_ship()

def draw(self):
    """
    Draws the game objects to the view.

    This method iterates through all game elements and draws them on the screen.
    The objects drawn depend on the current game state.
    """
    # Draw the main message if present
    if self._message is not None:
        self._message.draw(self.view)

    # Draw the title if present
    if self._title is not None:
        self._title.draw(self.view)

    # Draw the wave and related labels
    if self._wave is not None:
        self._wave.draw(self.view)
        self._lives = self._wave.getLives()            # Update player lives
        self._livesUFO = self._wave.getUFOLives()      # Update UFO lives
        self._labelLives.text = "Lives: " + str(self._lives)
        self._labelLives.draw(self.view)              # Draw lives label

    # Draw paused message if applicable
    if self._state == STATE_PAUSED and self._message is not None:
        self._message.draw(self.view)

    # Draw instructions, sound label, and "how to play" text if present
    if self._instructions is not None:
        self._instructions.draw(self.view)
    if self._soundLabel is not None:
        self._soundLabel.draw(self.view)
    if self._howto is not None:
        self._howto.draw(self.view)

def inactive_ast(self):
    """
    Handle winning state when all asteroids and UFOs are destroyed.

    Updates the title and message to reflect the win and transitions the state
    to STATE_COMPLETE.
    """
    self._state = STATE_COMPLETE
    self._wave = None  # Clear the wave
    # Set winning title
    self._title = GLabel(text="Congratulations!",
                         font_name=TITLE_FONT, font_size=TITLE_SIZE - 45)
    self._title.x = GAME_WIDTH / 2
    self._title.y = GAME_HEIGHT / 2 + TITLE_OFFSET
    # Set winning message
    self._message = GLabel(text="Wave Complete!",
                           font_name=MESSAGE_FONT, font_size=MESSAGE_SIZE - 15)
    self._message.x = GAME_WIDTH / 2
    self._message.y = GAME_HEIGHT / 2 + MESSAGE_OFFSET

def inactive_ship(self):
    """
    Handle state transition when the ship is destroyed.

    If lives are left, pauses the game and deducts one life. Otherwise,
    ends the game and transitions to STATE_COMPLETE.
    """
    if self._lives <= 1:  # No lives left
        self._state = STATE_COMPLETE
        self._wave = None  # Clear the wave
        # Set game over title and message
        self._title = GLabel(text="Game Over",
                             font_name=TITLE_FONT, font_size=TITLE_SIZE)
        self._title.x = GAME_WIDTH / 2
        self._title.y = GAME_HEIGHT / 2 + TITLE_OFFSET
        self._message = GLabel(text="Try again next time!",
                               font_name=MESSAGE_FONT, font_size=MESSAGE_SIZE)
        self._message.x = GAME_WIDTH / 2
        self._message.y = GAME_HEIGHT / 2 + MESSAGE_OFFSET
    else:  # Lives left, pause game
        self._lives = self._wave.getLives()  # Update lives
        self._state = STATE_PAUSED
        self._paused = True
        self._wave._ship = self._wave.newShip()  # Create new ship
        self._message = self._startmessage  # Display start message
        self.draw()  # Refresh screen

def welcome(self):
    """
    Display the welcome screen with instructions and sound toggle.

    This method sets up the labels and messages for the welcome screen.
    """
    # Set title and instructions
    self._title = GLabel(text="Welcome to Planetoids!",
                         font_name=TITLE_FONT, font_size=TITLE_SIZE - 73)
    self._title.x = GAME_WIDTH / 2
    self._title.y = GAME_HEIGHT - 80
    self._howto = GLabel(text="How to play:",
                         font_name=MESSAGE_FONT, font_size=MESSAGE_SIZE - 5)
    self._howto.x = GAME_WIDTH / 4 + 20
    self._howto.y = GAME_HEIGHT - 160
    self._instructions = GLabel(
        text="Press the up arrow to move forward.\n"
             "Press the left and right arrows to turn.\n"
             "Press the spacebar to shoot bullets.",
        font_name=MESSAGE_FONT, font_size=MESSAGE_SIZE - 22)
    self._instructions.x = GAME_WIDTH / 2
    self._instructions.y = GAME_HEIGHT - 265

    # Set sound toggle label
    sound_text = "Press N to turn sound OFF" if self._sound else "Press N to turn sound ON"
    self._soundLabel = GLabel(text=sound_text,
                              font_name=MESSAGE_FONT, font_size=MESSAGE_SIZE - 5)
    self._soundLabel.x = GAME_WIDTH / 2
    self._soundLabel.y = GAME_HEIGHT / 2 - 30

    # Set start message
    self._message = self._startmessage
    self._message.y = GAME_HEIGHT / 2 - 100

def welcome_state(self):
    """
    Transition from the welcome state to the loading state.

    This method clears all welcome screen labels and transitions the game
    to the STATE_LOADING state to initialize the first wave.
    """
    self._state = STATE_LOADING
    self._title = None
    self._howto = None
    self._instructions = None
    self._soundLabel = None
    self._message = None
