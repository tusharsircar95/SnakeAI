import numpy as np
import pygame

class Renderer:
    def __init__(self,SCREEN_DIMS,GRID_SQ,FONT):
        self.SCREEN_DIMS = SCREEN_DIMS
        self.GRID_SQ = GRID_SQ
        self.FONT = FONT

    def render_snake ( self, screen , snake ):
        for index,blob in enumerate(snake.blobs):
            pygame.draw.rect ( screen ,
                               (np.random.random () * 255 , np.random.random () * 255 , np.random.random () * 255) ,
                               pygame.Rect ( blob[ 0 ] * self.GRID_SQ , blob[ 1 ] * self.GRID_SQ ,
                                             self.GRID_SQ , self.GRID_SQ ) )

    def render_food ( self, screen , food ):
        if food is None:
            return
        pygame.draw.rect ( screen , (255 , 255 , 255) ,
                           pygame.Rect ( food.x * self.GRID_SQ , food.y * self.GRID_SQ ,
                                         self.GRID_SQ , self.GRID_SQ ) )

    def render_game_over( self, screen, text ):
        screen.blit ( text ,
                      ( (self.SCREEN_DIMS[ 0 ] * self.GRID_SQ / 2 - text.get_width () // 2) ,
                        (self.SCREEN_DIMS[ 1 ] * self.GRID_SQ/ 2 - text.get_height ()) ))
    def render_score(self, screen, score):
        text_score = self.FONT.render ( str(score) , True , (0 , 255 , 0) )
        screen.blit ( text_score ,
                      ((0.95*self.SCREEN_DIMS[ 0 ] * self.GRID_SQ - text_score.get_width () // 2) ,
                       (2 * self.GRID_SQ - text_score.get_height ())) )

