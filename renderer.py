#!/usr/bin/env python3
"""
Module de rendu optimisé pour le jeu Roguelike
"""

import pygame
import math
from typing import List, Tuple, Optional
from config import *

class OptimizedRenderer:
    """Rendu optimisé avec cache et réutilisation d'objets"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.fonts = self._create_fonts()
        self.cache = {}
        self.particles = []
    
    def _create_fonts(self) -> dict:
        """Crée les polices une seule fois"""
        return {
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 32),
            'small': pygame.font.Font(None, 24)
        }
    
    def draw_text(self, text: str, x: int, y: int, font_size: str = 'medium', 
                  color: Tuple[int, int, int] = WHITE, center: bool = False) -> None:
        """Dessine du texte avec cache"""
        cache_key = f"{text}_{font_size}_{color}"
        if cache_key not in self.cache:
            font = self.fonts[font_size]
            self.cache[cache_key] = font.render(text, True, color)
        
        surface = self.cache[cache_key]
        if center:
            x -= surface.get_width() // 2
            y -= surface.get_height() // 2
        
        self.screen.blit(surface, (x, y))
    
    def draw_button(self, x: int, y: int, width: int, height: int, 
                   text: str, color: Tuple[int, int, int] = GREEN) -> pygame.Rect:
        """Dessine un bouton optimisé"""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)
        
        # Texte centré
        text_surface = self.fonts['medium'].render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return rect
    
    def draw_health_bar(self, x: int, y: int, width: int, height: int, 
                       current: int, maximum: int, color: Tuple[int, int, int] = RED) -> None:
        """Dessine une barre de vie optimisée"""
        # Fond
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, height))
        
        # Vie actuelle
        if maximum > 0:
            fill_width = int((current / maximum) * width)
            pygame.draw.rect(self.screen, color, (x, y, fill_width, height))
        
        # Bordure
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 2)
    
    def draw_icon(self, x: int, y: int, icon_type: str, size: int = 20, 
                  color: Tuple[int, int, int] = WHITE) -> None:
        """Dessine une icône géométrique simple"""
        if icon_type == "heart":
            self._draw_heart(x, y, size, color)
        elif icon_type == "sword":
            self._draw_sword(x, y, size, color)
        elif icon_type == "shield":
            self._draw_shield(x, y, size, color)
        elif icon_type == "skull":
            self._draw_skull(x, y, size, color)
        elif icon_type == "crown":
            self._draw_crown(x, y, size, color)
        elif icon_type == "plus":
            self._draw_plus(x, y, size, color)
        elif icon_type == "castle":
            self._draw_castle(x, y, size, color)
    
    def _draw_heart(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine un cœur simple"""
        points = [
            (x, y + size//2),
            (x + size//4, y),
            (x + size//2, y + size//4),
            (x + size//2, y + size//2),
            (x, y + size)
        ]
        pygame.draw.polygon(self.screen, color, points)
    
    def _draw_sword(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine une épée simple"""
        # Lame
        pygame.draw.rect(self.screen, color, (x + size//2 - 1, y, 2, size//2))
        # Garde
        pygame.draw.rect(self.screen, color, (x, y + size//2 - 2, size, 4))
        # Poignée
        pygame.draw.rect(self.screen, color, (x + size//2 - 1, y + size//2, 2, size//2))
    
    def _draw_shield(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine un bouclier simple"""
        points = [
            (x, y + size//4),
            (x + size//4, y),
            (x + 3*size//4, y),
            (x + size, y + size//4),
            (x + size, y + 3*size//4),
            (x + 3*size//4, y + size),
            (x + size//4, y + size),
            (x, y + 3*size//4)
        ]
        pygame.draw.polygon(self.screen, color, points)
    
    def _draw_skull(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine un crâne simple"""
        # Tête
        pygame.draw.circle(self.screen, color, (x + size//2, y + size//2), size//3)
        # Yeux
        pygame.draw.circle(self.screen, BLACK, (x + size//2 - 3, y + size//2 - 2), 2)
        pygame.draw.circle(self.screen, BLACK, (x + size//2 + 3, y + size//2 - 2), 2)
    
    def _draw_crown(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine une couronne simple"""
        points = [
            (x, y + size//2),
            (x + size//4, y),
            (x + size//2, y + size//4),
            (x + 3*size//4, y),
            (x + size, y + size//2)
        ]
        pygame.draw.polygon(self.screen, color, points)
    
    def _draw_plus(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine un plus simple"""
        center_x, center_y = x + size//2, y + size//2
        thickness = 2
        # Horizontal
        pygame.draw.rect(self.screen, color, (x, center_y - thickness//2, size, thickness))
        # Vertical
        pygame.draw.rect(self.screen, color, (center_x - thickness//2, y, thickness, size))
    
    def _draw_castle(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        """Dessine un château simple"""
        # Base
        pygame.draw.rect(self.screen, color, (x, y + size//2, size, size//2))
        # Tours
        pygame.draw.rect(self.screen, color, (x, y, size//4, size//2))
        pygame.draw.rect(self.screen, color, (x + 3*size//4, y, size//4, size//2))
        # Tour centrale
        pygame.draw.rect(self.screen, color, (x + size//3, y + size//4, size//3, 3*size//4))
    
    def add_particle(self, x: int, y: int, color: Tuple[int, int, int], 
                    velocity: Tuple[float, float], life: int = 30) -> None:
        """Ajoute une particule simple"""
        self.particles.append({
            'x': x, 'y': y, 'color': color, 
            'vx': velocity[0], 'vy': velocity[1], 'life': life
        })
    
    def update_particles(self) -> None:
        """Met à jour les particules"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self) -> None:
        """Dessine les particules"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 30))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(self.screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 2)
    
    def clear_cache(self) -> None:
        """Vide le cache"""
        self.cache.clear()
