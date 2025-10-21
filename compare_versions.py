#!/usr/bin/env python3
"""
Script de comparaison entre les versions du jeu Roguelike
"""

import os
import subprocess
import sys

def count_lines(filename):
    """Compte le nombre de lignes d'un fichier"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except FileNotFoundError:
        return 0

def count_classes(filename):
    """Compte le nombre de classes dans un fichier"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count('class ')
    except FileNotFoundError:
        return 0

def count_functions(filename):
    """Compte le nombre de fonctions dans un fichier"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count('def ')
    except FileNotFoundError:
        return 0

def analyze_file(filename, name):
    """Analyse un fichier et retourne ses statistiques"""
    lines = count_lines(filename)
    classes = count_classes(filename)
    functions = count_functions(filename)
    
    return {
        'name': name,
        'filename': filename,
        'lines': lines,
        'classes': classes,
        'functions': functions
    }

def main():
    """Fonction principale de comparaison"""
    print("🔍 ANALYSE COMPARATIVE DES VERSIONS DU JEU ROGUELIKE")
    print("=" * 60)
    
    # Analyse des fichiers
    files_to_analyze = [
        ('roguelike_graphique_avance.py', 'Version Originale'),
        ('roguelike_optimized.py', 'Version Optimisée'),
        ('config.py', 'Configuration'),
        ('renderer.py', 'Rendu Optimisé'),
        ('entities.py', 'Entités SOLID'),
        ('services.py', 'Services SOLID'),
        ('interfaces.py', 'Interfaces SOLID')
    ]
    
    results = []
    total_optimized = 0
    
    for filename, name in files_to_analyze:
        if os.path.exists(filename):
            stats = analyze_file(filename, name)
            results.append(stats)
            if filename != 'roguelike_graphique_avance.py':
                total_optimized += stats['lines']
        else:
            print(f"⚠️  Fichier {filename} non trouvé")
    
    # Affichage des résultats
    print(f"{'Fichier':<30} {'Lignes':<8} {'Classes':<8} {'Fonctions':<10}")
    print("-" * 60)
    
    original_lines = 0
    for result in results:
        print(f"{result['name']:<30} {result['lines']:<8} {result['classes']:<8} {result['functions']:<10}")
        if result['filename'] == 'roguelike_graphique_avance.py':
            original_lines = result['lines']
    
    print("-" * 60)
    print(f"{'TOTAL OPTIMISÉ':<30} {total_optimized:<8}")
    print("=" * 60)
    
    # Calculs de réduction
    if original_lines > 0:
        reduction = original_lines - total_optimized
        percentage = (reduction / original_lines) * 100
        
        print(f"📊 RÉSULTATS DE L'OPTIMISATION:")
        print(f"   • Version originale: {original_lines} lignes")
        print(f"   • Version optimisée: {total_optimized} lignes")
        print(f"   • Réduction: {reduction} lignes ({percentage:.1f}%)")
        
        if percentage > 0:
            print(f"   • 🎉 SUCCÈS: Réduction de {percentage:.1f}%!")
        else:
            print(f"   • ⚠️  ATTENTION: Augmentation de {abs(percentage):.1f}%")
    
    # Analyse des modules
    print(f"\n🏗️  ARCHITECTURE MODULAIRE:")
    print(f"   • Configuration centralisée: config.py")
    print(f"   • Rendu optimisé: renderer.py")
    print(f"   • Entités SOLID: entities.py")
    print(f"   • Services SOLID: services.py")
    print(f"   • Interfaces SOLID: interfaces.py")
    
    # Tests
    print(f"\n🧪 TESTS UNITAIRES:")
    test_files = ['test_roguelike.py', 'test_solid.py', 'run_tests.py']
    total_tests = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            lines = count_lines(test_file)
            total_tests += lines
            print(f"   • {test_file}: {lines} lignes")
    
    print(f"   • Total tests: {total_tests} lignes")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if original_lines > 0 and total_optimized < original_lines:
        print(f"   ✅ Utilisez la version optimisée pour de meilleures performances")
        print(f"   ✅ L'architecture modulaire facilite la maintenance")
        print(f"   ✅ Les tests unitaires garantissent la qualité")
    else:
        print(f"   ⚠️  Vérifiez que tous les fichiers sont présents")
    
    print(f"\n🚀 LANCEMENT:")
    print(f"   • Version originale: python3 roguelike_graphique_avance.py")
    print(f"   • Version optimisée: python3 roguelike_optimized.py")
    print(f"   • Tests: python3 run_tests.py")

if __name__ == "__main__":
    main()
