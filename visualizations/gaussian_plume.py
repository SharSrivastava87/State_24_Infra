import numpy as np
import matplotlib.image as mimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
from matplotlib import image
import pandas as pd
import random


csv_file = "EOG-Resources-Dataset-main/sensor_readings.csv"
df = pd.read_csv(csv_file)


class pointSource:
    def __init__(self, x, y, z, rate, H):
        self.x = x
        self.y = y
        self.z = z
        self.rate = rate
        self.H = H
        self.sourceType = 'point'
        

class receptorGrid:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.yMesh, self.zMesh, self.xMesh = np.meshgrid(y, z, x)

class stabilityClass:
    def __init__(self, letter):
        self.letter = letter

        if letter == 'A':
            Iy = -1.104
            Jy = 0.9878
            Ky = -0.0076

            Iz = 4.679
            Jz = -1.7172
            Kz = 0.2770

        elif letter == 'B':
            Iy = -1.634
            Jy = 1.0350
            Ky = -0.0096

            Iz = -1.999
            Jz = 0.8752
            Kz = 0.0136

        elif letter == 'C':
            Iy = -2.054
            Jy = 1.0231
            Ky = -0.0076

            Iz = -2.341
            Jz = 0.9477
            Kz = -0.0020

        elif letter == 'D':
            Iy = -2.555
            Jy = 1.0423
            Ky = -0.0087

            Iz = -3.186
            Jz = 1.1737
            Kz = -0.0316

        elif letter == 'E':
            Iy = -2.754
            Jy = 1.0106
            Ky = -0.0064

            Iz = -3.783
            Jz = 1.3010
            Kz = -0.0450

        elif letter == 'F':
            Iy = -3.143
            Jy = 1.0148
            Ky = -0.0070

            Iz = -4.490
            Jz = 1.4024
            Kz = -0.0540

        def sy(dist):
            return np.exp(Iy + Jy*np.log(dist) + Ky*(np.log(dist)**2))

        def sz(dist):
            return np.exp(Iz + Jz*np.log(dist) + Kz*(np.log(dist)**2))

        self.sz = sz
        self.sy = sy


class gaussianPlume:
    def __init__(self, source, grid, stability, U):
        self.grid = grid
        self.source = source
        self.stability = stability
        self.U = U

    def calculateConcentration(self):
        conc = np.zeros_like(self.grid.xMesh, dtype=float)

        if self.source.sourceType == 'area':
            for x in self.source.x:
                for y in self.source.y:
                    a = self.source.rate*self.source.dx*self.source.dy / \
                        (2 * np.pi * self.U * self.stability.sy(self.grid.xMesh - x)
                         * self.stability.sz(self.grid.xMesh - x))
                    b = np.exp(-(self.grid.yMesh - y)**2 /
                               (2*self.stability.sy(self.grid.xMesh - x)**2))
                    c = np.exp(-(self.grid.zMesh-self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2)) + \
                        np.exp(-(self.grid.zMesh+self.source.H)**2 /
                               (2*self.stability.sz(self.grid.xMesh - x)**2))
                    conc += a*b*c

        if self.source.sourceType == 'point':
            x = self.source.x
            y = self.source.y
            a = self.source.rate / (2 * np.pi * self.U * self.stability.sy(
                self.grid.xMesh - x) * self.stability.sz(self.grid.xMesh - x))
            b = np.exp(-(self.grid.yMesh - y)**2 /
                       (2*self.stability.sy(self.grid.xMesh - x)**2))
            c = np.exp(-(self.grid.zMesh-self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2)) + \
                np.exp(-(self.grid.zMesh+self.source.H)**2 /
                       (2*self.stability.sz(self.grid.xMesh - x)**2))
            conc += a*b*c

        return conc


def plt_plume(regions, direction):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for region in regions:

        rate = 1.  # g/s/m2
        H = 0.  # m
        U = 5.  # m/s
        xGrid = np.linspace(0, 2228, 100)  # m
        yGrid = np.linspace(0, 1164, 100)  # m
        zGrid = 10.  # m

        if region == '4W':
            if direction == 0:
                pos = [510, 400]
            else:
                pos = [1400, 350]
        elif region == '4T':
            if direction == 0:
                pos = [1150, 500]
            else:
                pos = [950, 600]
        elif region == '4S':
            if direction == 0:
                pos = [700, 800]
            else:
                pos = [600, 400]
        elif region == '5S':
            if direction == 0:
                pos = [1500, 800]
            else:
                pos = [750, 800]
        elif region == '5T':
            if direction == 0:
                pos = [1500, 400]
            else:
                pos = [1400, 850]
        PS = pointSource(pos[0], pos[1], 0, rate, H)
        grid = receptorGrid(xGrid, yGrid, zGrid)
        stability = stabilityClass(random.choice(['A', 'B', 'C', 'D', 'E', 'F']))

        a = gaussianPlume(PS, grid, stability, U)

        concField = a.calculateConcentration()
        concField = concField[0]
        if direction == 1:
            concField = np.rot90(concField, k=1)

        original_cmap = plt.cm.YlOrRd
        colors = original_cmap(np.linspace(0, 1, 256))
        colors[int(256*0.07):, 3] = colors[int(256*0.07):, 3] * 0.2
        colors[:int(256*0.07), 3] = 0

        new_cmap = LinearSegmentedColormap.from_list("ModifiedCmap", colors)
        c = ax.contourf(grid.xMesh[0], grid.yMesh[0],
                        concField, 100, cmap=new_cmap)

    image = plt.imread('map2.jpg')
    ax.imshow(image)
    ax.axis('off')
    plt.tight_layout()
    return fig


def call_plume(df_row):
    cols = ['4T', '5S', '5W', '4W', '4S']
    present = []
    for col in cols:
        if df_row[col] == 1:
            present.append(col)
    if len(present) > 2:
        present = present[:2]
    fig = plt_plume(present, df_row['direction'])
    return fig
df = pd.read_csv('gaussian_plume.csv')


f = call_plume(df.iloc[53])

f.savefig('plume.png')