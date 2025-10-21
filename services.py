#!/usr/bin/env python3
"""
Services du jeu Roguelike - Implémentations concrètes
Respect des principes SOLID
"""

import json
import os
import random
import pygame
import math
from typing import List, Dict, Any, Optional
from interfaces import (
    IScoreManager, IRoomGenerator, ISoundManager, IGameService,
    IGameFactory, ICombatSystem, IGameRenderer, IPlayer, ICharacter, IRoom
)
from entities import Player, Enemy, Boss, EnemyRoom, BossRoom, HealingRoom, UpgradeRoom, PowerUpRoom

# =============================================================================
# SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =============================================================================

class ScoreManager(IScoreManager):
    """Gestionnaire de scores - SRP: Gère uniquement les scores"""
    
    def __init__(self, filename: str = "high_scores.json"):
        self._filename = filename
        self._high_scores: List[Dict[str, Any]] = self._load_scores()
    
    def _load_scores(self) -> List[Dict[str, Any]]:
        """Charge les scores depuis le fichier"""
        try:
            if os.path.exists(self._filename):
                with open(self._filename, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_scores(self) -> None:
        """Sauvegarde les scores dans le fichier"""
        try:
            with open(self._filename, 'w') as f:
                json.dump(self._high_scores, f, indent=2)
        except Exception:
            pass
    
    def ajouter_score(self, nom: str, score: int, salles: int, 
                     ennemis: int, boss: int) -> bool:
        """Ajoute un nouveau score"""
        nouveau_score = {
            'nom': nom,
            'score': score,
            'salles': salles,
            'ennemis': ennemis,
            'boss': boss,
            'date': pygame.time.get_ticks() // 1000
        }
        
        self._high_scores.append(nouveau_score)
        self._high_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Garder seulement les 10 meilleurs scores
        if len(self._high_scores) > 10:
            self._high_scores = self._high_scores[:10]
        
        self._save_scores()
        return nouveau_score in self._high_scores[:10]
    
    def est_high_score(self, score: int) -> bool:
        """Vérifie si un score est un high score"""
        if len(self._high_scores) < 10:
            return True
        return score > self._high_scores[-1]['score']
    
    def get_top_scores(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retourne les meilleurs scores"""
        return self._high_scores[:limit]

class RoomGenerator(IRoomGenerator):
    """Générateur de salles - SRP: Génère uniquement des salles"""
    
    # Probabilités des types de salles
    PROBABILITES = {
        'ennemi': 0.5,
        'boss': 0.2,
        'soin': 0.1,
        'amelioration': 0.1,
        'powerup': 0.1
    }
    
    def __init__(self, difficulty: int = 1):
        self._difficulty = difficulty
        self._derniere_salle_speciale = False
    
    def generer_salle(self) -> IRoom:
        """Génère une salle aléatoire selon les probabilités"""
        rand = random.random()
        cumul = 0
        
        # Si la dernière salle était spéciale, forcer un ennemi ou boss
        if self._derniere_salle_speciale:
            if rand < 0.7:  # 70% de chance d'ennemi
                self._derniere_salle_speciale = False
                return EnemyRoom(self._difficulty)
            else:  # 30% de chance de boss
                self._derniere_salle_speciale = False
                return BossRoom(self._difficulty)
        
        # Probabilités normales
        for type_salle, proba in self.PROBABILITES.items():
            cumul += proba
            if rand <= cumul:
                if type_salle == 'ennemi':
                    self._derniere_salle_speciale = False
                    return EnemyRoom(self._difficulty)
                elif type_salle == 'boss':
                    self._derniere_salle_speciale = False
                    return BossRoom(self._difficulty)
                elif type_salle == 'soin':
                    self._derniere_salle_speciale = True
                    return HealingRoom()
                elif type_salle == 'amelioration':
                    self._derniere_salle_speciale = True
                    return UpgradeRoom()
                elif type_salle == 'powerup':
                    self._derniere_salle_speciale = True
                    return PowerUpRoom()
        
        # Par défaut, retourner une salle d'ennemi
        self._derniere_salle_speciale = False
        return EnemyRoom(self._difficulty)

class SoundManager(ISoundManager):
    """Gestionnaire de sons - SRP: Gère uniquement les sons"""
    
    def __init__(self):
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._volume = 0.5
        self._initialized = False
        self._try_initialize()
    
    def _try_initialize(self):
        """Tente d'initialiser le système audio"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._initialized = True
            self._create_synthetic_sounds()
        except Exception:
            self._initialized = False
    
    def _create_synthetic_sounds(self) -> None:
        """Crée des sons synthétiques pour le jeu"""
        if not self._initialized:
            return
        
        try:
            self._sounds['attack'] = self._create_tone(440, 0.1, 'square')
            self._sounds['victory'] = self._create_victory_melody()
            self._sounds['defeat'] = self._create_tone(220, 0.5, 'sine')
            self._sounds['heal'] = self._create_tone(660, 0.2, 'sine')
            self._sounds['upgrade'] = self._create_tone(880, 0.15, 'square')
            self._sounds['click'] = self._create_tone(800, 0.05, 'square')
        except Exception:
            # Si la création des sons échoue, on continue sans sons
            pass
    
    def _create_tone(self, frequency: int, duration: float, wave_type: str = 'sine') -> pygame.mixer.Sound:
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
            if i < frames * 0.1:
                envelope = i / (frames * 0.1)
            elif i > frames * 0.9:
                envelope = (frames - i) / (frames * 0.1)
            
            sample = int(sample * envelope)
            arr.append([sample, sample])
        
        try:
            import numpy as np
            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
        except ImportError:
            sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
        
        sound.set_volume(self._volume)
        return sound
    
    def _create_victory_melody(self) -> pygame.mixer.Sound:
        """Crée une mélodie de victoire"""
        notes = [523, 659, 784, 1047]  # C, E, G, C
        duration = 0.2
        sample_rate = 22050
        arr = []
        
        for frequency in notes:
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
        
        try:
            import numpy as np
            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
        except ImportError:
            sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
        
        sound.set_volume(self._volume)
        return sound
    
    def play_sound(self, sound_name: str) -> None:
        """Joue un son"""
        if self._initialized and sound_name in self._sounds:
            try:
                self._sounds[sound_name].play()
            except Exception:
                pass  # Ignorer les erreurs de lecture
    
    def set_volume(self, volume: float) -> None:
        """Définit le volume des effets sonores"""
        self._volume = volume
        if self._initialized:
            for sound in self._sounds.values():
                try:
                    sound.set_volume(volume)
                except Exception:
                    pass  # Ignorer les erreurs de volume

# =============================================================================
# DEPENDENCY INVERSION PRINCIPLE (DIP)
# =============================================================================

class GameFactory(IGameFactory):
    """Factory pour créer les composants du jeu - DIP"""
    
    def create_player(self, nom: str = "Héros") -> IPlayer:
        """Crée un joueur"""
        return Player(nom)
    
    def create_enemy(self, difficulty: int = 1) -> ICharacter:
        """Crée un ennemi"""
        return Enemy(difficulty)
    
    def create_boss(self, difficulty: int = 1) -> ICharacter:
        """Crée un boss"""
        return Boss(difficulty)
    
    def create_room_generator(self, difficulty: int = 1) -> IRoomGenerator:
        """Crée un générateur de salles"""
        return RoomGenerator(difficulty)
    
    def create_score_manager(self) -> IScoreManager:
        """Crée un gestionnaire de scores"""
        return ScoreManager()
    
    def create_sound_manager(self) -> ISoundManager:
        """Crée un gestionnaire de sons"""
        return SoundManager()

class CombatSystem(ICombatSystem):
    """Système de combat - SRP: Gère uniquement le combat"""
    
    def start_combat(self, player: IPlayer, enemy: ICharacter) -> bool:
        """Démarre un combat"""
        return player.est_vivant() and enemy.est_vivant()
    
    def player_attack(self, player: IPlayer, enemy: ICharacter) -> int:
        """Le joueur attaque"""
        return player.attaquer(enemy)
    
    def enemy_attack(self, enemy: ICharacter, player: IPlayer) -> int:
        """L'ennemi attaque"""
        return enemy.attaquer(player)
    
    def is_combat_over(self, player: IPlayer, enemy: ICharacter) -> bool:
        """Vérifie si le combat est terminé"""
        return not player.est_vivant() or not enemy.est_vivant()

class GameService(IGameService):
    """Service principal du jeu - DIP: Dépend des abstractions"""
    
    def __init__(self, factory: IGameFactory):
        self._factory = factory
        self._player: Optional[IPlayer] = None
        self._current_room: Optional[IRoom] = None
        self._room_generator: Optional[IRoomGenerator] = None
        self._score_manager: Optional[IScoreManager] = None
        self._sound_manager: Optional[ISoundManager] = None
        self._combat_system: Optional[ICombatSystem] = None
        self._difficulty = 1
        self._salle_actuelle = 0
        self._salles_max = 5
    
    def start_game(self, difficulty: int) -> None:
        """Démarre une nouvelle partie"""
        self._difficulty = difficulty
        self._player = self._factory.create_player()
        self._room_generator = self._factory.create_room_generator(difficulty)
        self._score_manager = self._factory.create_score_manager()
        self._sound_manager = self._factory.create_sound_manager()
        self._combat_system = CombatSystem()
        
        # Définir le nombre de salles selon la difficulté
        if difficulty == 1:
            self._salles_max = 5
        elif difficulty == 2:
            self._salles_max = 7
        elif difficulty == 3:
            self._salles_max = 10
        
        self._salle_actuelle = 0
        self._current_room = None
    
    def reset_game(self, difficulty: int) -> None:
        """Réinitialise le jeu"""
        self.start_game(difficulty)
    
    def get_current_room(self) -> Optional[IRoom]:
        """Retourne la salle actuelle"""
        return self._current_room
    
    def get_player(self) -> IPlayer:
        """Retourne le joueur"""
        if self._player is None:
            raise RuntimeError("Jeu non initialisé")
        return self._player
    
    def generate_next_room(self) -> IRoom:
        """Génère la prochaine salle"""
        if self._room_generator is None:
            raise RuntimeError("Générateur de salles non initialisé")
        
        self._current_room = self._room_generator.generer_salle()
        self._salle_actuelle += 1
        return self._current_room
    
    def is_game_over(self) -> bool:
        """Vérifie si le jeu est terminé"""
        if self._player is None:
            return True
        return not self._player.est_vivant() or self._salle_actuelle >= self._salles_max
    
    def is_victory(self) -> bool:
        """Vérifie si le joueur a gagné"""
        if self._player is None:
            return False
        return self._player.est_vivant() and self._salle_actuelle >= self._salles_max
