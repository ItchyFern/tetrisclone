import pygame
import os
import time
import random
import math

pygame.font.init()

#Sizing shit
#GET SIZING

WIDTH, HEIGHT = 300, 750
PIECE_SIZE = 25
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GAME = pygame.Surface((WIDTH-PIECE_SIZE*2, HEIGHT-PIECE_SIZE*6))
SCORE = pygame.Surface((WIDTH-PIECE_SIZE*2, PIECE_SIZE*3))
pygame.display.set_caption("Tetris Clone")

#assets
#blocks
RED_BLOCK = pygame.image.load(os.path.join("assets", "red_block.png"))
BLUE_BLOCK = pygame.image.load(os.path.join("assets", "blue_block.png"))
GREEN_BLOCK = pygame.image.load(os.path.join("assets", "green_block.png"))
PURPLE_BLOCK = pygame.image.load(os.path.join("assets", "purple_block.png"))
YELLOW_BLOCK = pygame.image.load(os.path.join("assets", "yellow_block.png"))
CYAN_BLOCK = pygame.image.load(os.path.join("assets", "cyan_block.png"))
ORANGE_BLOCK = pygame.image.load(os.path.join("assets", "orange_block.png"))
GREY_BLOCK = pygame.image.load(os.path.join("assets", "grey_block.png"))

#previews
L_BLOCK = pygame.image.load(os.path.join("assets", "l_block.png"))
J_BLOCK = pygame.image.load(os.path.join("assets", "j_block.png"))
T_BLOCK = pygame.image.load(os.path.join("assets", "t_block.png"))
I_BLOCK = pygame.image.load(os.path.join("assets", "i_block.png"))
S_BLOCK = pygame.image.load(os.path.join("assets", "s_block.png"))
Z_BLOCK = pygame.image.load(os.path.join("assets", "z_block.png"))
O_BLOCK = pygame.image.load(os.path.join("assets", "o_block.png"))

#scale assets
RED_BLOCK = pygame.transform.scale(RED_BLOCK, (PIECE_SIZE, PIECE_SIZE))
BLUE_BLOCK = pygame.transform.scale(BLUE_BLOCK, (PIECE_SIZE, PIECE_SIZE))
GREEN_BLOCK = pygame.transform.scale(GREEN_BLOCK, (PIECE_SIZE, PIECE_SIZE))
PURPLE_BLOCK = pygame.transform.scale(PURPLE_BLOCK, (PIECE_SIZE, PIECE_SIZE))
YELLOW_BLOCK = pygame.transform.scale(YELLOW_BLOCK, (PIECE_SIZE, PIECE_SIZE))
CYAN_BLOCK = pygame.transform.scale(CYAN_BLOCK, (PIECE_SIZE, PIECE_SIZE))
ORANGE_BLOCK = pygame.transform.scale(ORANGE_BLOCK, (PIECE_SIZE, PIECE_SIZE))
GREY_BLOCK = pygame.transform.scale(GREY_BLOCK, (PIECE_SIZE, PIECE_SIZE))

