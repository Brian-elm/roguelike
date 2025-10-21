#!/usr/bin/env python3
"""
Tests pour les nouvelles fonctionnalités amusantes
"""

import pygame
import sys
import unittest
from config import *
from effects import EffectManager, ComboSystem, ReputationSystem, MiniGame
from events import EventManager, EasterEggManager, DynamicDifficulty, FunFeatures

class TestFunFeatures(unittest.TestCase):
    """Tests pour les fonctionnalités amusantes"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        pygame.init()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        pygame.quit()
    
    def test_effect_manager(self):
        """Test du gestionnaire d'effets"""
        effect_manager = EffectManager()
        
        # Test d'ajout d'effets
        effect_manager.add_explosion(100, 100, RED, 10)
        effect_manager.add_heal_effect(200, 200)
        effect_manager.add_damage_effect(300, 300)
        effect_manager.add_magic_effect(400, 400)
        
        # Vérifier que les particules sont ajoutées
        self.assertGreater(len(effect_manager.particles), 0)
        
        # Test de mise à jour
        effect_manager.update()
        
        # Test de tremblement d'écran
        effect_manager.add_screen_shake(10)
        self.assertEqual(effect_manager.screen_shake, 10)
        
        # Test de flash
        effect_manager.add_flash(WHITE, 5)
        self.assertEqual(effect_manager.flash_effect, 5)
    
    def test_combo_system(self):
        """Test du système de combos"""
        combo_system = ComboSystem()
        
        # Premier coup (last_hit_time = 0, donc sera considéré comme combo)
        result1 = combo_system.hit(1000)
        self.assertEqual(result1['combo_count'], 1)
        # Le premier coup est considéré comme combo car last_hit_time = 0
        
        # Deuxième coup rapide (combo)
        result2 = combo_system.hit(1500)
        self.assertEqual(result2['combo_count'], 2)
        self.assertTrue(result2['is_combo'])
        
        # Coup après timeout (reset)
        result3 = combo_system.hit(5000)
        self.assertEqual(result3['combo_count'], 1)
        self.assertFalse(result3['is_combo'])
    
    def test_reputation_system(self):
        """Test du système de réputation"""
        reputation = ReputationSystem()
        
        # Test d'ajout de réputation
        result = reputation.add_reputation(50, "Test")
        self.assertEqual(reputation.reputation, 50)
        self.assertEqual(reputation.get_current_title(), "Novice")
        
        # Test de progression
        reputation.add_reputation(100, "Test")
        self.assertEqual(reputation.get_current_title(), "Aventurier")
        
        # Test de niveau de réputation (150 points = Célèbre)
        self.assertEqual(reputation.get_reputation_level(), "Célèbre")
    
    def test_event_manager(self):
        """Test du gestionnaire d'événements"""
        event_manager = EventManager()
        
        # Mock player et game_service
        class MockPlayer:
            def __init__(self):
                self.score = 0
                self.pv_actuels = 100
                self.pv_max = 100
                self.attaque = 20
            
            def ajouter_score(self, amount):
                self.score += amount
            
            def soigner(self, amount):
                self.pv_actuels = min(self.pv_max, self.pv_actuels + amount)
            
            def augmenter_attaque(self, amount):
                self.attaque += amount
        
        class MockGameService:
            def __init__(self):
                self._salle_actuelle = 1
        
        player = MockPlayer()
        game_service = MockGameService()
        
        # Test d'événement aléatoire (peut ne pas se déclencher)
        result = event_manager.check_random_event(player, game_service)
        # Le résultat peut être None si aucun événement ne se déclenche
        
        # Test de reset
        event_manager.reset_events()
        for event in event_manager.events:
            self.assertFalse(event.used)
    
    def test_easter_egg_manager(self):
        """Test du gestionnaire d'easter eggs"""
        easter_egg = EasterEggManager()
        
        # Test du code Konami
        konami_keys = ["up", "up", "down", "down", "left", "right", "left", "right"]
        for key in konami_keys:
            result = easter_egg.add_key(key)
        
        # Le dernier devrait déclencher l'easter egg
        self.assertIn("konami", easter_egg.secrets_found)
        
        # Test du mot POWER
        power_keys = ["p", "o", "w", "e", "r"]
        for key in power_keys:
            result = easter_egg.add_key(key)
        
        self.assertIn("power", easter_egg.secrets_found)
    
    def test_fun_features(self):
        """Test des fonctionnalités amusantes"""
        fun = FunFeatures()
        
        # Test des messages
        silly_msg = fun.get_silly_message()
        self.assertIsInstance(silly_msg, str)
        self.assertGreater(len(silly_msg), 0)
        
        victory_quote = fun.get_victory_quote()
        self.assertIsInstance(victory_quote, str)
        self.assertGreater(len(victory_quote), 0)
        
        defeat_quote = fun.get_defeat_quote()
        self.assertIsInstance(defeat_quote, str)
        self.assertGreater(len(defeat_quote), 0)
        
        encouragement = fun.get_encouragement()
        self.assertIsInstance(encouragement, str)
        self.assertGreater(len(encouragement), 0)
    
    def test_dynamic_difficulty(self):
        """Test de la difficulté dynamique"""
        difficulty = DynamicDifficulty()
        
        # Mock player et game_service
        class MockPlayer:
            def __init__(self):
                self.score = 500
        
        class MockGameService:
            def __init__(self):
                self._salle_actuelle = 3
        
        player = MockPlayer()
        game_service = MockGameService()
        
        # Test de mise à jour de performance
        difficulty.update_performance(player, game_service)
        self.assertEqual(len(difficulty.player_performance), 1)
        
        # Test d'ajustement de difficulté
        multiplier = difficulty.adjust_difficulty()
        self.assertIsInstance(multiplier, float)
        self.assertGreaterEqual(multiplier, 0.5)
        self.assertLessEqual(multiplier, 2.0)
    
    def test_mini_game(self):
        """Test du mini-jeu"""
        mini_game = MiniGame()
        
        # Test de démarrage du mini-jeu de timing
        mini_game.start_timing_game(100)
        self.assertTrue(mini_game.active)
        self.assertEqual(mini_game.target_time, 100)
        
        # Test de mise à jour
        result = mini_game.update_timing_game(50)
        self.assertFalse(result)  # Pas encore terminé
        
        result = mini_game.update_timing_game(100)
        self.assertTrue(result)  # Terminé
        self.assertFalse(mini_game.active)

def run_tests():
    """Exécute tous les tests"""
    print("🧪 TESTS DES FONCTIONNALITÉS AMUSANTES")
    print("=" * 50)
    
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    test_classes = [TestFunFeatures]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Afficher le résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print("\nÉCHECS:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERREURS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Les fonctionnalités amusantes fonctionnent correctement!")
        return True
    else:
        print(f"\n❌ {len(result.failures + result.errors)} TEST(S) ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
