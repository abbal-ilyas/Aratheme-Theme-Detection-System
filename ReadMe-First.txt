
Etapes ; (Lancer le conteneur docker pour tester)

1- nettoyer les données " clean-data.pt " -> results3.json

2- lemmatiser les données netoyyer " lematize-data.py " -> results_lemmatized.json

3- Entrainer MLP sur les données nettoyer et lemmatiser -> " train-model.py " -> (Enregistrer les données du modele 'vectorizer + weights + labels' )

4- Tester sur nouveau texte arabe -> test-model.py -> 'prediction du theme'
