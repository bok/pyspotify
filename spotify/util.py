# -*- coding: utf-8 -*-

def utf8_str(string):
    try:
        return string.encode('utf-8')
    except Exception as e:
        return string
