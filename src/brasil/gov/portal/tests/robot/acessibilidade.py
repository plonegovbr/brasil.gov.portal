# -*- coding: utf-8 -*-


def _luminance(r, g, b):
    def normalize(value):
        value = float(value) / 255
        if value <= 0.03928:
            value = value / 12.92
        else:
            value = ((value + 0.055) / 1.055) ** 2.4
        return value
    r = normalize(r)
    g = normalize(g)
    b = normalize(b)
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return L + 0.05


def _color_to_rgb(color):
    color = color.split(',')
    r = float(''.join([c for c in color[0] if c.isdigit()]))
    g = float(''.join([c for c in color[1] if c.isdigit()]))
    b = float(''.join([c for c in color[2] if c.isdigit()]))
    return (r, g, b)


def _size_to_number(size):
    size = float(''.join([c for c in size if (c.isdigit() or c == '.')]))
    return size


class Acessibilidade:

    def validate_contrast(self, selector, bg, fg, size):
        """ Valida se o contraste esta dentro dos parametros aceitos
        """
        normal_ratio = 4.5
        large_ratio = 3.0
        ratio = normal_ratio
        size = _size_to_number(size)
        if size >= 18.0:
            ratio = large_ratio
        bg = _color_to_rgb(bg)
        fg = _color_to_rgb(fg)
        colors_luminance = [_luminance(*bg), _luminance(*fg)]
        colors_luminance.sort()
        contrast_ratio = colors_luminance[1] / colors_luminance[0]
        if contrast_ratio < ratio:
            msg = ('''Contraste incorreto para o seletor %s,'''
                   ''' valor obtido: %.2f, valor esperado: %.2f''' %
                   (selector, contrast_ratio, ratio))
            raise AssertionError(msg)

    def validate_contrast_aa(self, selector, bg, fg, size):
        """ Valida se o contraste esta dentro dos parametros aceitos
            para WCAG 2.0 AA
        """
        self.validate_contrast(selector, bg, fg, size)

    def validate_contrast_aaa(self, selector, bg, fg, size):
        """ Valida se o contraste esta dentro dos parametros aceitos
            para WCAG 2.0 AAA
        """
        normal_ratio = 7.1
        large_ratio = 4.5
        ratio = normal_ratio
        size = _size_to_number(size)
        if size >= 18.0:
            ratio = large_ratio
        bg = _color_to_rgb(bg)
        fg = _color_to_rgb(fg)
        colors_luminance = [_luminance(*bg), _luminance(*fg)]
        colors_luminance.sort()
        contrast_ratio = colors_luminance[1] / colors_luminance[0]
        if contrast_ratio < ratio:
            msg = ('''Contraste incorreto para o seletor %s,'''
                   ''' valor obtido: %.2f, valor esperado: %.2f''' %
                   (selector, contrast_ratio, ratio))
            raise AssertionError(msg)
