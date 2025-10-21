#!/usr/bin/env python3
"""
Script pour exécuter tous les tests unitaires
"""

import unittest
import sys
import os

def run_all_tests():
    """Exécute tous les tests unitaires"""
    
    # Ajouter le répertoire courant au path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Importer et ajouter les tests
    try:
        # Tests du code original
        from test_roguelike import (
            TestPersonnage, TestJoueur, TestEnnemi, TestBoss,
            TestPowerUp, TestSalle, TestScoreManager, 
            TestGenerateurSalles, TestJeu, TestIntegration
        )
        
        original_tests = [
            TestPersonnage, TestJoueur, TestEnnemi, TestBoss,
            TestPowerUp, TestSalle, TestScoreManager, 
            TestGenerateurSalles, TestJeu, TestIntegration
        ]
        
        for test_class in original_tests:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            test_suite.addTests(tests)
        
        print("✓ Tests du code original chargés")
        
    except ImportError as e:
        print(f"⚠ Impossible de charger les tests originaux: {e}")
    
    try:
        # Tests SOLID
        from test_solid import (
            TestSOLIDPrinciples, TestSingleResponsibilityPrinciple,
            TestOpenClosedPrinciple, TestLiskovSubstitutionPrinciple,
            TestInterfaceSegregationPrinciple, TestDependencyInversionPrinciple,
            TestCombatSystem, TestGameService
        )
        
        solid_tests = [
            TestSOLIDPrinciples, TestSingleResponsibilityPrinciple,
            TestOpenClosedPrinciple, TestLiskovSubstitutionPrinciple,
            TestInterfaceSegregationPrinciple, TestDependencyInversionPrinciple,
            TestCombatSystem, TestGameService
        ]
        
        for test_class in solid_tests:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            test_suite.addTests(tests)
        
        print("✓ Tests SOLID chargés")
        
    except ImportError as e:
        print(f"⚠ Impossible de charger les tests SOLID: {e}")
    
    # Exécuter les tests
    print("\n" + "="*60)
    print("EXÉCUTION DES TESTS UNITAIRES")
    print("="*60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
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
        return True
    else:
        print(f"\n❌ {len(result.failures + result.errors)} TEST(S) ONT ÉCHOUÉ")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
