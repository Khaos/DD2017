from __future__ import division
from __future__ import print_function


import os
import re
import sys
import argparse
import numpy as np
import copy
import annolist.AnnotationLib as al

import scipy as scp
import scipy.misc

import random

from collections import namedtuple


def annotation_to_h5(H, a, cell_width, cell_height, max_len):
    region_size = H['region_size']
    # assert H['region_size'] == H['image_height'] / H['grid_height']
    # assert H['region_size'] == H['image_width'] / H['grid_width']
    cell_regions = get_cell_grid(cell_width, cell_height, region_size)

    cells_per_image = len(cell_regions)

    box_list = [[] for idx in range(cells_per_image)]

    for cidx, c in enumerate(cell_regions):
        box_list[cidx] = [r for r in a.rects if all(r.intersection(c))]

    boxes = np.zeros((1, cells_per_image, 4, max_len, 1), dtype=np.float)
    box_flags = np.zeros((1, cells_per_image, 1, max_len, 1), dtype=np.float)

    for cidx in xrange(cells_per_image):
        # assert(cur_num_boxes <= max_len)

        cell_ox = 0.5 * (cell_regions[cidx].x1 + cell_regions[cidx].x2)
        cell_oy = 0.5 * (cell_regions[cidx].y1 + cell_regions[cidx].y2)

        unsorted_boxes = []
        for bidx in xrange(min(len(box_list[cidx]), max_len)):

            # relative box position with respect to cell
            ox = 0.5 * \
                (box_list[cidx][bidx].x1 + box_list[cidx][bidx].x2) - cell_ox
            oy = 0.5 * \
                (box_list[cidx][bidx].y1 + box_list[cidx][bidx].y2) - cell_oy

            width = abs(box_list[cidx][bidx].x2 - box_list[cidx][bidx].x1)
            height = abs(box_list[cidx][bidx].y2 - box_list[cidx][bidx].y1)

            if (abs(ox) < H['focus_size'] * region_size and abs(oy) < H['focus_size'] * region_size and
                    width < H['biggest_box_px'] and height < H['biggest_box_px']):
                unsorted_boxes.append(
                    np.array([ox, oy, width, height], dtype=np.float))

        for bidx, box in enumerate(sorted(unsorted_boxes, key=lambda x: x[0]**2 + x[1]**2)):
            boxes[0, cidx, :, bidx, 0] = box
            box_flags[0, cidx, 0, bidx, 0] = max(
                box_list[cidx][bidx].silhouetteID, 1)

    return boxes, box_flags


def get_cell_grid(cell_width, cell_height, region_size):

    cell_regions = []
    for iy in xrange(cell_height):
        for ix in xrange(cell_width):
            cidx = iy * cell_width + ix
            ox = (ix + 0.5) * region_size
            oy = (iy + 0.5) * region_size

            r = al.AnnoRect(ox - 0.5 * region_size, oy - 0.5 * region_size,
                            ox + 0.5 * region_size, oy + 0.5 * region_size)
            r.track_id = cidx

            cell_regions.append(r)

    return cell_regions


