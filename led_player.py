import machine, utime, ujson, os, neopixel, gc
from blink import blink

class LED_Player():
    def __init__(self):
        self.nxt = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
        self.dwn = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
        self.up = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pixels = neopixel.NeoPixel(machine.Pin(14), 200)
        #self.pixels.pixel_order = neopixel.GRB
        #self.pixels.auto_write = False
        self.reset_pixels()
        self.pixels.write()
        self.filelist = []
        self.index_files
        self.max_index = 0
        self.act_index = 0

    def index_files(self):
        filelist = []
        for file in os.listdir():
            #print(file)
            if '.led' in file:
                filelist.append(file)
                self.filelist = sorted(filelist)
                self.max_index = len(self.filelist) - 1
                blink(1)
        if not len(self.filelist):
            print('no ledfiles found - abort')
            blink(5)

    def load_next_file(self):
        #with open (self.filelist[self.act_index], 'r') as lfile:
        #    movie = ujson.load(lfile)
        #    if self.act_index < self.max_index:
        #        self.act_index += 1
        #    else:
        #        self.act_index = 0
        #    return movie
        file = self.filelist[self.act_index]
        if self.act_index < self.max_index:
            self.act_index += 1
        else:
            self.act_index = 0
        return file
        
        
    def set_brightness(self, bright=0.6):
        self.brightness = bright
        self.pixels.brightness = self.brightness
        self._show()

    def reset_pixels(self):
        self.pixels.fill([0,0,0])

    def show(self):
        self.pixels.write()

    def set_pixel(self, index, color):
        #print('set led', index, 'to', color)
        self.pixels[index] = color

    def show_picture(self, picture):
        #print('show picture ', picture)
        self._reset_pixels()
        for led in picture:
            self.set_pixel(index=led[0], color=int(led[1],16))
        self.show()

    def show_movie(self, piclist):
        for picture in piclist:
            self.reset_pixels()
            if not self.nxt.value():
                self._show()
                break
            self.show_picture(picture['picture'])
            utime.sleep(picture['delay'])        

    def play(self):
        while True:
            utime.sleep(1)
            if self.nxt.value():
                utime.sleep_ms(200)
            else:
                movie = self.load_next_file()
                if 'bright' in movie.keys():
                    self.set_brightness(movie['bright'])
                else:
                    self.set_brightness()

                self.show_movie(movie['picture_list'])
                
