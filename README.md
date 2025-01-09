# Planetoids-Game
This repository implements the game logic for an Asteroid Shooter Game, where the player controls a ship and shoots bullets to destroy asteroids and UFOs. 

Key features of the game include:

Ship and Bullet Mechanics: The ship can move and shoot bullets. The bullets move and update their position each frame. Bullet collision with asteroids or UFOs triggers asteroid destruction or UFO damage, respectively.
Asteroid Management: Asteroids break into smaller pieces when shot. The game handles different asteroid sizes and manages their movement based on collision vectors.
UFOs and Alien UFOs: The game can spawn regular or alien UFOs based on game data. UFOs have lives, and when hit by bullets, their health decreases.
Collision Detection: Precise collision detection checks whether bullets collide with asteroids or UFOs. Asteroids also break into smaller pieces when colliding with bullets.
UFO Lives: UFOs have a limited number of lives, represented visually with "life" objects that move in sync with the UFO.

This game includes real-time updates for objects, collision resolution, and smooth visual representation of objects within the game world
