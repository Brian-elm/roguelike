#!/usr/bin/env python3
"""
Module d'événements aléatoires et d'easter eggs pour rendre le jeu plus fun
"""

import random
import pygame
from typing import List, Dict, Optional, Callable
from config import *

class RandomEvent:
    """Événement aléatoire"""
    
    def __init__(self, name: str, description: str, probability: float, 
                 effect: Callable, icon: str = "exclamation"):
        self.name = name
        self.description = description
        self.probability = probability
        self.effect = effect
        self.icon = icon
        self.used = False

class EventManager:
    """Gestionnaire d'événements aléatoires"""
    
    def __init__(self):
        self.events: List[RandomEvent] = []
        self.active_events: List[RandomEvent] = []
        self.event_history: List[str] = []
        self._init_events()
    
    def _init_events(self):
        """Initialise les événements aléatoires"""
        
        # Événements positifs
        self.events.append(RandomEvent(
            "Trésor Caché",
            "Vous trouvez un coffre au trésor!",
            0.05,
            self._treasure_effect,
            "crown"
        ))
        
        self.events.append(RandomEvent(
            "Fée Bienfaitrice",
            "Une fée vous accorde sa bénédiction!",
            0.03,
            self._fairy_effect,
            "heart"
        ))
        
        self.events.append(RandomEvent(
            "Marchand Itinérant",
            "Un marchand vous propose ses services!",
            0.08,
            self._merchant_effect,
            "plus"
        ))
        
        self.events.append(RandomEvent(
            "Source Magique",
            "Vous découvrez une source de pouvoir!",
            0.04,
            self._magic_spring_effect,
            "sword"
        ))
        
        # Événements neutres
        self.events.append(RandomEvent(
            "Météo Changeante",
            "Le temps se déchaîne dans le donjon!",
            0.1,
            self._weather_change_effect,
            "exclamation"
        ))
        
        self.events.append(RandomEvent(
            "Écho Mystérieux",
            "Vous entendez des voix dans les murs...",
            0.06,
            self._mysterious_echo_effect,
            "skull"
        ))
        
        # Événements négatifs
        self.events.append(RandomEvent(
            "Piège Ancien",
            "Vous activez un piège oublié!",
            0.07,
            self._trap_effect,
            "skull"
        ))
        
        self.events.append(RandomEvent(
            "Malédiction",
            "Une malédiction ancienne vous affecte!",
            0.02,
            self._curse_effect,
            "skull"
        ))
    
    def _treasure_effect(self, player, game_service) -> str:
        """Effet du trésor caché"""
        gold = random.randint(50, 200)
        player.ajouter_score(gold)
        return f"Vous trouvez {gold} pièces d'or!"
    
    def _fairy_effect(self, player, game_service) -> str:
        """Effet de la fée bienfaitrice"""
        heal = player.pv_max // 2
        player.soigner(heal)
        return f"La fée vous soigne de {heal} PV!"
    
    def _merchant_effect(self, player, game_service) -> str:
        """Effet du marchand itinérant"""
        if random.random() < 0.5:
            # Potion de soin
            heal = random.randint(20, 40)
            player.soigner(heal)
            return f"Le marchand vous vend une potion de soin (+{heal} PV)!"
        else:
            # Amélioration d'attaque
            bonus = random.randint(2, 5)
            player.augmenter_attaque(bonus)
            return f"Le marchand vous vend une épée améliorée (+{bonus} attaque)!"
    
    def _magic_spring_effect(self, player, game_service) -> str:
        """Effet de la source magique"""
        # Restaure tous les PV et donne un bonus temporaire
        player.soigner(player.pv_max)
        bonus = random.randint(3, 8)
        player.augmenter_attaque(bonus)
        return f"La source magique vous restaure et vous donne +{bonus} attaque!"
    
    def _weather_change_effect(self, player, game_service) -> str:
        """Effet du changement de météo"""
        weathers = ["rain", "snow", "storm", "clear"]
        new_weather = random.choice(weathers)
        # Ici on pourrait changer la météo dans le jeu
        return f"Le temps change: {new_weather}!"
    
    def _mysterious_echo_effect(self, player, game_service) -> str:
        """Effet de l'écho mystérieux"""
        messages = [
            "Les murs murmurent des secrets anciens...",
            "Vous entendez des pas derrière vous...",
            "Une voix chuchote: 'Attention aux pièges...'",
            "Les ombres semblent bouger..."
        ]
        return random.choice(messages)
    
    def _trap_effect(self, player, game_service) -> str:
        """Effet du piège"""
        damage = random.randint(5, 15)
        player._pv_actuels = max(1, player._pv_actuels - damage)
        return f"Piège activé! Vous perdez {damage} PV!"
    
    def _curse_effect(self, player, game_service) -> str:
        """Effet de la malédiction"""
        # Réduit temporairement l'attaque
        penalty = random.randint(2, 5)
        player.augmenter_attaque(-penalty)
        return f"Malédiction! Votre attaque diminue de {penalty}!"
    
    def check_random_event(self, player, game_service) -> Optional[str]:
        """Vérifie s'il y a un événement aléatoire"""
        for event in self.events:
            if not event.used and random.random() < event.probability:
                event.used = True
                self.active_events.append(event)
                result = event.effect(player, game_service)
                self.event_history.append(f"{event.name}: {result}")
                return result
        return None
    
    def reset_events(self):
        """Remet à zéro les événements"""
        for event in self.events:
            event.used = False
        self.active_events.clear()

