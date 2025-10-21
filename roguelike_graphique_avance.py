#!/usr/bin/env python3
"""
Version graphique avancée du jeu roguelike avec des sprites détaillés et des animations
"""

import pygame
import random
import sys
import math
import json
import os
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod

# Initialisation de Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

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

# Système de score
SCORE_ENNEMI = 100
SCORE_BOSS = 500
SCORE_SALLE = 50
SCORE_SURVIE = 10  # Par tour de survie

# Probabilités des types de salles (plus équilibrées)
PROBABILITES_SALLES = {
    'ennemi': 0.5,      # 50% de chance d'avoir un ennemi
    'boss': 0.2,        # 20% de chance d'avoir un boss
    'soin': 0.1,        # 10% de chance d'avoir du soin
    'amelioration': 0.1,  # 10% de chance d'avoir une amélioration
    'powerup': 0.1      # 10% de chance d'avoir un power-up
}

# Noms des personnages
NOMS_ENNEMIS = ["Gobelin", "Orc", "Squelette", "Loup", "Araignée"]
NOMS_BOSS = ["Dragon", "Liche", "Démon", "Géant", "Hydre"]

class SoundManager:
    """Gestionnaire de sons et effets audio"""
    
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.3
        self.sfx_volume = 0.5
        self.create_synthetic_sounds()
    
    def create_synthetic_sounds(self):
        """Crée des sons synthétiques pour le jeu"""
        # Son d'attaque
        attack_sound = self.create_tone(440, 0.1, 'square')
        self.sounds['attack'] = attack_sound
        
        # Son de victoire
        victory_sound = self.create_victory_melody()
        self.sounds['victory'] = victory_sound
        
        # Son de défaite
        defeat_sound = self.create_tone(220, 0.5, 'sine')
        self.sounds['defeat'] = defeat_sound
        
        # Son de soin
        heal_sound = self.create_tone(660, 0.2, 'sine')
        self.sounds['heal'] = heal_sound
        
        # Son d'amélioration
        upgrade_sound = self.create_tone(880, 0.15, 'square')
        self.sounds['upgrade'] = upgrade_sound
        
        # Son de clic
        click_sound = self.create_tone(800, 0.05, 'square')
        self.sounds['click'] = click_sound
    
    def create_tone(self, frequency, duration, wave_type='sine'):
        """Crée un son synthétique"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            
            if wave_type == 'sine':
                sample = int(32767 * math.sin(2 * math.pi * frequency * time))
            elif wave_type == 'square':
                sample = 32767 if (int(frequency * time) % 2) else -32767
            elif wave_type == 'sawtooth':
                sample = int(32767 * (2 * (frequency * time - int(frequency * time)) - 1))
            else:
                sample = 0
            
            # Envelope pour éviter les clics
            envelope = 1.0
            if i < frames * 0.1:  # Attack
                envelope = i / (frames * 0.1)
            elif i > frames * 0.9:  # Release
                envelope = (frames - i) / (frames * 0.1)
            
            sample = int(sample * envelope)
            arr.append([sample, sample])
        
        # Créer le son avec numpy si disponible, sinon utiliser une méthode alternative
        try:
            import numpy as np
            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
        except ImportError:
            # Méthode alternative sans numpy
            sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
        sound.set_volume(self.sfx_volume)
        return sound
    
    def create_victory_melody(self):
        """Crée une mélodie de victoire"""
        notes = [523, 659, 784, 1047]  # C, E, G, C (octave supérieure)
        duration = 0.2
        sample_rate = 22050
        total_frames = int(len(notes) * duration * sample_rate)
        arr = []
        
        for note_idx, frequency in enumerate(notes):
            note_frames = int(duration * sample_rate)
            for i in range(note_frames):
                time = float(i) / sample_rate
                sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * time))
                
                # Envelope
                envelope = 1.0
                if i < note_frames * 0.1:
                    envelope = i / (note_frames * 0.1)
                elif i > note_frames * 0.8:
                    envelope = (note_frames - i) / (note_frames * 0.2)
                
                sample = int(sample * envelope)
                arr.append([sample, sample])
        
        # Créer le son avec numpy si disponible, sinon utiliser une méthode alternative
        try:
            import numpy as np
            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
        except ImportError:
            # Méthode alternative sans numpy
            sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
        sound.set_volume(self.sfx_volume)
        return sound
    
    def play_sound(self, sound_name):
        """Joue un son"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def set_volume(self, volume):
        """Définit le volume des effets sonores"""
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

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
        self.score = 0
        self.tours_survies = 0
        self.power_ups = []  # Liste des power-ups actifs
    
    def augmenter_attaque(self, bonus: int):
        """Augmente l'attaque du joueur"""
        self.attaque += bonus
        print(f"Votre attaque augmente de {bonus}! Nouvelle attaque: {self.attaque}")
    
    def ajouter_score(self, points: int):
        """Ajoute des points au score"""
        self.score += points
    
    def tuer_ennemi(self):
        """Marque un ennemi comme tué et ajoute le score"""
        self.ennemis_tues += 1
        self.ajouter_score(SCORE_ENNEMI)
    
    def vaincre_boss(self):
        """Marque un boss comme vaincu et ajoute le score"""
        self.boss_vaincus += 1
        self.ajouter_score(SCORE_BOSS)
    
    def survivre_tour(self):
        """Ajoute des points de survie"""
        self.tours_survies += 1
        self.ajouter_score(SCORE_SURVIE)
    
    def traverser_salle(self):
        """Ajoute des points pour traverser une salle"""
        self.ajouter_score(SCORE_SALLE)

