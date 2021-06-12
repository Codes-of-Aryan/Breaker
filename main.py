#My first game using the arcade library
#Made by Aryan Agrawal

import arcade
import math


# all constants here
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
TITLE = "BREAKER"

BREAKER_SCALING = 1.75
WALL_SCALING = 0.4
BALL_SCALING = 0.25
LAVA_SCALING = 0.5
ALIEN_SCALING = 0.25
BULLET_SCALING = 1

BREAKER_MOVEMENT_SPEED = 10
BULLET_SPEED = 10

BULLET_SOUND_LEVEL = 0.25
WALL_BREAKING_SOUND_LEVEL = 0.2
GAME_OVER_SOUND_LEVEL = 1



class My_Insane_Game_Start_Page(arcade.View) : #set up for the start page

    def __init__(self):

        super().__init__()

        self.texture = arcade.load_texture("start.png")

    def on_draw(self): #draw the start screen
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.P : #starts the game

            game_view = My_Insane_Game_View()
            game_view.setup()
            self.window.show_view(game_view)

class My_Insane_Game_Game_Over_Lost(arcade.View) : #setup for the end page when the user loses

    def __init__(self):

        super().__init__()

        self.texture = arcade.load_texture("gameover_lost.png")

    def on_draw(self): #draws the game over lost screen
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R : #restarts the game

            game_view = My_Insane_Game_View()
            game_view.setup()
            self.window.show_view(game_view)

        if key == arcade.key.M: #brings the user back to the start page
            show_view = My_Insane_Game_Start_Page()
            self.window.show_view(show_view)

class My_Insane_Game_Game_Over_Win(arcade.View) : #setup for the end page when user wins

    def __init__(self):

        super().__init__()

        self.texture = arcade.load_texture("gameover_win.png")

    def on_draw(self): # draw the game over win page
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.R : #restarts the game

            game_view = My_Insane_Game_View()
            game_view.setup()
            self.window.show_view(game_view)

        if key == arcade.key.M : # brings the user back to main menu

            show_view = My_Insane_Game_Start_Page()
            self.window.show_view(show_view)

