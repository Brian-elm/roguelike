#!/usr/bin/env python3
"""
Test rapide de lancement de la version optimisée avec fonctionnalités amusantes
"""

import pygame
import sys
import time
from config import *

def test_quick_launch():
    """Test rapide de lancement"""
    print("🚀 TEST RAPIDE DE LANCEMENT")
    print("=" * 40)
    
    try:
        # Test d'import
        print("🔧 Test des imports...")
        from roguelike_optimized import OptimizedRoguelike
        print("✅ Imports OK")
        
        # Test d'initialisation
        print("🔧 Test d'initialisation...")
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        game = OptimizedRoguelike()
        print("✅ Initialisation OK")
        
        # Test des systèmes amusants
        print("🔧 Test des systèmes amusants...")
        
        # Test du système de combo
        result = game.combo_system.hit(1000)
        print(f"✅ Système de combo: {result['combo_count']} combo")
        
        # Test du système de réputation
        title = game.reputation_system.get_current_title()
        print(f"✅ Système de réputation: {title}")
        
        # Test des effets
        game.effect_manager.add_explosion(100, 100, RED, 5)
        print(f"✅ Système d'effets: {len(game.effect_manager.particles)} particules")
        
        # Test des événements
        print(f"✅ Système d'événements: {len(game.event_manager.events)} événements")
        
        # Test des easter eggs
        print(f"✅ Système d'easter eggs: {len(game.easter_egg_manager.secret_combinations)} combinaisons")
        
        # Test des fonctionnalités amusantes
        message = game.fun_features.get_silly_message()
        print(f"✅ Messages amusants: '{message[:30]}...'")
        
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("La version optimisée avec fonctionnalités amusantes est prête!")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        pygame.quit()
        return False

if __name__ == "__main__":
    success = test_quick_launch()
    if success:
        print("\n🚀 Vous pouvez maintenant lancer le jeu avec:")
        print("python3 roguelike_optimized.py")
    sys.exit(0 if success else 1)
