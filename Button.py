import pygame

class Button():
    def __init__(self, x, y, image, scale):
        self.x_pos = x
        self.y_pos = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def update(self, screen):
        screen.blit(self.image, self.rect)
