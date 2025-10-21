#!/usr/bin/env python3
"""
Tests unitaires pour les implémentations SOLID
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports pour les tests
import pygame
from entities import Character, Player, Enemy, Boss, PowerUp, EnemyRoom, BossRoom, HealingRoom, UpgradeRoom, PowerUpRoom
from services import ScoreManager, RoomGenerator, SoundManager, GameFactory, CombatSystem, GameService
from interfaces import IPlayer, ICharacter, IRoom, IScoreManager, IRoomGenerator, ISoundManager

class TestSOLIDPrinciples(unittest.TestCase):
    """Tests pour vérifier le respect des principes SOLID"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        pygame.init()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        pygame.quit()

class TestSingleResponsibilityPrinciple(unittest.TestCase):
    """Tests pour le principe de responsabilité unique (SRP)"""
    
    def test_character_responsibility(self):
        """Test que Character ne gère que les stats de base"""
        char = Character("Test", 100, 20)
        
        # Character ne devrait gérer que les stats de base
        self.assertEqual(char.nom, "Test")
        self.assertEqual(char.pv_max, 100)
        self.assertEqual(char.attaque, 20)
        self.assertTrue(char.est_vivant())
    
    def test_player_responsibility(self):
        """Test que Player gère uniquement les stats du joueur"""
        player = Player("TestHero")
        
        # Player gère les stats du joueur spécifiques
        self.assertEqual(player.score, 0)
        self.assertEqual(player.ennemis_tues, 0)
        self.assertEqual(player.boss_vaincus, 0)
        
        # Test des méthodes spécifiques au joueur
        player.tuer_ennemi()
        self.assertEqual(player.ennemis_tues, 1)
        self.assertGreater(player.score, 0)
    
    def test_score_manager_responsibility(self):
        """Test que ScoreManager ne gère que les scores"""
        score_manager = ScoreManager()
        
        # ScoreManager ne devrait gérer que les scores
        self.assertTrue(score_manager.est_high_score(1000))
        
        result = score_manager.ajouter_score("TestPlayer", 1000, 5, 3, 1)
        self.assertTrue(result)
        self.assertGreaterEqual(len(score_manager.get_top_scores()), 1)
    
    def test_room_generator_responsibility(self):
        """Test que RoomGenerator ne génère que des salles"""
        generator = RoomGenerator()
        
        # RoomGenerator ne devrait générer que des salles
        room = generator.generer_salle()
        self.assertIsNotNone(room)
        self.assertIsInstance(room, IRoom)

class TestOpenClosedPrinciple(unittest.TestCase):
    """Tests pour le principe ouvert/fermé (OCP)"""
    
    def test_character_extension(self):
        """Test qu'on peut étendre Character sans le modifier"""
        class MagicCharacter(Character):
            def __init__(self, nom: str, pv_max: int, attaque: int, mana: int):
                super().__init__(nom, pv_max, attaque)
                self._mana = mana
            
            @property
            def mana(self) -> int:
                return self._mana
            
            def lancer_sort(self, cible: Character) -> int:
                if self._mana > 0:
                    self._mana -= 1
                    return self.attaquer(cible) * 2
                return 0
        
        # Test de l'extension
        mage = MagicCharacter("Mage", 80, 15, 10)
        self.assertEqual(mage.mana, 10)
        
        enemy = Character("Enemy", 50, 10)
        degats = mage.lancer_sort(enemy)
        self.assertGreater(degats, 0)
        self.assertEqual(mage.mana, 9)
    
    def test_room_extension(self):
        """Test qu'on peut étendre les salles sans les modifier"""
        class TreasureRoom(HealingRoom):
            def __init__(self):
                super().__init__()
                self._nom = "Salle au Trésor"
                self._gold = 100
            
            def appliquer_effet(self, joueur: IPlayer) -> None:
                super().appliquer_effet(joueur)
                joueur.ajouter_score(self._gold)
                print(f"Vous trouvez {self._gold} pièces d'or!")
        
        # Test de l'extension
        treasure_room = TreasureRoom()
        player = Player()
        initial_score = player.score
        
        treasure_room.entrer(player)
        
        self.assertGreater(player.score, initial_score)
        self.assertGreater(player.pv_actuels, player.pv_max * 0.8)  # Soigné