class EasterEggManager:
    """Gestionnaire d'easter eggs et secrets"""
    
    def __init__(self):
        self.secrets_found = []
        self.secret_combinations = {
            "konami": ["up", "up", "down", "down", "left", "right", "left", "right"],
            "power": ["p", "o", "w", "e", "r"],
            "secret": ["s", "e", "c", "r", "e", "t"]
        }
        self.current_combination = []
        self.secret_effects = {
            "konami": self._konami_code_effect,
            "power": self._power_effect,
            "secret": self._secret_effect
        }
    
    def add_key(self, key: str) -> Optional[str]:
        """Ajoute une touche à la combinaison secrète"""
        self.current_combination.append(key.lower())
        
        # Garder seulement les dernières touches
        max_length = max(len(combo) for combo in self.secret_combinations.values())
        if len(self.current_combination) > max_length:
            self.current_combination.pop(0)
        
        # Vérifier les combinaisons
        for secret_name, combination in self.secret_combinations.items():
            if (secret_name not in self.secrets_found and 
                self.current_combination[-len(combination):] == combination):
                self.secrets_found.append(secret_name)
                return self.secret_effects[secret_name]()
        
        return None
    
    def _konami_code_effect(self) -> str:
        """Effet du code Konami"""
        return "Code Konami activé! Vous obtenez 30 vies!"
    
    def _power_effect(self) -> str:
        """Effet du mot 'power'"""
        return "POWER! Votre attaque est doublée temporairement!"
    
    def _secret_effect(self) -> str:
        """Effet du mot 'secret'"""
        return "SECRET découvert! Vous obtenez un bonus de score!"
    
    def check_special_conditions(self, player, game_service) -> Optional[str]:
        """Vérifie des conditions spéciales pour des easter eggs"""
        
        # Easter egg: Score palindrome
        if str(player.score) == str(player.score)[::-1] and player.score > 100:
            if "palindrome" not in self.secrets_found:
                self.secrets_found.append("palindrome")
                return "Easter Egg: Score palindrome! Bonus mystique!"
        
        # Easter egg: Nombre parfait de salles
        if game_service._salle_actuelle in [7, 13, 21, 28]:
            if f"perfect_room_{game_service._salle_actuelle}" not in self.secrets_found:
                self.secrets_found.append(f"perfect_room_{game_service._salle_actuelle}")
                return f"Easter Egg: Salle {game_service._salle_actuelle} (nombre parfait)!"
        
        # Easter egg: Tous les ennemis tués avec le même nom
        if player.ennemis_tues > 0 and player.ennemis_tues % 10 == 0:
            if f"killer_{player.ennemis_tues}" not in self.secrets_found:
                self.secrets_found.append(f"killer_{player.ennemis_tues}")
                return f"Easter Egg: {player.ennemis_tues} ennemis tués! Vous êtes un tueur!"
        
        return None

