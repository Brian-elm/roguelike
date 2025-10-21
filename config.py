#!/usr/bin/env python3
"""
Configuration centralisée du jeu Roguelike
"""

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
SCORE_SURVIE = 10

# Probabilités des types de salles
PROBABILITES_SALLES = {
    'ennemi': 0.5,
    'boss': 0.2,
    'soin': 0.1,
    'amelioration': 0.1,
    'powerup': 0.1
}

# Noms des personnages
NOMS_ENNEMIS = ["Gobelin", "Orc", "Squelette", "Loup", "Araignée"]
NOMS_BOSS = ["Dragon", "Liche", "Démon", "Géant", "Hydre"]

# Configuration des difficultés
DIFFICULTES = {
    1: {"salles": 5, "nom": "Normal", "couleur": GREEN},
    2: {"salles": 7, "nom": "Difficile", "couleur": ORANGE},
    3: {"salles": 10, "nom": "Expert", "couleur": RED}
}
