#!/usr/bin/env python3
"""
Version graphique avancée du jeu roguelike avec des sprites détaillés et des animations
"""

import pygame
import random
import sys
import math
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod

# Initialisation de Pygame
pygame.init()

# Constantes de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
BROWN = (139, 69, 19)
DARK_BLUE = (0, 0, 139)
DARK_RED = (139, 0, 0)

# Configuration du jeu
JOUEUR_PV_MAX = 100
JOUEUR_ATTAQUE = 20
ENNEMI_PV_MAX = 30
ENNEMI_ATTAQUE = 15
BOSS_PV_MAX = 80
BOSS_ATTAQUE = 25
NOMBRE_SALLES = 5
POURCENTAGE_SOIN = 0.15
BONUS_ATTAQUE_MIN = 3
BONUS_ATTAQUE_MAX = 8

# Probabilités des types de salles (plus équilibrées)
PROBABILITES_SALLES = {
    'ennemi': 0.6,      # 60% de chance d'avoir un ennemi
    'boss': 0.2,        # 20% de chance d'avoir un boss
    'soin': 0.1,        # 10% de chance d'avoir du soin
    'amelioration': 0.1  # 10% de chance d'avoir une amélioration
}

# Noms des personnages
NOMS_ENNEMIS = ["Gobelin", "Orc", "Squelette", "Loup", "Araignée"]
NOMS_BOSS = ["Dragon", "Liche", "Démon", "Géant", "Hydre"]

class Personnage:
    """Classe de base pour tous les personnages (joueur, ennemis, boss)"""
    
    def __init__(self, nom: str, pv_max: int, attaque: int):
        self.nom = nom
        self.pv_max = pv_max
        self.pv_actuels = pv_max
        self.attaque = attaque
    
    def attaquer(self, cible: 'Personnage') -> int:
        """Attaque une cible et retourne les dégâts infligés"""
        degats = self.attaque
        cible.pv_actuels -= degats
        if cible.pv_actuels < 0:
            cible.pv_actuels = 0
        return degats
    
    def est_vivant(self) -> bool:
        """Vérifie si le personnage est vivant"""
        return self.pv_actuels > 0
    
    def soigner(self, points: int):
        """Soigne le personnage"""
        self.pv_actuels += points
        if self.pv_actuels > self.pv_max:
            self.pv_actuels = self.pv_max
    
    def __str__(self):
        return f"{self.nom} - PV: {self.pv_actuels}/{self.pv_max} - Attaque: {self.attaque}"

class Joueur(Personnage):
    """Classe représentant le joueur"""
    
    def __init__(self, nom: str = "Héros"):
        super().__init__(nom, JOUEUR_PV_MAX, JOUEUR_ATTAQUE)
        self.ennemis_tues = 0
        self.boss_vaincus = 0
    
    def augmenter_attaque(self, bonus: int):
        """Augmente l'attaque du joueur"""
        self.attaque += bonus
        print(f"Votre attaque augmente de {bonus}! Nouvelle attaque: {self.attaque}")

class Ennemi(Personnage):
    """Classe représentant un ennemi normal"""
    
    def __init__(self):
        nom = random.choice(NOMS_ENNEMIS)
        super().__init__(nom, ENNEMI_PV_MAX, ENNEMI_ATTAQUE)

class Boss(Personnage):
    """Classe représentant un boss (ennemi puissant)"""
    
    def __init__(self):
        nom = random.choice(NOMS_BOSS)
        super().__init__(nom, BOSS_PV_MAX, BOSS_ATTAQUE)

class Salle(ABC):
    """Classe abstraite pour tous les types de salles"""
    
    def __init__(self, nom: str):
        self.nom = nom
    
    @abstractmethod
    def entrer(self, joueur: Joueur) -> bool:
        """
        Le joueur entre dans la salle
        Retourne True si le joueur peut continuer, False si la partie se termine
        """
        pass

class SalleEnnemi(Salle):
    """Salle contenant un ennemi normal"""
    
    def __init__(self):
        super().__init__("Salle d'Ennemi")
        self.ennemi = Ennemi()
    
    def entrer(self, joueur: Joueur) -> bool:
        print(f"\n=== {self.nom} ===")
        print(f"Un {self.ennemi.nom} apparaît!")
        
        while joueur.est_vivant() and self.ennemi.est_vivant():
            # Le joueur attaque en premier
            degats = joueur.attaquer(self.ennemi)
            print(f"Vous attaquez le {self.ennemi.nom} pour {degats} dégâts!")
            print(f"{self.ennemi}")
            
            if not self.ennemi.est_vivant():
                print(f"Vous avez vaincu le {self.ennemi.nom}!")
                joueur.ennemis_tues += 1
                return True
            
            # L'ennemi attaque
            degats = self.ennemi.attaquer(joueur)
            print(f"Le {self.ennemi.nom} vous attaque pour {degats} dégâts!")
            print(f"{joueur}")
            
            if not joueur.est_vivant():
                print("Vous êtes mort! Game Over!")
                return False
        
        return True

class SalleBoss(Salle):
    """Salle contenant un boss"""
    
    def __init__(self):
        super().__init__("Salle de Boss")
        self.boss = Boss()
    
    def entrer(self, joueur: Joueur) -> bool:
        print(f"\n=== {self.nom} ===")
        print(f"Un {self.boss.nom} redoutable apparaît!")
        
        while joueur.est_vivant() and self.boss.est_vivant():
            # Le joueur attaque en premier
            degats = joueur.attaquer(self.boss)
            print(f"Vous attaquez le {self.boss.nom} pour {degats} dégâts!")
            print(f"{self.boss}")
            
            if not self.boss.est_vivant():
                print(f"Vous avez vaincu le {self.boss.nom}!")
                joueur.boss_vaincus += 1
                return True
            
            # Le boss attaque
            degats = self.boss.attaquer(joueur)
            print(f"Le {self.boss.nom} vous attaque pour {degats} dégâts!")
            print(f"{joueur}")
            
            if not joueur.est_vivant():
                print("Vous êtes mort! Game Over!")
                return False
        
        return True