class DynamicDifficulty:
    """Système de difficulté dynamique"""
    
    def __init__(self):
        self.base_difficulty = 1
        self.current_multiplier = 1.0
        self.player_performance = []
        self.adjustment_rate = 0.1
    
    def update_performance(self, player, game_service):
        """Met à jour la performance du joueur"""
        performance = {
            'score': player.score,
            'rooms': game_service._salle_actuelle,
            'deaths': 0,  # À implémenter si on ajoute un système de mort
            'time': pygame.time.get_ticks()
        }
        self.player_performance.append(performance)
        
        # Garder seulement les 10 dernières performances
        if len(self.player_performance) > 10:
            self.player_performance.pop(0)
    
    def adjust_difficulty(self) -> float:
        """Ajuste la difficulté selon la performance"""
        if len(self.player_performance) < 3:
            return self.current_multiplier
        
        # Calculer la performance moyenne
        recent_scores = [p['score'] for p in self.player_performance[-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        # Ajuster la difficulté
        if avg_score > 1000:  # Trop facile
            self.current_multiplier += self.adjustment_rate
        elif avg_score < 300:  # Trop difficile
            self.current_multiplier -= self.adjustment_rate
        
        # Limiter entre 0.5 et 2.0
        self.current_multiplier = max(0.5, min(2.0, self.current_multiplier))
        
        return self.current_multiplier
    
    def get_enemy_multiplier(self) -> float:
        """Retourne le multiplicateur pour les ennemis"""
        return self.current_multiplier

class FunFeatures:
    """Collection de fonctionnalités amusantes"""
    
    def __init__(self):
        self.silly_messages = [
            "Votre épée brille d'un éclat suspect...",
            "L'ennemi semble surpris de vous voir!",
            "Vous entendez des applaudissements lointains...",
            "Votre armure fait un bruit métallique satisfaisant!",
            "L'ennemi fait une grimace comique!",
            "Vous sentez que c'est votre jour de chance!",
            "L'ennemi semble avoir oublié de prendre son petit-déjeuner...",
            "Votre attaque est si puissante qu'elle fait trembler les murs!",
            "L'ennemi regarde votre épée avec envie...",
            "Vous avez l'air particulièrement héroïque aujourd'hui!"
        ]
        
        self.victory_quotes = [
            "Victoire! Vous êtes le héros de la journée!",
            "Excellent! L'ennemi n'était pas à votre niveau!",
            "Magnifique! Vous maîtrisez l'art du combat!",
            "Impressionnant! Vous combattez comme un légende!",
            "Fantastique! Vous êtes un vrai guerrier!",
            "Remarquable! Votre technique est parfaite!",
            "Extraordinaire! Vous êtes né pour ça!",
            "Splendide! Vous combattez avec grâce!",
            "Formidable! Vous êtes un maître du combat!",
            "Parfait! Vous êtes un héros accompli!"
        ]
        
        self.defeat_quotes = [
            "Défaite... mais vous vous relèverez plus fort!",
            "Perdu cette fois... mais la prochaine sera la bonne!",
            "Échec... mais chaque échec est une leçon!",
            "Défait... mais vous n'abandonnez jamais!",
            "Perdu... mais vous reviendrez plus sage!",
            "Échoué... mais vous apprenez de vos erreurs!",
            "Battu... mais vous êtes plus fort qu'avant!",
            "Défait... mais vous ne baissez pas les bras!",
            "Perdu... mais vous vous améliorez à chaque fois!",
            "Échec... mais vous êtes sur la bonne voie!"
        ]
    
    def get_silly_message(self) -> str:
        """Retourne un message amusant aléatoire"""
        return random.choice(self.silly_messages)
    
    def get_victory_quote(self) -> str:
        """Retourne une citation de victoire aléatoire"""
        return random.choice(self.victory_quotes)
    
    def get_defeat_quote(self) -> str:
        """Retourne une citation de défaite aléatoire"""
        return random.choice(self.defeat_quotes)
    
    def get_encouragement(self) -> str:
        """Retourne un message d'encouragement"""
        encouragements = [
            "Continuez comme ça!",
            "Vous êtes sur la bonne voie!",
            "Ne lâchez rien!",
            "Vous pouvez le faire!",
            "Allez-y, champion!",
            "Vous êtes formidable!",
            "Gardez le cap!",
            "Vous êtes incroyable!",
            "Ne vous arrêtez pas!",
            "Vous êtes le meilleur!"
        ]
        return random.choice(encouragements)
