#!/usr/bin/env python3
"""
Entités du jeu Roguelike - Implémentations concrètes
Respect des principes SOLID
"""

import random
from typing import List, Optional
from interfaces import (
    ICharacter, IPlayer, IRoom, ICombatRoom, ISpecialRoom, 
    IPowerUp, Drawable, Updatable
)

# =============================================================================
# SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =============================================================================

class Character(ICharacter):
    """Classe de base pour tous les personnages - SRP"""
    
    def __init__(self, nom: str, pv_max: int, attaque: int):
        self._nom = nom
        self._pv_max = pv_max
        self._pv_actuels = pv_max
        self._attaque = attaque
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def pv_max(self) -> int:
        return self._pv_max
    
    @property
    def pv_actuels(self) -> int:
        return self._pv_actuels
    
    @property
    def attaque(self) -> int:
        return self._attaque
    
    def est_vivant(self) -> bool:
        return self._pv_actuels > 0
    
    def attaquer(self, cible: ICharacter) -> int:
        """Attaque une cible et retourne les dégâts infligés"""
        if not self.est_vivant() or not cible.est_vivant():
            return 0
        
        degats = random.randint(1, self._attaque)
        cible._pv_actuels = max(0, cible._pv_actuels - degats)
        return degats
    
    def soigner(self, points: int) -> None:
        """Soigne le personnage"""
        self._pv_actuels = min(self._pv_max, self._pv_actuels + points)
    
    def __str__(self) -> str:
        return f"{self._nom} - PV: {self._pv_actuels}/{self._pv_max} - Attaque: {self._attaque}"

class Player(Character, IPlayer):
    """Joueur - SRP: Gère uniquement les stats du joueur"""
    
    def __init__(self, nom: str = "Héros"):
        super().__init__(nom, 100, 20)  # Valeurs par défaut
        self._ennemis_tues = 0
        self._boss_vaincus = 0
        self._score = 0
        self._tours_survies = 0
        self._power_ups: List[IPowerUp] = []
    
    @property
    def score(self) -> int:
        return self._score
    
    @property
    def ennemis_tues(self) -> int:
        return self._ennemis_tues
    
    @property
    def boss_vaincus(self) -> int:
        return self._boss_vaincus
    
    def ajouter_score(self, points: int) -> None:
        """Ajoute des points au score"""
        self._score += points
    
    def tuer_ennemi(self) -> None:
        """Marque un ennemi comme tué et ajoute le score"""
        self._ennemis_tues += 1
        self.ajouter_score(100)  # Score pour ennemi
    
    def vaincre_boss(self) -> None:
        """Marque un boss comme vaincu et ajoute le score"""
        self._boss_vaincus += 1
        self.ajouter_score(500)  # Score pour boss
    
    def survivre_tour(self) -> None:
        """Ajoute des points de survie"""
        self._tours_survies += 1
        self.ajouter_score(10)  # Score de survie
    
    def traverser_salle(self) -> None:
        """Ajoute des points pour traverser une salle"""
        self.ajouter_score(50)  # Score pour salle
    
    def augmenter_attaque(self, bonus: int) -> None:
        """Augmente l'attaque du joueur"""
        self._attaque += bonus
    
    def add_power_up(self, power_up: IPowerUp) -> None:
        """Ajoute un power-up au joueur"""
        self._power_ups.append(power_up)
        power_up.appliquer(self)

class Enemy(Character):
    """Ennemi - SRP: Gère uniquement les stats d'un ennemi"""
    
    NOMS = ["Gobelin", "Orc", "Squelette", "Loup", "Araignée"]
    
    def __init__(self, difficulty: int = 1):
        nom = random.choice(self.NOMS)
        # Ajuster les stats selon la difficulté
        pv = int(30 * (1 + (difficulty - 1) * 0.5))
        attaque = int(15 * (1 + (difficulty - 1) * 0.3))
        super().__init__(nom, pv, attaque)

class Boss(Character):
    """Boss - SRP: Gère uniquement les stats d'un boss"""
    
    NOMS = ["Dragon", "Liche", "Démon", "Géant", "Hydre"]
    
    def __init__(self, difficulty: int = 1):
        nom = random.choice(self.NOMS)
        # Ajuster les stats selon la difficulté
        pv = int(80 * (1 + (difficulty - 1) * 0.7))
        attaque = int(25 * (1 + (difficulty - 1) * 0.5))
        super().__init__(nom, pv, attaque)

# =============================================================================
# POWER-UPS - SRP
# =============================================================================

