# Memoire-M2HN

Ce projet analyse la circulation des modèles issus des arts de l’Islam dans la céramique européenne au XIXe siècle, en s’appuyant sur les supports imprimés et une approche quantitative basée sur la vision par ordinateur.

Le corpus comprend 1 932 numérisations d’imprimés et 1 758 photographies d’objets. La chaîne de traitement mise en place inclut :
	•	Détection d’objets (YOLO, Grounding DINO)
	•	Extraction d’embeddings (DINOv3)
	•	Calcul de similarité (FAISS)

# Structure 

- `data/` : Données brutes et certains états intermédiaires du corpus.  
- `experiments/` : Modèles, résultats et fichiers liés aux expérimentations.  
- `notebooks/` : Notebooks pour la réalisation des expériences et l’analyse des données.  
- `metadata/` : Listes d'acquisition, catalogues de métadonnées.  
- `src/` : Modules Python.  


