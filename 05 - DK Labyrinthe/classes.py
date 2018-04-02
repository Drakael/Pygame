import numpy as np
import pygame
from constantes import *
grid_size = 15
grid_size_moins_un = grid_size-1
square_size = cote_fenetre / grid_size
class Niveau:
	mur = pygame.image.load(mur_path).convert_alpha()
	depart = pygame.image.load(depart_path).convert_alpha()
	arrivee = pygame.image.load(arrivee_path).convert_alpha()
	def __init__(self):
		self.carte = np.array([[('O' if np.random.randint(0,2)==0 else 'M') for x in range(grid_size)] for y in range(grid_size)])
		self.carte[0][0] = 'D'
		self.carte[grid_size-1][grid_size-1] = 'A'
		self.carte = self.clean_carte(self.carte)
		print(self.carte)

	def affiche_niveau(self, fenetre):
		fenetre.blit(Niveau.depart, (0,0))
		fenetre.blit(Niveau.arrivee, ((grid_size-1)*square_size,(grid_size-1)*square_size))
		for x, arr in enumerate(self.carte):
			for y, value in enumerate(arr):
				#print(x, y, arr, value, sep=' ')
				if value == 'M':
					fenetre.blit(Niveau.mur, (x*square_size,y*square_size))
					#print(x, y, square_size,x*square_size, y*square_size, sep=' ')

	def clean_carte(self, carte):
		rot_mat_cw = np.array([[0,1],[-1,0]])
		rot_mat_ccw = np.array([[0,-1],[1,0]])

		if (carte[1][0]=='M') and (carte[0][1]=='M'):
			rand = np.random.randint(0,2)
			#print('depart rand=',rand)
			carte[rand][1-rand]='O'
		if (carte[grid_size_moins_un-1][grid_size_moins_un]=='M') and (carte[grid_size_moins_un][grid_size_moins_un-1]=='M'):
			rand = np.random.randint(0,2)
			#print('arrivee rand=',rand)
			carte[grid_size_moins_un-rand][grid_size_moins_un-1+rand]='O'

		grid_validated = False
		max_steps_2 = 60
		#print(carte)
		while (grid_validated == False) and (max_steps_2>0):
			#print('------')
			#print(carte)
			case = np.array([0,0])
			sens_recherche = np.array([0,1])
			max_x = 0
			max_y = 0
			max_steps_2-=1
			max_steps = 150
			cnt_d = 0
			validate = False
			#murs_connus = [[],[]]
			murs_connus_2 = []
			while max_steps>0 and (cnt_d<4):
				max_steps-=1
				if (case[0] == grid_size_moins_un) and (case[1] == grid_size_moins_un):
					grid_validated = True
					break
				next_case = case + sens_recherche
				#print(next_case, case, sens_recherche, sep=" ")
				if next_case[0]<0:
					next_case[0]=0
				elif next_case[0]>grid_size_moins_un:
					next_case[0]=grid_size_moins_un
				if next_case[1]<0:
					next_case[1]=0
				elif next_case[1]>grid_size_moins_un:
					next_case[1]=grid_size_moins_un
				if next_case[0]>max_x:
					max_x = next_case[0]
				if next_case[1]>max_y:
					max_y = next_case[1]
				#print('case=',case,'  sens_recherche=',sens_recherche,'  next_case=',next_case,' => ', carte[next_case[1]][next_case[0]],'   - cnt_d=',cnt_d)
				if (next_case[0] != case[0]) or (next_case[1] != case[1]):
					if(carte[next_case[1]][next_case[0]] == 'O'):
						case = next_case
						sens_recherche = np.matmul(sens_recherche,rot_mat_cw)
					else:
						if(carte[next_case[1]][next_case[0]] == 'A'):
							#print('case=',case,'  sens_recherche=',sens_recherche,'  next_case=',next_case,' => ', carte[next_case[1]][next_case[0]],'   - cnt_d=',cnt_d)
							grid_validated = True
							validate = True
							break
						#print('sens_recherche before: ',sens_recherche)
						sens_recherche = np.matmul(sens_recherche,rot_mat_ccw)
						#murs_connus[next_case[1]][next_case[0]] = 'M'
						murs_connus_2.append((next_case[0],next_case[1]))
						#print('sens_recherche after: ',sens_recherche)
				else:
					#print('sens_recherche before: ',sens_recherche)
					sens_recherche = np.matmul(sens_recherche,rot_mat_ccw)
					#print('sens_recherche after: ',sens_recherche)
				if validate == True:
					grid_validated = True
					break
				if (next_case[0]==0) and (next_case[1]==0):
					cnt_d+=1
			if grid_validated == False:
				test = False
				while test == False:
					rand_x = 0
					rand_y = 0
					while (rand_x<max_x*0.7) and (rand_y<max_y*0.7):
						rand = np.random.randint(0,len(murs_connus_2))
						tuple_case = murs_connus_2[rand]
						rand_x = tuple_case[0]
						rand_y = tuple_case[1]
					if(carte[rand_y][rand_x]=='M'):
						carte[rand_y][rand_x]='O'
						test = True
						#print('rand_x=',rand_x,' rand_y=',rand_y)
		return carte

class Perso():
	dk_bas = pygame.image.load(dk_bas_path).convert_alpha()
	dk_haut = pygame.image.load(dk_haut_path).convert_alpha()
	dk_gauche = pygame.image.load(dk_gauche_path).convert_alpha()
	dk_droite = pygame.image.load(dk_droite_path).convert_alpha()
	def __init__(self):
		self.position = [0,0]
		self.sens_marche = [0,0]
		self.go = False
		self.image = Perso.dk_bas
		pass
	def affiche(self, fenetre):
		self.image = Perso.dk_bas
		if self.sens_marche == [0,1]:
			self.image = Perso.dk_bas
		elif self.sens_marche == [0,-1]:
			self.image = Perso.dk_haut
		elif self.sens_marche == [1,0]:
			self.image = Perso.dk_droite
		elif self.sens_marche == [-1,0]:
			self.image = Perso.dk_gauche
		fenetre.blit(self.image, ((self.position[0])*square_size,(self.position[1])*square_size))

	def controles(self, keys):
		key_arrow_down = keys['down'] and not keys['up']
		key_arrow_up = keys['up'] and not keys['down']
		key_arrow_left = keys['left'] and not keys['right']
		key_arrow_right = keys['right'] and not keys['left']
		if(key_arrow_down):
			self.sens_marche = [0,1]
			self.go = True
			#print('controle    ',self.sens_marche)
		elif(key_arrow_up):
			self.sens_marche = [0,-1]
			self.go = True
			#print('controle    ',self.sens_marche)
		elif(key_arrow_left):
			self.sens_marche = [-1,0]
			self.go = True
			#print('controle    ',self.sens_marche)
		elif(key_arrow_right):
			self.sens_marche = [1,0]
			self.go = True
			#print('controle    ',self.sens_marche)
		else:
			self.go = False
			#print('controle    ',self.sens_marche)

	def move(self, niveau):
		next_case = [self.position[0] + self.sens_marche[0], self.position[1] + self.sens_marche[1]]
		if next_case[0]<0:
			next_case[0]=0
		elif next_case[0]>grid_size_moins_un:
			next_case[0]=grid_size_moins_un
		if next_case[1]<0:
			next_case[1]=0
		elif next_case[1]>grid_size_moins_un:
			next_case[1]=grid_size_moins_un
		#print(next_case)
		if(niveau.carte[next_case[0]][next_case[1]]!='M') and (self.go == True):
			self.position = next_case;
			print('pos   ',self.position)
			self.go = False
