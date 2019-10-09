#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from PIL import Image, ImageColor, ImageDraw, ImageFont
import queue

NB_LOOP = 300
NB_CARS = 20
FONT_SIZE = 12
CAR_HEIGHT = 14
CAR_WIDTH = 30
ROAD_HEIGHT = CAR_HEIGHT+4
ROAD_SPACE = 4
ROAD_WIDTH = 800
BOARD_WIDTH = 150
SPEED_FACTOR = 10

START_LINE = 200
END_LINE = 600

BACKGROUND_COLOR = (48, 48, 48)

# https://colorswall.com/palette/73/
palete = [
    (255, 241, 0),
    (255, 140, 0),
    (232, 17, 35),
    (236, 0, 140),
    (104, 33, 122),
    (0, 24, 143),
    (0, 188, 242),
    (0, 178, 148),
    (0, 158, 73),
    (186, 216, 10)
]


# Init properties
random.seed(50)

NOFRAME = 99999
cars_infos = [
    {
        'car_id': -1,
        'pos': (random.random()*START_LINE)-(random.random()*START_LINE),
        'speed': random.random()*SPEED_FACTOR,
        'color': (255, 221, 85),
        'start_frame': NOFRAME,
        'end_frame': NOFRAME,
        'nb_cars': 0
    }
    for i in range(NB_CARS)]


nb_cars = 0

###########################################
# Move Cars
###########################################

for loop in range(NB_LOOP):
    print(f"Compute image {loop}/{NB_LOOP}")
    im = Image.new(mode="RGB", size=(
        ROAD_WIDTH+BOARD_WIDTH, (ROAD_HEIGHT+ROAD_SPACE)*NB_CARS), color=BACKGROUND_COLOR)

    font = ImageFont.truetype(
        f'Cantarell-ExtraBold.otf', FONT_SIZE)
    d = ImageDraw.Draw(im)
    d.line([(START_LINE, 0), (START_LINE, (ROAD_HEIGHT+ROAD_SPACE)*NB_CARS)])
    d.line([(END_LINE, 0), (END_LINE, (ROAD_HEIGHT+ROAD_SPACE)*NB_CARS)])

    # Move cars
    for idx in range(NB_CARS):

        twidth, theight = d.textsize(
            str(idx), font=font)

        centery = ((CAR_HEIGHT-theight)/2)
        centerx = ((CAR_WIDTH-twidth)/2)

        cars_infos[idx]['car_id'] = idx
        cars_infos[idx]['pos'] += cars_infos[idx]['speed']
        cars_infos[idx]['nb_cars'] = 0

    top_pos = sorted(
        cars_infos, key=lambda item: item['pos'], reverse=True)
    top_start = sorted(
        cars_infos, key=lambda item: item['start_frame'])
    top_end = sorted(
        cars_infos, key=lambda item: item['end_frame'])
    nb_cars = 0
    for item in top_pos:
        if item['pos'] > START_LINE:
            if item['start_frame'] == NOFRAME:
                item['start_frame'] = loop
                item['color'] = palete[nb_cars % len(palete)]

            if item['pos'] < END_LINE:
                nb_cars += 1
                item['nb_cars'] = nb_cars

        if item['pos'] > END_LINE and item['end_frame'] == NOFRAME:
            item['end_frame'] = loop

    for idx in range(NB_CARS):

        twidth, theight = d.textsize(
            str(idx), font=font)

        centery = ((CAR_HEIGHT-theight)/2)
        centerx = ((CAR_WIDTH-twidth)/2)

        # Draw line with matched car
        if top_start[idx]['start_frame'] != NOFRAME and top_end[idx]['end_frame'] != NOFRAME:
            posy_start = 4+(top_start[idx]
                            ['car_id']*(ROAD_HEIGHT+ROAD_SPACE))
            posy_end = 4+(top_end[idx]['car_id']
                          * (ROAD_HEIGHT+ROAD_SPACE))
            d.line([(top_start[idx]['pos'], posy_start),
                    (top_end[idx]['pos'], posy_end)])

        posy = 4+(idx*(ROAD_HEIGHT+ROAD_SPACE))
        d.rectangle(
            [(cars_infos[idx]['pos'], posy), (cars_infos[idx]['pos']+CAR_WIDTH, posy+CAR_HEIGHT)], cars_infos[idx]['color'])

        if cars_infos[idx]['nb_cars'] > 0:
            d.text((cars_infos[idx]['pos']+centerx, posy+centery),
                   str(cars_infos[idx]['nb_cars']), font=font, fill=(0, 0, 0))

    d.rectangle(
        [(ROAD_WIDTH, 0), (ROAD_WIDTH+BOARD_WIDTH, (ROAD_HEIGHT+ROAD_SPACE)*NB_CARS)], BACKGROUND_COLOR)

    if nb_cars > 0:
        d.text((ROAD_WIDTH+BOARD_WIDTH-135, ((ROAD_HEIGHT+ROAD_SPACE)*NB_CARS)-(FONT_SIZE+ROAD_SPACE)),
               f'Cars in the segment: {nb_cars}', font=font, fill=(196, 196, 196))

    for idx in range(len(top_end)):
        if top_end[idx]['end_frame'] != NOFRAME:

            frames = top_end[idx]['end_frame'] - top_start[idx]['start_frame']
            speed = (END_LINE - START_LINE) / frames

            posy = 4+(idx*(ROAD_HEIGHT+ROAD_SPACE))
            d.text((ROAD_WIDTH+ROAD_SPACE, posy),
                   f'{speed:04.2f} pixels/frames', font=font, fill=(196, 196, 196))

    im.save(f'image_cars_{loop:04d}.png')
