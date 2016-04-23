# win32build.py
from distutils.core import setup
import py2exe, sys


args = ["py2exe","--force","-O2","--force-imports","pygame.mixer_music,pygame.surflock,pygame.rwobject,pygame.imageext"]
sys.argv[1:] = args


setup(name="ConnectFour",
        scripts=["c4.py"],
        data_files=[
        ('.',['.\\license',
                '.\\copying',
                '.\\readme',
                '.\\CHANGELOG',
                '.\\AUDIOFILES',
                '.\\IMAGEFILES']),
        ('images',['images\\6dlogo.gif',
                'images\\6dsoft.gif',
                'images\\startmenu.gif',
                'images\\arrowl.gif',
                'images\\arrowr.gif',
                'images\\background.gif',
                'images\\blackblock.gif',
                'images\\C4icon.ico',
                'images\\emptyblock.gif',
                'images\\fblackblock.gif',
                'images\\femptyblock.gif',
                'images\\fredblock.gif',
                'images\\redblock.gif',
                'images\\sdl_prgb.gif',
                'images\\wblackblock.gif',
                'images\\wredblock.gif']),
        ('fonts',['fonts\\times.ttf']),
        ('audio',['audio\\6d.wav',
                'audio\\sdl.wav',
                'audio\\textin.wav',
                'audio\\pick.wav',
                'audio\\drop.wav',
                'audio\\win.wav'])
        ])
