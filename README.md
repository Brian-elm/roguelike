# Roguelike Graphique

Un jeu roguelike simple avec interface graphique développé en Python.

## 🎮 Description

Le but du jeu est de faire avancer un joueur à travers plusieurs salles générées aléatoirement. Le joueur doit survivre à 5 salles pour gagner.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.6 ou supérieur
- Pygame

### Installation
```bash
pip install pygame
```

### Lancement
```bash
python3 roguelike_graphique_avance.py
```

## 🎯 Contrôles

- **Souris** : Navigation dans les menus et interface
- **Clic gauche** : Sélectionner les boutons et options
- **Bouton "ATTAQUER"** : Lancer une attaque contre l'ennemi
- **Bouton "CONTINUER L'AVENTURE"** : Passer à la salle suivante

## 🏰 Types de Salles

### Salle d'Ennemi
- Combat contre un ennemi normal (Gobelin, Orc, Squelette, Loup, Araignée)
- PV : 30, Attaque : 15

### Salle de Boss
- Combat contre un boss puissant (Dragon, Liche, Démon, Géant, Hydre)
- PV : 80, Attaque : 25

### Salle de Soin
- Restaure 15% des PV maximum du joueur

### Salle d'Amélioration
- Augmente l'attaque du joueur de 3 à 8 points

## 🎨 Fonctionnalités Graphiques

- **Interface graphique** avec Pygame
- **Sprites animés** pour les personnages
- **Barres de vie** animées
- **Système de particules** pour les effets visuels
- **Log de combat** en temps réel
- **Animations d'attaque** avec effets visuels

## ⚙️ Configuration

Les paramètres du jeu peuvent être modifiés dans `config.py` :
- Statistiques des personnages
- Probabilités des types de salles
- Noms des ennemis et boss

## 🎮 Comment Jouer

1. Lancez le jeu avec `python3 roguelike_graphique_avance.py`
2. Cliquez sur "COMMENCER L'AVENTURE"
3. Survivez aux combats en cliquant sur "ATTAQUER"
4. Utilisez les salles de soin et d'amélioration
5. Traversez 5 salles pour gagner !

## 📊 Statistiques de Fin de Partie

À la fin de la partie, le jeu affiche :
- Nombre d'ennemis tués
- Nombre de boss vaincus
- Nombre de salles traversées

---

**Amusez-vous bien ! 🎮**