class SalleSoin(Salle):
    """Salle de récupération de PV"""
    
    def __init__(self):
        super().__init__("Salle de Soin")
    
    def entrer(self, joueur: Joueur) -> bool:
        print(f"\n=== {self.nom} ===")
        soin = int(joueur.pv_max * POURCENTAGE_SOIN)
        joueur.soigner(soin)
        print(f"Vous vous reposez et récupérez {soin} PV!")
        print(f"{joueur}")
        return True

class SalleAmelioration(Salle):
    """Salle d'amélioration de l'attaque"""
    
    def __init__(self):
        super().__init__("Salle d'Amélioration")
    
    def entrer(self, joueur: Joueur) -> bool:
        print(f"\n=== {self.nom} ===")
        bonus = random.randint(BONUS_ATTAQUE_MIN, BONUS_ATTAQUE_MAX)
        joueur.augmenter_attaque(bonus)
        return True

class GenerateurSalles:
    """Générateur de salles aléatoires basé sur les probabilités"""
    
    def __init__(self):
        self.derniere_salle_speciale = False
    
    def generer_salle(self) -> Salle:
        """Génère une salle aléatoire selon les probabilités définies"""
        rand = random.random()
        cumul = 0
        
        # Si la dernière salle était spéciale, forcer un ennemi ou boss
        if self.derniere_salle_speciale:
            if rand < 0.7:  # 70% de chance d'ennemi
                self.derniere_salle_speciale = False
                return SalleEnnemi()
            else:  # 30% de chance de boss
                self.derniere_salle_speciale = False
                return SalleBoss()
        
        # Probabilités normales
        for type_salle, proba in PROBABILITES_SALLES.items():
            cumul += proba
            if rand <= cumul:
                if type_salle == 'ennemi':
                    self.derniere_salle_speciale = False
                    return SalleEnnemi()
                elif type_salle == 'boss':
                    self.derniere_salle_speciale = False
                    return SalleBoss()
                elif type_salle == 'soin':
                    self.derniere_salle_speciale = True
                    return SalleSoin()
                elif type_salle == 'amelioration':
                    self.derniere_salle_speciale = True
                    return SalleAmelioration()
        
        # Par défaut, retourner une salle d'ennemi
        self.derniere_salle_speciale = False
        return SalleEnnemi()

class Jeu:
    """Classe principale du jeu"""
    
    def __init__(self):
        self.joueur = Joueur()
        self.salle_actuelle = 0
        self.salles_max = NOMBRE_SALLES
        self.generateur_salles = GenerateurSalles()
    
    def afficher_statistiques(self):
        """Affiche les statistiques de fin de partie"""
        print("\n" + "="*50)
        print("STATISTIQUES DE FIN DE PARTIE")
        print("="*50)
        print(f"Ennemis tués: {self.joueur.ennemis_tues}")
        print(f"Boss vaincus: {self.joueur.boss_vaincus}")
        print(f"Salles traversées: {self.salle_actuelle}")
        print("="*50)

class AnimatedSprite:
    """Sprite animé pour les personnages"""
    
    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.visible = True
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 500  # 500ms
    
    def start_attack(self):
        """Démarre l'animation d'attaque"""
        self.is_attacking = True
        self.attack_timer = 0
    
    def update(self, dt: int):
        """Met à jour l'animation"""
        self.animation_frame += self.animation_speed * dt
        
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
    
    def draw(self, screen: pygame.Surface):
        """Dessine le sprite avec animation"""
        if not self.visible:
            return
        
        # Couleur de base
        color = self.color
        
        # Effet d'attaque (clignotement rouge)
        if self.is_attacking:
            flash = int(50 * math.sin(self.attack_timer * 0.02))
            color = (min(255, max(0, color[0] + flash)), 
                    min(255, max(0, color[1] - flash)), 
                    min(255, max(0, color[2] - flash)))
        
        # Dessiner le personnage avec des détails
        pygame.draw.rect(screen, color, self.rect)
        
        # Ajouter des détails selon le type
        if self.color == BLUE:  # Joueur
            # Casque
            helmet_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 5, 
                                    self.rect.width - 20, 15)
            pygame.draw.rect(screen, DARK_BLUE, helmet_rect)
            # Épée
            sword_rect = pygame.Rect(self.rect.right - 5, self.rect.y + 20, 8, 30)
            pygame.draw.rect(screen, GRAY, sword_rect)
        elif self.color == RED:  # Ennemi
            # Yeux rouges
            eye1 = pygame.Rect(self.rect.x + 15, self.rect.y + 15, 8, 8)
            eye2 = pygame.Rect(self.rect.right - 23, self.rect.y + 15, 8, 8)
            pygame.draw.rect(screen, DARK_RED, eye1)
            pygame.draw.rect(screen, DARK_RED, eye2)
            # Griffes
            claw1 = pygame.Rect(self.rect.x - 5, self.rect.y + 30, 10, 5)
            claw2 = pygame.Rect(self.rect.right - 5, self.rect.y + 30, 10, 5)
            pygame.draw.rect(screen, DARK_RED, claw1)
            pygame.draw.rect(screen, DARK_RED, claw2)
        elif self.color == PURPLE:  # Boss
            # Couronne
            crown_rect = pygame.Rect(self.rect.x + 5, self.rect.y - 10, 
                                   self.rect.width - 10, 15)
            pygame.draw.rect(screen, YELLOW, crown_rect)
            # Ailes
            wing1 = pygame.Rect(self.rect.x - 20, self.rect.y + 20, 20, 40)
            wing2 = pygame.Rect(self.rect.right, self.rect.y + 20, 20, 40)
            pygame.draw.rect(screen, DARK_GRAY, wing1)
            pygame.draw.rect(screen, DARK_GRAY, wing2)
        
        # Bordure
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Effet de particules pour l'attaque
        if self.is_attacking:
            for i in range(5):
                particle_x = self.rect.centerx + random.randint(-20, 20)
                particle_y = self.rect.centery + random.randint(-20, 20)
                particle_rect = pygame.Rect(particle_x, particle_y, 3, 3)
                pygame.draw.rect(screen, YELLOW, particle_rect)

