#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:42:31 2021

@author: loic
"""

from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)