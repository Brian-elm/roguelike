#!/usr/bin/env python3
"""
Version de debug pour tester la version optimisée
"""

import pygame
import sys
from config import *

def test_basic_pygame():
    """Test basique de Pygame"""
    print("🔧 Test de Pygame...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Test Pygame")
        
        font = pygame.font.Font(None, 36)
        text = font.render("Test Pygame OK!", True, WHITE)
        
        screen.fill(BLACK)
        screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        pygame.display.flip()
        
        print("✅ Pygame fonctionne correctement")
        return True
        
    except Exception as e:
        print(f"❌ Erreur Pygame: {e}")
        return False

def test_imports():
    """Test des imports"""
    print("🔧 Test des imports...")
    
    try:
        from entities import Player, Enemy, Boss
        from services import GameService, GameFactory
        from renderer import OptimizedRenderer
        print("✅ Tous les imports fonctionnent")
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_game_creation():
    """Test de création du jeu"""
    print("🔧 Test de création du jeu...")
    
    try:
        from roguelike_optimized import OptimizedRoguelike
        
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        game = OptimizedRoguelike()
        print("✅ Jeu créé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return False

def main():
    """Fonction principale de debug"""
    print("🚀 DEBUG DE LA VERSION OPTIMISÉE")
    print("=" * 50)
    
    tests = [
        test_basic_pygame,
        test_imports,
        test_game_creation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test: {e}")
            results.append(False)
    
    print("\n📊 RÉSULTATS:")
    print("=" * 50)
    
    for i, result in enumerate(results):
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"Test {i+1}: {status}")
    
    if all(results):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("La version optimisée devrait fonctionner correctement.")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
    
    pygame.quit()

if __name__ == "__main__":
    main()