class TestLiskovSubstitutionPrinciple(unittest.TestCase):
    """Tests pour le principe de substitution de Liskov (LSP)"""
    
    def test_character_substitution(self):
        """Test que toutes les sous-classes de Character sont substituables"""
        characters = [
            Character("Base", 100, 20),
            Player("Hero"),
            Enemy(1),
            Boss(1)
        ]
        
        for char in characters:
            # Tous doivent respecter le contrat de Character
            self.assertIsInstance(char, Character)
            self.assertIsInstance(char.nom, str)
            self.assertIsInstance(char.pv_max, int)
            self.assertIsInstance(char.pv_actuels, int)
            self.assertIsInstance(char.attaque, int)
            self.assertIsInstance(char.est_vivant(), bool)
            
            # Test d'attaque
            target = Character("Target", 50, 10)
            degats = char.attaquer(target)
            self.assertIsInstance(degats, int)
            self.assertGreaterEqual(degats, 0)
    
    def test_room_substitution(self):
        """Test que toutes les sous-classes de Room sont substituables"""
        rooms = [
            EnemyRoom(1),
            BossRoom(1),
            HealingRoom(),
            UpgradeRoom(),
            PowerUpRoom()
        ]
        
        player = Player()
        
        for room in rooms:
            # Toutes doivent respecter le contrat de Room
            self.assertIsInstance(room, IRoom)
            self.assertIsInstance(room.nom, str)
            
            # Test d'entrée
            result = room.entrer(player)
            self.assertIsInstance(result, bool)

class TestInterfaceSegregationPrinciple(unittest.TestCase):
    """Tests pour le principe de ségrégation des interfaces (ISP)"""
    
    def test_player_implements_correct_interfaces(self):
        """Test que Player implémente les bonnes interfaces"""
        player = Player()
        
        # Player doit implémenter IPlayer
        self.assertIsInstance(player, IPlayer)
        
        # IPlayer hérite de ICharacter
        self.assertIsInstance(player, ICharacter)
        
        # Test des méthodes spécifiques à IPlayer
        self.assertIsInstance(player.score, int)
        self.assertIsInstance(player.ennemis_tues, int)
        self.assertIsInstance(player.boss_vaincus, int)
    
    def test_services_implement_correct_interfaces(self):
        """Test que les services implémentent les bonnes interfaces"""
        # ScoreManager
        score_manager = ScoreManager()
        self.assertIsInstance(score_manager, IScoreManager)
        
        # RoomGenerator
        room_generator = RoomGenerator()
        self.assertIsInstance(room_generator, IRoomGenerator)
        
        # SoundManager
        sound_manager = SoundManager()
        self.assertIsInstance(sound_manager, ISoundManager)

class TestDependencyInversionPrinciple(unittest.TestCase):
    """Tests pour le principe d'inversion de dépendance (DIP)"""
    
    def test_game_service_depends_on_abstractions(self):
        """Test que GameService dépend des abstractions"""
        factory = GameFactory()
        game_service = GameService(factory)
        
        # GameService doit pouvoir fonctionner avec n'importe quelle implémentation
        game_service.start_game(1)
        
        player = game_service.get_player()
        self.assertIsInstance(player, IPlayer)
        
        room = game_service.generate_next_room()
        self.assertIsInstance(room, IRoom)
    
    def test_factory_creates_abstractions(self):
        """Test que la factory crée des abstractions"""
        factory = GameFactory()
        
        # La factory doit créer des implémentations des interfaces
        player = factory.create_player()
        self.assertIsInstance(player, IPlayer)
        
        enemy = factory.create_enemy()
        self.assertIsInstance(enemy, ICharacter)
        
        room_generator = factory.create_room_generator()
        self.assertIsInstance(room_generator, IRoomGenerator)
        
        score_manager = factory.create_score_manager()
        self.assertIsInstance(score_manager, IScoreManager)
        
        sound_manager = factory.create_sound_manager()
        self.assertIsInstance(sound_manager, ISoundManager)

