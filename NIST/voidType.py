#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .config import default_origin

voidType = {
    1: {
        1: '0',
        2: '0501',
        3: '1\x1f1\x1e2\x1f0',
        4: 'USA',
        5: '',
        6: '1',
        7: 'FILE',
        8: '',
        9: '',
        11: '00.00',
        12: '00.00'
    },
    
    2: {
        1: '0',
        2: '0',
        3: '0300',
        4: '',
        5: '',
        7: '',
        54: '0300\x1f\x1f'
    },
            
    13: {
        1: '0',
        2: '0',
        3: '4',
        4: '',
        5: '',
        6: '',
        7: '',
        8: '1',
        9: '',
        10: '',
        11: 'NONE',
        12: '8',
        13: '0'
    }
}
