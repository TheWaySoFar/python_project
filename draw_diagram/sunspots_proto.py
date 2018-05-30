#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF


data = []
with open('Predict.txt') as f:
    for line in f:
        if list(line)[0] == '#' or list(line)[0] == ':':
            continue
        data.append([float(x) for x in line.split()])

drawing = Drawing(400, 200)
pred = [row[2]-40 for row in data]
high = [row[3]-40 for row in data]
low = [row[4]-40 for row in data]
times = [200*((row[0] + row[1]/12.0) - 2007)-110 for row in data]
#drawing.add(PolyLine(list(zip(times, pred)), strokeColor=colors.blue))
#dr#awing.add(PolyLine(list(zip(times, high)), strokeColor=colors.red))
#drawing.add(PolyLine(list(zip(times, low)), strokeColor=colors.green))
#drawing.add(String(65, 115, 'Sunspots', fontSize=18, fillColor=colors.red))
#renderPDF.drawToFile(drawing, 'report1.pdf', 'Sunspots')
lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [list(zip(times, pred)),
list(zip(times, high)),
list(zip(times, low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green
drawing.add(lp)
drawing.add(String(250, 150, 'Sunspots', fontSize=14, fillColor=colors.red))
renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')