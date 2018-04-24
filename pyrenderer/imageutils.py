import array


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, num):
        if isinstance(num, Color):
            return Color(self.r * num.r, self.g * num.g, self.b * num.b)

        return Color(self.r*num, self.g*num, self.b*num)

    def __rmul__(self, num):
        if isinstance(num, Color):
            return Color(self.r * num.r, self.g * num.g, self.b * num.b)

        return Color(self.r*num, self.g*num, self.b*num)

    def __div__(self, num):
        return Color(self.r/num, self.g/num, self.b/num)

    def __truediv__(self, num):
        return Color(self.r/num, self.g/num, self.b/num)


class Pixel:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.r = 0
        self.g = 0
        self.b = 0


class ImageIterator:
    def __init__(self, start, end, image):
        self.start = start
        self.end = end
        self.current = start
        self.image = image

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration()
        else:
            pixel = self.image.pixels[self.current]
            self.current += 1
            return pixel

    def next(self):
        self.__next__(self)


class Image:
    def __init__(self):
        self.w = 128
        self.h = 128

        self.pixels = [Pixel(i, j) for i in range(0, self.w)
                       for j in range(0, self.h)]

    def write(self, filename):
        fout = open(filename, 'wb')

        max_value = 0
        for pixel in self.pixels:
            mv = max([pixel.r, pixel.g, pixel.b])

            if mv > max_value:
                max_value = mv

        buff = array.array('B')
        for px in self.pixels:
            buff.append(min(255, int(px.r/max_value * 255)))
            buff.append(min(255, int(px.g/max_value * 255)))
            buff.append(min(255, int(px.b/max_value * 255)))

        pgmHeader = ('P6' + '\n' + str(self.w) +
                     '  ' + str(self.h) +
                     '  ' + str(255) + '\n')
        fout.write(pgmHeader.encode())
        buff.tofile(fout)
        fout.close()

    def __iter__(self):
        return ImageIterator(0, self.w*self.h, self)

    def __str__(self):
        string = ""
        for i, px in enumerate(self.pixels):
            if px.r != 0:
                string += "%d" % px.r
            else:
                string += "_"

            if (i+1) % self.w == 0:
                string += "\n"

        return string