class ParticleSystem:
    """Système de particules pour les effets visuels"""
    
    def __init__(self):
        self.particles: List[dict] = []
    
    def add_particle(self, x: int, y: int, color: Tuple[int, int, int], 
                    velocity: Tuple[float, float], lifetime: int):
        """Ajoute une particule"""
        self.particles.append({
            'x': x, 'y': y,
            'vx': velocity[0], 'vy': velocity[1],
            'color': color,
            'lifetime': lifetime,
            'max_lifetime': lifetime
        })
    
    def update(self, dt: int):
        """Met à jour toutes les particules"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt * 0.1
            particle['y'] += particle['vy'] * dt * 0.1
            particle['lifetime'] -= dt
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Dessine toutes les particules"""
        for particle in self.particles:
            alpha = particle['lifetime'] / particle['max_lifetime']
            size = int(3 * alpha)
            if size > 0:
                rect = pygame.Rect(particle['x'], particle['y'], size, size)
                pygame.draw.rect(screen, particle['color'], rect)

class TextSprite:
    """Sprite pour afficher du texte avec des effets"""
    
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, 
                 color: Tuple[int, int, int] = WHITE, shadow: bool = True):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.shadow = shadow
        self.visible = True
        self.animation_offset = 0
    
    def draw(self, screen: pygame.Surface):
        """Dessine le texte avec ombre"""
        if not self.visible:
            return
        
        text_surface = self.font.render(self.text, True, self.color)
        
        # Ombre
        if self.shadow:
            shadow_surface = self.font.render(self.text, True, BLACK)
            screen.blit(shadow_surface, (self.x + 2, self.y + 2))
        
        # Texte principal
        screen.blit(text_surface, (self.x, self.y))

