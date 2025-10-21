#!/usr/bin/env python3
"""
Configuration pour les tests unitaires
"""

import os
import tempfile
import json

class TestConfig:
    """Configuration pour les tests"""
    
    # Dossier temporaire pour les tests
    TEST_DIR = tempfile.mkdtemp(prefix="roguelike_test_")
    
    # Fichier de scores temporaire
    TEST_SCORES_FILE = os.path.join(TEST_DIR, "test_scores.json")
    
    # Configuration des tests
    TEST_PLAYER_NAME = "TestPlayer"
    TEST_ENEMY_NAME = "TestEnemy"
    TEST_BOSS_NAME = "TestBoss"
    
    # Valeurs de test
    TEST_PLAYER_HP = 100
    TEST_PLAYER_ATTACK = 20
    TEST_ENEMY_HP = 30
    TEST_ENEMY_ATTACK = 15
    TEST_BOSS_HP = 80
    TEST_BOSS_ATTACK = 25
    
    @classmethod
    def setup_test_environment(cls):
        """Configure l'environnement de test"""
        # Créer le dossier de test
        os.makedirs(cls.TEST_DIR, exist_ok=True)
        
        # Créer un fichier de scores de test
        test_scores = [
            {"nom": "TestPlayer1", "score": 1000, "salles": 5, "ennemis": 3, "boss": 1, "date": 1234567890},
            {"nom": "TestPlayer2", "score": 800, "salles": 4, "ennemis": 2, "boss": 1, "date": 1234567891},
            {"nom": "TestPlayer3", "score": 600, "salles": 3, "ennemis": 2, "boss": 0, "date": 1234567892}
        ]
        
        with open(cls.TEST_SCORES_FILE, 'w') as f:
            json.dump(test_scores, f, indent=2)
    
    @classmethod
    def cleanup_test_environment(cls):
        """Nettoie l'environnement de test"""
        import shutil
        try:
            shutil.rmtree(cls.TEST_DIR)
        except Exception:
            pass
    
    @classmethod
    def get_test_scores_file(cls):
        """Retourne le chemin du fichier de scores de test"""
        return cls.TEST_SCORES_FILE
