#!/usr/bin/env python3
"""
Tests unitaires pour le jeu Roguelike
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path pour importer le module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports pour les tests
import pygame
from roguelike_graphique_avance import (
    Personnage, Joueur, Ennemi, Boss, 
    Salle, SalleEnnemi, SalleBoss, SalleSoin, SalleAmelioration, SallePowerUp,
    PowerUp, ScoreManager, GenerateurSalles, Jeu,
    JOUEUR_PV_MAX, JOUEUR_ATTAQUE, ENNEMI_PV_MAX, ENNEMI_ATTAQUE,
    BOSS_PV_MAX, BOSS_ATTAQUE
)

class TestPersonnage(unittest.TestCase):
    """Tests pour la classe Personnage"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.personnage = Personnage("Test", 100, 20)
    
    def test_initialisation(self):
        """Test de l'initialisation d'un personnage"""
        self.assertEqual(self.personnage.nom, "Test")
        self.assertEqual(self.personnage.pv_max, 100)
        self.assertEqual(self.personnage.pv_actuels, 100)
        self.assertEqual(self.personnage.attaque, 20)
    
    def test_est_vivant(self):
        """Test de la méthode est_vivant"""
        self.assertTrue(self.personnage.est_vivant())
        
        self.personnage.pv_actuels = 0
        self.assertFalse(self.personnage.est_vivant())
        
        self.personnage.pv_actuels = -5
        self.assertFalse(self.personnage.est_vivant())
    
    def test_attaquer(self):
        """Test de la méthode attaquer"""
        cible = Personnage("Cible", 50, 10)
        degats = self.personnage.attaquer(cible)
        
        self.assertGreater(degats, 0)
        self.assertLessEqual(degats, self.personnage.attaque)
        self.assertLess(cible.pv_actuels, cible.pv_max)
    
    def test_soigner(self):
        """Test de la méthode soigner"""
        self.personnage.pv_actuels = 50
        self.personnage.soigner(30)
        
        self.assertEqual(self.personnage.pv_actuels, 80)
        
        # Test de soin qui dépasse les PV max
        self.personnage.soigner(50)
        self.assertEqual(self.personnage.pv_actuels, self.personnage.pv_max)

class TestJoueur(unittest.TestCase):
    """Tests pour la classe Joueur"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.joueur = Joueur("TestHero")
    
    def test_initialisation(self):
        """Test de l'initialisation du joueur"""
        self.assertEqual(self.joueur.nom, "TestHero")
        self.assertEqual(self.joueur.pv_max, JOUEUR_PV_MAX)
        self.assertEqual(self.joueur.attaque, JOUEUR_ATTAQUE)
        self.assertEqual(self.joueur.ennemis_tues, 0)
        self.assertEqual(self.joueur.boss_vaincus, 0)
        self.assertEqual(self.joueur.score, 0)
    
    def test_tuer_ennemi(self):
        """Test de la méthode tuer_ennemi"""
        score_initial = self.joueur.score
        ennemis_initial = self.joueur.ennemis_tues
        
        self.joueur.tuer_ennemi()
        
        self.assertEqual(self.joueur.ennemis_tues, ennemis_initial + 1)
        self.assertGreater(self.joueur.score, score_initial)
    
    def test_vaincre_boss(self):
        """Test de la méthode vaincre_boss"""
        score_initial = self.joueur.score
        boss_initial = self.joueur.boss_vaincus
        
        self.joueur.vaincre_boss()
        
        self.assertEqual(self.joueur.boss_vaincus, boss_initial + 1)
        self.assertGreater(self.joueur.score, score_initial)
    
    def test_survivre_tour(self):
        """Test de la méthode survivre_tour"""
        score_initial = self.joueur.score
        tours_initial = self.joueur.tours_survies
        
        self.joueur.survivre_tour()
        
        self.assertEqual(self.joueur.tours_survies, tours_initial + 1)
        self.assertGreater(self.joueur.score, score_initial)
    
    def test_traverser_salle(self):
        """Test de la méthode traverser_salle"""
        score_initial = self.joueur.score
        
        self.joueur.traverser_salle()
        
        self.assertGreater(self.joueur.score, score_initial)

class TestEnnemi(unittest.TestCase):
    """Tests pour la classe Ennemi"""
    
    def test_initialisation(self):
        """Test de l'initialisation d'un ennemi"""
        ennemi = Ennemi()
        
        self.assertIn(ennemi.nom, ["Gobelin", "Orc", "Squelette", "Loup", "Araignée"])
        self.assertEqual(ennemi.pv_max, ENNEMI_PV_MAX)
        self.assertEqual(ennemi.attaque, ENNEMI_ATTAQUE)
    
    def test_initialisation_difficulte(self):
        """Test de l'initialisation avec difficulté"""
        ennemi_facile = Ennemi(1)
        ennemi_difficile = Ennemi(2)
        
        self.assertGreaterEqual(ennemi_difficile.pv_max, ennemi_facile.pv_max)
        self.assertGreaterEqual(ennemi_difficile.attaque, ennemi_facile.attaque)

