# 🎮 Roguelike Graphique Avancé - Architecture SOLID

Un jeu roguelike complet avec interface graphique, respectant les principes SOLID, avec système de sons, power-ups, scores et niveaux de difficulté.

## 🏗️ Architecture SOLID

Ce projet implémente une architecture respectant les principes SOLID :

- **S** - Single Responsibility Principle
- **O** - Open/Closed Principle  
- **L** - Liskov Substitution Principle
- **I** - Interface Segregation Principle
- **D** - Dependency Inversion Principle

### 📁 Structure Modulaire

```
jeu/
├── roguelike_graphique_avance.py  # Jeu principal (version graphique)
├── interfaces.py                   # Interfaces et contrats SOLID
├── entities.py                     # Entités du jeu (SRP)
├── services.py                     # Services et managers (DIP)
├── test_roguelike.py              # Tests unitaires du code original
├── test_solid.py                  # Tests unitaires SOLID
├── run_tests.py                   # Script d'exécution des tests
├── test_config.py                 # Configuration des tests
├── ARCHITECTURE_SOLID.md          # Documentation architecture
└── README.md                      # Cette documentation
```

## 🚀 Fonctionnalités

### 🎯 Gameplay
- **Combat au tour par tour** : Le joueur attaque toujours en premier
- **5 types de salles** : Ennemis, Boss, Soin, Amélioration, Power-Up
- **Système de progression** : Score, ennemis tués, boss vaincus
- **3 niveaux de difficulté** : Normal (5 salles), Difficile (7 salles), Expert (10 salles)

### 🎨 Interface Graphique
- **Design moderne** avec icônes géométriques
- **Barres de vie animées** pour le joueur et les ennemis
- **Écrans de transition** entre les salles
- **Interface intuitive** avec boutons cliquables

### 🔊 Système Audio
- **Sons synthétiques** pour tous les événements
- **Effets sonores** : Attaque, victoire, défaite, soin, amélioration
- **Mélodie de victoire** pour les boss
- **Contrôle du volume** intégré

### ⚡ Power-Ups
- **Potion de Force** : Augmente l'attaque
- **Potion de Soin** : Restaure les PV
- **Armure Magique** : Augmente la défense
- **Bottes de Vitesse** : Augmente la vitesse

### 🏆 Système de Score
- **Score en temps réel** affiché pendant le jeu
- **High scores** sauvegardés automatiquement
- **Statistiques détaillées** : Ennemis tués, boss vaincus, salles traversées
- **Bonus de score** pour différentes actions

### 🎲 Génération Procédurale
- **Salles aléatoires** avec probabilités équilibrées
- **Évite les salles spéciales consécutives** pour un gameplay équilibré
- **Ennemis et boss** avec stats adaptées à la difficulté

## 🧪 Tests Unitaires

### Couverture Complète
- **50 tests unitaires** couvrant tous les aspects
- **Tests de conformité SOLID** pour chaque principe
- **Tests d'intégration** pour les interactions
- **Tests de régression** pour la stabilité

### Exécution des Tests
```bash
# Exécuter tous les tests
python3 run_tests.py

# Exécuter les tests SOLID uniquement
python3 test_solid.py

# Exécuter les tests originaux uniquement
python3 test_roguelike.py
```

### Résultats des Tests
```
Tests exécutés: 50
Échecs: 0
Erreurs: 0
Succès: 50

🎉 TOUS LES TESTS SONT PASSÉS!
```

## 🎮 Comment Jouer

1. **Lancez le jeu** : `python3 roguelike_graphique_avance.py`
2. **Choisissez la difficulté** : Normal, Difficile, ou Expert
3. **Explorez les salles** et combattez les ennemis
4. **Utilisez les salles spéciales** pour vous soigner et vous améliorer
5. **Vainquez les boss** pour progresser
6. **Atteignez la fin** pour voir votre score final

## 🎯 Types de Salles

### ⚔️ Salle d'Ennemi
- **Ennemis variés** : Gobelin, Orc, Squelette, Loup, Araignée
- **Combat au tour par tour** avec le joueur qui attaque en premier
- **Score** : 100 points par ennemi tué

### 👑 Salle de Boss
- **Boss puissants** : Dragon, Liche, Démon, Géant, Hydre
- **Stats augmentées** selon la difficulté
- **Score** : 500 points par boss vaincu

### ❤️ Salle de Soin
- **Restaure 15%** des PV maximum
- **Pas de combat** requis
- **Score** : 50 points pour traverser

### ⚡ Salle d'Amélioration
- **Augmente l'attaque** de 3 à 8 points
- **Amélioration permanente**
- **Score** : 50 points pour traverser

