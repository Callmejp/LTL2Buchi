#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019.12.28
# @Author  : 金鹏, 王献辉， 张小禹
# @FileName: main.py
from util import packageFormula, formulaToStr, atomicToStr, getType
from graphviz import Digraph
from queue import Queue
import argparse


def convertToDNF(subformula, level):
    """
    @description: convert the LTL formula to the DNF form
    @param: 
        subformula{str}: LTL formula.
             level{int}: recurrent Level.
    @return: 
        dict: each object indicates the CNF clause.
    """
    # Termination
    if  len(subformula) == 1:
        if subformula == 'F':
            # special case for False
            return []
        return packageFormula(subformula, 'T')
    elif subformula[0] == 'X':
        # process the CNF in X()
        localFormula = subformula[2:-1]
        posList = []
        pos = 0
        cnt = 0
        for t in localFormula:
            if t == '(':
                cnt += 1
            elif t == ')':
                cnt -= 1
            elif t == 'O' and cnt == 0:
               posList.append(pos)
            pos += 1

        if len(posList) == 0: 
            return packageFormula('T', subformula[1:])
        else:
            posList.append(len(localFormula))
            tempList = []
            st = 0
            for ed in posList:
                tempFormula = localFormula[st:ed]
                tempList += packageFormula('T', tempFormula)
                st = ed + 1
            print("CNF occurs in the X:", tempList)
            return tempList
    
    left = 'left'
    operater = 'operater'
    right = 'right'
    rightIndex = 0
    # Process
    if subformula[0] != '(':
        if subformula[0].islower() or subformula[0] == 'T' or subformula[0] == 'F':
            left = subformula[0]
            operater = subformula[1]
            rightIndex = 2
    elif subformula[0] == '(':
        # (|left(1:pos)|)
        # 0|           |pos
        match = 1
        pos = 1
        for t in subformula[1:]:
            if t == ')':
                match -= 1
                if match == 0:
                    break
            elif t == '(':
                match += 1
            pos += 1
        left = subformula[1:pos]
        operater = subformula[pos+1]
        rightIndex = pos + 2
    else:
        print('Sth unexpected happened near Process!')
    # extract the right part
    if subformula[rightIndex] == '(':
        right = subformula[rightIndex+1:-1]
    else:
        right = subformula[rightIndex:]
    
    # choose the different action based on the operator
    if operater == 'A':
        # t: aAbAcAX()
        # And : termination
        t1 = convertToDNF(left, level+1)
        t2 = convertToDNF(right, level+1)
        if t1 == [] or t2 == []:
            # special case for false
            return []
        # multiply of the sets
        formulaList = []
        for left in t1:
            for right in t2:
                atomicList = list(set(left['atomic'] + right['atomic']))
                xFormula = list(set(left['xFormula'] + right['xFormula']))
                formulaList += packageFormula(atomicList, xFormula)
        return formulaList
    elif operater == 'R':
        t1 = convertToDNF('('+left+')A('+right+')', level+1)
        t2 = convertToDNF('('+right+')A(X('+subformula+'))', level+1)
        t3 = t1 + t2
        return t3
    elif operater == 'U':
        t1 = convertToDNF(right, level+1)
        t2 = convertToDNF('('+left+')A(X('+subformula+'))', level+1)
        t3 = t1 + t2
        return t3
    elif operater == 'O':
        t1 = convertToDNF(left, level+1)
        t2 = convertToDNF(right, level+1)
        t3 = t1 + t2
        return t3
    else:
        print("Ooops, sth unexpected happened near choosing operater")


"""
Function: clear & cleanFormula
description: just clear redundant Trues and brackets
"""
def clear(localList):
    length = len(localList)
    tempList = []
    for t in localList:
        if t == 'T' and length > 1:
            continue
        elif t[0] == '(' and t[-1] == ')':
            t = t[1:-1]
            tempList.append(t)
        else:
            tempList.append(t)
    # in case all elements are True
    if len(tempList) == 0:
        tempList.append('T')
    # Ensure uniqueness
    tempList.sort()
    return tempList

def cleanFormula(localList):
    
    for f in localList:
        f['atomic'] = clear(f['atomic'])
        f['xFormula'] = clear(f['xFormula'])


def drawAutomata():
    """
    @description: Draw the graph according to the nodes & edges
    @param: 
        subformula{str}: LTL formula.
             level{int}: recurrent Level.
    @return: 
        localCodeList{list}: each element is a segment of code.
    """
    global typeOfFormula, testFormula

    dot = Digraph(name="MyPicture", comment="the test", format="png")

    for n in nodes:
        # special for the start state
        label = n
        if n == testFormula:
            label = "st:" + testFormula
        # decide the type of formula
        if typeOfFormula == 1:
            # until-free
            if n == 'T':
                dot.node(name=n, label=label, color='green')
            else:
                dot.node(name=n, label=label, color='black')
        else:
            dot.node(name=n, label=label, color='green')

    for e in edges:
        dot.edge(e['u'], e['v'], label=e['label'], color='black')

    # dot.view(filename="mypicture", directory="D:\MyTest")
    dot.render(filename='MyPicture', directory="D:\MyTest",view=True)

def updateMap(name):
    """
    description: if the formula haven't existed before, update the map
    """
    global nodeCount
    mapDict[name] = nodeCount
    nodeCount += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("formula", type=str, help="LTL formula you wanna test.")
    args = parser.parse_args()

    # testFormula = '(X(aAb))R(cOd)'
    testFormula = args.formula

    typeOfFormula = getType(testFormula)

    edges = []
    nodes = []
    mapDict = {}
    nodeCount = 1
    updateMap(testFormula)
    nodes.append(testFormula)

    q = Queue()
    q.put(testFormula)
    while not q.empty():
        currentFormula = q.get()
        listOfDNF = convertToDNF(currentFormula, 0)
        # print(listOfDNF)
        cleanFormula(listOfDNF)
        # print(listOfDNF)

        for ele in listOfDNF:
            newFormula = formulaToStr(ele['xFormula'])
            # print("new Formula:", newFormula)
            if mapDict.get(newFormula, -1) == -1:
                q.put(newFormula)
                updateMap(newFormula)
                nodes.append(newFormula)
            
            newAtomic = atomicToStr(ele['atomic'])
            # print("new Atomic", newAtomic)

            edges.append({'u': currentFormula, 'v': newFormula, 'label': newAtomic})
    
    print(nodes)
    print(edges)

    drawAutomata()
