
# Game Settings
GAME_TITLE = 'Space Invaders'
GAME_SIZE = { 
	'w' : 450, 
	'h' : 320
}
FPS = 40
LIVES = 3

# HUD setting
HUD_FONT_TYPE = 'monospace'
HUD_FONT_SIZE = 15

# Folder settings
SPRITE_FOLDER = "sprite/"
AUDIO_FOLDER = "audio/"


# Position of game elements
ENEMY_GRID = { 
	'x' : 11, 
	'y' : 5
}

STARTING_POSITIONS = {
	'PLAYER' : {
		'x' : 0.5,
		'y' : 0.9
	},
	'ENEMY' : {
		'x' : 0.05,
		'y' : 0.12,
		'SPACING' : {
			'x' : 0.07,
			'y' : 0.08
		}
	},
	'HI_SCORE' : {
		'x' : 10,
		'y' : 10
	},
	'LIVES' : {
		'x' : 300,
		'y' : 10
	}
}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)