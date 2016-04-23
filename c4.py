#!/usr/bin/env python
"""
  Author: Daniel P. Clark
  6ft Dan(TM)

  Release 1.7b
  Code Version 0.0.9b

  01-04-2002 : 06-24-2003

  E-mail: LiquidRock@UReach.com
"""


VERSION = "Version 1.7b - 0.0.9b" # Keep up to date, and about 21 chars long


"""
Connect Four, 2 player game
Copyright © 2002-2003 Daniel P. Clark

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

###TODO###
#
# add network support
# add a config file for specifying snapshot output directory, and optional other directories
# add a home directory config file support
# possibly make window scalable, with the game centerable (would be handy later)
# add a subscript to check and see that all dependancies are in order
# add a Linux installation script
# maybe add dropping piece animation as a function, and will run unless -slow tag is used
#


###BETA ADD###
#
# K_PRINT KEY
# MENU / Removed (Menu features not yet implemented)
# UNREPEATABLE SNAPSHOT NAMING
# GLOBALIZED AND MADE DYNAMIC FONT LOADING
# SHRINK FONT TO FIT IN PLACE
# Prints "Snapshot Taken"
#


import time, os, sys, string, socket
#import ocnet # one connection network
import pygame, pygame.font, pygame.image # load media modules
from pygame.locals import * # get local values


pygame.init() # initialize pygame
pygame.font.init() # initialize font


helptag = 0
audiotag = 0
imagetag = 0
infotag = 0

for x in sys.argv:
        if string.lower(x) in ("/?", "-?", "-help", "--help"):
                helptag = 1
        elif string.lower(x) in ("-a", "-audio", "--audio"):
                audiotag = 1
        elif string.lower(x) in ("-i", "-images", "--images"):
                imagetag = 1
        elif string.lower(x) in ("-info", "--info"):
                infotag = 1


if helptag:
        print
        print "Py Connect Four: HELP"
        print VERSION
        print "---------------------"
        print
        print "\t-audio  DIR\tSpecify Audio Directory to use."
        print "\t-a"
        print "\t-images DIR\tSpecify Image Directory to use."
        print "\t-i"
        print "\t-info      \tAbout the game and author."
        print "\t-help      \tThis help dialog."
        print "\t-?"
        print "\t/?"
        print
        print
        print "This program is distrobuted under the GNU GPL"
        print "either version 2, or any later version."
        print "Please copy and redistribute!"


if infotag:
        print
        print "Py Connect Four: INFO"
        print VERSION
        print "---------------------"
        print
        print "DEVELOPED WITH"
        print "Language: Python 2.2"
        print "Libraries: SDL 1.2.3, PyGame 1.2"
        print
        print "Author: Daniel P. Clark"
        print "6ft Dan(TM)"
        print
        print "Contact: flaminglinux@yahoo.com"
        print
        print "This program is distrobuted under the GNU GPL"
        print "either version 2, or any later version."


if helptag or infotag:
        pygame.quit()
        sys.exit()


# directory containing audio (you may make your own audio distro/folders)
if audiotag:
        for x in range(len(sys.argv)):
                if sys.argv[x] == "-audio":
                        AudioDir = sys.argv[x+1]
                        if AudioDir[-1] == os.sep:
                                AudioDir = AudioDir[:-1]
else:
        AudioDir = "audio"


AUDIO = os.path.isdir(AudioDir) # if audio directory exists
if AUDIO: # if audio directory exists
	import pygame.mixer # import pygames mixer module (for audio)
	pygame.mixer.init() # initialize mixer (enable sound use)


# redefinable image directory (all images must exist in the defined dir)
if "-images" in sys.argv:
        for x in range(len(sys.argv)):
                if sys.argv[x] == "-images":
                        ImageDir = sys.argv[x+1]
                        if ImageDir[-1] == os.sep:
                                ImageDir = ImageDir[:-1]
else:
        ImageDir = "images"


if not pygame.image.get_extended(): # if you can't use images other than bmp
	raise SystemExit, "Get SDL_image support!" # stop and complain


FontDir = "fonts"
FontFile = "times.ttf"

# Bool  (here just for the heck of it)
TRUE = 1
FALSE = 0
true = 1
false = 0


# Main values
ScreenWidth = 660 # DO NOT CHANGE
ScreenHeight = 480 # DO NOT CHANGE
ScreenRes = 16 # default 8
IMGWidth = 60 # DO NOT CHANGE # default 60 (for game board pieces)
IMGHeight = 60 # DO NOT CHANGE # default 60 (for game board pieces)
alive = 1 # DO NOT CHANGE (you change this to 0, and you disable the game from ever starting)
Winner = "" # every game needs a winner!
Player1Score = 0 # self explanitory :-p
Player2Score = 0 # same as line above!
Player = "Black" # changing this will do nothing (because I say it again later)
network = 0

BG_Menu_Color = (200,200,255)
BG_Button_Color = (0,0,200)
TXT_Menu_Color = (0,0,0)
TXT_Button_Color = (255,255,255)


def Fonts(): # function for loading fonts for usage
                global F_SIZES
                F_SIZES = [12,13,14,15,16,17,18,19,20,21,22,23,24] # Font Sizes
                for x in F_SIZES:
                        ENV_FVAR = "F_Times" + str(x) # Creates Font Name and # of size
                        ENV_FVAR += " = pygame.font.Font(os.path.join('"+FontDir+"','"+FontFile+"'),"+str(x)+")\n" # the font loading string
                        exec(ENV_FVAR, globals()) # execute font loading string (load it in globally)

Fonts() # load my fonts!

GameZones = [ # the game board is defined here, and in the game init loop later
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[1st] top row (y=0)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[2nd] (y=1)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[3rd] (y=2)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[4th] (y=3)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[5th] (y=4)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"], #[6th] (y=5)
["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"] #[7th] bottom row (y=6)
] # EBlock = empty block; RBlock = Red Piece; BBlock = Black Piece

GameZones2 = GameZones # duplicate list (list remains filled with EBlock)
GameZones2[0][0] = ":-)" # change first block in list to a useless smiley (used for list comparison later)


def images(): # functions for loading my images
	global I_EBlock, I_BBlock, I_RBlock, I_BG, I_6D, I_6DS, I_Icon # make images available anywhere
	global I_SDL, I_FE, I_FB, I_FR, I_WB, I_WR, I_Arrow, I_RArrow, I_LArrow # make images available anywhere
        global I_SMENU
	I_Icon = pygame.image.load(os.path.join(ImageDir,"c4icon.ico"), "BMP") # A simple bitmap renamed to ico for an icon
	I_EBlock = pygame.image.load(os.path.join(ImageDir,"emptyblock.gif"), "GIF") # Empty Block
	I_BBlock = pygame.image.load(os.path.join(ImageDir,"blackblock.gif"), "GIF") # Black Piece
	I_RBlock = pygame.image.load(os.path.join(ImageDir,"redblock.gif"), "GIF") # Red Piece
	I_RArrow = pygame.image.load(os.path.join(ImageDir,"arrowr.gif"), "GIF") # Arrow Right
	I_LArrow = pygame.image.load(os.path.join(ImageDir,"arrowl.gif"), "GIF") # Arrow Left
	I_6D = pygame.image.load(os.path.join(ImageDir,"6dlogo.gif"), "GIF") # my company logo :-)
	I_6DS = pygame.image.load(os.path.join(ImageDir,"6dsoft.gif"), "GIF") # 6ft Dan(TM) Software
	I_SDL = pygame.image.load(os.path.join(ImageDir,"sdl_prgb.gif"), "GIF") # SDL image
        I_SMENU = pygame.image.load(os.path.join(ImageDir,"startmenu.gif"), "GIF") # Start Menu
	I_FE = pygame.image.load(os.path.join(ImageDir,"femptyblock.gif"), "GIF") # Flat Empty Block
	I_FB = pygame.image.load(os.path.join(ImageDir,"fblackblock.gif"), "GIF") # Flat Black Piece
	I_FR = pygame.image.load(os.path.join(ImageDir,"fredblock.gif"), "GIF") # Flat Red Piece
	I_BG = pygame.image.load(os.path.join(ImageDir,"background.gif"), "GIF") # Background Image
	I_WB = pygame.image.load(os.path.join(ImageDir,"wblackblock.gif"), "GIF") # Winning Black Piece
	I_WR = pygame.image.load(os.path.join(ImageDir,"wredblock.gif"), "GIF") # Winning Red Piece

images() # load my beautiful images

def Sounds(): # define a function to load sounds
	global AU_6d, AU_sdl, AU_textin, AU_pick, AU_drop, AU_win # make sounds available anywhere
	AU_6d = pygame.mixer.Sound(os.path.join(AudioDir,"6d.wav"))
	AU_sdl = pygame.mixer.Sound(os.path.join(AudioDir,"sdl.wav"))
	AU_textin = pygame.mixer.Sound(os.path.join(AudioDir,"textin.wav"))
	AU_pick = pygame.mixer.Sound(os.path.join(AudioDir,"pick.wav"))
	AU_drop = pygame.mixer.Sound(os.path.join(AudioDir,"drop.wav"))
	AU_win = pygame.mixer.Sound(os.path.join(AudioDir,"win.wav"))

if AUDIO: Sounds() # if audio directory exists, load audio sounds

#write text to screen, with position, font, and font attributes specified
def write_text(text, dest_surface, x_origin, y_origin, font, fg_color, bg_color):
	font_surf = font.render(text, 1, fg_color, bg_color) # use text to make a font surface rendered in memory
	dest_surface.blit(font_surf,(x_origin, y_origin, font_surf.get_width(), font_surf.get_height()),(0, 0, font_surf.get_width(), font_surf.get_height())) # blit the rendered text with however wide the text is, and however tall
	pygame.display.update((x_origin, y_origin, font_surf.get_width(), font_surf.get_height())) # update the text we just wrote to the display

#write text centered between two x points, with position, font, and font attributes specified
def center_write_text(text, dest_surface, (x_origin,x_originEnd), y_origin, font, fg_color, bg_color):
	font_surf = font.render(text, 1, fg_color, bg_color) # use text to make a font surface rendered in memory
	x_Origin = (x_originEnd - x_origin)/2+x_origin-font_surf.get_width()/2 # center the text within the to x coords given
	dest_surface.blit(font_surf,(x_Origin, y_origin, font_surf.get_width(), font_surf.get_height()),(0, 0, font_surf.get_width(), font_surf.get_height())) # blit the rendered text with however wide the text is, and however tall
	pygame.display.update((x_Origin, y_origin, font_surf.get_width(), font_surf.get_height())) # update the text we just wrote to the display

# NOTE X and Y StartBlock should always be 0 (it's just here because of some other app I'm working on  (hint: navigatable maps))
def DrawGame(target, GameZones, XStartBlock = 0, YStartBlock = 0): # draw the board with all it's pieces
	for y in range(len(GameZones[YStartBlock:(420/IMGHeight+YStartBlock)])): # for each row in game list
		for x in range(len(GameZones[y][XStartBlock:(420/IMGWidth+XStartBlock)])): # for each column in game list
			if (y * IMGHeight < 420 + YStartBlock * IMGHeight) and (x * IMGWidth < 420 + XStartBlock * IMGWidth): # if x and y are less then max size of game board
				if GameZones[y+YStartBlock][x+XStartBlock] == "EBlock": # if the game list at y,x is empty block
					if GameZones[0][0] != GameZones2[0][0]: # if the current list is not the second list with the smiley
						target.blit(I_EBlock,((x*IMGWidth)+120,(y*IMGHeight)+IMGHeight,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw empty block
				elif GameZones[y+YStartBlock][x+XStartBlock] == "BBlock": # if game list at y,x is BBlock
					target.blit(I_BBlock,((x*IMGWidth)+120,(y*IMGHeight)+IMGHeight,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw black block
				elif GameZones[y+YStartBlock][x+XStartBlock] == "RBlock": # if game list at y,x is RBlock
					target.blit(I_RBlock,((x*IMGWidth)+120,(y*IMGHeight)+IMGHeight,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw red block
				elif GameZones[y+YStartBlock][x+XStartBlock] == "WB": # if game list at y,x is WB
					target.blit(I_WB,((x*IMGWidth)+120,(y*IMGHeight)+IMGHeight,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw winning black piece
				elif GameZones[y+YStartBlock][x+XStartBlock] == "WR": # if game list at y,x is WB
                                        target.blit(I_WR,((x*IMGWidth)+120,(y*IMGHeight)+IMGHeight,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw winning red piece
	for x in range(7): # loop 7 times (0-6)
		target.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty flat block
	target.blit(I_EBlock,(590,90,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # empty the piece picked block
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update the whole screen


# This is totally used for not just doing the first key in alphabetical order that is held down
# I have it so the if the last key used is still held down. it now checks all the other keys
# If no other key is pressed, it enters a repeat, otherwise it enters the other key held down
# e.g. try holding down 2 keys at the name enter prompt, like l and s, you get lslslslslsls etc.
def CheckOtherKeys(curKey):
        global keystate, VarIn
        other = 0
        if keystate[K_SPACE] and curKey != "space": # if space key in key pressed list is true
                other = 1
                VarIn += " " # add space to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_a] and curKey != "a": # if "a" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "A" # add to string
                else:
                        VarIn += "a" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_b] and curKey != "b": # if "b" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "B" # add to string
                else:
                        VarIn += "b" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_c] and curKey != "c": # if "c" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "C" # add to string
                else:
                        VarIn += "c" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_d] and curKey != "d": # if "d" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "D" # add to string
                else:
                        VarIn += "d" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_e] and curKey != "e": # if "e" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "E" # add to string
                else:
                        VarIn += "e" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_f] and curKey != "f": # if "f" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "F" # add to string
                else:
                        VarIn += "f" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_g] and curKey != "g": # if "g" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "G" # add to string
                else:
                        VarIn += "g" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_h] and curKey != "h": # if "h" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "H" # add to string
                else:
                        VarIn += "h" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_i] and curKey != "i": # if "i" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "I" # add to string
                else:
                        VarIn += "i" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_j] and curKey != "j": # if "j" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "J" # add to string
                else:
                        VarIn += "j" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_k] and curKey != "k": # if "k" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "K" # add to string
                else:
                        VarIn += "k" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_l] and curKey != "l": # if "l" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "L" # add to string
                else:
                        VarIn += "l" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_m] and curKey != "m": # if "m" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "M" # add to string
                else:
                        VarIn += "m" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_n] and curKey != "n": # if "n" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "N" # add to string
                else:
                        VarIn += "n" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_o] and curKey != "o": # if "o" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "O" # add to string
                else:
                        VarIn += "o" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_p] and curKey != "p": # if "p" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "P" # add to string
                else:
                        VarIn += "p" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_q] and curKey != "q": # if "q" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "Q" # add to string
                else:
                        VarIn += "q" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_r] and curKey != "r": # if "r" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "R" # add to string
                else:
                        VarIn += "r" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_s] and curKey != "s": # if "s" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "S" # add to string
                else:
                        VarIn += "s" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_t] and curKey != "t": # if "t" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "T" # add to string
                else:
                        VarIn += "t" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_u] and curKey != "u": # if "u" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "U" # add to string
                else:
                        VarIn += "u" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_v] and curKey != "v": # if "v" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "V" # add to string
                else:
                        VarIn += "v" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_w] and curKey != "w": # if "w" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "W" # add to string
                else:
                        VarIn += "w" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_x] and curKey != "x": # if "x" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "X" # add to string
                else:
                        VarIn += "x" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_y] and curKey != "y": # if "y" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "Y" # add to string
                else:
                        VarIn += "y" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_z] and curKey != "z": # if "z" key in key pressed list is true
                other = 1
                if keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
                        VarIn += "Z" # add to string
                else:
                        VarIn += "z" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_0] and curKey != "0": # if "0" key in key pressed list is true
                other = 1
                VarIn += "0" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_1] and curKey != "1": # if "1" key in key pressed list is true
                other = 1
                VarIn += "1" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_2] and curKey != "2": # if "2" key in key pressed list is true
                other = 1
                VarIn += "2" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_3] and curKey != "3": # if "3" key in key pressed list is true
                other = 1
                VarIn += "3" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_4] and curKey != "4": # if "4" key in key pressed list is true
                other = 1
                VarIn += "4" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_5] and curKey != "5": # if "5" key in key pressed list is true
                other = 1
                VarIn += "5" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_6] and curKey != "6": # if "6" key in key pressed list is true
                other = 1
                VarIn += "6" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_7] and curKey != "7": # if "7" key in key pressed list is true
                other = 1
                VarIn += "7" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_8] and curKey != "8": # if "8" key in key pressed list is true
                other = 1
                VarIn += "8" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        elif keystate[K_9] and curKey != "9": # if "9" key in key pressed list is true
                other = 1
                VarIn += "9" # add to string
                if AUDIO: AU_textin.play() # if audio dir exists, play sound
        return other


def TextInput(XPos,YPos,Font=F_Times16,FGColor=(255,255,255),BGColor=(0,0,0),MaxLen=18): # Check for key input, and display it where specified
        global keystate, VarIn
	VarIn = "" # this will contain the string the user enters
        lastChar = ""
	while 1: # just keep loopin!
                if len(VarIn) > MaxLen: # if string is too long
			VarIn = VarIn[:-1] # take 1 character off text
		if len(VarIn) > 0: # if character(s) exists
			write_text(VarIn,fb,XPos,YPos,Font,FGColor,BGColor) # display the string
                        lastChar = VarIn[-1] # for no repetitions unless nescesary
		event = pygame.event.poll() # check for input
		if event == NOEVENT: # if no input
			pass # do nothing
                elif event.type == QUIT: # if the found the X button that marks the spot (to close app)
                        pygame.quit() # close game
                        sys.exit() # exit out
		elif event.type in (KEYDOWN,): # if a key was just pressed
			keystate = pygame.key.get_pressed() # make a list off all the keys and their states
			if keystate[K_ESCAPE]: # if escape key in key pressed list is true
				pygame.quit() # shutdown pygame modules
				sys.exit() # exit app
			elif keystate[K_RETURN]: # if return key in key pressed list is true
				fb.fill(fb.map_rgb(BGColor),(XPos,YPos,Font.size(VarIn)[0],Font.size(VarIn)[1])) # erase text on display
				pygame.display.update((XPos,YPos,Font.size(VarIn)[0],Font.size(VarIn)[1])) # update display
				if AUDIO: AU_textin.play() # if audio dir exists, play sound # if audio dir exists, play sound
				return VarIn # return the string the user entered
			elif keystate[K_SPACE]: # if space key in key pressed list is true
                                if " " == lastChar:
                                        if CheckOtherKeys("space"):
                                                continue
                                VarIn += " " # add space to string
                                if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_a]: # if "a" key in key pressed list is true
                                if lastChar in ("a", "A"):
                                        if CheckOtherKeys("a") or CheckOtherKeys("A"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "A" # add to string
				else:
					VarIn += "a" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_b]: # if "b" key in key pressed list is true
                                if lastChar in ("b", "B"):
                                        if CheckOtherKeys("b") or CheckOtherKeys("B"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "B" # add to string
				else:
					VarIn += "b" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_c]: # if "c" key in key pressed list is true
                                if lastChar in ("c", "C"):
                                        if CheckOtherKeys("c") or CheckOtherKeys("C"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "C" # add to string
				else:
					VarIn += "c" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_d]: # if "d" key in key pressed list is true
                                if lastChar in ("d", "D"):
                                        if CheckOtherKeys("d") or CheckOtherKeys("D"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "D" # add to string
				else:
					VarIn += "d" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_e]: # if "e" key in key pressed list is true
                                if lastChar in ("e", "E"):
                                        if CheckOtherKeys("e") or CheckOtherKeys("E"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "E" # add to string
				else:
					VarIn += "e" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_f]: # if "f" key in key pressed list is true
                                if lastChar in ("f", "F"):
                                        if CheckOtherKeys("f") or CheckOtherKeys("F"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "F" # add to string
				else:
					VarIn += "f" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_g]: # if "g" key in key pressed list is true
                                if lastChar in ("g", "G"):
                                        if CheckOtherKeys("g") or CheckOtherKeys("G"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "G" # add to string
				else:
					VarIn += "g" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_h]: # if "h" key in key pressed list is true
                                if lastChar in ("h", "H"):
                                        if CheckOtherKeys("h") or CheckOtherKeys("H"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "H" # add to string
				else:
					VarIn += "h" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_i]: # if "i" key in key pressed list is true
                                if lastChar in ("i", "I"):
                                        if CheckOtherKeys("i") or CheckOtherKeys("I"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "I" # add to string
				else:
					VarIn += "i" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_j]: # if "j" key in key pressed list is true
                                if lastChar in ("j", "J"):
                                        if CheckOtherKeys("j") or CheckOtherKeys("J"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "J" # add to string
				else:
					VarIn += "j" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_k]: # if "k" key in key pressed list is true
                                if lastChar in ("k", "K"):
                                        if CheckOtherKeys("k") or CheckOtherKeys("K"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "K" # add to string
				else:
					VarIn += "k" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_l]: # if "l" key in key pressed list is true
                                if lastChar in ("l", "L"):
                                        if CheckOtherKeys("l") or CheckOtherKeys("L"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "L" # add to string
				else:
					VarIn += "l" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_m]: # if "m" key in key pressed list is true
                                if lastChar in ("m", "M"):
                                        if CheckOtherKeys("m") or CheckOtherKeys("M"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "M" # add to string
				else:
					VarIn += "m" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_n]: # if "n" key in key pressed list is true
                                if lastChar in ("n", "N"):
                                        if CheckOtherKeys("n") or CheckOtherKeys("N"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "N" # add to string
				else:
					VarIn += "n" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_o]: # if "o" key in key pressed list is true
                                if lastChar in ("o", "O"):
                                        if CheckOtherKeys("o") or CheckOtherKeys("O"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "O" # add to string
				else:
					VarIn += "o" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_p]: # if "p" key in key pressed list is true
                                if lastChar in ("p", "P"):
                                        if CheckOtherKeys("p") or CheckOtherKeys("P"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "P" # add to string
				else:
					VarIn += "p" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_q]: # if "q" key in key pressed list is true
                                if lastChar in ("q", "Q"):
                                        if CheckOtherKeys("q") or CheckOtherKeys("Q"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "Q" # add to string
				else:
					VarIn += "q" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_r]: # if "r" key in key pressed list is true
                                if lastChar in ("r", "R"):
                                        if CheckOtherKeys("r") or CheckOtherKeys("R"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "R" # add to string
				else:
					VarIn += "r" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_s]: # if "s" key in key pressed list is true
                                if lastChar in ("s", "S"):
                                        if CheckOtherKeys("s") or CheckOtherKeys("S"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "S" # add to string
				else:
					VarIn += "s" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_t]: # if "t" key in key pressed list is true
                                if lastChar in ("t", "T"):
                                        if CheckOtherKeys("t") or CheckOtherKeys("T"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "T" # add to string
				else:
					VarIn += "t" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_u]: # if "u" key in key pressed list is true
                                if lastChar in ("u", "U"):
                                        if CheckOtherKeys("u") or CheckOtherKeys("U"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "U" # add to string
				else:
					VarIn += "u" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_v]: # if "v" key in key pressed list is true
                                if lastChar in ("v", "V"):
                                        if CheckOtherKeys("v") or CheckOtherKeys("V"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "V" # add to string
				else:
					VarIn += "v" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_w]: # if "w" key in key pressed list is true
                                if lastChar in ("w", "W"):
                                        if CheckOtherKeys("w") or CheckOtherKeys("W"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "W" # add to string
				else:
					VarIn += "w" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_x]: # if "x" key in key pressed list is true
                                if lastChar in ("x", "X"):
                                        if CheckOtherKeys("x") or CheckOtherKeys("X"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "X" # add to string
				else:
					VarIn += "x" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_y]: # if "y" key in key pressed list is true
                                if lastChar in ("y", "Y"):
                                        if CheckOtherKeys("y") or CheckOtherKeys("Y"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "Y" # add to string
				else:
					VarIn += "y" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_z]: # if "z" key in key pressed list is true
                                if lastChar in ("z", "Z"):
                                        if CheckOtherKeys("z") or CheckOtherKeys("Z"):
                                                continue
                                elif keystate[K_RSHIFT] or keystate[K_LSHIFT]: # if shift key in key pressed list is true
					VarIn += "Z" # add to string
				else:
					VarIn += "z" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_0]: # if "0" key in key pressed list is true
                                if "0" == lastChar:
                                        if CheckOtherKeys("0"):
                                                continue
				VarIn += "0" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_1]: # if "1" key in key pressed list is true
                                if "1" == lastChar:
                                        if CheckOtherKeys("1"):
                                                continue
				VarIn += "1" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_2]: # if "2" key in key pressed list is true
                                if "2" == lastChar:
                                        if CheckOtherKeys("2"):
                                                continue
				VarIn += "2" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_3]: # if "3" key in key pressed list is true
                                if "3" == lastChar:
                                        if CheckOtherKeys("3"):
                                                continue
				VarIn += "3" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_4]: # if "4" key in key pressed list is true
                                if "4" == lastChar:
                                        if CheckOtherKeys("4"):
                                                continue
				VarIn += "4" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_5]: # if "5" key in key pressed list is true
                                if "5" == lastChar:
                                        if CheckOtherKeys("5"):
                                                continue
				VarIn += "5" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_6]: # if "6" key in key pressed list is true
                                if "6" == lastChar:
                                        if CheckOtherKeys("6"):
                                                continue
				VarIn += "6" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_7]: # if "7" key in key pressed list is true
                                if "7" == lastChar:
                                        if CheckOtherKeys("7"):
                                                continue
				VarIn += "7" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_8]: # if "8" key in key pressed list is true
                                if "8" == lastChar:
                                        if CheckOtherKeys("8"):
                                                continue
				VarIn += "8" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_9]: # if "9" key in key pressed list is true
                                if "9" == lastChar:
                                        if CheckOtherKeys("9"):
                                                continue
				VarIn += "9" # add to string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
			elif keystate[K_BACKSPACE]: # if backspace key in key pressed list is true
				fb.fill(fb.map_rgb(BGColor),(XPos+Font.size(VarIn[:-1])[0],YPos,Font.size(VarIn[-1:])[0],Font.size(VarIn[-1:])[1]))
				pygame.display.update((XPos+Font.size(VarIn[:-1])[0],YPos,Font.size(VarIn[-1:])[0],Font.size(VarIn[-1:])[1]))
				VarIn = VarIn[:-1] # subtract 1 off of end of string
				if AUDIO: AU_textin.play() # if audio dir exists, play sound
                pygame.time.delay(4)



def Draw_Box((x,y,x2,y2),Color=(0,0,0),EdgeWidth=1): # Draw an empty Box
	fb.fill(fb.map_rgb(Color),(x,y,x2-x,EdgeWidth)) # draw top of box
	fb.fill(fb.map_rgb(Color),(x,y,EdgeWidth,y2-y)) # draw left side of box
	fb.fill(fb.map_rgb(Color),(x2-EdgeWidth,y,EdgeWidth,y2-y)) # draw right side of box
	fb.fill(fb.map_rgb(Color),(x,y2-EdgeWidth,x2-x,EdgeWidth)) # draw bottom of box

def Draw_FBox((x,y,x2,y2),IColor=(50,50,50),Color=(0,0,0),EdgeWidth=1): # Draw a filled Box
	fb.fill(fb.map_rgb(IColor),(x,y,x2-x,y2-y)) # draw filled box
	fb.fill(fb.map_rgb(Color),(x,y,x2-x,EdgeWidth)) # draw top of box
	fb.fill(fb.map_rgb(Color),(x,y,EdgeWidth,y2-y)) # draw left side of box
	fb.fill(fb.map_rgb(Color),(x2-EdgeWidth,y,EdgeWidth,y2-y)) # draw right side of box
	fb.fill(fb.map_rgb(Color),(x,y2-EdgeWidth,x2-x,EdgeWidth)) # draw bottom of box

def IdealFont(dest_surface, x, y, fg, bg, String, PixelWidth, FontS=16, SizeList=F_SIZES):
        NOW_OK = 0
        while not NOW_OK:
                ENV_FVAR = "SWidth = F_Times" + str(FontS) + ".size(\"" + String + "\")[0]"
                exec(ENV_FVAR)
                CFONT = "F_Times"+str(FontS)
                if SWidth >= PixelWidth:
                        FontS = SizeList[SizeList.index(FontS)-1]
                else:
                        exec("center_write_text('"+String+"',dest_surface,(x,x+PixelWidth), y,"+CFONT+", fg, bg)")
                        NOW_OK = 1

def Draw_Esc_Menu(): # menu display to quit the game
	fb.fill(fb.map_rgb(BG_Menu_Color),(ScreenWidth/2-250/2,ScreenHeight/2-100/2,250,100)) # draw a box in the center of the screen
	fb.fill(fb.map_rgb(BG_Button_Color),((ScreenWidth/2-250/2)+40,(ScreenHeight/2-100/2)+60,75,20)) # draw the box for the yes key, related to center
	fb.fill(fb.map_rgb(BG_Button_Color),((ScreenWidth/2-250/2)+135,(ScreenHeight/2-100/2)+60,75,20)) # draw the box for the no key, related to center
	Draw_Box(((ScreenWidth/2-250/2),(ScreenHeight/2-100/2),(ScreenWidth/2-250/2)+250,(ScreenHeight/2-100/2)+100)) # draw empty box border
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update full display
	IdealFont(fb,(ScreenWidth/2-250/2),(ScreenHeight/2-100/2)+5,TXT_Menu_Color,BG_Menu_Color,"Are you sure you want to quit? y or n",250) # OLD-> # write_text("Are you sure you want to quit? y or n",fb,(ScreenWidth/2-250/2)+5,(ScreenHeight/2-100/2)+5,F_Times16,(0,0,0),(125,125,255)) # write text within box, related to center pos
	IdealFont(fb,(ScreenWidth/2-250/2)+40,(ScreenHeight/2-100/2)+60,TXT_Button_Color,BG_Button_Color,"yes",75) # OLD-> # write_text("yes",fb,(ScreenWidth/2-250/2)+67,(ScreenHeight/2-100/2)+60,F_Times16,(255,255,0),(0,0,255)) # draw yes in yes box, related to center
	IdealFont(fb,(ScreenWidth/2-250/2)+135,(ScreenHeight/2-100/2)+60,TXT_Button_Color,BG_Button_Color,"no",75) # OLD-> # write_text("no",fb,(ScreenWidth/2-250/2)+165,(ScreenHeight/2-100/2)+60,F_Times16,(255,255,0),(0,0,255)) # draw no in no box, related to center

def Play_Again_Menu(): # play again menu lower left side of screen
	fb.fill(fb.map_rgb(BG_Menu_Color),(ScreenWidth/2-250/2,ScreenHeight/2-100/2,250,100)) # draw a box in the center of the screen
	fb.fill(fb.map_rgb(BG_Button_Color),((ScreenWidth/2-250/2)+40,(ScreenHeight/2-100/2)+60,75,20)) # draw the box for the yes key, related to center
	fb.fill(fb.map_rgb(BG_Button_Color),((ScreenWidth/2-250/2)+135,(ScreenHeight/2-100/2)+60,75,20)) # draw the box for the no key, related to center
	Draw_Box(((ScreenWidth/2-250/2),(ScreenHeight/2-100/2),(ScreenWidth/2-250/2)+250,(ScreenHeight/2-100/2)+100)) # draw empty box border
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update full display
	IdealFont(fb,(ScreenWidth/2-250/2),(ScreenHeight/2-100/2)+5,TXT_Menu_Color,BG_Menu_Color,"Play Again? y or n",250) # OLD-> # write_text("Are you sure you want to quit? y or n",fb,(ScreenWidth/2-250/2)+5,(ScreenHeight/2-100/2)+5,F_Times16,(0,0,0),(125,125,255)) # write text within box, related to center pos
	IdealFont(fb,(ScreenWidth/2-250/2)+40,(ScreenHeight/2-100/2)+60,TXT_Button_Color,BG_Button_Color,"yes",75) # OLD-> # write_text("yes",fb,(ScreenWidth/2-250/2)+67,(ScreenHeight/2-100/2)+60,F_Times16,(255,255,0),(0,0,255)) # draw yes in yes box, related to center
	IdealFont(fb,(ScreenWidth/2-250/2)+135,(ScreenHeight/2-100/2)+60,TXT_Button_Color,BG_Button_Color,"no",75) # OLD-> # write_text("no",fb,(ScreenWidth/2-250/2)+165,(ScreenHeight/2-100/2)+60,F_Times16,(255,255,0),(0,0,255)) # draw no in no box, related to center

def Back(target): # draw background of the game
	target.blit(I_BG,(0,0,ScreenWidth,ScreenHeight),(0,0,ScreenWidth,ScreenHeight)) # blit background image to surface
	center_write_text(Black+": "+str(Player1Score),fb,(0,ScreenWidth/2),5,F_Times16,(0,0,0),(255,255,255)) # write Black players name and score
	center_write_text(Red+": "+str(Player2Score),fb,(ScreenWidth/2,ScreenWidth),5,F_Times16,(0,0,0),(255,255,255)) # write Red players name and score
        target.blit(I_LArrow,(ScreenWidth/2-38/2,0,38,38),(0,0,38,38)) # draw arrow pointing up (between names)
	IdealFont(fb,580,70,(0,0,0),(255,255,255),"Piece Picked",ScreenWidth-580) # OLD-> # write_text("Piece Picked",fb,580,70,F_Times16,(0,0,0),(255,255,255))
	target.blit(I_EBlock,(590,90,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw empty block on right of surface, under piece picked text

def PiecePicked(target, Color): # used for showing whos turn it is
	if Color == "Red": # if player is red
		target.blit(I_RArrow,(ScreenWidth/2-38/2,0,38,38),(0,0,38,38)) # point to red players name
		pygame.display.update(ScreenWidth/2-38/2,0,38,38) # update display where the arrow is
		target.blit(I_RBlock,(590,90,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw red block for piece picked
		pygame.display.update(590,90,IMGWidth,IMGHeight) # update red block for piece picked (on right of surface)
	elif Color == "Black": # if player is black
		target.blit(I_LArrow,(ScreenWidth/2-38/2,0,38,38),(0,0,38,38)) # point to black players name
		pygame.display.update(ScreenWidth/2-38/2,0,38,38) # update display where the arrow is
		target.blit(I_BBlock,(590,90,IMGWidth,IMGHeight),(0,0,IMGWidth,IMGHeight)) # draw black block for piece picked
		pygame.display.update(590,90,IMGWidth,IMGHeight) # update black block for piece picked (on right of surface)
	if AUDIO: AU_pick.play() # if audio dir exists, play sound

def FindWinner((y,x),List): # check for a winner in the game
	global Winner, Player1Score, Player2Score # make values changable globaly/ make available
	for A in range(len(GameZones)): # for each place in GameZones, give me each row 1 at a time
		for B in range(len(GameZones[A])): # for each place in Gamezones rows, give me each column 1 at a time
			GameZones2[A][B] = GameZones[A][B] # copy item in list to other list, in same position
	# the directional strings that follow, have a 1 in it for the piece that was just put in it, adding to the beginning of the string, is for left in general, and to the end, for right in general
	NWSE = "1" # UP LEFT TO DOWN RIGHT (NorthWest - SouthEast)
	WE = "1" # LEFT TO RIGHT (West - East)
	SWNE = "1" # DOWN LEFT TO UP RIGHT (SouthWest - NorthEast)
	S = "1" # DOWN (South) ##NOTE for each piece put in, we check from the piece just put on top of the current column, so there is NO piece above it
	D2 = List[y][x] # Dropped Type (get type of piece just put in)
	for P in range(1,6): # for all the possible distances from piece just put in, not including itself
		if -1 < y-P < 7 and -1 < x-P < 7: # if exists (don't go further than the list's border) (don't go further than the list's border)
			if List[y-P][x-P] == D2: # if same piece
				NWSE = "1"+NWSE # add 1 to beginning of string
			else:
				NWSE = "0"+NWSE # add 0 to beginning of string
		if -1 < y+P < 7 and -1 < x+P < 7: # if exists (don't go further than the list's border)
			if List[y+P][x+P] == D2: # if same piece
				NWSE = NWSE+"1" # add 1 to end of string
			else:
				NWSE = NWSE+"0" # add 0 to end of string
		if -1 < x-P < 7: # if exists (don't go further than the list's border)
			if List[y][x-P] == D2: # if same piece
				WE = "1"+WE # add 1 to beginning of string
			else:
				WE = "0"+WE # add 0 to beginning of string
		if -1 < x+P < 7: # if exists (don't go further than the list's border)
			if List[y][x+P] == D2: # if same piece
				WE = WE+"1" # add 1 to end of string
			else:
				WE = WE+"0" # add 0 to end of string
		if -1 < y+P < 7 and -1 < x-P < 7: # if exists (don't go further than the list's border)
			if List[y+P][x-P] == D2: # if same piece
				SWNE = "1"+SWNE # add 1 to beginning of string
			else:
				SWNE = "0"+SWNE # add 0 to beginning of string
		if -1 < y-P < 7 and -1 < x+P < 7: # if exists (don't go further than the list's border)
			if List[y-P][x+P] == D2: # if same piece
				SWNE = SWNE+"1" # add 1 to end of string
			else:
				SWNE = SWNE+"0" # add 0 to end of string
		if -1 < y+P < 7: # if exists (don't go further than the list's border)
			if List[y+P][x] == D2: # if same piece
				S=S+"1" # add 1 to beginning of string
			else:
				S=S+"0" # add 0 to beginning of string
	if len(NWSE) > 3: # if it's greater than 4 pieces (in 2 corners this will not be true)
		NW = 0 # needed for knowing how far to go nw drawing the winning pieces to list
		SE = 0 # needed for knowing how far to go se drawing the winning pieces to list
		for P in range(6): # loop 7 times, incementing P each time
			if string.find(NWSE,"1111") != -1: # if 4 in a row!
				if List[y][x] == "BBlock": # check for piece put in
					Winner = "Black" # declare winner
				elif List[y][x] == "RBlock": # check for piece put in
					Winner = "Red" # declare winner
				if -1 < y-P < 7 and -1 < x-P < 7: # if exists (don't go further than the list's border)
					if List[y-P][x-P] == D2: # if same piece
						if NW == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y-P][x-P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y-P][x-P] = "WR" # put winning piece in list
					else:
						NW = 1
				if -1 < y+P < 7 and -1 < x+P < 7: # if exists (don't go further than the list's border)
					if List[y+P][x+P] == D2: # if same piece
						if SE == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y+P][x+P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y+P][x+P] = "WR" # put winning piece in list
					else:
						SE = 1
				DrawGame(fb,GameZones2)
	if len(WE) > 3: # will always be true, no real need for it, but keeps the code in order
		W = 0 # needed for knowing how far to go w drawing the winning pieces to list
		E = 0 # needed for knowing how far to go e drawing the winning pieces to list
		for P in range(6): # loop 7 times, incementing P each time
			if string.find(WE,"1111") != -1: # if 4 in a row!
				if List[y][x] == "BBlock": # check for piece put in
					Winner = "Black" # declare winner
				elif List[y][x] == "RBlock": # check for piece put in
					Winner = "Red" # declare winner
				if -1 < x-P < 7: # if exists (don't go further than the list's border)
					if List[y][x-P] == D2: # if same piece
						if W == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y][x-P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y][x-P] = "WR" # put winning piece in list
					else:
						W = 1
				if -1 < x+P < 7: # if exists (don't go further than the list's border)
					if List[y][x+P] == D2: # if same piece
						if E == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y][x+P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y][x+P] = "WR" # put winning piece in list
					else:
						E = 1
				DrawGame(fb,GameZones2)
	if len(SWNE) > 3: # if it's greater than 4 pieces (in 2 corners this will not be true)
		SW = 0 # needed for knowing how far to go sw drawing the winning pieces to list
		NE = 0 # needed for knowing how far to go ne drawing the winning pieces to list
		for P in range(6): # loop 7 times, incementing P each time
			if string.find(SWNE,"1111") != -1: # if 4 in a row!
				if List[y][x] == "BBlock": # check for piece put in
					Winner = "Black" # declare winner
				elif List[y][x] == "RBlock": # check for piece put in
					Winner = "Red" # declare winner
				if -1 < y+P < 7 and -1 < x-P < 7: # if exists (don't go further than the list's border)
					if List[y+P][x-P] == D2: # if same piece
						if SW == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y+P][x-P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y+P][x-P] = "WR" # put winning piece in list
					else:
						SW = 1
				if -1 < y-P < 7 and -1 < x+P < 7: # if exists (don't go further than the list's border)
					if List[y-P][x+P] == D2: # if same piece
						if NE == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y-P][x+P] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y-P][x+P] = "WR" # put winning piece in list
					else:
						NE = 1
				DrawGame(fb,GameZones2)
	if len(S) > 3: # if it's greater than 4 pieces
		ST = 0 # needed for knowing how far to go s drawing the winning pieces to list
		for P in range(6): # loop 7 times, incementing P each time
			if string.find(S,"1111") != -1: # if 4 in a row!
				if List[y][x] == "BBlock": # check for piece put in
					Winner = "Black" # declare winner
				elif List[y][x] == "RBlock": # check for piece put in
					Winner = "Red" # declare winner
				if -1 < y+P < 7: # if exists (don't go further than the list's border)
					if List[y+P][x] == D2: # if same piece
						if ST == 0: # check for continuation from piece put in
							if Winner == "Black": # if winner is black player
								GameZones2[y+P][x] = "WB" # put winning piece in list
							if Winner == "Red": # if winner is red player
								GameZones2[y+P][x] = "WR" # put winning piece in list
					else:
						ST = 1
				DrawGame(fb,GameZones2)
	if Winner == "Black": # check winner
		Player1Score += 1 # add 1 point to winners score
		if AUDIO: AU_win.play() # if audio dir exists, play sound
		center_write_text(Black+": "+str(Player1Score),fb,(0,ScreenWidth/2),5,F_Times16,(0,0,0),(255,255,255)) # write new score to screen
		print Black+": "+str(Player1Score) # write on console black players score
		print Red+": "+str(Player2Score) # write on console red players score
	if Winner == "Red": # check winner
		Player2Score += 1 # add 1 point to winners score
		if AUDIO: AU_win.play() # if audio dir exists, play sound
		center_write_text(Red+": "+str(Player2Score),fb,(ScreenWidth/2,ScreenWidth),5,F_Times16,(0,0,0),(255,255,255)) # write new score to screen
		print Black+": "+str(Player1Score) # write on console black players score
		print Red+": "+str(Player2Score) # write on console red players score
	if List[0].count("EBlock") == 0: # count number of accurances of "EBlock" in top row, if none
		Winner = "NO1" # Game is full, no 1 won, time for next game


def PYC4(): # This is were the application truly begins
        global fb, Player, Black, Red, Winner, network # make available and editable
	pygame.display.set_caption("Connect Four") # set windows caption to Connect Four
	pygame.display.set_icon(I_Icon) # set Icon for the window
	fb = pygame.display.set_mode((ScreenWidth, ScreenHeight), SWSURFACE | ANYFORMAT, ScreenRes) # make a display surface
	pygame.mouse.set_visible(TRUE) # mouse is available
	pygame.event.set_blocked(ACTIVEEVENT) # don't care for knowing when the app is in focus
	pygame.event.set_blocked(KEYUP) # don't notice keyup instances
	pygame.event.set_blocked(MOUSEMOTION) # not looking for when a user moves the mouse
	pygame.event.set_blocked(MOUSEBUTTONUP) # don't notice button up instance
	pygame.event.set_blocked(JOYHATMOTION) # no joystick
	pygame.event.set_blocked(JOYAXISMOTION) # no joystick
	pygame.event.set_blocked(JOYBALLMOTION) # no joystick
	pygame.event.set_blocked(JOYBUTTONUP) # no joystick
	pygame.event.set_blocked(JOYBUTTONDOWN) # no joystick
	pygame.event.set_allowed(QUIT) # let the quit be handed to the program
	pygame.event.set_allowed(KEYDOWN) # let the program take not of when a key is pressed
	pygame.event.set_allowed(MOUSEBUTTONDOWN) # watch the mouse button
	pygame.key.set_repeat(500,10) # how many time a character repeats when a key is held down
	fb.fill(fb.map_rgb((255,255,255))) # fill the surface with white
	fb.blit(I_6D,(130,5,400,400),(0,0,400,400)) # 6D Logo
	fb.blit(I_6DS,(120,405,420,65),(0,0,420,65)) # 6ft Dan(TM) Software
	if AUDIO: AU_6d.play() # if audio dir exists, play sound
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update the screen
        pygame.time.delay(4000) # pause 4 seconds
	for x in range(0,255,5): # loop through 255 by 5's
		fb.fill(fb.map_rgb(((255-x),(255-x),(255-x)))) # fill screen from color white to black
		pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update screen
	fb.blit(I_SDL,(210,180,240,120),(0,0,240,120)) # draw SDL image to surface
	if AUDIO: AU_sdl.play() # if audio dir exists, play sound
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update screen
	pygame.time.delay(3800) # pause 3.8 seconds
	fb.fill(fb.map_rgb((0,0,0)),(210,180,240,120)) # draw black over SDL image
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update screen
#        LNJ = 0 # 1, 2, or 3 (Local, Net, Just play)
#        fb.blit(I_SMENU,(120,0,400,480),(0,0,400,480)) # Start Menu
#        while 1:
#                pygame.display.update((120,0,400,480)) # update screen
#                event = pygame.event.poll() # get user event
#                if event == NOEVENT: # if the players are sleeping (not on the keyboard mind you)
#                        pass # pretend like I don't care
#                elif event.type == QUIT: # if the found the X button that marks the spot (to close app)
#                        pygame.quit() # close game
#                        sys.exit() # exit out
#                elif event.type in (KEYDOWN,):
#                        keystate = pygame.key.get_pressed() # get list of keys states
#                        if keystate[K_ESCAPE]: # if escape was pressed in the list
#                                pygame.quit() # close game
#                                sys.exit() # exit out
#                        elif keystate[K_l]:
#                                LNJ = 1
#                                break
#                        elif keystate[K_n]:
#                                LNJ = 2
#                                break
#                        elif keystate[K_j]:
#                                LNJ = 3
#                                break
#                elif event.type in (MOUSEBUTTONDOWN,):
#                        mouse_button = pygame.mouse.get_pressed() # get mouse key values # right handed mouse(1 = left, 2 = middle, 3 = right)
#                        if event.button == 1: # if they used the standard mouse button
#                                mouse_position = pygame.mouse.get_pos()
#                                if (426 > mouse_position[0] > 202) and (171 > mouse_position[1] > 106):
#                                        LNJ = 1
#                                        break
#                                elif (426 > mouse_position[0] > 202) and (253 > mouse_position[1] > 171):
#                                        LNJ = 2
#                                        break
#                                elif (426 > mouse_position[0] > 202) and (350 > mouse_position[1] > 253):
#                                        LNJ = 3
#                                        break
#                mouse_position = pygame.mouse.get_pos() # find where the heck the mouse is
#                if (426 > mouse_position[0] > 202) and (171 > mouse_position[1] > 106):
#                        Draw_Box((202,106,426,171),(70,70,70))
#                        fb.fill(fb.map_rgb((0,0,0)),(120,398,400,42))
#                        center_write_text("2 Player, enter your names.", fb, (0,ScreenWidth), 400, F_Times24, (255,255,255), (0,0,0))
#                        Draw_Box((202,171,426,253),(0,0,0))
#                        Draw_Box((202,253,426,350),(0,0,0))
#                elif (426 > mouse_position[0] > 202) and (253 > mouse_position[1] > 171):
#                        Draw_Box((202,171,426,253),(70,70,70))
#                        fb.fill(fb.map_rgb((0,0,0)),(120,398,400,42))
#                        center_write_text("Network Play.", fb, (0,ScreenWidth), 400, F_Times24, (255,255,255), (0,0,0))
#                        Draw_Box((202,106,426,171),(0,0,0))
#                        Draw_Box((202,253,426,350),(0,0,0))
#                elif (426 > mouse_position[0] > 202) and (350 > mouse_position[1] > 253):
#                        Draw_Box((202,253,426,350),(70,70,70))
#                        fb.fill(fb.map_rgb((0,0,0)),(120,398,400,42))
#                        center_write_text("2 Player, skip entering names.", fb, (0,ScreenWidth), 400, F_Times24, (255,255,255), (0,0,0))
#                        Draw_Box((202,106,426,171),(0,0,0))
#                        Draw_Box((202,171,426,253),(0,0,0))
#                else:
#                        fb.fill(fb.map_rgb((0,0,0)),(120,398,400,42))
#                        Draw_Box((202,106,426,171),(0,0,0))
#                        Draw_Box((202,171,426,253),(0,0,0))
#                        Draw_Box((202,253,426,350),(0,0,0))
#                pygame.time.delay(10) # 10 milliseconds of a delay for full game loop
	LNJ = 1 # This should be here unless menu is un-commented.
        if LNJ == 1:
                fb.fill(fb.map_rgb((0,0,0)),(120,0,400,480))
                pygame.display.update((120,0,400,480))
                center_write_text("(Player 1) Enter Your Name",fb,(0,ScreenWidth),0,F_Times24,(255,255,255),(0,0,0)) # draw text at top of screen for user to enter name
                Black = TextInput(60,220) # run the text input function to get black players name
                center_write_text("(Player 2) Enter Your Name",fb,(0,ScreenWidth),0,F_Times24,(255,255,255),(0,0,0)) # draw text at top of screen for user to enter name
                Red = TextInput(60,220) # run the text input function to get black players name
#        elif LNJ == 2:
#                network = 1
#                print "Not yet implemented!"
#                pygame.quit() # close game
#                sys.exit() # exit out
#        elif LNJ == 3:
#                Black = "Player One"
#                Red = "Player Two"
	Back(fb) # draw background
	pygame.display.update((0,0,ScreenWidth,ScreenHeight)) # update screen
	IOMode = "Start" # Interface option (for controling input/ouput)
	while alive: # if no idiots have disabled the game (look at beginning of source "alive = 1")
		# Check for key input
		event = pygame.event.poll() # get user event
		if IOMode == "Start": # for starting a game round
			GameZones = [ # define an empty board
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"],
			["EBlock","EBlock","EBlock","EBlock","EBlock","EBlock","EBlock"]
			]
			for A in range(len(GameZones)): # for all of the rows in the game
				for B in range(len(GameZones[A])): # for all of the columns in the game
					GameZones2[A][B] = GameZones[A][B] # copy
			GameZones2[0][0] = ":-)" # change the first item so the lists differ (used for list checking later)
			Back(fb) # draw background
			DrawGame(fb, GameZones) # draw board and pieces
			CanWin = 0 # game counts to 7 before some one can win (no one can win till an 8th piece is put in)
			Player = "Black" # starting player
			Winner = ""
			Space = 0
			center_write_text("Right Click or Hit Space to pick up piece",fb,(120,540),41,F_Times16,(0,0,0),(255,255,255))
			IOMode = "Game"
		elif IOMode == "Game":
			if event == NOEVENT:
				pass
			elif event.type == QUIT:
				Draw_Esc_Menu()
				IOMode="Esc Menu"
                        elif event.type in (KEYDOWN,):
				keystate = pygame.key.get_pressed()
				if keystate[K_ESCAPE]:
					Draw_Esc_Menu()
					IOMode="Esc Menu"
				elif keystate[K_SPACE]:
					Space = 1
					PiecePicked(fb,Player)
				elif keystate[K_F12] or keystate[K_PRINT]: # if they pushed the screenshot key F12
					pygame.image.save(fb, "snapshot"+str(time.time())+".bmp") # give them a snapshot of the game
					IdealFont(fb,120,40,(0,0,0),(255,255,255),"Snapshot Taken",420)
                        elif event.type in (MOUSEBUTTONDOWN,):
				mouse_button = pygame.mouse.get_pressed() # get mouse key values # right handed mouse(1 = left, 2 = middle, 3 = right)
				if event.button == 1: # if they used the standard mouse button
					mouse_position = pygame.mouse.get_pos()
					if Space:
						if (180 > mouse_position[0] > 120) and mouse_position[1] >= 40: # if the mouse is over the first column
							if GameZones[0][0] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][0] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][0] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,0),GameZones) # check for win send (y, x) coords, and check from list gamezones
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][0] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][0] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,0),GameZones) # check for win send (y, x) coords, and check from list gamezones
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (240 > mouse_position[0] > 180) and mouse_position[1] >= 40: # if the mouse is over the second column
							if GameZones[0][1] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][1] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][1] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,1),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][1] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][1] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,1),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (300 > mouse_position[0] > 240) and mouse_position[1] >= 40: # if the mouse is over the third column
							if GameZones[0][2] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][2] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][2] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,2),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][2] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][2] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,2),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (360 > mouse_position[0] > 300) and mouse_position[1] >= 40: # if the mouse is over the fourth column
							if GameZones[0][3] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][3] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][3] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,3),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][3] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][3] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,3),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (420 > mouse_position[0] > 360) and mouse_position[1] >= 40: # if the mouse is over the fith column
							if GameZones[0][4] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][4] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][4] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,4),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][4] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][4] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,4),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (480 > mouse_position[0] > 420) and mouse_position[1] >= 40: # if the mouse is over the sixth column
							if GameZones[0][5] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][5] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][5] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,5),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][5] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][5] = "RBlock" # insert red block at first available position from bottom to top
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,5),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
						elif (540 > mouse_position[0] > 480) and mouse_position[1] >= 40: # if the mouse is over the seventh column
							if GameZones[0][6] == "EBlock": # if the top block of the column is empty, user can put piece in
								if Player == "Black": # if the current player is the black player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][6] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][6] = "BBlock" # insert black block at first available position from bottom to top
											Space = 0 # reset the pickup piece value                   
											Player = "Red" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,6),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
								elif Player == "Red": # if the current player is the red player
									for x in range(len(GameZones)): # just loops 7 times (this should be y, for it to make more sense)
										if GameZones[6-x][6] == "EBlock": # check from bottom to top, where the first place the piece can go is
											GameZones[6-x][6] = "RBlock"
											Space = 0 # reset the pickup piece value
											Player = "Black" # set next player
											CanWin += 1 # increment CanWin by one (keep track for when it's possible to win, needs to be atleast 7 to win)
											if AUDIO: AU_drop.play() # if audio dir exists, play sound
											DrawGame(fb, GameZones) # draw board and pieces
											if CanWin > 6: # if more than 6 pieces have been entered, it is possible for a win
												FindWinner((6-x,6),GameZones)
												if Winner != "": # if round is over
													Play_Again_Menu() # ask if a new game is desired
													IOMode = "Again Menu" # give control over to the play again menu
											break
				elif event.button == 3: # if third mouse button is pressed
					Space = 1 # set piece as picked
					PiecePicked(fb,Player) # do what is required when a piece is picked
				else:
					pass
			if Space: # if a piece is picked (follow the mouse on top of game with piece color)
				mouse_position = pygame.mouse.get_pos() # get were the mouse is
				if (180 > mouse_position[0] > 120) and mouse_position[1] >= 40: # if the mouse is over the firs coloumn
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 0: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 0: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (240 > mouse_position[0] > 180) and mouse_position[1] >= 40: # if the mouse is over the second column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 1: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 1: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (300 > mouse_position[0] > 240) and mouse_position[1] >= 40: # if the mouse is over the third column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 2: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 2: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (360 > mouse_position[0] > 300) and mouse_position[1] >= 40: # if the mouse is over the fourth column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 3: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 3: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (420 > mouse_position[0] > 360) and mouse_position[1] >= 40: # if the mouse is over the fith column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 4: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 4: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (480 > mouse_position[0] > 420) and mouse_position[1] >= 40: # if the mouse is over the sixth column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 5: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 5: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
				elif (540 > mouse_position[0] > 480) and mouse_position[1] >= 40: # if the mouse is over the seventh column
					if Player == "Black": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 6: # if x is where the mouse currently is
								fb.blit(I_FB,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
					elif Player == "Red": # check player color
						for x in range(7): # loops 7 times, 0-6, changing x value each time
							if x == 6: # if x is where the mouse currently is
								fb.blit(I_FR,(60*x+120,40,60,20),(0,0,60,20)) # draw piece in line with mouse
							else:
								fb.blit(I_FE,(60*x+120,40,60,20),(0,0,60,20)) # draw empty piece
			pygame.display.update((120,40,420,20)) # update the rectangle of flat pieces above board
		elif IOMode == "Again Menu": # if control is passed over to Again Menu
			if event == NOEVENT: # nothings happening
				pass # act like I care
			elif event.type in (KEYDOWN,): # if key was pressed
				keystate = pygame.key.get_pressed() # get list of keys states
				if keystate[K_ESCAPE]: # if esc key in list
					pygame.quit() # quit the game
					sys.exit() # exit out
				elif keystate[K_y]: # if y key is pressed (for yes)
					IOMode="Start" # start a new round (free checkers for everyone, on the house!)
				elif keystate[K_n]: # n for no they don't want to start a new game
					pygame.quit() # quit the game
					sys.exit() # exit out
				elif keystate[K_F12] or keystate[K_PRINT]: # take snapshot key F12
					DrawGame(fb,GameZones) # draw game board
					pygame.image.save(fb, "snapshot"+str(time.time())+".bmp") # give them a screenshot
					Play_Again_Menu()
					IdealFont(fb,120,40,(0,0,0),(255,255,255),"Snapshot Taken",420)
			elif event.type in (MOUSEBUTTONDOWN,): # mouse button pressed
				mouse_button = pygame.mouse.get_pressed() # get mouse button pressed
				if event.button == 1: # if first button
					mouse_position = pygame.mouse.get_pos() # get mouse position
					if (ScreenWidth/2-250/2)+115 > mouse_position[0] > (ScreenWidth/2-250/2)+40 and (ScreenHeight/2-100/2)+80 > mouse_position[1] > (ScreenHeight/2-100/2)+60: # if in (Yes) area
						IOMode="Start" # start a new game
					elif (ScreenWidth/2-250/2)+210 > mouse_position[0] > (ScreenWidth/2-250/2)+135 and (ScreenHeight/2-100/2)+80 > mouse_position[1] > (ScreenHeight/2-100/2)+60: # if in (No) area
						pygame.quit() # quit the game
						sys.exit() # exit out
				else:
					pass
			else:
				pass
		elif IOMode == "Esc Menu": # control for leaving or returning to the game
			if event == NOEVENT:
				pass
			elif event.type == QUIT: # if they press the X box
				pygame.quit() # close the game
				sys.exit() # exit out
			elif event.type in (KEYDOWN,): # if a key was pressed
				keystate = pygame.key.get_pressed() # get a list of the keys states
				if keystate[K_ESCAPE]: # if key ESC in list
					DrawGame(fb,GameZones) # draw game board
					IOMode="Game" # continue back to game control
				elif keystate[K_y]: # if y as in yes
					pygame.quit() # quit
					sys.exit() # exit out
				elif keystate[K_n]: # if n as in no
					DrawGame(fb,GameZones) # draw game board
					IOMode="Game" # continue back to game control
				elif keystate[K_F12] or keystate[K_PRINT]: # if screenshot key in list
					DrawGame(fb,GameZones) # draw game board
					pygame.image.save(fb, "snapshot"+str(time.time())+".bmp") # give them a screenshot
					Draw_Esc_Menu()
					IdealFont(fb,120,40,(0,0,0),(255,255,255),"Snapshot Taken",420)
			elif event.type in (MOUSEBUTTONDOWN,): # if mouse button pressed
				mouse_button = pygame.mouse.get_pressed() # find out which button
				if event.button == 1: # if first button
                                        mouse_position = pygame.mouse.get_pos() # gets the mouse position
					if (ScreenWidth/2-250/2)+115 > mouse_position[0] > (ScreenWidth/2-250/2)+40 and (ScreenHeight/2-100/2)+80 > mouse_position[1] > (ScreenHeight/2-100/2)+60: # if in (Yes) area
						pygame.quit() # quit game
						sys.exit() # exit out
					elif (ScreenWidth/2-250/2)+210 > mouse_position[0] > (ScreenWidth/2-250/2)+135 and (ScreenHeight/2-100/2)+80 > mouse_position[1] > (ScreenHeight/2-100/2)+60: # if in (No) area
						DrawGame(fb,GameZones) # draw the game board
						IOMode="Game" # give control back over to game play
				else:
					pass
			else:
				pass
		pygame.time.delay(10) # 10 milliseconds of a delay for full game loop
	return 1


if __name__ == '__main__': # if run and not imported
        PYC4() # run game
	pygame.quit() # close game
	sys.exit() # exit out
