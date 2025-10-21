#!/usr/bin/env python3
"""
Interfaces et contrats pour le jeu Roguelike
Respect des principes SOLID
"""

from abc import ABC, abstractmethod
from typing import Protocol, Any, List, Dict, Optional
import pygame

# =============================================================================
# INTERFACE SEGREGATION PRINCIPLE (ISP)
# =============================================================================

class Drawable(Protocol):
    """Interface pour les objets qui peuvent être dessinés"""
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dessine l'objet sur l'écran"""
        ...

class Updatable(Protocol):
    """Interface pour les objets qui peuvent être mis à jour"""
    
    def update(self, dt: int) -> None:
        """Met à jour l'objet"""
        ...

class Clickable(Protocol):
    """Interface pour les objets cliquables"""
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère un événement de clic"""
        ...

# =============================================================================
# SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =============================================================================

class ICharacter(ABC):
    """Interface pour tous les personnages du jeu"""
    
    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom du personnage"""
        pass
    
    @property
    @abstractmethod
    def pv_max(self) -> int:
        """Points de vie maximum"""
        pass
    
    @property
    @abstractmethod
    def pv_actuels(self) -> int:
        """Points de vie actuels"""
        pass
    
    @property
    @abstractmethod
    def attaque(self) -> int:
        """Points d'attaque"""
        pass
    
    @abstractmethod
    def est_vivant(self) -> bool:
        """Vérifie si le personnage est vivant"""
        pass
    
    @abstractmethod
    def attaquer(self, cible: 'ICharacter') -> int:
        """Attaque une cible et retourne les dégâts infligés"""
        pass
    
    @abstractmethod
    def soigner(self, points: int) -> None:
        """Soigne le personnage"""
        pass

class IPlayer(ICharacter):
    """Interface spécifique au joueur"""
    
    @property
    @abstractmethod
    def score(self) -> int:
        """Score du joueur"""
        pass
    
    @property
    @abstractmethod
    def ennemis_tues(self) -> int:
        """Nombre d'ennemis tués"""
        pass
    
    @property
    @abstractmethod
    def boss_vaincus(self) -> int:
        """Nombre de boss vaincus"""
        pass
    
    @abstractmethod
    def ajouter_score(self, points: int) -> None:
        """Ajoute des points au score"""
        pass
    
    @abstractmethod
    def tuer_ennemi(self) -> None:
        """Marque un ennemi comme tué"""
        pass
    
    @abstractmethod
    def vaincre_boss(self) -> None:
        """Marque un boss comme vaincu"""
        pass

class IRoom(ABC):
    """Interface pour toutes les salles"""
    
    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom de la salle"""
        pass
    
    @abstractmethod
    def entrer(self, joueur: IPlayer) -> bool:
        """Le joueur entre dans la salle"""
        pass

class ICombatRoom(IRoom):
    """Interface pour les salles de combat"""
    
    @property
    @abstractmethod
    def ennemi(self) -> ICharacter:
        """Ennemi de la salle"""
        pass

class ISpecialRoom(IRoom):
    """Interface pour les salles spéciales"""
    
    @abstractmethod
    def appliquer_effet(self, joueur: IPlayer) -> None:
        """Applique l'effet de la salle"""
        pass

class IPowerUp(ABC):
    """Interface pour les power-ups"""
    
    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom du power-up"""
        pass
    
    @property
    @abstractmethod
    def effet(self) -> str:
        """Type d'effet"""
        pass
    
    @property
    @abstractmethod
    def valeur(self) -> int:
        """Valeur de l'effet"""
        pass
    
    @abstractmethod
    def appliquer(self, joueur: IPlayer) -> None:
        """Applique l'effet au joueur"""
        pass
    
    @abstractmethod
    def retirer(self, joueur: IPlayer) -> None:
        """Retire l'effet du joueur"""
        pass