PREVIEW_SIZE = PIECE_SIZE * 2
L_BLOCK = pygame.transform.scale(L_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
J_BLOCK = pygame.transform.scale(J_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
T_BLOCK = pygame.transform.scale(T_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
I_BLOCK = pygame.transform.scale(I_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
S_BLOCK = pygame.transform.scale(S_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
Z_BLOCK = pygame.transform.scale(Z_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))
O_BLOCK = pygame.transform.scale(O_BLOCK, (PREVIEW_SIZE, PREVIEW_SIZE))


# CONTROLS
CONTROLS = {
			"ROTATE": pygame.K_UP,
			"LEFT": pygame.K_LEFT,
			"RIGHT": pygame.K_RIGHT,
			"FASTDOWN": pygame.K_DOWN,
			"FULLDOWN": pygame.K_SPACE,
			"PAUSE": pygame.K_p
			}
PIECES = {
		"L": [	[(0, -1), (0, 0), (0, 1), (1, 1)], 
				[(-1, 0), (0, 0), (1, 0), (-1, 1)], 
				[(0, 1), (0, 0), (0, -1), (-1, -1)],
				[(1, 0), (0, 0), (-1, 0), (1, -1)]],
		"J": [	[(0, -1), (0, 0), (0, 1), (-1, 1)],
				[(-1, 0), (0, 0), (1, 0), (1, 1)],
				[(0, -1), (0, 0), (0, 1), (1, -1)],
				[(-1, 0), (0, 0), (1, 0), (-1, -1)]],
		"T": [	[(0, -1), (0, 0), (1, 0), (-1, 0)],
				[(0, -1), (0, 0), (0, 1), (1, 0)],
				[(-1, 0), (0, 0), (1, 0), (0, 1)],
				[(0, -1), (0, 0), (0, 1), (-1, 0)]],
		"I": [	[(0, -1), (0, 0), (0, 1), (0, 2)], 
				[(-1, 0), (0, 0), (1, 0), (-2, 0)]],
		"S": [	[(0, -1), (1, -1),(-1, 0), (0, 0)],
				[(0, 0), (1, 0), (0, -1), (1, 1)]],
		"Z": [	[(-1, -1), (0, -1), (0, 0), (1, 0)],
				[(0, 1), (0, 0), (1, 0), (1, -1)]],
		"O": [	[(0, -1), (1, -1), (0, 0), (1, 0)]]
		}

PIECES_COLOUR = {
				"L": (255, 128, 0),
				"J": (0, 0, 255),
				"T": (200, 0, 200),
				"I": (0, 255, 255),
				"S": (0, 255, 0),
				"Z": (255, 0, 0),
				"O": (255, 255, 0)
				}
PIECES_BLOCK = {
				"L": ORANGE_BLOCK,
				"J": BLUE_BLOCK,
				"T": PURPLE_BLOCK,
				"I": CYAN_BLOCK,
				"S": GREEN_BLOCK,
				"Z": RED_BLOCK,
				"O": YELLOW_BLOCK
}
PREVIEW_BLOCKS = {
				"L": L_BLOCK,
				"J": J_BLOCK,
				"T": T_BLOCK,
				"I": I_BLOCK,
				"S": S_BLOCK,
				"Z": Z_BLOCK,
				"O": O_BLOCK
}


def check_if_exist(d, key):
	error = False 
	try:
	    GetDictData = d[key]
	except KeyError:
	    error = True 
	return error
#load assets if I make any

class Board():
	def __init__(self, size):
		self.size = size
		self.board_data = {}

	def create_empty(self):
		self.board_data = {}
		for y in range(self.size[1]):
			for x in range (self.size[0]):
				self.board_data[(x, y)] = None

	def draw(self, window):
		for pos in self.board_data.keys():
			if not self.board_data[pos] == None:
				window.blit(self.board_data[pos], (pos[0] * PIECE_SIZE, pos[1] * PIECE_SIZE))

	def update(self, piece):
		for block in piece.locarray[piece.rotation]:
			self.board_data[(block[0] + piece.x, block[1] + piece.y)] = piece.block_img

		#check finished lines
		finished_lines = []
		partial_lines = []
		for y in range (self.size[1]):
			count = 0

			for x in range (self.size[0]):
				if not self.board_data[(x, y)] == None:
					count += 1
				if count >= 10:
					finished_lines.append(y)
			if count >= 1 and count < 10:
				partial_lines.append(y)


		if len(finished_lines) > 0:
			for y in finished_lines:
				for x in range(self.size[0]):
					self.board_data[(x, y)] = None

			#redraw board
			newboard = []
			for y in partial_lines:
				temparr = []
				for x in range (self.size[0]):
					temparr.append(self.board_data[(x, y)])
				newboard.append(temparr)
			newboard.reverse()

			self.create_empty()
			for y in range(len(newboard)):
				for x in range (self.size[0]):
					self.board_data[(x, self.size[1] - 1 - y)] = newboard[y][x]

		return len(finished_lines)





	def collision(self, piece, dx=0):
		xcol, ycol = False, False
		for block in piece.get_blocks():
			if 	( 
					block[0] + piece.x + dx <= 0 - 1 or 
					block[0] + piece.x + dx >= self.size[0] or
					not self.board_data[block[0] + piece.x + dx, block[1] + piece.y] == None
				):

				xcol = True


			if 	(
					block[1] + piece.y >= self.size[1] - 1 or
					check_if_exist(self.board_data, (block[0] + piece.x, block[1] + piece.y)) or
					not self.board_data[block[0] + piece.x, block[1] + piece.y + 1] == None 
				):

				ycol = True

		return xcol, ycol

	def check_lose(self):
		if not self.board_data[(4, 0)] == None:
			return True
		else:
			return False



class Piece():
	def __init__(self, x, y, name, ghost = False):
		self.name = name
		self.locarray = PIECES[name]
		self.colour = PIECES_COLOUR[name]
		self.block_img = PIECES_BLOCK[name]
		self.x = x
		self.y = y
		self.rotation = 0
		self.moving = True
		self.is_ghost = ghost
		if not ghost:
			self.ghost = Piece (self.x, self.y, self.name, True)

	def update_ghost(self, board):
		self.ghost.x = self.x
		self.ghost.y = self.y
		self.ghost.rotation = self.rotation
		self.ghost.moving = self.moving
		while self.ghost.moving:
			self.ghost.move(0, 1, board)

	def draw(self, window):
		for block in self.locarray[self.rotation]:
			#pygame.draw.rect(window, self.colour, pygame.Rect((	(block[0] + self.x) * PIECE_SIZE,
			#														(block[1] + self.y) * PIECE_SIZE), 
			#														(PIECE_SIZE, PIECE_SIZE)))
			window.blit(self.block_img, ((block[0] + self.x) * PIECE_SIZE,(block[1] + self.y) * PIECE_SIZE))

		for block in self.ghost.locarray[self.rotation]:
			pygame.draw.rect(window, self.colour, pygame.Rect(((block[0] + self.ghost.x) * PIECE_SIZE, (block[1] + self.ghost.y) * PIECE_SIZE), (PIECE_SIZE, PIECE_SIZE)), 2)


	def rotate(self, board):
		if self.moving:
			temprotation = self.rotation
			if self.rotation >= len(self.locarray)-1:
				self.rotation = 0
			else:
				self.rotation += 1
			if True in board.collision(self):
				self.rotation = temprotation

		self.update_ghost(board)




	def move(self, dx, dy, board):
		if self.moving:
			xmove = True
			if dx != 0:
				if not board.collision(self, dx)[0]:
					self.x += dx


			if dy == 1:
				if board.collision(self)[1]:
					self.moving = False
					return 0;
				else:
					self.y += dy

		if not self.is_ghost:
			self.update_ghost(board)

	def drop(self, board):
		drop_distance = self.ghost.y - self.y
		self.x = self.ghost.x
		self.y = self.ghost.y
		self.rotation = self.ghost.rotation
		self.moving = False
		return drop_distance



	def get_blocks(self):
		return self.locarray[self.rotation]

def format_controls(key):
	return chr(key).title()

def game():
	run = True
	FPS = 60
	main_font = pygame.font.SysFont("monospace", 18, bold=True, italic=False)
	pause_font = pygame.font.SysFont("monospace", 60, bold=False, italic=False)
	board = Board((10, 24))
	board.create_empty()

	clock = pygame.time.Clock()
	
	move_cooldown = 0

	drop_delay = 30
	drop_timer = 0

	score = 0
	lines = 0

	current_piece = Piece(4, 1, random.choice(["L", "J", "T", "I", "S", "Z", "O"]))
	next_piece = random.choice(["L", "J", "T", "I", "S", "Z", "O"])
	current_piece.update_ghost(board)

	#space bar keyup flag
	keyup_flag = True

	#pause flag
	ispaused = False

	
		

	def redraw_window():
		GAME.fill((0,0,0))
		SCORE.fill((0,0,0))
		board.draw(GAME)
		current_piece.draw(GAME)
		if ispaused:

			pause_label1 = pause_font.render(f"Press", 1, (255,255,255))
			pause_label2 = pause_font.render(f"{format_controls(CONTROLS['PAUSE'])}", 1, (255, 255, 255))
			GAME.blit(pause_label1, (GAME.get_width()/2 - pause_label1.get_width()/2, GAME.get_height()/2 - pause_label1.get_height()))
			GAME.blit(pause_label2, (GAME.get_width()/2 - pause_label2.get_width()/2, GAME.get_height()/2 + pause_label2.get_height()))
			print ("paused")
		#score.draw()

		score_label = main_font.render(f"Score: {score}", 1, (255,255,255))
		lines_label = main_font.render(f"Lines: {lines}", 1, (255,255,255))

		SCORE.blit(score_label, (10, 5))
		SCORE.blit(lines_label, (10, score_label.get_height() + 10))
		SCORE.blit(PREVIEW_BLOCKS[next_piece], (SCORE.get_width() - 5 - PREVIEW_BLOCKS[next_piece].get_width(), SCORE.get_height() - 5 - PREVIEW_BLOCKS[next_piece].get_width()))

		WIN.blit(GAME, (PIECE_SIZE,PIECE_SIZE))
		WIN.blit(SCORE, (PIECE_SIZE, PIECE_SIZE*26))

		

		pygame.display.update()

	while run:
		clock.tick(FPS)
		redraw_window()		
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()
				if event.type == pygame.KEYUP:
					keyup_flag = True
					if event.key == CONTROLS["PAUSE"]:
						ispaused = not ispaused
							

		if not ispaused:

			# Player controls

			# movement delay
			if move_cooldown == 0:
				moveable = True
			elif move_cooldown >= 5:
				move_cooldown = 0
			else:
				move_cooldown += 1
				moveable = False

			# control options
			keys = pygame.key.get_pressed()
			if keys[CONTROLS["LEFT"]] and moveable: 
				current_piece.move(-1, 0, board)
				move_cooldown += 1
			if keys[CONTROLS["RIGHT"]] and moveable: 
				current_piece.move(1, 0, board)
				move_cooldown += 1
			if keys[CONTROLS["ROTATE"]] and moveable: 
				current_piece.rotate(board)
				move_cooldown += 1
			if keys[CONTROLS["FASTDOWN"]]:
				current_piece.move(0, 1, board)
				score += 1
				drop_timer = 0
			if keys[CONTROLS["FULLDOWN"]] and keyup_flag: 
				score += current_piece.drop(board) * 3
				keyup_flag = False





			drop_timer += 1
			if drop_timer >= drop_delay:
				drop_timer = 0
				current_piece.move(0, 1, board)

			if not current_piece.moving:
				numoflines = board.update(current_piece)
				score += pow(numoflines * 10,2)
				lines += numoflines
				current_piece = Piece(4, 1, next_piece)
				next_piece = random.choice(["L", "J", "T", "I", "I", "S", "Z", "O"])
				current_piece.update_ghost(board)
				if board.check_lose():
					run = False

def main_menu():
	main_font = pygame.font.SysFont("monospace", 40, bold=True, italic=False)
	run = True
	#INITAL DRAWING
	for y in range (math.ceil(HEIGHT/PIECE_SIZE)):
		for x in range (math.ceil(WIDTH/PIECE_SIZE)):
			WIN.blit(GREY_BLOCK, (x * PIECE_SIZE, y * PIECE_SIZE))

	while run:
		title_label1 = main_font.render(f"TETRIS", 1, (255,255,255))
		title_label2 = main_font.render(f"Clone", 1, (255,255,255))
		WIN.blit(title_label1, (WIDTH/2 - title_label1.get_width()/2, HEIGHT/2 - title_label1.get_height()/2))
		WIN.blit(title_label2, (WIDTH/2 - title_label2.get_width()/2, HEIGHT/2 + title_label2.get_height()/2))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					game()
					
	pygame.quit()


main_menu()





