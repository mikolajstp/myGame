
import math
import os
import arcade
import random
import mysql.connector
import time 



SPRITE_SCALING_LASER = 0.4
SPRITE_SCALING = 0.5
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.4   
COIN_COUNT = 13
COIN_SPEED = 0.7

BULLET_SPEED = 7

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "finito"

MOVEMENT_SPEED = 5
SPRITE_SPEED = 3

Window = None

class Coin(arcade.Sprite):


    def follow_sprite(self, player_sprite):
        

        self.center_x += self.change_x
        self.center_y += self.change_y

        
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            
                        
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            
            self.change_y = math.sin(angle) * COIN_SPEED


class Player(arcade.Sprite):
    """ spiller Class """

    def update(self):
    
        "flytt spilleren"
        
        self.center_x += self.change_x
        self.center_y += self.change_y

        
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        super().__init__(width, height, title)

        

        # Variables som vil holde sprite lists
        self.player_list = None
        self.bullet_list = None
        self.coin_list = None

        # Set opp spiller info
        self.player_sprite = None
        self.score =  0 

         # pistol lyder
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")

        # Set bakgrunns fargen
        arcade.set_background_color(arcade.color.CAMEL)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.score = 0

        # Set opp spilleren
        self.player_sprite = Player(":resources:images/animated_characters/male_person/malePerson_idle.png", SPRITE_SCALING)
       
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

 # lag coins
        for i in range(COIN_COUNT):
            # lag coins instanse
            
            coin = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", SPRITE_SCALING_COIN)

            # Posiser zombiene/coinsa
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # legg coinen til listen
            self.coin_list.append(coin)



    def on_draw(self):
        """
        Render the screen.
        """

        
        arcade.start_render()

        # tegn alle sprites.
        self.player_list.draw()
        self.bullet_list.draw()
        self.coin_list.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

    

        
       

    def on_update(self, delta_time):
        """ Movement and game logic """

        for coin in self.coin_list:
            coin.follow_sprite(self.player_sprite)

        # Generer en liste med alle sprites som colliderer med spillerne.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop gjennom hver colliderende sprite, fjern den, og add til scoren.
        for coin in hit_list:
            coin.kill()
            self.score += 1

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked."""

        # lag en kule
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        # Posiser kulen på spillerns location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # få fra musen destinasjonen til kulen

        dest_x = x
        dest_y = y

        # hvordan få kulen til destinasjonen.
        
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # flytt på kulen så det ikke ser ut som den flyr sidelengs
        # sideways.
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        #
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # legg til kulen til riktig liste
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # få update på alle sprites
        self.bullet_list.update()

        # Loop gjennom hver kule
        for bullet in self.bullet_list:

            # sjekk om kulen traff en coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # hvis den gjorde det fjern coinen
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # for hver coin den treffer add til score og fjern coinen
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1

            # hvis kulen flyr av skjermen fjern den
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()



    def on_update(self, delta_time):
        """ Movement and game logic """

        # flytt spilleren
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # hvis en spiller trykker en knapp endre raskheten
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # hvis spilleren slipper en knapp zero ut farten.
        
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0




def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()