class TestCombatSystem(unittest.TestCase):
    """Tests pour le système de combat"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.combat_system = CombatSystem()
        self.player = Player("TestHero")
        self.enemy = Enemy(1)
    
    def test_combat_start(self):
        """Test du démarrage d'un combat"""
        result = self.combat_system.start_combat(self.player, self.enemy)
        self.assertTrue(result)
        
        # Combat avec joueur mort
        self.player._pv_actuels = 0
        result = self.combat_system.start_combat(self.player, self.enemy)
        self.assertFalse(result)
    
    def test_player_attack(self):
        """Test de l'attaque du joueur"""
        initial_hp = self.enemy.pv_actuels
        degats = self.combat_system.player_attack(self.player, self.enemy)
        
        self.assertGreater(degats, 0)
        self.assertLess(self.enemy.pv_actuels, initial_hp)
    
    def test_enemy_attack(self):
        """Test de l'attaque de l'ennemi"""
        initial_hp = self.player.pv_actuels
        degats = self.combat_system.enemy_attack(self.enemy, self.player)
        
        self.assertGreater(degats, 0)
        self.assertLess(self.player.pv_actuels, initial_hp)
    
    def test_combat_over(self):
        """Test de la fin de combat"""
        # Combat en cours
        self.assertFalse(self.combat_system.is_combat_over(self.player, self.enemy))
        
        # Joueur mort
        self.player._pv_actuels = 0
        self.assertTrue(self.combat_system.is_combat_over(self.player, self.enemy))
        
        # Ennemi mort
        self.player._pv_actuels = 100
        self.enemy._pv_actuels = 0
        self.assertTrue(self.combat_system.is_combat_over(self.player, self.enemy))

class TestGameService(unittest.TestCase):
    """Tests pour le service principal du jeu"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.factory = GameFactory()
        self.game_service = GameService(self.factory)
    
    def test_game_initialization(self):
        """Test de l'initialisation du jeu"""
        self.game_service.start_game(1)
        
        player = self.game_service.get_player()
        self.assertIsInstance(player, IPlayer)
        self.assertEqual(player.nom, "Héros")
    
    def test_room_generation(self):
        """Test de la génération de salles"""
        self.game_service.start_game(1)
        
        room = self.game_service.generate_next_room()
        self.assertIsInstance(room, IRoom)
        self.assertIsNotNone(room)
    
    def test_game_over_conditions(self):
        """Test des conditions de fin de jeu"""
        self.game_service.start_game(1)
        
        # Jeu pas encore terminé
        self.assertFalse(self.game_service.is_game_over())
        self.assertFalse(self.game_service.is_victory())
        
        # Simuler la mort du joueur
        player = self.game_service.get_player()
        player._pv_actuels = 0
        self.assertTrue(self.game_service.is_game_over())
        self.assertFalse(self.game_service.is_victory())
    
    def test_difficulty_scaling(self):
        """Test de l'échelle de difficulté"""
        # Difficulté 1
        self.game_service.start_game(1)
        room1 = self.game_service.generate_next_room()
        
        # Difficulté 3
        self.game_service.start_game(3)
        room3 = self.game_service.generate_next_room()
        
        # Les salles de difficulté 3 devraient avoir des ennemis plus forts
        if hasattr(room1, 'ennemi') and hasattr(room3, 'ennemi'):
            self.assertGreaterEqual(room3.ennemi.pv_max, room1.ennemi.pv_max)

if __name__ == '__main__':
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    test_classes = [
        TestSOLIDPrinciples,
        TestSingleResponsibilityPrinciple,
        TestOpenClosedPrinciple,
        TestLiskovSubstitutionPrinciple,
        TestInterfaceSegregationPrinciple,
        TestDependencyInversionPrinciple,
        TestCombatSystem,
        TestGameService
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Sortir avec le code d'erreur approprié
    sys.exit(0 if result.wasSuccessful() else 1)
