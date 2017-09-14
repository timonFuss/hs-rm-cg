#!/usr/bin/python
# -*- coding: utf-8 -*-

class Light(object):
    def __init__(self, position, color, shiny):
        self.position = position      #point
        self.color = color
        self.shiny=shiny