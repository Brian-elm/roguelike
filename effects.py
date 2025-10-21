#!/usr/bin/env python3
"""
Module d'effets visuels et d'animations pour rendre le jeu plus fun
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from config import *

class Particle:
    """Particule pour les effets visuels"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 velocity: Tuple[float, float], life: int = 60, size: int = 3):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 0.1
        self.fade = True
    
    def update(self) -> bool:
        """Met à jour la particule"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        
        # Friction
        self.vx *= 0.98
        self.vy *= 0.98
        
        return self.life > 0
    
    def draw(self, screen: pygame.Surface):
        """Dessine la particule"""
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life)) if self.fade else 255
            color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class EffectManager:
    """Gestionnaire d'effets visuels"""
    
    def __init__(self):
        self.particles: List[Particle] = []
        self.screen_shake = 0
        self.flash_effect = 0
        self.rain_particles = []
        self.snow_particles = []
        self.weather = "clear"  # clear, rain, snow, storm
    
    def add_explosion(self, x: int, y: int, color: Tuple[int, int, int] = RED, count: int = 20):
        """Ajoute un effet d'explosion"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, color, (vx, vy), random.randint(30, 60), random.randint(2, 5))
            self.particles.append(particle)
    
    def add_heal_effect(self, x: int, y: int):
        """Ajoute un effet de soin"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2  # Remonte
            particle = Particle(x, y, GREEN, (vx, vy), random.randint(40, 80), 2)
            self.particles.append(particle)
    
    def add_damage_effect(self, x: int, y: int):
        """Ajoute un effet de dégâts"""
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, RED, (vx, vy), random.randint(20, 40), 2)
            self.particles.append(particle)
    
    def add_magic_effect(self, x: int, y: int):
        """Ajoute un effet magique"""
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([PURPLE, BLUE, YELLOW])
            particle = Particle(x, y, color, (vx, vy), random.randint(50, 100), 3)
            self.particles.append(particle)
    
    def add_screen_shake(self, intensity: int = 10):
        """Ajoute un effet de tremblement d'écran"""
        self.screen_shake = intensity
    
    def add_flash(self, color: Tuple[int, int, int] = WHITE, duration: int = 10):
        """Ajoute un effet de flash"""
        self.flash_effect = duration
        self.flash_color = color
    
    def set_weather(self, weather_type: str):
        """Définit le type de météo"""
        self.weather = weather_type
        if weather_type == "rain":
            self._init_rain()
        elif weather_type == "snow":
            self._init_snow()
    
    def _init_rain(self):
        """Initialise la pluie"""
        self.rain_particles = []
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-100, 0)
            self.rain_particles.append([x, y, random.uniform(2, 5)])
    
    def _init_snow(self):
        """Initialise la neige"""
        self.snow_particles = []
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-50, 0)
            self.snow_particles.append([x, y, random.uniform(0.5, 2), random.uniform(0.1, 0.3)])
    
    def update(self):
        """Met à jour tous les effets"""
        # Particules
        self.particles = [p for p in self.particles if p.update()]
        
        # Tremblement d'écran
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Flash
        if self.flash_effect > 0:
            self.flash_effect -= 1
        
        # Météo
        if self.weather == "rain":
            self._update_rain()
        elif self.weather == "snow":
            self._update_snow()
    
    def _update_rain(self):
        """Met à jour la pluie"""
        for drop in self.rain_particles:
            drop[1] += drop[2]  # Vitesse de chute
            if drop[1] > SCREEN_HEIGHT:
                drop[1] = random.randint(-100, 0)
                drop[0] = random.randint(0, SCREEN_WIDTH)
    
    def _update_snow(self):
        """Met à jour la neige"""
        for flake in self.snow_particles:
            flake[1] += flake[2]  # Vitesse de chute
            flake[0] += math.sin(flake[1] * 0.01) * 0.5  # Mouvement latéral
            if flake[1] > SCREEN_HEIGHT:
                flake[1] = random.randint(-50, 0)
                flake[0] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen: pygame.Surface):
        """Dessine tous les effets"""
        # Météo
        if self.weather == "rain":
            for drop in self.rain_particles:
                pygame.draw.line(screen, BLUE, (drop[0], drop[1]), (drop[0], drop[1] + 10), 1)
        elif self.weather == "snow":
            for flake in self.snow_particles:
                pygame.draw.circle(screen, WHITE, (int(flake[0]), int(flake[1])), 2)
        
        # Particules
        for particle in self.particles:
            particle.draw(screen)
        
        # Flash
        if self.flash_effect > 0:
            alpha = int(255 * (self.flash_effect / 10))
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(alpha)
            flash_surface.fill(self.flash_color)
            screen.blit(flash_surface, (0, 0))
    
    def get_screen_offset(self) -> Tuple[int, int]:
        """Retourne l'offset pour le tremblement d'écran"""
        if self.screen_shake > 0:
            return (random.randint(-self.screen_shake, self.screen_shake),
                    random.randint(-self.screen_shake, self.screen_shake))
        return (0, 0)