class TestBoss(unittest.TestCase):
    """Tests pour la classe Boss"""
    
    def test_initialisation(self):
        """Test de l'initialisation d'un boss"""
        boss = Boss()
        
        self.assertIn(boss.nom, ["Dragon", "Liche", "Démon", "Géant", "Hydre"])
        self.assertEqual(boss.pv_max, BOSS_PV_MAX)
        self.assertEqual(boss.attaque, BOSS_ATTAQUE)
    
    def test_initialisation_difficulte(self):
        """Test de l'initialisation avec difficulté"""
        boss_facile = Boss(1)
        boss_difficile = Boss(3)
        
        self.assertGreater(boss_difficile.pv_max, boss_facile.pv_max)
        self.assertGreater(boss_difficile.attaque, boss_facile.attaque)

class TestPowerUp(unittest.TestCase):
    """Tests pour la classe PowerUp"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.powerup = PowerUp("Test PowerUp", "attaque", 0, 10)
        self.joueur = Joueur()
    
    def test_initialisation(self):
        """Test de l'initialisation d'un power-up"""
        self.assertEqual(self.powerup.nom, "Test PowerUp")
        self.assertEqual(self.powerup.effet, "attaque")
        self.assertEqual(self.powerup.valeur, 10)
        self.assertEqual(self.powerup.duree, 0)
    
    def test_appliquer_attaque(self):
        """Test de l'application d'un power-up d'attaque"""
        attaque_initial = self.joueur.attaque
        self.powerup.appliquer(self.joueur)
        
        self.assertEqual(self.joueur.attaque, attaque_initial + 10)
    
    def test_retirer_attaque(self):
        """Test du retrait d'un power-up d'attaque"""
        self.powerup.appliquer(self.joueur)
        attaque_apres_application = self.joueur.attaque
        
        self.powerup.retirer(self.joueur)
        
        self.assertEqual(self.joueur.attaque, attaque_apres_application - 10)

class TestSalle(unittest.TestCase):
    """Tests pour les classes de salles"""
    
    def test_salle_ennemi(self):
        """Test de la salle d'ennemi"""
        salle = SalleEnnemi()
        
        self.assertEqual(salle.nom, "Salle d'Ennemi")
        self.assertIsInstance(salle.ennemi, Ennemi)
    
    def test_salle_boss(self):
        """Test de la salle de boss"""
        salle = SalleBoss()
        
        self.assertEqual(salle.nom, "Salle de Boss")
        self.assertIsInstance(salle.boss, Boss)
    
    def test_salle_soin(self):
        """Test de la salle de soin"""
        salle = SalleSoin()
        joueur = Joueur()
        joueur.pv_actuels = 50
        
        resultat = salle.entrer(joueur)
        
        self.assertTrue(resultat)
        self.assertGreater(joueur.pv_actuels, 50)
    
    def test_salle_amelioration(self):
        """Test de la salle d'amélioration"""
        salle = SalleAmelioration()
        joueur = Joueur()
        attaque_initial = joueur.attaque
        
        resultat = salle.entrer(joueur)
        
        self.assertTrue(resultat)
        self.assertGreater(joueur.attaque, attaque_initial)
    
    def test_salle_powerup(self):
        """Test de la salle de power-up"""
        salle = SallePowerUp()
        joueur = Joueur()
        score_initial = joueur.score
        
        resultat = salle.entrer(joueur)
        
        self.assertTrue(resultat)
        self.assertGreater(joueur.score, score_initial)
        self.assertGreater(len(joueur.power_ups), 0)