class PowerUp:
    """Classe pour les power-ups et objets spéciaux"""
    
    def __init__(self, nom: str, effet: str, duree: int = 0, valeur: int = 0):
        self.nom = nom
        self.effet = effet  # 'attaque', 'defense', 'vitesse', 'regeneration'
        self.duree = duree  # 0 = permanent
        self.valeur = valeur
        self.temps_restant = duree
    
    def appliquer(self, joueur: Joueur):
        """Applique l'effet du power-up au joueur"""
        if self.effet == 'attaque':
            joueur.attaque += self.valeur
        elif self.effet == 'defense':
            # Réduit les dégâts reçus
            joueur.defense = getattr(joueur, 'defense', 0) + self.valeur
        elif self.effet == 'regeneration':
            # Soigne le joueur
            joueur.soigner(self.valeur)
        elif self.effet == 'vitesse':
            # Réduit le temps entre les attaques
            joueur.vitesse = getattr(joueur, 'vitesse', 1) + self.valeur
    
    def retirer(self, joueur: Joueur):
        """Retire l'effet du power-up du joueur"""
        if self.effet == 'attaque':
            joueur.attaque -= self.valeur
        elif self.effet == 'defense':
            joueur.defense = getattr(joueur, 'defense', 0) - self.valeur
        elif self.effet == 'vitesse':
            joueur.vitesse = getattr(joueur, 'vitesse', 1) - self.valeur
    
    def update(self, dt: int):
        """Met à jour le power-up"""
        if self.duree > 0:
            self.temps_restant -= dt
            return self.temps_restant > 0
        return True

