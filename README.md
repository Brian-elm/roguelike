# Roguelike Graphique Avancé

Un jeu roguelike en Python avec Pygame, entièrement graphique et interactif avec de nombreuses améliorations dynamiques.

## 🎮 Fonctionnalités

### 🎯 Gameplay
- **Interface graphique complète** avec Pygame
- **3 niveaux de difficulté** : Normal, Difficile, Expert
- **Système de score** avec high scores sauvegardés
- **Power-ups et objets spéciaux** pour améliorer le joueur
- **Salles variées** : ennemis, boss, soin, amélioration, power-ups
- **Système de progression** adaptatif selon la difficulté

### 🎨 Visuel et Audio
- **Sprites animés** pour le joueur et les ennemis
- **Icônes visuelles** dessinées avec des formes géométriques
- **Effets de particules** améliorés pour chaque action
- **Sons synthétiques** pour toutes les interactions
- **Transitions fluides** entre les salles
- **Interface utilisateur** intuitive avec boutons et menus

### 🏆 Système de Score
- **Points pour chaque action** : tuer ennemis, survivre, traverser salles
- **High scores** sauvegardés automatiquement
- **Statistiques détaillées** : ennemis tués, boss vaincus, salles traversées
- **Power-ups** avec bonus de score

## 🚀 Installation

```bash
# Cloner le projet
git clone <votre-repo>
cd jeu

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python3 roguelike_graphique_avance.py
```

## 🎯 Comment jouer

1. **Menu principal** : Choisissez votre niveau de difficulté
   - **Normal** : 5 salles, ennemis standard
   - **Difficile** : 7 salles, ennemis plus forts
   - **Expert** : 10 salles, ennemis très puissants

2. **Combat** : Cliquez sur "ATTAQUER" pour combattre
3. **Salles spéciales** : Cliquez sur "CONTINUER L'AVENTURE" pour progresser
4. **Power-ups** : Collectez des objets pour vous renforcer
5. **Objectif** : Survivez à toutes les salles pour gagner !

## 🏗️ Architecture

### Classes principales

- **`RoguelikeGraphiqueAvance`** : Classe principale du jeu
- **`Jeu`** : Logique métier du jeu avec système de difficulté
- **`Joueur`** : Personnage avec système de score et power-ups
- **`Ennemi`** / **`Boss`** : Adversaires adaptés à la difficulté
- **`Salle`** : Différents types de salles
- **`GenerateurSalles`** : Génération aléatoire des salles

### Système de sprites et effets

- **`AnimatedSprite`** : Sprites avec animations
- **`TextSprite`** : Affichage de texte
- **`IconTextSprite`** : Texte avec icônes visuelles
- **`Button`** : Boutons interactifs
- **`HealthBar`** : Barres de vie
- **`ParticleSystem`** : Système de particules
- **`SoundManager`** : Gestionnaire de sons synthétiques

### Systèmes avancés

- **`PowerUp`** : Objets spéciaux avec effets
- **`ScoreManager`** : Gestion des scores et high scores
- **`IconDrawer`** : Dessin d'icônes géométriques

## 🎨 Personnalisation

### Modifier les statistiques

```python
# Dans le fichier principal
JOUEUR_PV_MAX = 100
JOUEUR_ATTAQUE = 20
ENNEMI_PV_MAX = 30
ENNEMI_ATTAQUE = 15
BOSS_PV_MAX = 80
BOSS_ATTAQUE = 25

# Système de score
SCORE_ENNEMI = 100
SCORE_BOSS = 500
SCORE_SALLE = 50
SCORE_SURVIE = 10
```

### Ajouter de nouveaux power-ups

```python
class PowerUp:
    def __init__(self, nom, effet, duree, valeur):
        self.nom = nom
        self.effet = effet  # 'attaque', 'defense', 'vitesse', 'regeneration'
        self.duree = duree
        self.valeur = valeur
```

### Modifier les probabilités

```python
PROBABILITES_SALLES = {
    'ennemi': 0.5,      # 50% de chance
    'boss': 0.2,        # 20% de chance
    'soin': 0.1,        # 10% de chance
    'amelioration': 0.1,  # 10% de chance
    'powerup': 0.1      # 10% de chance
}
```

## 🎵 Système Audio

Le jeu utilise des sons synthétiques générés en temps réel :
- **Attaque** : Son d'épée
- **Victoire** : Mélodie de victoire
- **Défaite** : Son grave
- **Soin** : Son apaisant
- **Amélioration** : Son de power-up
- **Clic** : Son d'interface

## 🏆 Système de Score

### Points attribués
- **Ennemi tué** : 100 points
- **Boss vaincu** : 500 points
- **Salle traversée** : 50 points
- **Tour de survie** : 10 points
- **Power-up trouvé** : 200 points

### High Scores
- Sauvegarde automatique dans `high_scores.json`
- Top 10 des meilleurs scores
- Statistiques détaillées par partie

## 🐛 Dépannage

### Problèmes courants

1. **Erreur de module** : Vérifiez que Pygame est installé
2. **Fenêtre ne s'ouvre pas** : Vérifiez les permissions d'affichage
3. **Performance lente** : Réduisez le nombre de particules
4. **Sons ne fonctionnent pas** : Vérifiez les paramètres audio

### Logs de débogage

Le jeu affiche des informations dans la console pour le débogage.

## 📝 Licence

Ce projet est sous licence MIT. Libre d'utilisation et de modification.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités
- Créer de nouveaux power-ups
- Améliorer les effets visuels

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

## 🎉 Améliorations Récentes

- ✅ Système de sons synthétiques
- ✅ Power-ups et objets spéciaux
- ✅ Système de score et high scores
- ✅ Effets de particules améliorés
- ✅ Interface plus interactive
- ✅ Sauvegarde automatique des scores
- ✅ 3 niveaux de difficulté
- ✅ Ennemis et boss adaptés à la difficulté
- ✅ Icônes visuelles géométriques
- ✅ Plus de salles selon la difficulté