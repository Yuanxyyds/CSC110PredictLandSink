"""
Instructions (READ THIS FIRST!)
===============================
Read the comments and comment/uncomment specific lines to choose
what part of the program intended to run.

Copyright and Usage Information
===============================

This program is provided solely for the personal and private use of teachers and TAs
checking and grading the CSC110 project at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Alex Lin, Steven Liu, Haitao Zeng, William Zhang.
"""
from typing import Any

import json
import webbrowser
from sys import exit
from pyecharts.charts import Map
from pyecharts import options
import pygame
import model


##############################################
# Part 1
# This part is to collect information of which year user to see.
##############################################


class TextBox:
    """The class of textbox.
    Attribute:
        - width: the width of the text box.
        - height: the height of the text box.
        - x: the text location on x axis of the pygame surface.
        - y: the location on y axis of the pygame surface.
        - text: what the textbox contain.
        - __surface: the main surface of the pygame.
        - callback: what the text box can call back.
        - font: the Font of the text box.
    Precondition:
        - self.width > 0
        - self.height > 0
        - self.x > 0
        - self.y > 0

    """
    width: int
    height: int
    x: int
    y: int
    text: str
    __surface: pygame.Surface
    font: pygame.font

    def __init__(self, w: int, h: int, x: int, y: int) -> None:
        """
        initialize the class.
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ''
        self.__surface = pygame.Surface((w, h))
        self.__surface.fill(pygame.color.Color('#332222'))
        self.font = pygame.font.Font(None, 32)

    def draw(self, dest_surf: pygame.surface) -> None:
        """
        Put the text box onto the main pygame screen.
        """
        # create a surface of the text box.
        text_surf = self.font.render(self.text, True, (255, 255, 255))

        # put the surface onto the main pygame surface of location (x, y).
        dest_surf.blit(self.__surface, (self.x, self.y))
        dest_surf.blit(text_surf, (
            self.x + (self.width - text_surf.get_width()) / 2,
            self.y + (self.height - text_surf.get_height())), (0, 0, self.width, self.height))

    def key_down(self, event: pygame.event) -> Any:
        """
        When something input form keyboard, make a judgement of what should do next.
        Precondition:
            - do not input through the right of the keyboard please.
        """
        global INPUT_YEAR, MARK1, MARK2
        unicode = event.unicode
        key = event.key

        #  to delete the last character of the text in text box.
        if key == 8:
            self.text = self.text[:-1]
            return

        #  to open / close the caps lock. (just do not put 'capslock' into text)
        if key == 301:
            return

        #  when enter is push, sent the value to INPUT_YEAR
        #  and change the switches MARK1, MARK2 to stop the main pygame.
        if key == 13:
            INPUT_YEAR = self.text
            MARK1 = False
            MARK2 = True
            return

        #  if not all the above situation, input what keyboard push into text of the text box.
        if unicode != '':
            char = unicode
        else:
            char = chr(key)
        self.text = self.text + char


def accepting_data() -> None:
    """
    the main function to accept data form user typing.
    """
    global MARK1, MARK2, INPUT_YEAR
    while MARK1 is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                text_box.key_down(event)
        pygame.time.delay(33)
        text_box.draw(WinSur)
        text_string.draw(WinSur)
        attention1.draw(WinSur)
        attention2.draw(WinSur)
        attention3.draw(WinSur)
        pygame.display.flip()
        if MARK2 is True:
            attention4.text = f'The sunk map of year: {INPUT_YEAR} is processing...'
            attention4.draw(WinSur)
            pygame.display.flip()
            pygame.time.delay(1000)
            model.build_models()
            temp = model.year_to_tem(int(INPUT_YEAR))
            eve = model.tem_to_sealevel(temp)
            # draw the map.
            if temp is not None:
                draw_map(eve)
                attention5.text = 'Successfully! The map will be directed to you in 10s!'
                attention5.draw(WinSur)
                attention6.text = 'An alternative link of the map has ' \
                                  'been saved in the project folder!'

                result.text = 'RESULT:'
                result.draw(WinSur)
                attention7.text = f'At {INPUT_YEAR} the predicted temperature is {round(temp, 3)} C'
                attention8.text = f'At Temperature of {round(temp, 3)} C, ' \
                                  f'the predicted sea level is {round(eve, 3)} m'
                attention7.draw(WinSur)
                attention8.draw(WinSur)
                pygame.display.flip()

                warning.text = 'NOTE:'
                attention9.text = "The prediction may vary due to several factors " \
                                  "(Water's boiling point..)"
                attention10.text = "The models we based on are plotted in Python Plots"
                warning.draw(WinSur)
                attention9.draw(WinSur)
                attention10.draw(WinSur)
                pygame.display.flip()

                pygame.time.delay(10000)
                pygame.quit()
                webbrowser.open_new_tab('index.html')
            else:
                attention5.text = 'Oops, Somewhere Went Wrong'
                attention5.draw(WinSur)
                pygame.time.delay(5000)
                pygame.quit()


##############################################
# Part 2
# This part is to draw a global map.
##############################################

def translation(sea_level_1: float) -> list:
    """
    translate the information form txt.
    """
    #  form txt input data.
    f = open('map_data.txt', 'r')
    js = f.read()
    dic = json.loads(js)
    realdata = {}

    # change the data format into what pyecharts need to draw.
    for data in dic['data']:
        name = data['name']
        ele = data['avg_ele']

        #  There are 2 country which has error in translating data,
        #  so this if statement is to fix them.
        for c in name:
            if c == '么':
                name = "Côte d'Ivoire"
            if c == '茅':
                name = "São Tomé and Principe"

        # There are 2 country which ele is 0, we assume whenever time goes,
        # these country will sunk immediately.
        if float(ele) != 0:
            realdata[name] = min(100.0, round(sea_level_1 / float(ele) * 100, 4))
        else:
            realdata[name] = 100

    #  change the realdata into what pyecharts need.
    return list(realdata.items())


def draw_map(sea_level_2: float) -> None:
    """5
    set the map setting and draw the map.
    """
    element = translation(sea_level_2)
    sunk_map = Map(options.InitOpts(bg_color="#87CEFA", page_title='sunk percentage map')). \
        add(series_name="Sunk Rate of Country in %",
            data_pair=element,
            is_map_symbol_show=False,
            maptype='world',
            layout_size=150
            )

    #  set different color to different danger level.
    sunk_map.set_global_opts(
        visualmap_opts=options.VisualMapOpts(max_=1100000, is_piecewise=True, pieces=[
            {"min": 96},
            {"min": 72.9, "max": 95.999},
            {"min": 50.4, "max": 72.899},
            {"min": 27.8, "max": 50.399},
            {"min": 5.001, "max": 27.799},
            {"max": 5}, ]))

    #  set Map data format.
    sunk_map.set_series_opts(label_opts=options.LabelOpts(is_show=False))  # set country divisible
    sunk_map.render('index.html')  # create a map


if __name__ == '__main__':
    pygame.init()  # initialize the pygame.
    INPUT_YEAR = ''  # the value of INPUT_YEAR
    MARK1 = True  # the option to continue or not the main pygame.
    MARK2 = False  # the option to ready to stop the main pygame.

    #  main input text box
    text_box = TextBox(150, 40, 370, 180)
    text_string = TextBox(150, 40, 220, 180)

    #  attention of what to input.
    text_string.text = 'Input Year:'
    attention1 = TextBox(750, 30, 5, 50)
    attention1.text = 'Enter a year to start predicting!'
    attention2 = TextBox(750, 30, 5, 80)
    attention2.text = 'We recommend you to input a large year such as 20,000!'
    attention3 = TextBox(750, 30, 5, 110)
    attention3.text = 'As the sea level is increasing slow! (10 meters per 3000 years)'

    # attention of pygame's job finish.
    attention4 = TextBox(750, 30, 5, 250)
    attention5 = TextBox(750, 30, 5, 280)
    attention6 = TextBox(750, 30, 5, 310)
    result = TextBox(100, 30, 5, 340)
    attention7 = TextBox(750, 30, 5, 370)
    attention8 = TextBox(750, 30, 5, 400)

    warning = TextBox(100, 30, 5, 460)
    attention9 = TextBox(750, 30, 5, 490)
    attention10 = TextBox(750, 30, 5, 520)

    #  Creating main pygame surface.
    WinSur = pygame.display.set_mode((760, 570))
    Background = pygame.color.Color('#EE7621')
    WinSur.fill(Background)
    pygame.display.flip()

    # Processing Data
    accepting_data()
    model.plot()
