"""
Jeu Donkey Kong Labyrinthe
Jeu dans lequel on doit déplacer DK jusqu'aux bananes à travers un labyrinthe.

Script Python
Fichiers : dklabyrinthe.py, classes.py, constantes.py, n1, n2 + images
"""
#import numpy as np
import pygame
from pygame.locals import *
from constantes import *
pygame.init()
#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
from classes import *


#Limitation de vitesse de la boucle
#30 frames par secondes suffisent
pygame.time.Clock().tick(30)
#Icone
icone = pygame.image.load(icone_path)
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption(titre_fenetre)

#chargement de l'image de fond
fond = pygame.image.load(fond_path).convert()

niveau = Niveau()
perso = Perso()

def display():
	fenetre.blit(fond, (0,0))
	niveau.affiche_niveau(fenetre)
	perso.affiche(fenetre)
	pygame.display.flip()

keys = dict()
def init_keys(keys):
	keys['down'] = False
	keys['up'] = False
	keys['left'] = False
	keys['right'] = False
	return keys
keys = init_keys(keys)
#Variable qui continue la boucle si = 1, stoppe si = 0
continuer = 1
#Boucle infinie
while continuer:#On parcours la liste de tous les événements reçus
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			#Si un de ces événements est de type QUIT
			if (event.type == pygame.QUIT) or (event.key == pygame.K_ESCAPE):
				continuer = 0 
			if event.key == pygame.K_DOWN: #Si "flèche bas"
				keys['down'] = True
			if event.key == pygame.K_UP: #Si "flèche haut"
				keys['up'] = True
			if event.key == pygame.K_LEFT: #Si "flèche gauche"
				keys['left'] = True
			if event.key == pygame.K_RIGHT: #Si "flèche droite"
				keys['right'] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN: #Si "flèche bas"
				keys['down'] = False
			if event.key == pygame.K_UP: #Si "flèche haut"
				keys['up'] = False
			if event.key == pygame.K_LEFT: #Si "flèche gauche"
				keys['left'] = False
			if event.key == pygame.K_RIGHT: #Si "flèche droite"
				keys['right'] = False
	perso.controles(keys)
	keys = init_keys(keys)
	perso.move(niveau)
	display()