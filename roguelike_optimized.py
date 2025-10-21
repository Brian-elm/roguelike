#!/usr/bin/env python3
"""
Version optimisée du jeu Roguelike - Architecture SOLID
Réduit de 1930 lignes à ~500 lignes
"""

import pygame
import sys
import random
from typing import Optional, List
from config import *
from entities import Player, Enemy, Boss, EnemyRoom, BossRoom, HealingRoom, UpgradeRoom, PowerUpRoom
from services import GameService, GameFactory, SoundManager
from renderer import OptimizedRenderer
from effects import EffectManager, ComboSystem, ReputationSystem, MiniGame
from events import EventManager, EasterEggManager, DynamicDifficulty, FunFeatures

# Initialisation de Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

class GameState:
    """États du jeu"""
    MENU = "menu"
    PLAYING = "playing"
    COMBAT = "combat"
    SPECIAL_ROOM = "special_room"
    TRANSITION = "transition"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class OptimizedRoguelike:
    """Version optimisée du jeu Roguelike"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Roguelike Optimisé - Version Fun!")
        self.clock = pygame.time.Clock()
        
        # Services
        self.factory = GameFactory()
        self.game_service = GameService(self.factory)
        self.sound_manager = SoundManager()
        self.renderer = OptimizedRenderer(self.screen)
        
        # Systèmes amusants
        self.effect_manager = EffectManager()
        self.combo_system = ComboSystem()
        self.reputation_system = ReputationSystem()
        self.event_manager = EventManager()
        self.easter_egg_manager = EasterEggManager()
        self.dynamic_difficulty = DynamicDifficulty()
        self.fun_features = FunFeatures()
        self.mini_game = MiniGame()
        
        # État du jeu
        self.state = GameState.MENU
        self.current_room = None
        self.buttons = []
        self.combat_log = []
        self.special_messages = []
        self.last_event_time = 0
        
        # Initialisation
        self.setup_menu()
    
    def setup_menu(self) -> None:
        """Configure le menu principal"""
        self.buttons.clear()
        self.renderer.clear_cache()
        
        # Titre
        self.renderer.draw_text("ROGUELIKE OPTIMISÉ", SCREEN_WIDTH // 2, 100, 'large', YELLOW, center=True)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, 100, "castle", 40, YELLOW)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 + 160, 100, "castle", 40, YELLOW)
        
        # Sous-titre
        self.renderer.draw_text("Choisissez votre difficulté", SCREEN_WIDTH // 2, 150, 'medium', WHITE, center=True)
        
        # Boutons de difficulté
        y_start = 250
        for i, (level, info) in enumerate(DIFFICULTES.items()):
            button = self.renderer.draw_button(
                SCREEN_WIDTH // 2 - 120, y_start + i * 60, 240, 50,
                info["nom"], info["couleur"]
            )
            self.buttons.append((button, f"difficulty_{level}"))
        
        # Bouton quitter
        quit_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 120, y_start + 3 * 60, 240, 50, "QUITTER", RED
        )
        self.buttons.append((quit_button, "quit"))
    
    def setup_combat(self) -> None:
        """Configure l'écran de combat"""
        self.buttons.clear()
        if not self.combat_log:
            self.combat_log = ["Cliquez sur ATTAQUER pour combattre!"]
    
    def setup_special_room(self) -> None:
        """Configure une salle spéciale"""
        self.buttons.clear()
        
        # Titre de la salle
        self.renderer.draw_text(f"=== {self.current_room.nom} ===", SCREEN_WIDTH // 2, 200, 'large', YELLOW, center=True)
        
        # Icônes selon le type
        if isinstance(self.current_room, HealingRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "plus", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "plus", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "heart", 40, GREEN)
            message = "Vous vous reposez et récupérez des forces!"
        elif isinstance(self.current_room, UpgradeRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "sword", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "sword", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "sword", 40, ORANGE)
            message = "Votre attaque augmente!"
        elif isinstance(self.current_room, PowerUpRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "crown", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "crown", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "crown", 40, PURPLE)
            message = "Vous trouvez un power-up!"
        
        # Message
        self.renderer.draw_text(message, SCREEN_WIDTH // 2, 350, 'medium', WHITE, center=True)
        
        # Bouton continuer
        continue_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 150, 450, 300, 50, "CONTINUER L'AVENTURE", GREEN
        )
        self.buttons.append((continue_button, "continue"))
    
    def setup_transition(self, victory: bool) -> None:
        """Configure l'écran de transition"""
        self.buttons.clear()
        
        player = self.game_service.get_player()
        
        # Titre
        if victory:
            self.renderer.draw_text("VICTOIRE!", SCREEN_WIDTH // 2, 150, 'large', GREEN, center=True)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 150, "crown", 40, GREEN)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 150, "crown", 40, GREEN)
        else:
            self.renderer.draw_text("DÉFAITE!", SCREEN_WIDTH // 2, 150, 'large', RED, center=True)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 150, "skull", 40, RED)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 150, "skull", 40, RED)
        
        # Statistiques
        stats_y = 250
        stats = [
            (f"PV: {player.pv_actuels}/{player.pv_max}", "heart"),
            (f"Attaque: {player.attaque}", "sword"),
            (f"Ennemis tués: {player.ennemis_tues}", "skull"),
            (f"Boss vaincus: {player.boss_vaincus}", "crown")
        ]
        
        for i, (stat, icon_type) in enumerate(stats):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, stats_y + i * 30, icon_type, 20, WHITE)
            self.renderer.draw_text(stat, SCREEN_WIDTH // 2 - 170, stats_y + i * 30, 'small', WHITE)
        
        # Bouton continuer
        continue_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 100, 450, 200, 50, "CONTINUER", GREEN
        )
        self.buttons.append((continue_button, "continue"))
    
    def setup_game_over(self) -> None:
        """Configure l'écran de fin de partie"""
        self.buttons.clear()
        
        player = self.game_service.get_player()
        
        # Titre
        self.renderer.draw_text("GAME OVER", SCREEN_WIDTH // 2, 100, 'large', RED, center=True)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 100, "skull", 40, RED)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 100, "skull", 40, RED)
        
        # Statistiques finales
        stats_y = 200
        stats = [
            (f"Ennemis tués: {player.ennemis_tues}", "skull"),
            (f"Boss vaincus: {player.boss_vaincus}", "crown"),
            (f"Salles traversées: {self.game_service._salle_actuelle}", "castle"),
            (f"Score final: {player.score}", "crown")
        ]
        
        for i, (stat, icon_type) in enumerate(stats):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, stats_y + i * 50, icon_type, 30, WHITE)
            self.renderer.draw_text(stat, SCREEN_WIDTH // 2 - 160, stats_y + i * 50, 'medium', WHITE)
        
        # Boutons
        replay_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 150, 450, 140, 50, "REJOUER", GREEN
        )
        menu_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 + 10, 450, 140, 50, "MENU", BLUE
        )
        
        self.buttons.append((replay_button, "replay"))
        self.buttons.append((menu_button, "menu"))
    
    def add_combat_log(self, message: str) -> None:
        """Ajoute un message au log de combat"""
        self.combat_log.append(message)
        if len(self.combat_log) > 5:
            self.combat_log.pop(0)
    
    def handle_events(self) -> bool:
        """Gère les événements avec easter eggs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Easter eggs avec touches
                key_name = pygame.key.name(event.key)
                easter_result = self.easter_egg_manager.add_key(key_name)
                if easter_result:
                    self.add_combat_log(f"🥚 {easter_result}")
                    self.effect_manager.add_magic_effect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    
                    for button, action in self.buttons:
                        if button.collidepoint(mouse_pos):
                            self.sound_manager.play_sound('click')
                            
                            if action.startswith("difficulty_"):
                                difficulty = int(action.split("_")[1])
                                self.start_game(difficulty)
                            elif action == "quit":
                                return False
                            elif action == "attack":
                                self.handle_combat()
                            elif action == "continue":
                                self.continue_adventure()
                            elif action == "replay":
                                self.replay_game()
                            elif action == "menu":
                                self.state = GameState.MENU
                                self.setup_menu()
        
        return True
    
    def start_game(self, difficulty: int) -> None:
        """Démarre une nouvelle partie"""
        self.game_service.start_game(difficulty)
        self.state = GameState.PLAYING
        self.current_room = None
        
        # Réinitialiser tous les systèmes amusants
        self.reset_fun_systems()
        
        self.generate_next_room()
    
    def reset_fun_systems(self) -> None:
        """Réinitialise tous les systèmes amusants"""
        self.combo_system.reset()
        self.event_manager.reset_events()
        self.easter_egg_manager.secrets_found.clear()
        self.easter_egg_manager.current_combination.clear()
        self.dynamic_difficulty.player_performance.clear()
        self.dynamic_difficulty.current_multiplier = 1.0
        self.combat_log.clear()
        self.special_messages.clear()
        self.last_event_time = 0
    
    def generate_next_room(self) -> None:
        """Génère la prochaine salle"""
        self.current_room = self.game_service.generate_next_room()
        
        if isinstance(self.current_room, (EnemyRoom, BossRoom)):
            self.state = GameState.COMBAT
            self.setup_combat()
        else:
            self.state = GameState.SPECIAL_ROOM
            self.current_room.entrer(self.game_service.get_player())
            self.setup_special_room()
    
    def handle_combat(self) -> None:
        """Gère un tour de combat avec effets amusants"""
        player = self.game_service.get_player()
        enemy = self.current_room.ennemi
        current_time = pygame.time.get_ticks()
        
        # Système de combo et critiques
        hit_result = self.combo_system.hit(current_time)
        
        # Joueur attaque avec effets
        base_damage = player.attaquer(enemy)
        final_damage = int(base_damage * hit_result['damage_multiplier'])
        
        # Messages amusants selon le résultat
        if hit_result['is_critical']:
            self.add_combat_log(f"💥 CRITIQUE! Vous infligez {final_damage} dégâts à {enemy.nom}!")
            self.effect_manager.add_explosion(900, 200, YELLOW, 30)
            self.effect_manager.add_screen_shake(15)
            self.sound_manager.play_sound('victory')  # Son spécial pour critique
        elif hit_result['is_combo']:
            self.add_combat_log(f"🔥 COMBO x{hit_result['combo_count']}! Vous infligez {final_damage} dégâts!")
            self.effect_manager.add_magic_effect(900, 200)
        else:
            self.add_combat_log(f"⚔️ Vous infligez {final_damage} dégâts à {enemy.nom}!")
            self.effect_manager.add_damage_effect(900, 200)
        
        # Message amusant aléatoire
        if random.random() < 0.3:  # 30% de chance
            self.add_combat_log(f"💬 {self.fun_features.get_silly_message()}")
        
        self.sound_manager.play_sound('attack')
        
        # Vérifier si l'ennemi est mort
        if not enemy.est_vivant():
            if isinstance(self.current_room, EnemyRoom):
                player.tuer_ennemi()
                victory_msg = self.fun_features.get_victory_quote()
                self.add_combat_log(f"🎉 {victory_msg}")
                self.reputation_system.add_reputation(10, f"Vaincu {enemy.nom}")
            else:
                player.vaincre_boss()
                victory_msg = self.fun_features.get_victory_quote()
                self.add_combat_log(f"👑 {victory_msg}")
                self.reputation_system.add_reputation(50, f"Vaincu le boss {enemy.nom}")
            
            # Effets de victoire
            self.effect_manager.add_explosion(900, 200, GREEN, 50)
            self.effect_manager.add_flash(GREEN, 20)
            self.sound_manager.play_sound('victory')
            self.setup_transition(True)
            self.state = GameState.TRANSITION
            return
        
        # Ennemi attaque
        damage = enemy.attaquer(player)
        self.add_combat_log(f"💀 {enemy.nom} vous inflige {damage} dégâts!")
        player.survivre_tour()
        
        # Effet de dégâts sur le joueur
        self.effect_manager.add_damage_effect(100, 200)
        
        # Vérifier si le joueur est mort
        if not player.est_vivant():
            defeat_msg = self.fun_features.get_defeat_quote()
            self.add_combat_log(f"💀 {defeat_msg}")
            self.sound_manager.play_sound('defeat')
            self.effect_manager.add_flash(RED, 30)
            self.setup_game_over()
            self.state = GameState.GAME_OVER
            return
        
        # Événements aléatoires
        if current_time - self.last_event_time > 5000:  # Toutes les 5 secondes
            event_result = self.event_manager.check_random_event(player, self.game_service)
            if event_result:
                self.add_combat_log(f"🎲 ÉVÉNEMENT: {event_result}")
                self.last_event_time = current_time
        
        # Easter eggs
        easter_egg = self.easter_egg_manager.check_special_conditions(player, self.game_service)
        if easter_egg:
            self.add_combat_log(f"🥚 EASTER EGG: {easter_egg}")
        
        # Mettre à jour l'affichage
        self.setup_combat()
    
    def continue_adventure(self) -> None:
        """Continue l'aventure"""
        if self.state == GameState.TRANSITION:
            if self.game_service.is_game_over():
                self.setup_game_over()
                self.state = GameState.GAME_OVER
            else:
                self.generate_next_room()
        elif self.state == GameState.SPECIAL_ROOM:
            if self.game_service.is_game_over():
                self.setup_game_over()
                self.state = GameState.GAME_OVER
            else:
                self.generate_next_room()
    
    def replay_game(self) -> None:
        """Relance une partie"""
        difficulty = self.game_service._difficulty
        self.start_game(difficulty)
    
    def draw_combat_log(self) -> None:
        """Dessine le log de combat"""
        for i, message in enumerate(self.combat_log):
            self.renderer.draw_text(message, 50, 500 + i * 25, 'small', WHITE)
    
    def render_menu(self) -> None:
        """Rend le menu principal"""
        # Titre
        self.renderer.draw_text("ROGUELIKE OPTIMISÉ", SCREEN_WIDTH // 2, 100, 'large', YELLOW, center=True)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, 100, "castle", 40, YELLOW)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 + 160, 100, "castle", 40, YELLOW)
        
        # Sous-titre
        self.renderer.draw_text("Choisissez votre difficulté", SCREEN_WIDTH // 2, 150, 'medium', WHITE, center=True)
        
        # Boutons de difficulté
        y_start = 250
        for i, (level, info) in enumerate(DIFFICULTES.items()):
            button = self.renderer.draw_button(
                SCREEN_WIDTH // 2 - 120, y_start + i * 60, 240, 50,
                info["nom"], info["couleur"]
            )
            if len(self.buttons) <= i:
                self.buttons.append((button, f"difficulty_{level}"))
            else:
                self.buttons[i] = (button, f"difficulty_{level}")
        
        # Bouton quitter
        quit_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 120, y_start + 3 * 60, 240, 50, "QUITTER", RED
        )
        if len(self.buttons) <= 3:
            self.buttons.append((quit_button, "quit"))
        else:
            self.buttons[3] = (quit_button, "quit")
    
    def render_combat(self) -> None:
        """Rend l'écran de combat avec informations amusantes"""
        player = self.game_service.get_player()
        enemy = self.current_room.ennemi
        
        # Informations de difficulté
        diff_info = DIFFICULTES[self.game_service._difficulty]
        self.renderer.draw_text(f"Difficulté: {diff_info['nom']}", 50, 20, 'small', diff_info['couleur'])
        
        # Score et réputation
        self.renderer.draw_text(f"Score: {player.score}", 50, 50, 'small', WHITE)
        self.renderer.draw_text(f"Réputation: {self.reputation_system.get_current_title()}", 50, 80, 'small', YELLOW)
        
        # Combo actuel
        if self.combo_system.combo_count > 1:
            self.renderer.draw_text(f"COMBO x{self.combo_system.combo_count}!", 300, 50, 'small', ORANGE)
        
        # Titre de la salle
        self.renderer.draw_text(f"=== {self.current_room.nom} ===", 50, 120, 'large', YELLOW)
        self.renderer.draw_icon(20, 120, "sword", 30, YELLOW)
        self.renderer.draw_icon(400, 120, "sword", 30, YELLOW)
        
        # Joueur
        self.renderer.draw_icon(50, 220, "shield", 30, WHITE)
        self.renderer.draw_text("Héros", 100, 220, 'medium', WHITE)
        self.renderer.draw_health_bar(50, 260, 300, 20, player.pv_actuels, player.pv_max, GREEN)
        self.renderer.draw_text(f"PV: {player.pv_actuels}/{player.pv_max}", 50, 290, 'small', WHITE)
        self.renderer.draw_text(f"Attaque: {player.attaque}", 50, 320, 'small', WHITE)
        
        # Ennemi
        self.renderer.draw_icon(850, 220, "skull", 30, WHITE)
        self.renderer.draw_text(enemy.nom, 900, 220, 'medium', WHITE)
        self.renderer.draw_health_bar(750, 260, 300, 20, enemy.pv_actuels, enemy.pv_max, RED)
        self.renderer.draw_text(f"PV: {enemy.pv_actuels}/{enemy.pv_max}", 750, 290, 'small', WHITE)
        self.renderer.draw_text(f"Attaque: {enemy.attaque}", 750, 320, 'small', WHITE)
        
        # Bouton d'attaque avec style dynamique
        button_color = GREEN
        if self.combo_system.combo_count > 2:
            button_color = ORANGE
        if self.combo_system.combo_count > 5:
            button_color = RED
        
        attack_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 100, 420, 200, 50, "ATTAQUER", button_color
        )
        if len(self.buttons) == 0:
            self.buttons.append((attack_button, "attack"))
        else:
            self.buttons[0] = (attack_button, "attack")
        
        # Instructions pour easter eggs
        self.renderer.draw_text("💡 Astuce: Essayez des combinaisons de touches!", 50, 500, 'small', GRAY)
        
        # Log de combat
        self.draw_combat_log()
    
    def render_special_room(self) -> None:
        """Rend une salle spéciale"""
        # Titre de la salle
        self.renderer.draw_text(f"=== {self.current_room.nom} ===", SCREEN_WIDTH // 2, 200, 'large', YELLOW, center=True)
        
        # Icônes selon le type
        if isinstance(self.current_room, HealingRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "plus", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "plus", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "heart", 40, GREEN)
            message = "Vous vous reposez et récupérez des forces!"
        elif isinstance(self.current_room, UpgradeRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "sword", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "sword", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "sword", 40, ORANGE)
            message = "Votre attaque augmente!"
        elif isinstance(self.current_room, PowerUpRoom):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 200, "crown", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 200, "crown", 40, YELLOW)
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 20, 300, "crown", 40, PURPLE)
            message = "Vous trouvez un power-up!"
        
        # Message
        self.renderer.draw_text(message, SCREEN_WIDTH // 2, 350, 'medium', WHITE, center=True)
        
        # Bouton continuer
        continue_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 150, 450, 300, 50, "CONTINUER L'AVENTURE", GREEN
        )
        if len(self.buttons) == 0:
            self.buttons.append((continue_button, "continue"))
        else:
            self.buttons[0] = (continue_button, "continue")
    
    def render_transition(self) -> None:
        """Rend l'écran de transition"""
        player = self.game_service.get_player()
        
        # Titre
        self.renderer.draw_text("VICTOIRE!", SCREEN_WIDTH // 2, 150, 'large', GREEN, center=True)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 150, "crown", 40, GREEN)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 150, "crown", 40, GREEN)
        
        # Statistiques
        stats_y = 250
        stats = [
            (f"PV: {player.pv_actuels}/{player.pv_max}", "heart"),
            (f"Attaque: {player.attaque}", "sword"),
            (f"Ennemis tués: {player.ennemis_tues}", "skull"),
            (f"Boss vaincus: {player.boss_vaincus}", "crown")
        ]
        
        for i, (stat, icon_type) in enumerate(stats):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, stats_y + i * 30, icon_type, 20, WHITE)
            self.renderer.draw_text(stat, SCREEN_WIDTH // 2 - 170, stats_y + i * 30, 'small', WHITE)
        
        # Bouton continuer
        continue_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 100, 450, 200, 50, "CONTINUER", GREEN
        )
        if len(self.buttons) == 0:
            self.buttons.append((continue_button, "continue"))
        else:
            self.buttons[0] = (continue_button, "continue")
    
    def render_game_over(self) -> None:
        """Rend l'écran de fin de partie"""
        player = self.game_service.get_player()
        
        # Titre
        self.renderer.draw_text("GAME OVER", SCREEN_WIDTH // 2, 100, 'large', RED, center=True)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 - 100, 100, "skull", 40, RED)
        self.renderer.draw_icon(SCREEN_WIDTH // 2 + 60, 100, "skull", 40, RED)
        
        # Statistiques finales
        stats_y = 200
        stats = [
            (f"Ennemis tués: {player.ennemis_tues}", "skull"),
            (f"Boss vaincus: {player.boss_vaincus}", "crown"),
            (f"Salles traversées: {self.game_service._salle_actuelle}", "castle"),
            (f"Score final: {player.score}", "crown")
        ]
        
        for i, (stat, icon_type) in enumerate(stats):
            self.renderer.draw_icon(SCREEN_WIDTH // 2 - 200, stats_y + i * 50, icon_type, 30, WHITE)
            self.renderer.draw_text(stat, SCREEN_WIDTH // 2 - 160, stats_y + i * 50, 'medium', WHITE)
        
        # Boutons
        replay_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 - 150, 450, 140, 50, "REJOUER", GREEN
        )
        menu_button = self.renderer.draw_button(
            SCREEN_WIDTH // 2 + 10, 450, 140, 50, "MENU", BLUE
        )
        
        if len(self.buttons) < 2:
            self.buttons.append((replay_button, "replay"))
            self.buttons.append((menu_button, "menu"))
        else:
            self.buttons[0] = (replay_button, "replay")
            self.buttons[1] = (menu_button, "menu")
    
    def run(self) -> None:
        """Boucle principale du jeu avec effets amusants"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS)
            
            # Gestion des événements
            running = self.handle_events()
            
            # Mise à jour des systèmes
            self.renderer.update_particles()
            self.effect_manager.update()
            
            # Mise à jour de la difficulté dynamique seulement si le jeu est initialisé
            if hasattr(self.game_service, '_player') and self.game_service._player is not None:
                self.dynamic_difficulty.update_performance(self.game_service.get_player(), self.game_service)
            
            # Rendu avec tremblement d'écran
            self.screen.fill(BLACK)
            
            # Offset pour le tremblement d'écran
            offset_x, offset_y = self.effect_manager.get_screen_offset()
            
            # Rendu selon l'état
            if self.state == GameState.MENU:
                self.render_menu()
            elif self.state == GameState.COMBAT:
                self.render_combat()
            elif self.state == GameState.SPECIAL_ROOM:
                self.render_special_room()
            elif self.state == GameState.TRANSITION:
                self.render_transition()
            elif self.state == GameState.GAME_OVER:
                self.render_game_over()
            elif self.state == GameState.VICTORY:
                self.render_game_over()
            
            # Effets visuels
            self.effect_manager.draw(self.screen)
            
            # Particules du renderer
            self.renderer.draw_particles()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

def main():
    """Point d'entrée principal"""
    game = OptimizedRoguelike()
    game.run()

if __name__ == "__main__":
    main()