class IScoreManager(ABC):
    """Interface pour la gestion des scores"""
    
    @abstractmethod
    def ajouter_score(self, nom: str, score: int, salles: int, 
                     ennemis: int, boss: int) -> bool:
        """Ajoute un nouveau score"""
        pass
    
    @abstractmethod
    def est_high_score(self, score: int) -> bool:
        """Vérifie si un score est un high score"""
        pass
    
    @abstractmethod
    def get_top_scores(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retourne les meilleurs scores"""
        pass

class IRoomGenerator(ABC):
    """Interface pour le générateur de salles"""
    
    @abstractmethod
    def generer_salle(self) -> IRoom:
        """Génère une salle aléatoire"""
        pass

class ISoundManager(ABC):
    """Interface pour la gestion des sons"""
    
    @abstractmethod
    def play_sound(self, sound_name: str) -> None:
        """Joue un son"""
        pass
    
    @abstractmethod
    def set_volume(self, volume: float) -> None:
        """Définit le volume"""
        pass

class IGameState(ABC):
    """Interface pour les états du jeu"""
    
    @abstractmethod
    def enter(self) -> None:
        """Entrée dans l'état"""
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """Sortie de l'état"""
        pass
    
    @abstractmethod
    def update(self, dt: int) -> None:
        """Met à jour l'état"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère un événement"""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Dessine l'état"""
        pass

# =============================================================================
# DEPENDENCY INVERSION PRINCIPLE (DIP)
# =============================================================================

class IGameService(ABC):
    """Service principal du jeu"""
    
    @abstractmethod
    def start_game(self, difficulty: int) -> None:
        """Démarre une nouvelle partie"""
        pass
    
    @abstractmethod
    def reset_game(self, difficulty: int) -> None:
        """Réinitialise le jeu"""
        pass
    
    @abstractmethod
    def get_current_room(self) -> Optional[IRoom]:
        """Retourne la salle actuelle"""
        pass
    
    @abstractmethod
    def get_player(self) -> IPlayer:
        """Retourne le joueur"""
        pass

class IGameFactory(ABC):
    """Factory pour créer les composants du jeu"""
    
    @abstractmethod
    def create_player(self, nom: str = "Héros") -> IPlayer:
        """Crée un joueur"""
        pass
    
    @abstractmethod
    def create_enemy(self, difficulty: int = 1) -> ICharacter:
        """Crée un ennemi"""
        pass
    
    @abstractmethod
    def create_boss(self, difficulty: int = 1) -> ICharacter:
        """Crée un boss"""
        pass
    
    @abstractmethod
    def create_room_generator(self, difficulty: int = 1) -> IRoomGenerator:
        """Crée un générateur de salles"""
        pass
    
    @abstractmethod
    def create_score_manager(self) -> IScoreManager:
        """Crée un gestionnaire de scores"""
        pass
    
    @abstractmethod
    def create_sound_manager(self) -> ISoundManager:
        """Crée un gestionnaire de sons"""
        pass

# =============================================================================
# OPEN/CLOSED PRINCIPLE (OCP) - Extensions
# =============================================================================

class IGameExtension(ABC):
    """Interface pour les extensions du jeu"""
    
    @abstractmethod
    def initialize(self, game_service: IGameService) -> None:
        """Initialise l'extension"""
        pass
    
    @abstractmethod
    def update(self, dt: int) -> None:
        """Met à jour l'extension"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Nettoie l'extension"""
        pass

class IEventHandler(ABC):
    """Interface pour les gestionnaires d'événements"""
    
    @abstractmethod
    def can_handle(self, event: pygame.event.Event) -> bool:
        """Vérifie si l'événement peut être géré"""
        pass
    
    @abstractmethod
    def handle(self, event: pygame.event.Event) -> bool:
        """Gère l'événement"""
        pass

# =============================================================================
# LISKOV SUBSTITUTION PRINCIPLE (LSP) - Contrats
# =============================================================================

class ICombatSystem(ABC):
    """Interface pour le système de combat"""
    
    @abstractmethod
    def start_combat(self, player: IPlayer, enemy: ICharacter) -> bool:
        """Démarre un combat"""
        pass
    
    @abstractmethod
    def player_attack(self, player: IPlayer, enemy: ICharacter) -> int:
        """Le joueur attaque"""
        pass
    
    @abstractmethod
    def enemy_attack(self, enemy: ICharacter, player: IPlayer) -> int:
        """L'ennemi attaque"""
        pass
    
    @abstractmethod
    def is_combat_over(self, player: IPlayer, enemy: ICharacter) -> bool:
        """Vérifie si le combat est terminé"""
        pass

class IGameRenderer(ABC):
    """Interface pour le rendu du jeu"""
    
    @abstractmethod
    def render_menu(self, screen: pygame.Surface) -> None:
        """Rend le menu"""
        pass
    
    @abstractmethod
    def render_combat(self, screen: pygame.Surface, player: IPlayer, 
                     enemy: ICharacter) -> None:
        """Rend le combat"""
        pass
    
    @abstractmethod
    def render_special_room(self, screen: pygame.Surface, room: ISpecialRoom) -> None:
        """Rend une salle spéciale"""
        pass
    
    @abstractmethod
    def render_game_over(self, screen: pygame.Surface, player: IPlayer) -> None:
        """Rend l'écran de fin de partie"""
        pass