class My_Insane_Game_View(arcade.View) :

    def __init__(self) :
        super().__init__()

        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.GRAY)

        #Intializing the sprite list
        self.breaker_list = None
        self.wall_list = None
        self.ball_list = None
        self.lava_list = None
        self.alien_list = None
        self.bullet_list = None

        #seprate variables for the ball and breaker
        self.breaker_sprite = None
        self.ball_sprite = None

        #physics engine for the ball and breaker
        self.physics_engine = None
        self.ball_physics_engine = None

        #loading sounds
        self.wall_break_sound = arcade.load_sound(":resources:sounds/coin1.wav" )
        self.breaker_bounce_sound = arcade.load_sound(":resources:sounds/hit4.wav")
        self.bullet_shoot_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.game_over_sound_lose = arcade.load_sound(":resources:sounds/gameover3.wav")
        self.game_over_sound_win = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.score = 0
        self.frame = 0



    def setup (self) :

        self.score = 0
        self.frame = 0

        #creating the sprite list
        self.breaker_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.lava_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        #placing the aliens on the two top edges
        for _ in range (40, 961, 920) :
            alien = arcade.Sprite(":resources:images/alien/alienBlue_front.png", ALIEN_SCALING)
            alien.center_x = _
            alien.center_y = 600
            self.alien_list.append(alien)

        #placing the breaker
        image_source = ":resources:images/topdown_tanks/tankBody_dark.png"
        self.breaker_sprite = arcade.Sprite(image_source, BREAKER_SCALING)
        self.breaker_sprite.center_x = 450
        self.breaker_sprite.center_y = 128
        self.breaker_list.append(self.breaker_sprite)

        #placing the walls
        for i in range (400 , 571, 30) :
            for x in range(100 , 901, 80 ) :
                wall = arcade.Sprite(":resources:gui_basic_assets/red_button_normal.png", WALL_SCALING)
                wall.center_y = i
                wall.center_x = x
                self.wall_list.append(wall)

        #placing the ball and giving it speed
        self.ball_sprite = arcade.Sprite(":resources:images/pinball/pool_cue_ball.png" , BALL_SCALING)
        self.ball_sprite.center_x = 450
        self.ball_sprite.center_y = 300
        self.ball_sprite.change_y = -7
        self.ball_sprite.change_x = 2
        self.ball_list.append(self.ball_sprite)

        #placing the lava ( water in this case) on the floor
        for _ in range(0, 1200, 64)  :
            lava = arcade.Sprite(":resources:images/tiles/waterTop_high.png", LAVA_SCALING)
            lava.center_y = 20
            lava.center_x = _
            self.lava_list.append(lava)


        #declaring our physics engines
        self.physics_engine = arcade.PhysicsEngineSimple( self.breaker_sprite, self.wall_list)
        self.ball_physics_engine = arcade.PhysicsEngineSimple(self.ball_sprite, self.lava_list)



    def on_draw(self):

        arcade.start_render()

        #drawing all elements in the sprite list
        self.breaker_list.draw()
        self.wall_list.draw()
        self.ball_list.draw()
        self.lava_list.draw()
        self.alien_list.draw()
        self.bullet_list.draw()

        #displaying the score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 750, 600, arcade.csscolor.BLACK, 18 )



    def on_key_release(self, key, modifiers):

        #when keys are released, make the speed of the breaker 0

        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.breaker_sprite.change_x = 0

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.breaker_sprite.change_x = 0



    def on_key_press(self, key, modifiers):

        #when right key is pressed, move the breaker right.
        if key == arcade.key.RIGHT or key == arcade.key.D :
            if self.breaker_sprite.center_x <= 1000 :
                self.breaker_sprite.change_x = BREAKER_MOVEMENT_SPEED

        #when left key is pressed, move the breaker left.
        elif key == arcade.key.LEFT or key == arcade.key.A :
            self.breaker_sprite.change_x = -BREAKER_MOVEMENT_SPEED



    def on_update(self, delta_time: float): #updates 60 times a second


        self.frame += 1
        self.physics_engine.update()
        self.ball_physics_engine.update()


        #check for collisions between the ball and the breaker
        hits = arcade.check_for_collision_with_list(self.ball_sprite, self.breaker_list)

        if len(hits) > 0 :

            arcade.set_background_color(arcade.color.DARK_GRAY)
            self.ball_sprite.change_y *= -1


        #check for collision betweent the ball and the ball
        wall_hits = arcade.check_for_collision_with_list(self.ball_sprite, self.wall_list)

        #if wall has been hit, increase the score, remove that wall etc.
        for hit in wall_hits :

            hit.remove_from_sprite_lists()
            arcade.play_sound(self.wall_break_sound, WALL_BREAKING_SOUND_LEVEL)
            self.ball_sprite.change_y *= -1.
            self.score += 1


        #for both the aliens, every 2 seconds shoot a bullet
        # shoot the bullet directly at the breaker's current position
        for alien in self.alien_list :

            if self.frame % 120 == 0 :

                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", BULLET_SCALING)

                x_diff = self.breaker_sprite.center_x - alien.center_x
                y_diff = self.breaker_sprite.center_y - alien.center_y
                angles = math.atan2(y_diff, x_diff)

                bullet.center_y = alien.center_y
                bullet.center_x = alien.center_x
                bullet.angle = math.degrees(angles)
                bullet.change_x = math.cos(angles) * BULLET_SPEED
                bullet.change_y = math.sin(angles) * BULLET_SPEED

                self.bullet_list.append(bullet)
                arcade.play_sound(self.bullet_shoot_sound, BULLET_SOUND_LEVEL)


        #once the bullet leaves the bottom of the screen, remove it from the list
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

        #check for hits between the breaker and the bullet
        bullet_hits = arcade.check_for_collision_with_list(self.breaker_sprite, self.bullet_list)

        #game over condition 1 : if bullet hits the breaker
        for hit in bullet_hits :
            arcade.play_sound(self.game_over_sound_lose, GAME_OVER_SOUND_LEVEL)
            end_view = My_Insane_Game_Game_Over_Lost()
            self.window.show_view(end_view)

        #change the direction of the ball once it touches the edges of the screen
        if self.ball_sprite.center_x >= SCREEN_WIDTH :
            self.ball_sprite.change_x *= -1

        if self.ball_sprite.center_x <= 0 :
            self.ball_sprite.change_x *= -1

        if self.ball_sprite.center_y >= SCREEN_HEIGHT :
            self.ball_sprite.change_y *= -1


        #move the breaker from right edge to left and vice-versa
        if self.breaker_sprite.center_x >= 1050 :
            arcade.set_background_color(arcade.color.GRAY)
            self.breaker_sprite.center_x = 20

        if self.breaker_sprite.center_x <= 0 :
            arcade.set_background_color(arcade.color.DARK_GRAY)
            self.breaker_sprite.center_x = 970


        #game over condition 2 : if ball drops into the lava
        if self.ball_sprite.center_y <= 60 :
            arcade.play_sound(self.game_over_sound_lose, GAME_OVER_SOUND_LEVEL)
            end_view = My_Insane_Game_Game_Over_Lost()
            self.window.show_view(end_view)

        #game over condition 3 : if player wins
        if self.score == 66 :
            arcade.play_sound(self.game_over_sound_win, GAME_OVER_SOUND_LEVEL)
            end_view = My_Insane_Game_Game_Over_Win()
            self.window.show_view(end_view)



def main () :

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = My_Insane_Game_Start_Page()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__" :
    main()