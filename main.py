import pygame as pg
import numpy as np
import sys

disp_width = 1200
disp_height = 800
disp_depth = 1500
disp_4depth = 1500

offset_x = 0
offset_y = 0
z_dist = np.sqrt((disp_width / 2)**2 + (disp_height/2)**2 + (disp_depth * 2)**2)

class Table:
    def __init__(self, screen, gravity, count):
        self.screen = screen
        self.body_list = []
        self.gravity = gravity
        for i in range(0, count):
            self.body_list.append(Body(0.5, np.random.randint(0, disp_width),
                                       np.random.randint(0, disp_height),
                                       np.random.randint(0, disp_depth),
                                       np.random.randint(0, disp_4depth), self))
        self.body_list.append(Body(10, disp_width / 2, disp_height / 2, disp_depth / 2, disp_4depth / 2, self))

    def next(self):
        self.body_list.sort(key=lambda x: -x.z)
        for i in self.body_list:
            i.calculate_vels()
        for i in self.body_list:
            i.next()


class Body:
    def __init__(self, mass, x, y, z, v, table):
        self.mass = mass
        self.table = table
        self.range = (5 * self.mass) ** 0.33

        #Координаты
        self.x = x
        self.y = y
        self.z = z
        self.v = v

        #Скорости
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0
        self.v_vel = 0

        #Рисование
        self.draw_x = (self.x - disp_width / 2) / ((self.z + 1) / z_dist) + disp_width / 2
        self.draw_y = (self.y - disp_height / 2) / ((self.z + 1) / z_dist) + disp_height / 2
        self.draw_range = self.range / ((self.z + 1) / z_dist)
        self.draw_red = max(0, min(255, int(50 + 205 * (1 - ((self.z + 1) / z_dist)))))
        self.draw_blue = max(0, min(255, int(0 + 255 * (1 - ((self.v + 1) / disp_4depth)))))
        self.rect = pg.draw.circle(self.table.screen, (self.draw_red, 0, self.draw_blue), (self.draw_x, self.draw_y),
                                   self.draw_range)

    def calculate_vels(self):
        for i in self.table.body_list:
            if self == i:
                continue
            distance_square = (self.x - i.x)**2 + (self.y - i.y)**2 + (self.z - i.z)**2 + (self.v - i.v)**2
            if distance_square != 0:
                distance = distance_square**0.5
                g = self.table.gravity * i.mass / distance_square
                cos = (i.x - self.x) / distance
                sin = (i.y - self.y) / distance
                zre = (i.z - self.z) / distance
                vre = (i.v - self.v) / distance
                self.x_vel += g * cos
                self.y_vel += g * sin
                self.z_vel += g * zre
                self.v_vel += g * vre

            '''distance_square = (disp_width - self.x - i.x) ** 2 + (disp_height - self.y - i.y) ** 2
            if distance_square != 0:
                distance = distance_square ** 0.5
                g = self.table.gravity * (self.mass * i.mass) / distance_square
                cos = (i.x - (disp_width - self.x)) / distance
                sin = (i.y - (disp_height - self.y)) / distance
                self.x_vel += g * cos
                self.y_vel += g * sin'''


    def next(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.z += self.z_vel
        self.v += self.v_vel
        #if self.x > disp_width or self.x < 0: self.x %= disp_width
        #if self.y > disp_height or self.y < 0: self.y %= disp_height
        self.range = (5 * self.mass) ** 0.33
        self.draw_x = (self.x - disp_width / 2) / ((self.z + 1) / z_dist) + disp_width / 2
        self.draw_y = (self.y - disp_height / 2) / ((self.z + 1) / z_dist) + disp_height / 2
        self.draw_range = self.range / ((self.z + 1) / z_dist)
        self.draw_red = max(0, min(255, int(50 + 205 * (1 - ((self.z + 1) / z_dist)))))
        self.draw_blue = max(0, min(255, int(0 + 255 * (1 - ((self.v + 1) / disp_4depth)))))
        self.rect = pg.draw.circle(self.table.screen, (self.draw_red, 0, self.draw_blue), (self.draw_x, self.draw_y),
                                   self.draw_range)
        for i in self.table.body_list:
            if i == self:
                continue
            distance = ((self.x - i.x)**2 + (self.y - i.y)**2 + (self.z - i.z)**2)**0.5
            if distance < self.range + i.range:
                self.x = (self.x * self.mass + i.x * i.mass) / (self.mass + i.mass)
                self.y = (self.y * self.mass + i.y * i.mass) / (self.mass + i.mass)
                self.z = (self.z * self.mass + i.z * i.mass) / (self.mass + i.mass)
                self.v = (self.v * self.mass + i.v * i.mass) / (self.mass + i.mass)
                self.x_vel = (self.x_vel * self.mass + i.x_vel * i.mass) / (self.mass + i.mass)
                self.y_vel = (self.y_vel * self.mass + i.y_vel * i.mass) / (self.mass + i.mass)
                self.z_vel = (self.z_vel * self.mass + i.z_vel * i.mass) / (self.mass + i.mass)
                self.v_vel = (self.v_vel * self.mass + i.v_vel * i.mass) / (self.mass + i.mass)
                self.mass = self.mass + i.mass
                self.table.body_list.remove(i)
                self.range = (5 * self.mass) ** 0.33
                self.draw_x = (self.x - disp_width / 2) / ((self.z + 1) / z_dist) + disp_width / 2
                self.draw_y = (self.y - disp_height / 2) / ((self.z + 1) / z_dist) + disp_height / 2
                self.draw_range = self.range / ((self.z + 1) / z_dist)
                self.draw_red = max(0, min(255, int(50 + 205 * (1 - ((self.z + 1) / z_dist)))))
                self.draw_blue = max(0, min(255, int(0 + 255 * (1 - ((self.v + 1) / disp_4depth)))))
                self.rect = pg.draw.circle(self.table.screen, (self.draw_red, 0, self.draw_blue),
                                           (self.draw_x, self.draw_y),
                                           self.draw_range)


def main():
    sc = pg.display.set_mode((disp_width, disp_height))

    clock = pg.time.Clock()
    pg.display.update()

    table = Table(sc, 2.5, 125)

    while 1:
        sc.fill((0, 0, 0))
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
        table.next()
        pg.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()