class Button:
    """Bouton amélioré avec animations"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font: pygame.font.Font, color: Tuple[int, int, int] = GRAY,
                 text_color: Tuple[int, int, int] = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = LIGHT_GRAY
        self.is_hovered = False
        self.visible = True
        self.scale = 1.0
        self.target_scale = 1.0
    
    def draw(self, screen: pygame.Surface):
        """Dessine le bouton avec animation"""
        if not self.visible:
            return
        
        # Animation de scale
        if self.is_hovered:
            self.target_scale = 1.1
        else:
            self.target_scale = 1.0
        
        self.scale += (self.target_scale - self.scale) * 0.1
        
        # Calculer la nouvelle taille
        new_width = int(self.rect.width * self.scale)
        new_height = int(self.rect.height * self.scale)
        new_x = self.rect.x - (new_width - self.rect.width) // 2
        new_y = self.rect.y - (new_height - self.rect.height) // 2
        
        scaled_rect = pygame.Rect(new_x, new_y, new_width, new_height)
        
        # Couleur du bouton
        color = self.hover_color if self.is_hovered else self.color
        
        # Dessiner le bouton avec gradient
        pygame.draw.rect(screen, color, scaled_rect)
        pygame.draw.rect(screen, WHITE, scaled_rect, 2)
        
        # Centrer le texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère les événements du bouton"""
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class HealthBar:
    """Barre de vie améliorée avec animation"""
    
    def __init__(self, x: int, y: int, width: int, height: int, max_health: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.current_health = max_health
        self.target_health = max_health
        self.visible = True
    
    def update_health(self, current_health: int):
        """Met à jour la santé cible"""
        self.target_health = max(0, min(current_health, self.max_health))
    
    def update(self, dt: int):
        """Met à jour l'animation de la barre de vie"""
        diff = self.target_health - self.current_health
        if abs(diff) > 0.1:
            self.current_health += diff * 0.05 * dt * 0.1
    
    def draw(self, screen: pygame.Surface):
        """Dessine la barre de vie avec animation"""
        if not self.visible:
            return
        
        # Fond de la barre
        pygame.draw.rect(screen, DARK_RED, self.rect)
        
        # Barre de vie actuelle
        health_width = int((self.current_health / self.max_health) * self.rect.width)
        if health_width > 0:
            health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
            # Gradient de couleur
            color = GREEN if self.current_health > self.max_health * 0.5 else YELLOW
            if self.current_health <= self.max_health * 0.25:
                color = RED
            pygame.draw.rect(screen, color, health_rect)
        
        # Bordure
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Texte de santé avec symbole
        font = pygame.font.Font(None, 20)
        health_text = f"HP {int(self.current_health)}/{self.max_health}"
        text_surface = font.render(health_text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class IconDrawer:
    """Classe pour dessiner des icônes visuelles avec des formes géométriques"""
    
    @staticmethod
    def draw_heart(screen, x, y, size, color):
        """Dessine un cœur"""
        # Cœur simplifié avec des cercles et un triangle
        pygame.draw.circle(screen, color, (x - size//4, y - size//4), size//4)
        pygame.draw.circle(screen, color, (x + size//4, y - size//4), size//4)
        points = [(x, y + size//2), (x - size//2, y), (x + size//2, y)]
        pygame.draw.polygon(screen, color, points)
    
    @staticmethod
    def draw_sword(screen, x, y, size, color):
        """Dessine une épée"""
        # Lame
        pygame.draw.rect(screen, color, (x - size//8, y - size//2, size//4, size))
        # Garde
        pygame.draw.rect(screen, color, (x - size//3, y - size//8, size*2//3, size//4))
        # Pommeau
        pygame.draw.circle(screen, color, (x, y + size//2 + size//8), size//6)
    
    @staticmethod
    def draw_shield(screen, x, y, size, color):
        """Dessine un bouclier"""
        points = [(x, y - size//2), (x - size//2, y - size//4), (x - size//2, y + size//4), 
                 (x, y + size//2), (x + size//2, y + size//4), (x + size//2, y - size//4)]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
    
    @staticmethod
    def draw_crown(screen, x, y, size, color):
        """Dessine une couronne"""
        # Base de la couronne
        pygame.draw.rect(screen, color, (x - size//2, y, size, size//3))
        # Pointes
        for i in range(3):
            px = x - size//3 + i * size//3
            points = [(px, y), (px - size//6, y - size//3), (px + size//6, y - size//3)]
            pygame.draw.polygon(screen, color, points)
    
    @staticmethod
    def draw_skull(screen, x, y, size, color):
        """Dessine un crâne"""
        # Tête
        pygame.draw.circle(screen, color, (x, y), size//2)
        # Yeux
        pygame.draw.circle(screen, WHITE, (x - size//6, y - size//6), size//8)
        pygame.draw.circle(screen, WHITE, (x + size//6, y - size//6), size//8)
        # Bouche
        pygame.draw.rect(screen, WHITE, (x - size//4, y + size//6, size//2, size//8))
    
    @staticmethod
    def draw_plus(screen, x, y, size, color):
        """Dessine un plus"""
        pygame.draw.rect(screen, color, (x - size//8, y - size//2, size//4, size))
        pygame.draw.rect(screen, color, (x - size//2, y - size//8, size, size//4))
    
    @staticmethod
    def draw_exclamation(screen, x, y, size, color):
        """Dessine un point d'exclamation"""
        pygame.draw.rect(screen, color, (x - size//8, y - size//2, size//4, size*3//4))
        pygame.draw.circle(screen, color, (x, y + size//3), size//8)
    
    @staticmethod
    def draw_castle(screen, x, y, size, color):
        """Dessine un château"""
        # Base
        pygame.draw.rect(screen, color, (x - size//2, y, size, size//2))
        # Tours
        pygame.draw.rect(screen, color, (x - size//2, y - size//2, size//3, size//2))
        pygame.draw.rect(screen, color, (x - size//6, y - size//2, size//3, size//2))
        pygame.draw.rect(screen, color, (x + size//6, y - size//2, size//3, size//2))
    
    @staticmethod
    def draw_trophy(screen, x, y, size, color):
        """Dessine un trophée"""
        # Base
        pygame.draw.rect(screen, color, (x - size//4, y + size//4, size//2, size//4))
        # Coupe
        pygame.draw.ellipse(screen, color, (x - size//3, y - size//4, size*2//3, size//2))
        # Anses
        pygame.draw.arc(screen, color, (x - size//2, y - size//4, size//2, size//2), 0, 3.14, 3)
        pygame.draw.arc(screen, color, (x, y - size//4, size//2, size//2), 0, 3.14, 3)

class IconTextSprite:
    """Sprite qui combine une icône visuelle et du texte"""
    
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, 
                 icon_type: str, color: Tuple[int, int, int] = WHITE, shadow: bool = True):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.icon_type = icon_type
        self.color = color
        self.shadow = shadow
        self.visible = True
        self.icon_size = 20
    
    def draw(self, screen: pygame.Surface):
        """Dessine l'icône et le texte"""
        if not self.visible:
            return
        
        # Dessiner l'icône
        icon_x = self.x
        icon_y = self.y + 10  # Centrer verticalement avec le texte
        
        if self.icon_type == "heart":
            IconDrawer.draw_heart(screen, icon_x, icon_y, self.icon_size, RED)
        elif self.icon_type == "sword":
            IconDrawer.draw_sword(screen, icon_x, icon_y, self.icon_size, GRAY)
        elif self.icon_type == "shield":
            IconDrawer.draw_shield(screen, icon_x, icon_y, self.icon_size, BLUE)
        elif self.icon_type == "crown":
            IconDrawer.draw_crown(screen, icon_x, icon_y, self.icon_size, YELLOW)
        elif self.icon_type == "skull":
            IconDrawer.draw_skull(screen, icon_x, icon_y, self.icon_size, WHITE)
        elif self.icon_type == "plus":
            IconDrawer.draw_plus(screen, icon_x, icon_y, self.icon_size, GREEN)
        elif self.icon_type == "exclamation":
            IconDrawer.draw_exclamation(screen, icon_x, icon_y, self.icon_size, YELLOW)
        elif self.icon_type == "castle":
            IconDrawer.draw_castle(screen, icon_x, icon_y, self.icon_size, GRAY)
        elif self.icon_type == "trophy":
            IconDrawer.draw_trophy(screen, icon_x, icon_y, self.icon_size, YELLOW)
        
        # Dessiner le texte à côté de l'icône
        text_x = self.x + 30  # Espacement après l'icône
        text_surface = self.font.render(self.text, True, self.color)
        
        # Ombre
        if self.shadow:
            shadow_surface = self.font.render(self.text, True, BLACK)
            screen.blit(shadow_surface, (text_x + 2, self.y + 2))
        
        # Texte principal
        screen.blit(text_surface, (text_x, self.y))

class GameState:
    """États du jeu"""
    MENU = "menu"
    PLAYING = "playing"
    COMBAT = "combat"
    TRANSITION = "transition"
    SALLE_SPECIALE = "salle_speciale"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class RoguelikeGraphiqueAvance:
    """Classe principale du jeu graphique avancé"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Roguelike Graphique Avancé")
        self.clock = pygame.time.Clock()
        
        # Polices
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # État du jeu
        self.state = GameState.MENU
        self.jeu = Jeu()
        self.salle_actuelle = None
        
        # Sprites
        self.sprites: List[AnimatedSprite] = []
        self.text_sprites: List[TextSprite] = []
        self.buttons: List[Button] = []
        
        # Interface de combat
        self.player_sprite = None
        self.enemy_sprite = None
        self.player_health_bar = None
        self.enemy_health_bar = None
        self.combat_log: List[str] = []
        
        # Système de particules
        self.particles = ParticleSystem()
        
        # Animation
        self.animation_timer = 0
        self.last_time = pygame.time.get_ticks()
        
        self.setup_menu()
    
    def setup_menu(self):
        """Configure le menu principal avec un design amélioré"""
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        
        # Titre avec effet
        title = TextSprite(SCREEN_WIDTH // 2 - 300, 100, "ROGUELIKE GRAPHIQUE", 
                          self.font_large, YELLOW)
        self.text_sprites.append(title)
        
        # Icônes du titre
        castle1 = IconTextSprite(SCREEN_WIDTH // 2 - 350, 100, "", self.font_large, "castle", YELLOW)
        castle2 = IconTextSprite(SCREEN_WIDTH // 2 + 250, 100, "", self.font_large, "castle", YELLOW)
        self.text_sprites.append(castle1)
        self.text_sprites.append(castle2)
        
        # Sous-titre
        subtitle = TextSprite(SCREEN_WIDTH // 2 - 200, 180, "Aventure Epique dans le Donjon", 
                             self.font_medium, WHITE)
        self.text_sprites.append(subtitle)
        
        # Icônes du sous-titre
        sword1 = IconTextSprite(SCREEN_WIDTH // 2 - 250, 180, "", self.font_medium, "sword", WHITE)
        sword2 = IconTextSprite(SCREEN_WIDTH // 2 + 200, 180, "", self.font_medium, "sword", WHITE)
        self.text_sprites.append(sword1)
        self.text_sprites.append(sword2)
        
        # Bouton Jouer
        play_button = Button(SCREEN_WIDTH // 2 - 120, 300, 240, 60, "COMMENCER L'AVENTURE", 
                            self.font_medium, GREEN)
        self.buttons.append(play_button)
        
        # Bouton Quitter
        quit_button = Button(SCREEN_WIDTH // 2 - 120, 400, 240, 60, "QUITTER", 
                            self.font_medium, RED)
        self.buttons.append(quit_button)
        
        # Instructions avec icônes
        instructions = [
            ("Utilisez la souris pour naviguer", "sword"),
            ("Cliquez sur ATTAQUER pour combattre", "sword"),
            ("Survivez a 5 salles pour gagner!", "trophy")
        ]
        
        for i, (instruction, icon_type) in enumerate(instructions):
            inst_text = IconTextSprite(SCREEN_WIDTH // 2 - 150, 500 + i * 30, 
                                      instruction, self.font_small, icon_type, LIGHT_GRAY)
            self.text_sprites.append(inst_text)
    
    def setup_combat(self, salle: Salle):
        """Configure l'interface de combat améliorée"""
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        self.combat_log.clear()
        
        # Titre de la salle
        if isinstance(salle, SalleEnnemi):
            salle_title = TextSprite(50, 50, f"=== {salle.nom} ===", 
                                    self.font_large, YELLOW)
            sword1 = IconTextSprite(20, 50, "", self.font_large, "sword", YELLOW)
            sword2 = IconTextSprite(400, 50, "", self.font_large, "sword", YELLOW)
            self.text_sprites.append(sword1)
            self.text_sprites.append(sword2)
        elif isinstance(salle, SalleBoss):
            salle_title = TextSprite(50, 50, f"=== {salle.nom} ===", 
                                    self.font_large, YELLOW)
            crown1 = IconTextSprite(20, 50, "", self.font_large, "crown", YELLOW)
            crown2 = IconTextSprite(400, 50, "", self.font_large, "crown", YELLOW)
            self.text_sprites.append(crown1)
            self.text_sprites.append(crown2)
        else:
            salle_title = TextSprite(50, 50, f"=== {salle.nom} ===", 
                                    self.font_large, YELLOW)
        self.text_sprites.append(salle_title)
        
        # Joueur
        self.player_sprite = AnimatedSprite(150, 250, 120, 120, BLUE)
        self.sprites.append(self.player_sprite)
        
        player_name = IconTextSprite(150, 390, "Heros", self.font_medium, "shield", WHITE)
        self.text_sprites.append(player_name)
        
        # Barre de vie du joueur
        self.player_health_bar = HealthBar(150, 420, 250, 25, self.jeu.joueur.pv_max)
        self.player_health_bar.update_health(self.jeu.joueur.pv_actuels)
        
        # Ennemi ou Boss
        if isinstance(salle, SalleEnnemi):
            self.enemy_sprite = AnimatedSprite(850, 250, 120, 120, RED)
            enemy_name = IconTextSprite(850, 390, f"{salle.ennemi.nom}", self.font_medium, "skull", WHITE)
            self.enemy_health_bar = HealthBar(850, 420, 250, 25, salle.ennemi.pv_max)
            self.enemy_health_bar.update_health(salle.ennemi.pv_actuels)
        elif isinstance(salle, SalleBoss):
            self.enemy_sprite = AnimatedSprite(850, 230, 140, 140, PURPLE)
            enemy_name = IconTextSprite(850, 390, f"{salle.boss.nom}", self.font_medium, "crown", WHITE)
            self.enemy_health_bar = HealthBar(850, 420, 250, 25, salle.boss.pv_max)
            self.enemy_health_bar.update_health(salle.boss.pv_actuels)
        
        self.sprites.append(self.enemy_sprite)
        self.text_sprites.append(enemy_name)
        
        # Bouton Attaquer
        attack_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 60, "ATTAQUER", 
                              self.font_medium, ORANGE)
        self.buttons.append(attack_button)
        
        # Zone de log de combat
        log_bg = pygame.Rect(50, 550, 500, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), log_bg)
        pygame.draw.rect(self.screen, WHITE, log_bg, 2)
        
        log_title = TextSprite(60, 560, "📜 Journal de Combat:", self.font_small, WHITE)
        self.text_sprites.append(log_title)
    
    def setup_salle_speciale(self, salle: Salle):
        """Configure l'interface pour les salles spéciales"""
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        
        # Réinitialiser les barres de vie
        self.player_health_bar = None
        self.enemy_health_bar = None
        
        # Titre de la salle
        if isinstance(salle, SalleSoin):
            salle_title = TextSprite(SCREEN_WIDTH // 2 - 250, 200, "=== Salle de Soin ===", 
                                    self.font_large, YELLOW)
            plus1 = IconTextSprite(SCREEN_WIDTH // 2 - 300, 200, "", self.font_large, "plus", YELLOW)
            plus2 = IconTextSprite(SCREEN_WIDTH // 2 + 200, 200, "", self.font_large, "plus", YELLOW)
            self.text_sprites.append(plus1)
            self.text_sprites.append(plus2)
        elif isinstance(salle, SalleAmelioration):
            salle_title = TextSprite(SCREEN_WIDTH // 2 - 250, 200, "=== Salle d'Amelioration ===", 
                                    self.font_large, YELLOW)
            exclamation1 = IconTextSprite(SCREEN_WIDTH // 2 - 300, 200, "", self.font_large, "exclamation", YELLOW)
            exclamation2 = IconTextSprite(SCREEN_WIDTH // 2 + 200, 200, "", self.font_large, "exclamation", YELLOW)
            self.text_sprites.append(exclamation1)
            self.text_sprites.append(exclamation2)
        else:
            salle_title = TextSprite(SCREEN_WIDTH // 2 - 250, 200, f"=== {salle.nom} ===", 
                                    self.font_large, YELLOW)
        self.text_sprites.append(salle_title)
        
        # Icône selon le type de salle
        if isinstance(salle, SalleSoin):
            icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "plus", GREEN)
            message = "Vous vous reposez et recuperez des forces!"
        elif isinstance(salle, SalleAmelioration):
            icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "exclamation", YELLOW)
            message = "Vous trouvez une amelioration d'arme!"
        
        self.text_sprites.append(icon)
        
        message_text = TextSprite(SCREEN_WIDTH // 2 - 200, 350, message, 
                                 self.font_medium, WHITE)
        self.text_sprites.append(message_text)
        
        # Bouton Continuer
        continue_button = Button(SCREEN_WIDTH // 2 - 120, 450, 240, 60, "[PLAY] CONTINUER L'AVENTURE", 
                                self.font_medium, GREEN)
        self.buttons.append(continue_button)
    
    def setup_transition(self, victoire: bool, nom_adversaire: str, est_boss: bool = False):
        """Configure l'écran de transition entre les salles"""
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        
        # Réinitialiser les barres de vie
        self.player_health_bar = None
        self.enemy_health_bar = None
        
        if victoire:
            # Écran de victoire
            title = TextSprite(SCREEN_WIDTH // 2 - 200, 200, "[VICTORY] VICTOIRE! [VICTORY]", 
                              self.font_large, GREEN)
            self.text_sprites.append(title)
            
            if est_boss:
                message = f"Vous avez vaincu le redoutable {nom_adversaire}!"
                icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "crown", YELLOW)
            else:
                message = f"Vous avez vaincu {nom_adversaire}!"
                icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "sword", BLUE)
            
            self.text_sprites.append(icon)
            
            # Statistiques du joueur
            stats_y = 400
            stats = [
                (f"PV: {self.jeu.joueur.pv_actuels}/{self.jeu.joueur.pv_max}", "heart"),
                (f"Attaque: {self.jeu.joueur.attaque}", "sword"),
                (f"Ennemis tues: {self.jeu.joueur.ennemis_tues}", "skull"),
                (f"Boss vaincus: {self.jeu.joueur.boss_vaincus}", "crown")
            ]
            
            for i, (stat, icon_type) in enumerate(stats):
                stat_text = IconTextSprite(SCREEN_WIDTH // 2 - 150, stats_y + i * 30, 
                                          stat, self.font_small, icon_type, WHITE)
                self.text_sprites.append(stat_text)
            
        else:
            # Écran de défaite
            title = TextSprite(SCREEN_WIDTH // 2 - 200, 200, "DEFAITE", 
                              self.font_large, RED)
            self.text_sprites.append(title)
            
            message = f"{nom_adversaire} vous a vaincu!"
            icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "skull", RED)
            self.text_sprites.append(icon)
        
        # Message principal
        message_text = TextSprite(SCREEN_WIDTH // 2 - 200, 350, message, 
                                 self.font_medium, WHITE)
        self.text_sprites.append(message_text)
        
        # Bouton Continuer
        if victoire:
            continue_button = Button(SCREEN_WIDTH // 2 - 120, 550, 240, 60, "[PLAY] CONTINUER L'AVENTURE", 
                                    self.font_medium, GREEN)
        else:
            continue_button = Button(SCREEN_WIDTH // 2 - 120, 450, 240, 60, "[HOME] RETOUR AU MENU", 
                                    self.font_medium, RED)
        self.buttons.append(continue_button)
    
    def add_combat_log(self, message: str):
        """Ajoute un message au log de combat"""
        self.combat_log.append(message)
        if len(self.combat_log) > 8:
            self.combat_log.pop(0)
    
    def draw_combat_log(self):
        """Dessine le log de combat"""
        for i, message in enumerate(self.combat_log):
            log_text = TextSprite(60, 590 + i * 20, f"• {message}", self.font_small, WHITE)
            log_text.draw(self.screen)
    
    def handle_combat(self, salle: Salle) -> bool:
        """Gère le combat avec animations"""
        if isinstance(salle, SalleEnnemi):
            ennemi = salle.ennemi
        elif isinstance(salle, SalleBoss):
            ennemi = salle.boss
        else:
            return True
        
        # Animation d'attaque du joueur
        self.player_sprite.start_attack()
        
        # Le joueur attaque
        degats = self.jeu.joueur.attaquer(ennemi)
        self.add_combat_log(f"[SWORD] Vous attaquez {ennemi.nom} pour {degats} degats!")
        
        # Effet de particules
        for i in range(10):
            self.particles.add_particle(
                self.enemy_sprite.rect.centerx, self.enemy_sprite.rect.centery,
                YELLOW, (random.uniform(-2, 2), random.uniform(-2, 2)), 1000
            )
        
        # Mettre à jour la barre de vie de l'ennemi
        self.enemy_health_bar.update_health(ennemi.pv_actuels)
        
        if not ennemi.est_vivant():
            if isinstance(salle, SalleEnnemi):
                self.jeu.joueur.ennemis_tues += 1
                self.add_combat_log(f"[SKULL] Vous avez vaincu {ennemi.nom}!")
            else:
                self.jeu.joueur.boss_vaincus += 1
                self.add_combat_log(f"[BOSS] Vous avez vaincu le boss {ennemi.nom}!")
            return True
        
        # Animation d'attaque de l'ennemi
        self.enemy_sprite.start_attack()
        
        # L'ennemi attaque
        degats = ennemi.attaquer(self.jeu.joueur)
        self.add_combat_log(f"[HIT] {ennemi.nom} vous attaque pour {degats} degats!")
        
        # Effet de particules
        for i in range(8):
            self.particles.add_particle(
                self.player_sprite.rect.centerx, self.player_sprite.rect.centery,
                RED, (random.uniform(-2, 2), random.uniform(-2, 2)), 1000
            )
        
        # Mettre à jour la barre de vie du joueur
        self.player_health_bar.update_health(self.jeu.joueur.pv_actuels)
        
        if not self.jeu.joueur.est_vivant():
            self.add_combat_log("[SKULL] Vous etes mort! Game Over!")
            return False
        
        return True
    
    def handle_salle_speciale(self, salle: Salle):
        """Gère les salles spéciales avec effets visuels"""
        if isinstance(salle, SalleSoin):
            soin = int(self.jeu.joueur.pv_max * POURCENTAGE_SOIN)
            self.jeu.joueur.soigner(soin)
            message = f"Vous récupérez {soin} PV!"
            
            # Effet de particules de soin
            for i in range(15):
                self.particles.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    GREEN, (random.uniform(-3, 3), random.uniform(-3, 3)), 1500
                )
        elif isinstance(salle, SalleAmelioration):
            bonus = random.randint(BONUS_ATTAQUE_MIN, BONUS_ATTAQUE_MAX)
            self.jeu.joueur.augmenter_attaque(bonus)
            message = f"Votre attaque augmente de {bonus}!"
            
            # Effet de particules d'amélioration
            for i in range(20):
                self.particles.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    YELLOW, (random.uniform(-4, 4), random.uniform(-4, 4)), 2000
                )
        
        # Afficher le message
        message_text = TextSprite(SCREEN_WIDTH // 2 - 200, 400, message, 
                                 self.font_medium, GREEN)
        self.text_sprites.append(message_text)
    
    def setup_game_over(self):
        """Configure l'écran de fin de partie amélioré"""
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        
        # Réinitialiser les barres de vie
        self.player_health_bar = None
        self.enemy_health_bar = None
        
        # Titre
        if self.jeu.joueur.est_vivant() and self.jeu.salle_actuelle >= self.jeu.salles_max:
            title = TextSprite(SCREEN_WIDTH // 2 - 250, 150, "[VICTORY] VICTOIRE EPIQUE! [VICTORY]", 
                              self.font_large, YELLOW)
            subtitle = TextSprite(SCREEN_WIDTH // 2 - 200, 220, "[TROPHY] Vous avez conquis le donjon! [TROPHY]", 
                                 self.font_medium, WHITE)
        else:
            title = TextSprite(SCREEN_WIDTH // 2 - 200, 150, "[GAME OVER] GAME OVER [GAME OVER]", 
                              self.font_large, RED)
            subtitle = TextSprite(SCREEN_WIDTH // 2 - 150, 220, "[SAD] Votre aventure s'arrete ici... [SAD]", 
                                 self.font_medium, WHITE)
        
        self.text_sprites.append(title)
        self.text_sprites.append(subtitle)
        
        # Statistiques
        stats_y = 300
        stats = [
            (f"Ennemis tues: {self.jeu.joueur.ennemis_tues}", "skull"),
            (f"Boss vaincus: {self.jeu.joueur.boss_vaincus}", "crown"),
            (f"Salles traversees: {self.jeu.salle_actuelle}", "castle")
        ]
        
        for i, (stat, icon_type) in enumerate(stats):
            stat_text = IconTextSprite(SCREEN_WIDTH // 2 - 150, stats_y + i * 50, 
                                      stat, self.font_medium, icon_type, WHITE)
            self.text_sprites.append(stat_text)
        
        # Bouton Rejouer
        replay_button = Button(SCREEN_WIDTH // 2 - 120, 500, 240, 60, "[REPLAY] REJOUER", 
                              self.font_medium, GREEN)
        self.buttons.append(replay_button)
        
        # Bouton Menu
        menu_button = Button(SCREEN_WIDTH // 2 - 120, 580, 240, 60, "[HOME] MENU", 
                            self.font_medium, BLUE)
        self.buttons.append(menu_button)
    
    def handle_events(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Gestion des boutons
            for button in self.buttons:
                if button.handle_event(event):
                    if self.state == GameState.MENU:
                        if "AVENTURE" in button.text:
                            self.state = GameState.PLAYING
                            self.jeu = Jeu()
                            self.jeu.salles_max = 5
                        elif button.text == "QUITTER":
                            return False
                    
                    elif self.state == GameState.COMBAT:
                        if "ATTAQUER" in button.text:
                            if not self.handle_combat(self.salle_actuelle):
                                self.setup_game_over()
                                self.state = GameState.GAME_OVER
                            else:
                                # Vérifier si l'ennemi est mort
                                if isinstance(self.salle_actuelle, SalleEnnemi):
                                    if not self.salle_actuelle.ennemi.est_vivant():
                                        # Afficher l'écran de victoire
                                        self.setup_transition(True, self.salle_actuelle.ennemi.nom, False)
                                        self.state = GameState.TRANSITION
                                elif isinstance(self.salle_actuelle, SalleBoss):
                                    if not self.salle_actuelle.boss.est_vivant():
                                        # Afficher l'écran de victoire
                                        self.setup_transition(True, self.salle_actuelle.boss.nom, True)
                                        self.state = GameState.TRANSITION
                    
                    elif self.state == GameState.TRANSITION:
                        if "CONTINUER" in button.text or "AVENTURE" in button.text:
                            self.jeu.salle_actuelle += 1
                            self.salle_actuelle = None
                            self.state = GameState.PLAYING
                        elif "MENU" in button.text:
                            self.state = GameState.MENU
                            self.setup_menu()
                    
                    elif self.state == GameState.SALLE_SPECIALE:
                        if "CONTINUER" in button.text or "AVENTURE" in button.text:
                            self.jeu.salle_actuelle += 1
                            self.salle_actuelle = None
                            self.state = GameState.PLAYING
                    
                    elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                        if "REJOUER" in button.text:
                            self.state = GameState.PLAYING
                            self.jeu = Jeu()
                            self.jeu.salles_max = 5
                            self.salle_actuelle = None
                        elif "MENU" in button.text:
                            self.state = GameState.MENU
                            self.setup_menu()
                        elif "CONTINUER" in button.text:
                            self.jeu.salle_actuelle += 1
                            self.salle_actuelle = None
                            self.state = GameState.PLAYING
        
        return True
    
    def update(self, dt: int):
        """Met à jour la logique du jeu"""
        # Mettre à jour les sprites animés
        for sprite in self.sprites:
            sprite.update(dt)
        
        # Mettre à jour les barres de vie
        if self.player_health_bar:
            self.player_health_bar.update(dt)
        if self.enemy_health_bar:
            self.enemy_health_bar.update(dt)
        
        # Mettre à jour les particules
        self.particles.update(dt)
        
        if self.state == GameState.PLAYING:
            # Générer une nouvelle salle si nécessaire
            if self.salle_actuelle is None:
                self.salle_actuelle = self.jeu.generateur_salles.generer_salle()
                
                if isinstance(self.salle_actuelle, (SalleEnnemi, SalleBoss)):
                    self.state = GameState.COMBAT
                    self.setup_combat(self.salle_actuelle)
                else:
                    self.state = GameState.SALLE_SPECIALE
                    self.setup_salle_speciale(self.salle_actuelle)
                    self.handle_salle_speciale(self.salle_actuelle)
            
            # Vérifier la fin de partie
            if self.jeu.salle_actuelle >= self.jeu.salles_max:
                self.setup_game_over()
                self.state = GameState.VICTORY
            elif not self.jeu.joueur.est_vivant():
                self.setup_game_over()
                self.state = GameState.GAME_OVER
    
    def draw_background(self):
        """Dessine le fond selon l'état du jeu"""
        if self.state == GameState.MENU:
            # Fond dégradé pour le menu
            for y in range(SCREEN_HEIGHT):
                color_value = int(20 + (y / SCREEN_HEIGHT) * 30)
                pygame.draw.line(self.screen, (color_value, 0, color_value), (0, y), (SCREEN_WIDTH, y))
        elif self.state == GameState.COMBAT:
            # Fond dégradé pour le combat
            for y in range(SCREEN_HEIGHT):
                color_value = int(30 + (y / SCREEN_HEIGHT) * 20)
                pygame.draw.line(self.screen, (color_value, color_value, 0), (0, y), (SCREEN_WIDTH, y))
        elif self.state == GameState.TRANSITION:
            # Fond dégradé pour les transitions
            for y in range(SCREEN_HEIGHT):
                color_value = int(30 + (y / SCREEN_HEIGHT) * 25)
                pygame.draw.line(self.screen, (color_value, color_value, color_value), (0, y), (SCREEN_WIDTH, y))
        elif self.state == GameState.SALLE_SPECIALE:
            # Fond vert pour les salles spéciales
            for y in range(SCREEN_HEIGHT):
                color_value = int(20 + (y / SCREEN_HEIGHT) * 40)
                pygame.draw.line(self.screen, (0, color_value, 0), (0, y), (SCREEN_WIDTH, y))
        elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
            # Fond dégradé pour les écrans de fin
            for y in range(SCREEN_HEIGHT):
                color_value = int(20 + (y / SCREEN_HEIGHT) * 30)
                pygame.draw.line(self.screen, (color_value, 0, 0), (0, y), (SCREEN_WIDTH, y))
        else:
            # Fond simple pour les autres états
            self.screen.fill(BLACK)

    def draw(self):
        """Dessine tout le jeu"""
        self.screen.fill(BLACK)
        
        # Dessiner le fond
        self.draw_background()
        
        # Dessiner tous les sprites
        for sprite in self.sprites:
            sprite.draw(self.screen)
        
        # Dessiner toutes les particules
        self.particles.draw(self.screen)
        
        # Dessiner tous les textes
        for text_sprite in self.text_sprites:
            text_sprite.draw(self.screen)
        
        # Dessiner tous les boutons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Dessiner les barres de vie
        if self.player_health_bar:
            self.player_health_bar.draw(self.screen)
        if self.enemy_health_bar:
            self.enemy_health_bar.draw(self.screen)
        
        # Dessiner le log de combat
        if self.state == GameState.COMBAT:
            self.draw_combat_log()
        
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu"""
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Fonction principale"""
    game = RoguelikeGraphiqueAvance()
    game.run()

if __name__ == "__main__":
    main()