import sgengine
import pygame
from sgengine import Data2D

class Camera(sgengine.lifecycle.Entity):
    def start(self):
        self.size = Data2D(128, 72)
        self.tag = sgengine.DEFAULT_CAMERA
        self.current_frame = None
        self.debug_collider = False
        
    def update(self, events):
        pass
    
    def draw(self, screen):
        entity_list = self.current_scene().entity_list[:]
        
        entity_list.sort(key=lambda e: e.drawing_order)
        
        flags = pygame.SRCALPHA|pygame.HWSURFACE
        self.current_frame = pygame.Surface((self.size.x, self.size.y), flags)
        self.current_frame = self.current_frame.convert_alpha()
        
        for e in entity_list:
            if issubclass(type(e), SpriteRenderer):
                self.current_frame.blit(pygame.transform.rotate(pygame.transform.flip(e.get_sprite_data(), e.get_sprite_flipped().x, e.get_sprite_flipped().y), e.get_sprite_rotation()), (e.position.x - self.position.x - e.get_sprite_pivot().x, e.position.y - self.position.y - e.get_sprite_pivot().x))
        
        if self.debug_collider:
            for c in self.current_scene().colliders_list():
                collider = pygame.Surface((c.get_collider_size().x, c.get_collider_size().y))
                collider.fill((0, 255, 0))
                self.current_frame.blit(collider, (c.get_collider_position().x - self.position.x - c.get_collider_pivot().x, c.get_collider_position().y - self.position.y - c.get_collider_pivot().y))
        
        w, h = pygame.display.get_surface().get_size()
        self.current_frame = pygame.transform.scale(self.current_frame, (w, h))
        screen.blit(self.current_frame, (0,0))

class SpriteRenderer:
    def set_sprite_data(self, sprite_data):
        self.sprite_data = sprite_data
            
    def get_sprite_data(self):
        if not hasattr(self, "sprite_data"):
            self.sprite_data = None
        return self.sprite_data
    
    def set_spite_flipped(self, sprite_flipped):
        self.sprite_flipped = sprite_flipped
    
    def get_sprite_flipped(self):
        if not hasattr(self, "sprite_flipped"):
            self.sprite_flipped = Data2D(False, False)
        return self.sprite_flipped
    
    def set_sprite_pivot(self, sprite_pivot):
        self.sprite_pivot = sprite_pivot
    
    def get_sprite_pivot(self):
        if not hasattr(self, "sprite_pivot"):
            self.sprite_pivot = Data2D(0, 0)
        return self.sprite_pivot
    
    def set_sprite_rotation(self, sprite_rotation):
        self.sprite_rotation = sprite_rotation
    
    def get_sprite_rotation(self):
        if not hasattr(self, "sprite_rotation"):
            self.sprite_rotation = 0
        return self.sprite_rotation
    
    def set_sprite(self, sprite_path):
        self.sprite_data = sgengine.load_image(sprite_path)

class Animation:
    def __init__(self, frame_time, *frames):
        self.animation_frames = frames
        self.frame_time = frame_time
        self.last_time = current_time_ms()
        self.current_frame = 0
    
    def reset_timer(self):
        self.last_time = current_time_ms()
    
    def get_frame_at_time(self, time):
        while self.last_time < time:
            self.last_time += self.frame_time
            self.current_frame += 1
            
            if self.current_frame >= len(self.animation_frames):
                self.current_frame = 0
        
        return self.animation_frames[self.current_frame]
 