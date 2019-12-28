#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019.12.28
# @Author  : 肖思慧
# @FileName: util.py


def packageFormula(atomic, xFormula):
    if type(atomic) != type([]):
        atomic = [atomic]
    if type(xFormula) != type([]):
        xFormula = [xFormula]
    formulaDict = {'atomic': atomic, 'xFormula': xFormula}
    return [formulaDict]


def formulaToStr(localList):
    """
    description: combine the elements in the formula list to a string
    """
    if len(localList) <= 1:
        return localList[0]
    else:
        tempStr = '(' + localList[0] + ')'
        for t in localList[1:]:
            tempStr += 'A(' + t + ')'
        return tempStr


def atomicToStr(localList):
    """
    description: combine the atomic with A(/\)
    """
    tempStr = ''
    pos = 0
    for t in localList:
        if pos >= 1:
            tempStr += ( 'A ' + t)
        else:
            tempStr += t
        pos += 1
    return tempStr


def getType(formula):
    """
    0: Until-Free
    1: Release-Free
    """
    flag = 1
    for t in formula:
        if t == 'R':
            flag = 0
            break
    
    return flag