class PowerUp(IPowerUp):
    """Power-up de base - SRP: Gère uniquement un effet"""
    
    def __init__(self, nom: str, effet: str, duree: int = 0, valeur: int = 0):
        self._nom = nom
        self._effet = effet
        self._duree = duree
        self._valeur = valeur
        self._temps_restant = duree
    
    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def effet(self) -> str:
        return self._effet
    
    @property
    def valeur(self) -> int:
        return self._valeur
    
    def appliquer(self, joueur: IPlayer) -> None:
        """Applique l'effet du power-up au joueur"""
        if self._effet == 'attaque':
            joueur.augmenter_attaque(self._valeur)
        elif self._effet == 'regeneration':
            joueur.soigner(self._valeur)
        # Autres effets peuvent être ajoutés ici
    
    def retirer(self, joueur: IPlayer) -> None:
        """Retire l'effet du power-up du joueur"""
        if self._effet == 'attaque':
            joueur.augmenter_attaque(-self._valeur)
        # Autres effets peuvent être ajoutés ici
    
    def update(self, dt: int) -> bool:
        """Met à jour le power-up"""
        if self._duree > 0:
            self._temps_restant -= dt
            return self._temps_restant > 0
        return True

# =============================================================================
# SALLES - SRP
# =============================================================================

class Room(IRoom):
    """Classe de base pour toutes les salles - SRP"""
    
    def __init__(self, nom: str):
        self._nom = nom
    
    @property
    def nom(self) -> str:
        return self._nom
    
    def entrer(self, joueur: IPlayer) -> bool:
        """Le joueur entre dans la salle"""
        return True

class CombatRoom(Room, ICombatRoom):
    """Salle de combat - SRP: Gère uniquement le combat"""
    
    def __init__(self, nom: str, ennemi: ICharacter):
        super().__init__(nom)
        self._ennemi = ennemi
    
    @property
    def ennemi(self) -> ICharacter:
        return self._ennemi
    
    def entrer(self, joueur: IPlayer) -> bool:
        """Le joueur entre dans la salle de combat"""
        print(f"\n=== {self._nom} ===")
        print(f"Un {self._ennemi.nom} apparaît!")
        return True

class EnemyRoom(CombatRoom):
    """Salle d'ennemi - SRP"""
    
    def __init__(self, difficulty: int = 1):
        ennemi = Enemy(difficulty)
        super().__init__("Salle d'Ennemi", ennemi)

class BossRoom(CombatRoom):
    """Salle de boss - SRP"""
    
    def __init__(self, difficulty: int = 1):
        boss = Boss(difficulty)
        super().__init__("Salle de Boss", boss)

class SpecialRoom(Room, ISpecialRoom):
    """Salle spéciale - SRP: Gère uniquement l'effet spécial"""
    
    def __init__(self, nom: str):
        super().__init__(nom)
    
    def entrer(self, joueur: IPlayer) -> bool:
        """Le joueur entre dans la salle spéciale"""
        print(f"\n=== {self._nom} ===")
        self.appliquer_effet(joueur)
        return True
    
    def appliquer_effet(self, joueur: IPlayer) -> None:
        """Applique l'effet de la salle"""
        pass

class HealingRoom(SpecialRoom):
    """Salle de soin - SRP"""
    
    def __init__(self):
        super().__init__("Salle de Soin")
    
    def appliquer_effet(self, joueur: IPlayer) -> None:
        """Soigne le joueur"""
        soin = int(joueur.pv_max * 0.15)  # 15% des PV max
        joueur.soigner(soin)
        print(f"Vous récupérez {soin} PV!")

class UpgradeRoom(SpecialRoom):
    """Salle d'amélioration - SRP"""
    
    def __init__(self):
        super().__init__("Salle d'Amélioration")
    
    def appliquer_effet(self, joueur: IPlayer) -> None:
        """Améliore l'attaque du joueur"""
        bonus = random.randint(3, 8)
        joueur.augmenter_attaque(bonus)
        print(f"Votre attaque augmente de {bonus}!")

class PowerUpRoom(SpecialRoom):
    """Salle de power-up - SRP"""
    
    def __init__(self):
        super().__init__("Salle de Power-Up")
        self._power_up = self._generer_power_up()
    
    def _generer_power_up(self) -> IPowerUp:
        """Génère un power-up aléatoire"""
        power_ups = [
            PowerUp("Potion de Force", "attaque", 0, random.randint(5, 15)),
            PowerUp("Potion de Soin", "regeneration", 0, random.randint(20, 40)),
        ]
        return random.choice(power_ups)
    
    def appliquer_effet(self, joueur: IPlayer) -> None:
        """Applique le power-up au joueur"""
        print(f"Vous trouvez: {self._power_up.nom}!")
        print(f"Effet: +{self._power_up.valeur} {self._power_up.effet}")
        
        joueur.add_power_up(self._power_up)
        joueur.ajouter_score(200)  # Bonus pour trouver un power-up