class ComboSystem:
    """Système de combos et critiques"""
    
    def __init__(self):
        self.combo_count = 0
        self.last_hit_time = 0
        self.combo_timeout = 2000  # 2 secondes
        self.critical_chance = 0.1  # 10% de chance de critique
    
    def hit(self, current_time: int) -> dict:
        """Enregistre un coup et retourne les informations"""
        # Vérifier si c'est un combo
        if current_time - self.last_hit_time < self.combo_timeout:
            self.combo_count += 1
            is_combo = True
        else:
            self.combo_count = 1
            is_combo = False
        
        self.last_hit_time = current_time
        
        result = {
            'is_critical': False,
            'is_combo': is_combo,
            'combo_count': self.combo_count,
            'damage_multiplier': 1.0
        }
        
        # Vérifier si c'est un critique
        if random.random() < self.critical_chance + (self.combo_count * 0.05):
            result['is_critical'] = True
            result['damage_multiplier'] = 2.0 + (self.combo_count * 0.2)
        
        # Bonus de combo
        if self.combo_count > 1:
            result['damage_multiplier'] += (self.combo_count - 1) * 0.1
        
        return result
    
    def reset(self):
        """Remet à zéro le combo"""
        self.combo_count = 0

class ReputationSystem:
    """Système de réputation et titres"""
    
    def __init__(self):
        self.reputation = 0
        self.titles = [
            "Novice", "Aventurier", "Guerrier", "Héros", "Légende",
            "Tueur de Dragons", "Maître du Donjon", "Roi des Combats"
        ]
        self.current_title_index = 0
        self.achievements = []
    
    def add_reputation(self, amount: int, reason: str = ""):
        """Ajoute de la réputation"""
        self.reputation += amount
        if reason:
            self.achievements.append(f"+{amount} réputation: {reason}")
        
        # Vérifier si on peut obtenir un nouveau titre
        new_title_index = min(self.reputation // 100, len(self.titles) - 1)
        if new_title_index > self.current_title_index:
            self.current_title_index = new_title_index
            return f"Nouveau titre: {self.titles[new_title_index]}!"
        return None
    
    def get_current_title(self) -> str:
        """Retourne le titre actuel"""
        return self.titles[self.current_title_index]
    
    def get_reputation_level(self) -> str:
        """Retourne le niveau de réputation"""
        if self.reputation < 50:
            return "Inconnu"
        elif self.reputation < 150:
            return "Reconnu"
        elif self.reputation < 300:
            return "Célèbre"
        elif self.reputation < 500:
            return "Légendaire"
        else:
            return "Mythique"

class MiniGame:
    """Mini-jeu simple pour les salles spéciales"""
    
    def __init__(self, game_type: str = "timing"):
        self.game_type = game_type
        self.active = False
        self.success = False
        self.timer = 0
        self.target_time = 0
        self.precision = 0
    
    def start_timing_game(self, target_time: int = 60):
        """Démarre un mini-jeu de timing"""
        self.game_type = "timing"
        self.active = True
        self.success = False
        self.timer = 0
        self.target_time = target_time
        self.precision = 0
    
    def update_timing_game(self, dt: int) -> bool:
        """Met à jour le mini-jeu de timing"""
        if not self.active:
            return False
        
        self.timer += dt
        
        # Vérifier si le joueur a cliqué au bon moment
        if self.timer >= self.target_time - 10 and self.timer <= self.target_time + 10:
            self.success = True
            self.precision = 100 - abs(self.timer - self.target_time) * 5
            self.active = False
            return True
        elif self.timer > self.target_time + 20:
            self.success = False
            self.active = False
            return True
        
        return False
    
    def draw_timing_game(self, screen: pygame.Surface, renderer):
        """Dessine le mini-jeu de timing"""
        if not self.active:
            return
        
        # Barre de progression
        progress = min(self.timer / self.target_time, 1.0)
        bar_width = 400
        bar_height = 20
        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = SCREEN_HEIGHT // 2 - bar_height // 2
        
        # Fond
        pygame.draw.rect(screen, DARK_GRAY, (x, y, bar_width, bar_height))
        
        # Progression
        pygame.draw.rect(screen, GREEN, (x, y, bar_width * progress, bar_height))
        
        # Zone cible
        target_x = x + bar_width * 0.8
        pygame.draw.rect(screen, YELLOW, (target_x, y, 20, bar_height))
        
        # Instructions
        renderer.draw_text("Cliquez quand la barre atteint la zone jaune!", 
                          SCREEN_WIDTH // 2, y - 50, 'medium', WHITE, center=True)
        renderer.draw_text(f"Temps: {self.timer}ms", 
                          SCREEN_WIDTH // 2, y + bar_height + 20, 'small', WHITE, center=True)