def annotation_jitter(I, a_in, min_box_width=20, jitter_scale_min=0.9, jitter_scale_max=1.1, jitter_offset=16, target_width=640, target_height=480):
    a = copy.deepcopy(a_in)

    # MA: sanity check
    new_rects = []
    for i in range(len(a.rects)):
        r = a.rects[i]
        try:
            assert(r.x1 < r.x2 and r.y1 < r.y2)
            new_rects.append(r)
        except:
            print('bad rectangle')
    a.rects = new_rects

    if a.rects:
        cur_min_box_width = min([r.width() for r in a.rects])
    else:
        cur_min_box_width = min_box_width / jitter_scale_min

    # don't downscale below min_box_width
    jitter_scale_min = max(
        jitter_scale_min, float(min_box_width) / cur_min_box_width)

    # it's always ok to upscale
    jitter_scale_min = min(jitter_scale_min, 1.0)

    jitter_scale_max = jitter_scale_max

    jitter_scale = np.random.uniform(jitter_scale_min, jitter_scale_max)

    jitter_flip = np.random.random_integers(0, 1)

    if jitter_flip == 1:
        I = np.fliplr(I)

        for r in a:
            r.x1 = I.shape[1] - r.x1
            r.x2 = I.shape[1] - r.x2
            r.x1, r.x2 = r.x2, r.x1

            for p in r.point:
                p.x = I.shape[1] - p.x

    if random.random > 0.8:
        return I, a

    I1 = scp.misc.imresize(I, jitter_scale, interp='cubic')

    print("Resized image with scale {}".format(jitter_scale))

    jitter_offset_x = np.random.random_integers(-jitter_offset, jitter_offset)
    jitter_offset_y = np.random.random_integers(-jitter_offset, jitter_offset)

    rescaled_width = I1.shape[1]
    rescaled_height = I1.shape[0]



    px = round(0.5*(target_width)) - \
        round(0.5*(rescaled_width)) + jitter_offset_x
    py = round(0.5*(target_height)) - \
        round(0.5*(rescaled_height)) + jitter_offset_y

    I2 = np.zeros((target_height, target_width, 3), dtype=I1.dtype)

    x1 = int(max(0, px))
    y1 = int(max(0, py))
    x2 = min(rescaled_width, target_width - x1)
    y2 = min(rescaled_height, target_height - y1)

    I2[0:(y2 - y1), 0:(x2 - x1), :] = I1[y1:y2, x1:x2, :]

    ox1 = round(0.5*rescaled_width) + jitter_offset_x
    oy1 = round(0.5*rescaled_height) + jitter_offset_y

    ox2 = round(0.5*target_width)
    oy2 = round(0.5*target_height)

    for r in a:
        r.x1 = round(jitter_scale*r.x1 - x1)
        r.x2 = round(jitter_scale*r.x2 - x1)

        r.y1 = round(jitter_scale*r.y1 - y1)
        r.y2 = round(jitter_scale*r.y2 - y1)

        if r.x1 < 0:
            r.x1 = 0

        if r.y1 < 0:
            r.y1 = 0

        if r.x2 >= I2.shape[1]:
            r.x2 = I2.shape[1] - 1

        if r.y2 >= I2.shape[0]:
            r.y2 = I2.shape[0] - 1

        for p in r.point:
            p.x = round(jitter_scale*p.x - x1)
            p.y = round(jitter_scale*p.y - y1)

        # MA: make sure all points are inside the image
        r.point = [p for p in r.point if p.x >= 0 and p.y >=
                   0 and p.x < I2.shape[1] and p.y < I2.shape[0]]

    new_rects = []
    for r in a.rects:
        if r.x1 <= r.x2 and r.y1 <= r.y2:
            new_rects.append(r)
        else:
            pass

    a.rects = new_rects

    return I2, a


from PIL import Image, ImageDraw

rect = namedtuple('Rectangel', ['left', 'top', 'right', 'bottom'])


def _get_ignore_rect(x, y, cell_size):
    left = x*cell_size
    right = (x+1)*cell_size
    top = y*cell_size
    bottom = (y+1)*cell_size

    return rect(left, top, right, bottom)


def draw_rect(draw, rect, color):
    rect_cords = ((rect.left, rect.top), (rect.left, rect.bottom),
                  (rect.right, rect.bottom), (rect.right, rect.top),
                  (rect.left, rect.top))
    draw.line(rect_cords, fill=color, width=2)


def draw_encoded(image, confs, mask=None, rects=None, cell_size=32):
    image = image.astype('uint8')
    im = Image.fromarray(image)

    shape = confs.shape
    if mask is None:
        mask = np.ones(shape)

    # overimage = mycm(confs_pred, bytes=True)

    poly = Image.new('RGBA', im.size)
    pdraw = ImageDraw.Draw(poly)

    for y in range(shape[0]):
        for x in range(shape[1]):
            outline = (0, 0, 0, 255)
            if confs[y, x]:
                fill = (0, 255, 0, 100)
            else:
                fill = (0, 0, 0, 0)
            rect = _get_ignore_rect(x, y, cell_size)
            pdraw.rectangle(rect, fill=fill,
                            outline=fill)
            if not mask[y, x]:
                pdraw.line(((rect.left, rect.bottom), (rect.right, rect.top)),
                           fill=(0, 0, 0, 255), width=2)
                pdraw.line(((rect.left, rect.top), (rect.right, rect.bottom)),
                           fill=(0, 0, 0, 255), width=2)

    color = (0, 0, 255)
    if rects is not None:
        for rect in rects:
            rect_cords = ((rect.x1, rect.y1), (rect.x1, rect.y2),
                          (rect.x2, rect.y2), (rect.x2, rect.y1),
                          (rect.x1, rect.y1))
            pdraw.line(rect_cords, fill=color, width=2)

    im.paste(poly, mask=poly)

    return np.array(im)