class ScoreManager:
    """Gestionnaire des scores et high scores"""
    
    def __init__(self):
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.charger_high_scores()
    
    def charger_high_scores(self) -> List[dict]:
        """Charge les high scores depuis le fichier"""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def sauvegarder_high_scores(self):
        """Sauvegarde les high scores dans le fichier"""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except:
            pass
    
    def ajouter_score(self, nom: str, score: int, salles: int, ennemis: int, boss: int):
        """Ajoute un nouveau score"""
        nouveau_score = {
            'nom': nom,
            'score': score,
            'salles': salles,
            'ennemis': ennemis,
            'boss': boss,
            'date': pygame.time.get_ticks() // 1000  # Timestamp
        }
        
        self.high_scores.append(nouveau_score)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Garder seulement les 10 meilleurs scores
        if len(self.high_scores) > 10:
            self.high_scores = self.high_scores[:10]
        
        self.sauvegarder_high_scores()
        return nouveau_score in self.high_scores[:10]  # True si c'est un high score
    
    def est_high_score(self, score: int) -> bool:
        """Vérifie si un score est un high score"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]['score']
    
    def get_top_scores(self, limit: int = 5) -> List[dict]:
        """Retourne les meilleurs scores"""
        return self.high_scores[:limit]

class Ennemi(Personnage):
    """Classe représentant un ennemi normal"""
    
    def __init__(self, difficulte: int = 1):
        nom = random.choice(NOMS_ENNEMIS)
        # Ajuster les stats selon la difficulté
        pv = int(ENNEMI_PV_MAX * (1 + (difficulte - 1) * 0.5))
        attaque = int(ENNEMI_ATTAQUE * (1 + (difficulte - 1) * 0.3))
        super().__init__(nom, pv, attaque)

class Boss(Personnage):
    """Classe représentant un boss (ennemi puissant)"""
    
    def __init__(self, difficulte: int = 1):
        nom = random.choice(NOMS_BOSS)
        # Ajuster les stats selon la difficulté
        pv = int(BOSS_PV_MAX * (1 + (difficulte - 1) * 0.7))
        attaque = int(BOSS_ATTAQUE * (1 + (difficulte - 1) * 0.5))
        super().__init__(nom, pv, attaque)

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
    
    def __init__(self, difficulte: int = 1):
        super().__init__("Salle d'Ennemi")
        self.ennemi = Ennemi(difficulte)
    
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
    
    def __init__(self, difficulte: int = 1):
        super().__init__("Salle de Boss")
        self.boss = Boss(difficulte)
    
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

class SallePowerUp(Salle):
    """Salle contenant un power-up"""
    
    def __init__(self):
        super().__init__("Salle de Power-Up")
        self.power_up = self.generer_power_up()
    
    def generer_power_up(self) -> PowerUp:
        """Génère un power-up aléatoire"""
        power_ups = [
            PowerUp("Potion de Force", "attaque", 0, random.randint(5, 15)),
            PowerUp("Armure Magique", "defense", 0, random.randint(3, 8)),
            PowerUp("Potion de Soin", "regeneration", 0, random.randint(20, 40)),
            PowerUp("Bottes de Vitesse", "vitesse", 0, 1)
        ]
        return random.choice(power_ups)
    
    def entrer(self, joueur: Joueur) -> bool:
        print(f"\n=== {self.nom} ===")
        print(f"Vous trouvez: {self.power_up.nom}!")
        print(f"Effet: +{self.power_up.valeur} {self.power_up.effet}")
        
        self.power_up.appliquer(joueur)
        joueur.power_ups.append(self.power_up)
        joueur.ajouter_score(200)  # Bonus pour trouver un power-up
        
        return True

class GenerateurSalles:
    """Générateur de salles aléatoires basé sur les probabilités"""
    
    def __init__(self, difficulte: int = 1):
        self.derniere_salle_speciale = False
        self.difficulte = difficulte
    
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
                    return SalleEnnemi(self.difficulte)
                elif type_salle == 'boss':
                    self.derniere_salle_speciale = False
                    return SalleBoss(self.difficulte)
                elif type_salle == 'soin':
                    self.derniere_salle_speciale = True
                    return SalleSoin()
                elif type_salle == 'amelioration':
                    self.derniere_salle_speciale = True
                    return SalleAmelioration()
                elif type_salle == 'powerup':
                    self.derniere_salle_speciale = True
                    return SallePowerUp()
        
        # Par défaut, retourner une salle d'ennemi
        self.derniere_salle_speciale = False
        return SalleEnnemi(self.difficulte)

class Jeu:
    """Classe principale du jeu"""
    
    def __init__(self, difficulte: int = 1):
        self.joueur = Joueur()
        self.salle_actuelle = 0
        self.salles_max = NOMBRE_SALLES
        self.difficulte = difficulte
        self.generateur_salles = GenerateurSalles(difficulte)
        self.score_manager = ScoreManager()
    
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
    """Classe pour dessiner des icônes visuelles avec des formes géométriques améliorées"""
    
    @staticmethod
    def draw_heart(screen, x, y, size, color):
        """Dessine un cœur avec dégradé et ombre"""
        # Ombre
        shadow_offset = 2
        pygame.draw.circle(screen, (50, 0, 0), (x - size//4 + shadow_offset, y - size//4 + shadow_offset), size//4)
        pygame.draw.circle(screen, (50, 0, 0), (x + size//4 + shadow_offset, y - size//4 + shadow_offset), size//4)
        shadow_points = [(x + shadow_offset, y + size//2 + shadow_offset), 
                        (x - size//2 + shadow_offset, y + shadow_offset), 
                        (x + size//2 + shadow_offset, y + shadow_offset)]
        pygame.draw.polygon(screen, (50, 0, 0), shadow_points)
        
        # Cœur principal avec dégradé
        pygame.draw.circle(screen, color, (x - size//4, y - size//4), size//4)
        pygame.draw.circle(screen, color, (x + size//4, y - size//4), size//4)
        points = [(x, y + size//2), (x - size//2, y), (x + size//2, y)]
        pygame.draw.polygon(screen, color, points)
        
        # Reflet
        pygame.draw.circle(screen, (255, 200, 200), (x - size//6, y - size//3), size//8)
        pygame.draw.circle(screen, (255, 200, 200), (x + size//6, y - size//3), size//8)
    
    @staticmethod
    def draw_sword(screen, x, y, size, color):
        """Dessine une épée avec détails"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//8 + shadow_offset, y - size//2 + shadow_offset, size//4, size))
        pygame.draw.rect(screen, (30, 30, 30), (x - size//3 + shadow_offset, y - size//8 + shadow_offset, size*2//3, size//4))
        
        # Lame avec dégradé
        pygame.draw.rect(screen, (200, 200, 255), (x - size//8, y - size//2, size//4, size))
        pygame.draw.rect(screen, (150, 150, 255), (x - size//8, y - size//2, size//4, size//2))
        
        # Garde
        pygame.draw.rect(screen, (139, 69, 19), (x - size//3, y - size//8, size*2//3, size//4))
        pygame.draw.rect(screen, (160, 82, 45), (x - size//4, y - size//10, size//2, size//6))
        
        # Pommeau
        pygame.draw.circle(screen, (139, 69, 19), (x, y + size//2 + size//8), size//6)
        pygame.draw.circle(screen, (160, 82, 45), (x, y + size//2 + size//8), size//8)
    
    @staticmethod
    def draw_shield(screen, x, y, size, color):
        """Dessine un bouclier avec motif"""
        # Ombre
        shadow_offset = 2
        shadow_points = [(x + shadow_offset, y - size//2 + shadow_offset), 
                        (x - size//2 + shadow_offset, y - size//4 + shadow_offset), 
                        (x - size//2 + shadow_offset, y + size//4 + shadow_offset), 
                        (x + shadow_offset, y + size//2 + shadow_offset), 
                        (x + size//2 + shadow_offset, y + size//4 + shadow_offset), 
                        (x + size//2 + shadow_offset, y - size//4 + shadow_offset)]
        pygame.draw.polygon(screen, (30, 30, 30), shadow_points)
        
        # Bouclier principal
        points = [(x, y - size//2), (x - size//2, y - size//4), (x - size//2, y + size//4), 
                 (x, y + size//2), (x + size//2, y + size//4), (x + size//2, y - size//4)]
        pygame.draw.polygon(screen, color, points)
        
        # Bordure
        pygame.draw.polygon(screen, (255, 215, 0), points, 3)
        
        # Motif central
        pygame.draw.circle(screen, (255, 215, 0), (x, y), size//4)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size//6)
    
    @staticmethod
    def draw_crown(screen, x, y, size, color):
        """Dessine une couronne avec joyaux"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//2 + shadow_offset, y + shadow_offset, size, size//3))
        
        # Base de la couronne
        pygame.draw.rect(screen, color, (x - size//2, y, size, size//3))
        pygame.draw.rect(screen, (255, 215, 0), (x - size//2, y, size, size//3), 2)
        
        # Pointes avec joyaux
        for i in range(3):
            px = x - size//3 + i * size//3
            # Ombre de la pointe
            shadow_points = [(px + shadow_offset, y + shadow_offset), 
                           (px - size//6 + shadow_offset, y - size//3 + shadow_offset), 
                           (px + size//6 + shadow_offset, y - size//3 + shadow_offset)]
            pygame.draw.polygon(screen, (30, 30, 30), shadow_points)
            
            # Pointe
            points = [(px, y), (px - size//6, y - size//3), (px + size//6, y - size//3)]
            pygame.draw.polygon(screen, color, points)
            
            # Joyau
            pygame.draw.circle(screen, (255, 0, 0), (px, y - size//4), size//12)
            pygame.draw.circle(screen, (255, 255, 255), (px, y - size//4), size//16)
    
    @staticmethod
    def draw_skull(screen, x, y, size, color):
        """Dessine un crâne avec détails"""
        # Ombre
        shadow_offset = 2
        pygame.draw.circle(screen, (20, 20, 20), (x + shadow_offset, y + shadow_offset), size//2)
        
        # Tête
        pygame.draw.circle(screen, color, (x, y), size//2)
        pygame.draw.circle(screen, (200, 200, 200), (x, y), size//2, 2)
        
        # Yeux avec reflet
        pygame.draw.circle(screen, (255, 0, 0), (x - size//6, y - size//6), size//8)
        pygame.draw.circle(screen, (255, 0, 0), (x + size//6, y - size//6), size//8)
        pygame.draw.circle(screen, (255, 255, 255), (x - size//8, y - size//8), size//12)
        pygame.draw.circle(screen, (255, 255, 255), (x + size//8, y - size//8), size//12)
        
        # Bouche
        pygame.draw.rect(screen, (0, 0, 0), (x - size//4, y + size//6, size//2, size//8))
        # Dents
        for i in range(3):
            tooth_x = x - size//6 + i * size//6
            pygame.draw.rect(screen, (255, 255, 255), (tooth_x, y + size//6, size//12, size//12))
    
    @staticmethod
    def draw_plus(screen, x, y, size, color):
        """Dessine un plus avec effet de brillance"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//8 + shadow_offset, y - size//2 + shadow_offset, size//4, size))
        pygame.draw.rect(screen, (30, 30, 30), (x - size//2 + shadow_offset, y - size//8 + shadow_offset, size, size//4))
        
        # Plus principal
        pygame.draw.rect(screen, color, (x - size//8, y - size//2, size//4, size))
        pygame.draw.rect(screen, color, (x - size//2, y - size//8, size, size//4))
        
        # Reflet
        pygame.draw.rect(screen, (255, 255, 255), (x - size//12, y - size//2, size//6, size//3))
        pygame.draw.rect(screen, (255, 255, 255), (x - size//2, y - size//12, size//3, size//6))
    
    @staticmethod
    def draw_exclamation(screen, x, y, size, color):
        """Dessine un point d'exclamation avec effet"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//8 + shadow_offset, y - size//2 + shadow_offset, size//4, size*3//4))
        pygame.draw.circle(screen, (30, 30, 30), (x + shadow_offset, y + size//3 + shadow_offset), size//8)
        
        # Barre principale
        pygame.draw.rect(screen, color, (x - size//8, y - size//2, size//4, size*3//4))
        pygame.draw.rect(screen, (255, 255, 255), (x - size//12, y - size//2, size//6, size//3))
        
        # Point
        pygame.draw.circle(screen, color, (x, y + size//3), size//8)
        pygame.draw.circle(screen, (255, 255, 255), (x, y + size//3), size//12)
    
    @staticmethod
    def draw_castle(screen, x, y, size, color):
        """Dessine un château avec détails"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//2 + shadow_offset, y + shadow_offset, size, size//2))
        pygame.draw.rect(screen, (30, 30, 30), (x - size//2 + shadow_offset, y - size//2 + shadow_offset, size//3, size//2))
        pygame.draw.rect(screen, (30, 30, 30), (x - size//6 + shadow_offset, y - size//2 + shadow_offset, size//3, size//2))
        pygame.draw.rect(screen, (30, 30, 30), (x + size//6 + shadow_offset, y - size//2 + shadow_offset, size//3, size//2))
        
        # Base
        pygame.draw.rect(screen, color, (x - size//2, y, size, size//2))
        pygame.draw.rect(screen, (139, 69, 19), (x - size//2, y, size, size//2), 2)
        
        # Tours
        pygame.draw.rect(screen, color, (x - size//2, y - size//2, size//3, size//2))
        pygame.draw.rect(screen, color, (x - size//6, y - size//2, size//3, size//2))
        pygame.draw.rect(screen, color, (x + size//6, y - size//2, size//3, size//2))
        
        # Drapeaux
        for i, px in enumerate([x - size//3, x, x + size//3]):
            flag_color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i]
            pygame.draw.polygon(screen, flag_color, [(px, y - size//2), (px + size//8, y - size//3), (px, y - size//4)])
    
    @staticmethod
    def draw_trophy(screen, x, y, size, color):
        """Dessine un trophée avec brillance"""
        # Ombre
        shadow_offset = 2
        pygame.draw.rect(screen, (30, 30, 30), (x - size//4 + shadow_offset, y + size//4 + shadow_offset, size//2, size//4))
        pygame.draw.ellipse(screen, (30, 30, 30), (x - size//3 + shadow_offset, y - size//4 + shadow_offset, size*2//3, size//2))
        
        # Base
        pygame.draw.rect(screen, (139, 69, 19), (x - size//4, y + size//4, size//2, size//4))
        pygame.draw.rect(screen, (160, 82, 45), (x - size//6, y + size//3, size//3, size//6))
        
        # Coupe
        pygame.draw.ellipse(screen, color, (x - size//3, y - size//4, size*2//3, size//2))
        pygame.draw.ellipse(screen, (255, 215, 0), (x - size//3, y - size//4, size*2//3, size//2), 3)
        
        # Reflet
        pygame.draw.ellipse(screen, (255, 255, 255), (x - size//4, y - size//3, size//2, size//4))
        
        # Anses
        pygame.draw.arc(screen, (255, 215, 0), (x - size//2, y - size//4, size//2, size//2), 0, 3.14, 4)
        pygame.draw.arc(screen, (255, 215, 0), (x, y - size//4, size//2, size//2), 0, 3.14, 4)

class UnicodeIcons:
    """Classe pour gérer les icônes Unicode si disponibles"""
    
    # Dictionnaire des icônes Unicode
    ICONS = {
        'heart': '♥',
        'sword': '⚔',
        'shield': '🛡',
        'crown': '👑',
        'skull': '☠',
        'plus': '✚',
        'exclamation': '❗',
        'castle': '🏰',
        'trophy': '🏆',
        'star': '★',
        'diamond': '♦',
        'spade': '♠',
        'club': '♣'
    }
    
    @staticmethod
    def get_icon(icon_name: str) -> str:
        """Retourne l'icône Unicode si disponible, sinon retourne un caractère de fallback"""
        return UnicodeIcons.ICONS.get(icon_name, '●')
    
    @staticmethod
    def draw_icon_text(screen, x: int, y: int, icon_name: str, text: str, 
                      font: pygame.font.Font, color: Tuple[int, int, int] = WHITE):
        """Dessine une icône Unicode avec du texte"""
        try:
            # Essayer d'utiliser une police qui supporte Unicode
            unicode_font = pygame.font.Font(None, font.get_height())
            icon = UnicodeIcons.get_icon(icon_name)
            
            # Dessiner l'icône
            icon_surface = unicode_font.render(icon, True, color)
            screen.blit(icon_surface, (x, y))
            
            # Dessiner le texte à côté
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (x + 25, y))
            
        except:
            # Fallback vers les icônes géométriques
            IconDrawer.draw_icon_fallback(screen, x, y, icon_name, 20, color)

class IconDrawer:
    """Classe pour dessiner des icônes visuelles avec des formes géométriques améliorées"""
    
    @staticmethod
    def draw_icon_fallback(screen, x: int, y: int, icon_name: str, size: int, color: Tuple[int, int, int]):
        """Dessine une icône de fallback si Unicode n'est pas disponible"""
        if icon_name == 'heart':
            IconDrawer.draw_heart(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'sword':
            IconDrawer.draw_sword(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'shield':
            IconDrawer.draw_shield(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'crown':
            IconDrawer.draw_crown(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'skull':
            IconDrawer.draw_skull(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'plus':
            IconDrawer.draw_plus(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'exclamation':
            IconDrawer.draw_exclamation(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'castle':
            IconDrawer.draw_castle(screen, x + size//2, y + size//2, size, color)
        elif icon_name == 'trophy':
            IconDrawer.draw_trophy(screen, x + size//2, y + size//2, size, color)
    
    @staticmethod
    def draw_heart(screen, x, y, size, color):
        """Dessine un cœur avec dégradé et ombre"""
        # Ombre
        shadow_offset = 2
        pygame.draw.circle(screen, (50, 0, 0), (x - size//4 + shadow_offset, y - size//4 + shadow_offset), size//4)
        pygame.draw.circle(screen, (50, 0, 0), (x + size//4 + shadow_offset, y - size//4 + shadow_offset), size//4)
        shadow_points = [(x + shadow_offset, y + size//2 + shadow_offset), 
                        (x - size//2 + shadow_offset, y + shadow_offset), 
                        (x + size//2 + shadow_offset, y + shadow_offset)]
        pygame.draw.polygon(screen, (50, 0, 0), shadow_points)
        
        # Cœur principal avec dégradé
        pygame.draw.circle(screen, color, (x - size//4, y - size//4), size//4)
        pygame.draw.circle(screen, color, (x + size//4, y - size//4), size//4)
        points = [(x, y + size//2), (x - size//2, y), (x + size//2, y)]
        pygame.draw.polygon(screen, color, points)
        
        # Reflet
        pygame.draw.circle(screen, (255, 200, 200), (x - size//6, y - size//3), size//8)
        pygame.draw.circle(screen, (255, 200, 200), (x + size//6, y - size//3), size//8)

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
        
        # Essayer d'abord les icônes Unicode
        try:
            unicode_font = pygame.font.Font(None, self.font.get_height())
            icon = UnicodeIcons.get_icon(self.icon_type)
            icon_surface = unicode_font.render(icon, True, self.color)
            screen.blit(icon_surface, (self.x, self.y))
            
            # Dessiner le texte à côté
            text_x = self.x + 25
            text_surface = self.font.render(self.text, True, self.color)
            
            # Ombre
            if self.shadow:
                shadow_surface = self.font.render(self.text, True, BLACK)
                screen.blit(shadow_surface, (text_x + 2, self.y + 2))
            
            # Texte principal
            screen.blit(text_surface, (text_x, self.y))
            
        except:
            # Fallback vers les icônes géométriques améliorées
            icon_x = self.x
            icon_y = self.y + 10  # Centrer verticalement avec le texte
            
            # Couleurs spécifiques pour chaque icône
            colors = {
                "heart": RED,
                "sword": (200, 200, 255),
                "shield": BLUE,
                "crown": YELLOW,
                "skull": WHITE,
                "plus": GREEN,
                "exclamation": YELLOW,
                "castle": GRAY,
                "trophy": YELLOW
            }
            
            color = colors.get(self.icon_type, self.color)
            
            if self.icon_type == "heart":
                IconDrawer.draw_heart(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "sword":
                IconDrawer.draw_sword(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "shield":
                IconDrawer.draw_shield(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "crown":
                IconDrawer.draw_crown(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "skull":
                IconDrawer.draw_skull(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "plus":
                IconDrawer.draw_plus(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "exclamation":
                IconDrawer.draw_exclamation(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "castle":
                IconDrawer.draw_castle(screen, icon_x, icon_y, self.icon_size, color)
            elif self.icon_type == "trophy":
                IconDrawer.draw_trophy(screen, icon_x, icon_y, self.icon_size, color)
            
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
        
        # Gestionnaires
        self.sound_manager = SoundManager()
        
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
        
        # Bouton Jouer (Normal)
        play_button = Button(SCREEN_WIDTH // 2 - 120, 280, 240, 50, "NORMAL", 
                            self.font_medium, GREEN)
        self.buttons.append(play_button)
        
        # Bouton Jouer (Difficile)
        hard_button = Button(SCREEN_WIDTH // 2 - 120, 340, 240, 50, "DIFFICILE", 
                            self.font_medium, ORANGE)
        self.buttons.append(hard_button)
        
        # Bouton Jouer (Expert)
        expert_button = Button(SCREEN_WIDTH // 2 - 120, 400, 240, 50, "EXPERT", 
                              self.font_medium, RED)
        self.buttons.append(expert_button)
        
        # Bouton Quitter
        quit_button = Button(SCREEN_WIDTH // 2 - 120, 480, 240, 50, "QUITTER", 
                            self.font_medium, GRAY)
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
        
        # Affichage du score
        score_text = TextSprite(50, 20, f"Score: {self.jeu.joueur.score}", 
                               self.font_small, WHITE)
        self.text_sprites.append(score_text)
        
        # Affichage de la difficulté
        difficulte_names = {1: "Normal", 2: "Difficile", 3: "Expert"}
        difficulte_colors = {1: GREEN, 2: ORANGE, 3: RED}
        difficulte_text = TextSprite(50, 50, f"Difficulte: {difficulte_names[self.jeu.difficulte]}", 
                                    self.font_small, difficulte_colors[self.jeu.difficulte])
        self.text_sprites.append(difficulte_text)
        
        # Affichage des power-ups actifs
        if self.jeu.joueur.power_ups:
            power_up_text = TextSprite(50, 80, f"Power-ups: {len(self.jeu.joueur.power_ups)}", 
                                      self.font_small, YELLOW)
            self.text_sprites.append(power_up_text)
        
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
        elif isinstance(salle, SallePowerUp):
            icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "trophy", PURPLE)
            message = f"Vous trouvez: {salle.power_up.nom}!"
        else:
            # Icône par défaut
            icon = IconTextSprite(SCREEN_WIDTH // 2 - 50, 300, "", self.font_large, "sword", BLUE)
            message = "Salle mystérieuse..."
        
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
                self.jeu.joueur.tuer_ennemi()
                self.add_combat_log(f"[SKULL] Vous avez vaincu {ennemi.nom}!")
            else:
                self.jeu.joueur.vaincre_boss()
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
        
        # Ajouter des points de survie
        self.jeu.joueur.survivre_tour()
        
        if not self.jeu.joueur.est_vivant():
            self.add_combat_log("[SKULL] Vous etes mort! Game Over!")
            return False
        
        return True
    
    def handle_salle_speciale(self, salle: Salle):
        """Gère les salles spéciales avec effets visuels"""
        if isinstance(salle, SalleSoin):
            soin = int(self.jeu.joueur.pv_max * POURCENTAGE_SOIN)
            self.jeu.joueur.soigner(soin)
            self.sound_manager.play_sound('heal')
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
            self.sound_manager.play_sound('upgrade')
            message = f"Votre attaque augmente de {bonus}!"
            
            # Effet de particules d'amélioration
            for i in range(20):
                self.particles.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    YELLOW, (random.uniform(-4, 4), random.uniform(-4, 4)), 2000
                )
        elif isinstance(salle, SallePowerUp):
            self.sound_manager.play_sound('upgrade')
            message = f"Vous obtenez: {salle.power_up.nom}!"
            
            # Effet de particules de power-up
            for i in range(25):
                self.particles.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    PURPLE, (random.uniform(-5, 5), random.uniform(-5, 5)), 2500
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
                        if button.text == "NORMAL":
                            self.sound_manager.play_sound('click')
                            self.reset_game(1)
                        elif button.text == "DIFFICILE":
                            self.sound_manager.play_sound('click')
                            self.reset_game(2)
                        elif button.text == "EXPERT":
                            self.sound_manager.play_sound('click')
                            self.reset_game(3)
                        elif button.text == "QUITTER":
                            self.sound_manager.play_sound('click')
                            return False
                    
                    elif self.state == GameState.COMBAT:
                        if "ATTAQUER" in button.text:
                            self.sound_manager.play_sound('attack')
                            if not self.handle_combat(self.salle_actuelle):
                                self.sound_manager.play_sound('defeat')
                                self.setup_game_over()
                                self.state = GameState.GAME_OVER
                            else:
                                # Vérifier si l'ennemi est mort
                                if isinstance(self.salle_actuelle, SalleEnnemi):
                                    if not self.salle_actuelle.ennemi.est_vivant():
                                        self.sound_manager.play_sound('victory')
                                        # Afficher l'écran de victoire
                                        self.setup_transition(True, self.salle_actuelle.ennemi.nom, False)
                                        self.state = GameState.TRANSITION
                                elif isinstance(self.salle_actuelle, SalleBoss):
                                    if not self.salle_actuelle.boss.est_vivant():
                                        self.sound_manager.play_sound('victory')
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
                            self.sound_manager.play_sound('click')
                            # Réinitialiser le jeu avec la même difficulté
                            difficulte_actuelle = self.jeu.difficulte
                            self.reset_game(difficulte_actuelle)
                        elif "MENU" in button.text:
                            self.sound_manager.play_sound('click')
                            # Retourner au menu principal
                            self.state = GameState.MENU
                            self.setup_menu()
                        elif "CONTINUER" in button.text:
                            self.jeu.salle_actuelle += 1
                            self.salle_actuelle = None
                            self.state = GameState.PLAYING
        
        return True
    
    def reset_game(self, difficulte: int = 1):
        """Réinitialise complètement le jeu"""
        # Réinitialiser le jeu
        self.jeu = Jeu(difficulte)
        
        # Définir le nombre de salles selon la difficulté
        if difficulte == 1:
            self.jeu.salles_max = 5
        elif difficulte == 2:
            self.jeu.salles_max = 7
        elif difficulte == 3:
            self.jeu.salles_max = 10
        
        # Réinitialiser l'état
        self.salle_actuelle = None
        self.state = GameState.PLAYING
        
        # Réinitialiser les sprites et boutons
        self.sprites.clear()
        self.text_sprites.clear()
        self.buttons.clear()
        self.combat_log.clear()
        
        # Réinitialiser les barres de vie
        self.player_health_bar = None
        self.enemy_health_bar = None
    
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
                self.jeu.joueur.traverser_salle()  # Ajouter des points pour traverser une salle
                
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