### 🎁 Salle de Power-Up
- **Power-up aléatoire** avec effet temporaire ou permanent
- **Effets variés** : Attaque, défense, soin, vitesse
- **Score** : 200 points pour trouver un power-up

## 🏆 Système de Score

### Points Attribués
- **Ennemi tué** : 100 points
- **Boss vaincu** : 500 points
- **Survie d'un tour** : 10 points
- **Salle traversée** : 50 points
- **Power-up trouvé** : 200 points

### High Scores
- **Sauvegarde automatique** des 10 meilleurs scores
- **Affichage** du nom, score, salles, ennemis et boss
- **Fichier** : `high_scores.json`

## 🎚️ Niveaux de Difficulté

### 🟢 Normal
- **5 salles** à traverser
- **Ennemis** : Stats de base
- **Boss** : Stats de base
- **Idéal pour** : Débutants

### 🟠 Difficile
- **7 salles** à traverser
- **Ennemis** : +50% PV, +30% attaque
- **Boss** : +70% PV, +50% attaque
- **Idéal pour** : Joueurs expérimentés

### 🔴 Expert
- **10 salles** à traverser
- **Ennemis** : +100% PV, +60% attaque
- **Boss** : +140% PV, +100% attaque
- **Idéal pour** : Experts

## 🛠️ Installation

### Prérequis
- Python 3.7+
- Pygame 2.0+

### Installation
```bash
# Cloner le projet
git clone <repository>
cd jeu

# Installer les dépendances
pip install pygame

# Lancer le jeu
python3 roguelike_graphique_avance.py
```

## 🏗️ Architecture SOLID

### Single Responsibility Principle (SRP)
Chaque classe a une seule responsabilité :
- `Character` : Stats de base
- `Player` : Stats du joueur
- `ScoreManager` : Gestion des scores
- `RoomGenerator` : Génération de salles

### Open/Closed Principle (OCP)
Le code est ouvert à l'extension, fermé à la modification :
```python
class MagicCharacter(Character):
    def lancer_sort(self, cible):
        # Extension sans modification de Character
```

### Liskov Substitution Principle (LSP)
Toutes les sous-classes sont substituables :
```python
characters = [Character(), Player(), Enemy(), Boss()]
for char in characters:
    char.attaquer(target)  # Tous fonctionnent
```

### Interface Segregation Principle (ISP)
Interfaces spécifiques et cohérentes :
- `ICharacter` : Interface de base
- `IPlayer` : Interface spécifique au joueur
- `IRoom` : Interface de base pour les salles

### Dependency Inversion Principle (DIP)
Dépendance des abstractions, pas des implémentations :
```python
class GameService:
    def __init__(self, factory: IGameFactory):
        self._factory = factory  # Dépend de l'abstraction
```

## 🎨 Personnalisation

### Modifier les Probabilités des Salles
```python
PROBABILITES_SALLES = {
    'ennemi': 0.5,      # 50% de chance
    'boss': 0.2,        # 20% de chance
    'soin': 0.1,        # 10% de chance
    'amelioration': 0.1, # 10% de chance
    'powerup': 0.1      # 10% de chance
}
```

### Ajouter de Nouveaux Ennemis
```python
NOMS_ENNEMIS = ["Gobelin", "Orc", "Squelette", "Loup", "Araignée", "VotreEnnemi"]
```

### Modifier les Stats
```python
JOUEUR_PV_MAX = 100
JOUEUR_ATTAQUE = 20
ENNEMI_PV_MAX = 30
ENNEMI_ATTAQUE = 15
```

## 🐛 Dépannage

### Problèmes Courants
1. **Erreur de couleur** : Vérifiez que Pygame est correctement installé
2. **Sons qui ne marchent pas** : Le jeu fonctionne sans sons si l'audio n'est pas disponible
3. **Fichier de scores** : Créé automatiquement au premier lancement

### Support
- Vérifiez que Python 3.7+ est installé
- Vérifiez que Pygame 2.0+ est installé
- Consultez les logs d'erreur pour plus de détails

## 🎉 Améliorations Futures

- [ ] **Système d'inventaire** avec objets collectibles
- [ ] **Classes de personnages** (Guerrier, Mage, Archer)
- [ ] **Système de magie** avec sorts et mana
- [ ] **Salles secrètes** et événements spéciaux
- [ ] **Système de guildes** et classements
- [ ] **Mode multijoueur** local
- [ ] **Éditeur de niveaux** intégré
- [ ] **Système de sauvegarde** de progression

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer le code existant
- Ajouter de nouveaux tests

## 🎮 Amusez-vous bien !

Profitez de ce roguelike complet avec architecture SOLID, tests unitaires et toutes ses fonctionnalités avancées. Que la chance soit avec vous dans vos aventures !