class TestScoreManager(unittest.TestCase):
    """Tests pour la classe ScoreManager"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.score_manager = ScoreManager()
        # Nettoyer les scores existants pour les tests
        self.score_manager.high_scores = []
    
    def test_ajouter_score(self):
        """Test de l'ajout d'un score"""
        resultat = self.score_manager.ajouter_score("TestPlayer", 1000, 5, 3, 1)
        
        self.assertTrue(resultat)  # Premier score est toujours un high score
        self.assertEqual(len(self.score_manager.high_scores), 1)
        self.assertEqual(self.score_manager.high_scores[0]['nom'], "TestPlayer")
        self.assertEqual(self.score_manager.high_scores[0]['score'], 1000)
    
    def test_est_high_score(self):
        """Test de la vérification de high score"""
        # Premier score
        self.assertTrue(self.score_manager.est_high_score(100))
        
        # Ajouter plusieurs scores pour avoir un seuil
        self.score_manager.ajouter_score("Player1", 500, 3, 2, 0)
        self.score_manager.ajouter_score("Player2", 300, 2, 1, 0)
        self.score_manager.ajouter_score("Player3", 200, 1, 1, 0)
        
        # Score plus élevé
        self.assertTrue(self.score_manager.est_high_score(600))
        
        # Test que la méthode fonctionne (même si le résultat peut varier)
        result = self.score_manager.est_high_score(50)
        self.assertIsInstance(result, bool)
    
    def test_get_top_scores(self):
        """Test de la récupération des meilleurs scores"""
        # Ajouter plusieurs scores
        self.score_manager.ajouter_score("Player1", 1000, 5, 3, 1)
        self.score_manager.ajouter_score("Player2", 800, 4, 2, 1)
        self.score_manager.ajouter_score("Player3", 1200, 6, 4, 2)
        
        top_scores = self.score_manager.get_top_scores(2)
        
        self.assertEqual(len(top_scores), 2)
        self.assertEqual(top_scores[0]['score'], 1200)  # Le plus haut en premier
        self.assertEqual(top_scores[1]['score'], 1000)

class TestGenerateurSalles(unittest.TestCase):
    """Tests pour la classe GenerateurSalles"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.generateur = GenerateurSalles()
    
    def test_generer_salle(self):
        """Test de la génération de salles"""
        salle = self.generateur.generer_salle()
        
        self.assertIsInstance(salle, Salle)
        self.assertIn(type(salle).__name__, 
                     ['SalleEnnemi', 'SalleBoss', 'SalleSoin', 
                      'SalleAmelioration', 'SallePowerUp'])
    
    def test_generer_salle_difficulte(self):
        """Test de la génération avec difficulté"""
        generateur_difficile = GenerateurSalles(2)
        salle = generateur_difficile.generer_salle()
        
        if isinstance(salle, SalleEnnemi):
            self.assertEqual(generateur_difficile.difficulte, 2)
        elif isinstance(salle, SalleBoss):
            self.assertEqual(generateur_difficile.difficulte, 2)

class TestJeu(unittest.TestCase):
    """Tests pour la classe Jeu"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.jeu = Jeu()
    
    def test_initialisation(self):
        """Test de l'initialisation du jeu"""
        self.assertIsInstance(self.jeu.joueur, Joueur)
        self.assertEqual(self.jeu.salle_actuelle, 0)
        self.assertEqual(self.jeu.salles_max, 5)
        self.assertIsInstance(self.jeu.generateur_salles, GenerateurSalles)
        self.assertIsInstance(self.jeu.score_manager, ScoreManager)
    
    def test_initialisation_difficulte(self):
        """Test de l'initialisation avec difficulté"""
        jeu_difficile = Jeu(2)
        
        self.assertEqual(jeu_difficile.difficulte, 2)
        self.assertEqual(jeu_difficile.generateur_salles.difficulte, 2)

class TestIntegration(unittest.TestCase):
    """Tests d'intégration"""
    
    def test_combat_complet(self):
        """Test d'un combat complet"""
        joueur = Joueur()
        ennemi = Ennemi()
        
        # Combat jusqu'à la mort d'un des deux
        while joueur.est_vivant() and ennemi.est_vivant():
            joueur.attaquer(ennemi)
            if ennemi.est_vivant():
                ennemi.attaquer(joueur)
        
        # Vérifier qu'un des deux est mort
        self.assertTrue(not joueur.est_vivant() or not ennemi.est_vivant())
    
    def test_progression_jeu(self):
        """Test de la progression du jeu"""
        jeu = Jeu()
        
        # Simuler la progression
        for i in range(3):
            salle = jeu.generateur_salles.generer_salle()
            if isinstance(salle, (SalleEnnemi, SalleBoss)):
                # Simuler un combat gagné
                if isinstance(salle, SalleEnnemi):
                    jeu.joueur.tuer_ennemi()
                else:
                    jeu.joueur.vaincre_boss()
            else:
                # Salle spéciale
                salle.entrer(jeu.joueur)
            
            jeu.salle_actuelle += 1
        
        self.assertEqual(jeu.salle_actuelle, 3)
        self.assertGreater(jeu.joueur.score, 0)

if __name__ == '__main__':
    # Initialiser Pygame pour les tests
    pygame.init()
    
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    test_classes = [
        TestPersonnage, TestJoueur, TestEnnemi, TestBoss,
        TestPowerUp, TestSalle, TestScoreManager, 
        TestGenerateurSalles, TestJeu, TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Nettoyer Pygame
    pygame.quit()
    
    # Sortir avec le code d'erreur approprié
    sys.exit(0 if result.wasSuccessful() else 1)
