import numpy as np
import pygame

class Renderer:
    def __init__(self,SCREEN_DIMS,BORDERS,GRID_SQ,FONT):
        self.SCREEN_DIMS = SCREEN_DIMS
        self.BORDERS = BORDERS
        self.GRID_SQ = GRID_SQ
        self.FONT = FONT

    def render_borders(self,screen):
        width_percent = 0.20
        j = self.BORDERS[0]-1
        for i in range(self.SCREEN_DIMS[1]-self.BORDERS[1]-self.BORDERS[3]):
            i = i + self.BORDERS[1]
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect((j+1-width_percent) * self.GRID_SQ,
                                         (i) * self.GRID_SQ,
                                         width_percent*self.GRID_SQ, self.GRID_SQ))
        j = 0
        for i in range(self.SCREEN_DIMS[1]-self.BORDERS[1]-self.BORDERS[3]):
            i = i + self.BORDERS[1]
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect((self.SCREEN_DIMS[0]-j-1) * self.GRID_SQ,
                                         (i) * self.GRID_SQ,
                                         width_percent*self.GRID_SQ, self.GRID_SQ))
        j = self.BORDERS[1]-1
        for i in range(self.SCREEN_DIMS[0] - self.BORDERS[0] - self.BORDERS[2]):
            i = i + self.BORDERS[0]
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect((i) * self.GRID_SQ,
                                         (j+1-width_percent) * self.GRID_SQ,
                                             self.GRID_SQ, width_percent*self.GRID_SQ))
        j = 0
        for i in range(self.SCREEN_DIMS[0] - self.BORDERS[0] - self.BORDERS[2]):
            i = i + self.BORDERS[0]
            pygame.draw.rect(screen, (255, 255, 255),
                             pygame.Rect((i) * self.GRID_SQ,
                                         (self.SCREEN_DIMS[1]-j-1) * self.GRID_SQ,
                                         self.GRID_SQ, width_percent*self.GRID_SQ))

    def render_snake ( self, screen , snake ):
        for index,blob in enumerate(snake.blobs):

            pygame.draw.rect ( screen ,
                               (255,255,255),
                               pygame.Rect ( (self.BORDERS[0] +blob[ 0 ]) * self.GRID_SQ , (self.BORDERS[1]+blob[ 1 ]) * self.GRID_SQ ,
                                             self.GRID_SQ , self.GRID_SQ ) )
            if index != 0:
                pygame.draw.rect(screen,
                                 (0,0,0),
                                 pygame.Rect((self.BORDERS[0] + blob[0] + 0.20) * self.GRID_SQ,
                                             (self.BORDERS[1] + blob[1] + 0.20) * self.GRID_SQ,
                                             0.60*self.GRID_SQ, 0.60*self.GRID_SQ))

    def render_food ( self, screen , food ):
        if food is None:
            return
        pygame.draw.rect ( screen , (255 , 255 , 255) ,
                           pygame.Rect ( (self.BORDERS[0]+food.x) * self.GRID_SQ , (self.BORDERS[1]+food.y) * self.GRID_SQ ,
                                         self.GRID_SQ , self.GRID_SQ ) )

    def render_obstacles(self,screen,obstacles):
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0),
                             pygame.Rect((self.BORDERS[0]+obstacle[0]) * self.GRID_SQ, (self.BORDERS[1]+obstacle[1]) * self.GRID_SQ,
                                         self.GRID_SQ, self.GRID_SQ))
    def render_game_over( self, screen, text ):
        screen.blit ( text ,
                      ( (self.SCREEN_DIMS[ 0 ] * self.GRID_SQ / 2 - text.get_width () // 2) ,
                        (self.SCREEN_DIMS[ 1 ] * self.GRID_SQ/ 2 - text.get_height ()) ))
    def render_score(self, screen, points):
        text_points = self.FONT.render("Points: " + str(points), True, (0, 255, 0))
        screen.blit(text_points,
                    ((0.75 * self.SCREEN_DIMS[0] * self.GRID_SQ - text_points.get_width() // 2),
                     (1.5 * self.GRID_SQ - text_points.get_height())))

    def render_gnn_info(self, screen, gnn_info):
        if len(gnn_info.keys()) < 4:
            return
        info1 = "Gen %d, N = %d"%(gnn_info['gen'],gnn_info['n'])
        info2 = "Best Fitness: %d, Points: %d"%(gnn_info['best_fitness'],gnn_info['best_fitness_points'])
        info1 = self.FONT.render(info1, True, (0, 255, 0))
        info2 = self.FONT.render(info2, True, (0, 255, 0))
        screen.blit(info1,
                    ((0.25 * self.SCREEN_DIMS[0] * self.GRID_SQ - info1.get_width() // 2),
                     (1.5 * self.GRID_SQ - info1.get_height())))
        screen.blit(info2,
                    ((0.25 * self.SCREEN_DIMS[0] * self.GRID_SQ - info2.get_width() // 2),
                     (2.5 * self.GRID_SQ - info2.get_height())))