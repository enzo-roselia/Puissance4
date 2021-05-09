# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:23:07 2020

@author: nzoro
"""



import math
import time

def Initial():
    grille=[]
    for i in range(12):
        grille.append([' ' for j in range(6)])
    return grille
        
def Afficher(grille):
    for j in range(6):
        for i in range(12):
            if(grille[i][j]==" "): 
                print(".",end =' |')
            else:
                print(grille[i][j],end =' |')
        print()
    for i in range(1,13):
        if (i<=9) : c ="  "
        else: c = " "
        print(i,end=c)


def Actions(grille):
    return [j for j in range(12) if grille[j].__contains__(' ')]

def Result(grille,a,symbole,index = -1):
    copie = [list(i) for i in grille]
    while copie[a][index]!=' ':
        index-=1
    copie[a][index]=symbole
    return copie

def TerminalTest(grille):
    return Actions(grille)==[] or Utility2(grille)==10000000 or Utility2(grille)==-10000000#grande valeur en cas de victoires

def calcul(liste,choix,value=0):#heuristique
    attaque =0
    adv = 'X'
    if(choix =='X'): adv = 'O'
    for i in range(len(liste)):
        fenetre = liste[i:i+4]
        if(len(fenetre)==4):
            if(fenetre.count(choix)==3 and fenetre.count(" ")==1):#attaque
                value+=100
                attaque+=1
            elif(fenetre.count(choix)==2 and fenetre.count(" ")==2):
                value+=10
            if(fenetre.count(adv)==3 and fenetre.count(" ")==1):#defense
                value+=-80
            elif(fenetre.count(adv)==2 and fenetre.count(" ")==2):
                value+=-8            
    return value+(attaque*2)

def UtilityPlus(grille,choix):
    score = 0
    adv = 'X'
    if(choix =='X'): adv = 'O'
    for j in grille:
        score+=calcul(j,choix)
        
    for a in range (6):
        ligne = [grille[b][a] for b in range(12)]
        if("| |"+3*(choix+"|")+" |" in "|".join(ligne)): score +=1500#coup quasi gagnant
        if("| |"+3*(adv+"|")+" |" in "|".join(ligne)): score +=-2500
        else: score+=calcul(ligne,choix)
        
    
    for j in range(9):
        diag1 =[]
        diag2 =[]
        a = j+3
        b = j
        for i in range(6):
            if(a>=0):
                diag1.append(grille[a][i])
                a-=1
            if(b<=11):
                diag2.append(grille[b][i])
                b+=1
        if("| |"+3*(choix+"|")+" |" in "|".join(diag1)): score +=1500
        if("| |"+3*(adv+"|")+" |" in "|".join(diag1)): score +=-2500
        else: score+=calcul(diag1,choix)
        if("| |"+3*(choix+"|")+" |" in "|".join(diag2)): score +=1500
        if("| |"+3*(adv+"|")+" |" in "|".join(diag2)): score +=-2500
        else: score+=calcul(diag2,choix)
    
    for j in range(2):
        diag1 = []
        diag2 =[]
        a = 0
        b = 11
        for i in range(j+1,6):
            if(a<=4):
                diag1.append(grille[a][i])
                a+=1
            if(b>=7):
                diag2.append(grille[b][i])
                b=b-1
        if("| |"+3*(choix+"|")+" |" in "|".join(diag1)): score +=1500
        if("| |"+3*(adv+"|")+" |" in "|".join(diag1)): score +=-2500
        else: score+=calcul(diag1,choix)
        if("| |"+3*(choix+"|")+" |" in "|".join(diag2)): score +=1500
        if("| |"+3*(adv+"|")+" |" in "|".join(diag2)): score +=-2500
        else: score+=calcul(diag2,choix)
    
    score += 3*(grille[6].count(choix)+grille[5].count(choix))
    return score

def Utility2(grille):
    val=0
    #Parcours les colonnes
    for j in grille:
        if('X|X|X|X' in '|'.join(j)): return 10000000
        if('O|O|O|O' in '|'.join(j)): return -10000000

    #Parcours les lignes
    for a in range (6):
        ligne = [grille[b][a] for b in range(12)]
        if('X|X|X|X' in '|'.join(ligne)): return 10000000
        if('O|O|O|O' in '|'.join(ligne)): return -10000000     
        
    #Parcours les diagonales
    for j in range(9):
        diag1 =[]
        diag2 =[]
        a = j+3
        b = j
        for i in range(6):
            if(a>=0):
                diag1.append(grille[a][i])
                a-=1
            if(b<=11):
                diag2.append(grille[b][i])
                b+=1        
        if('X|X|X|X' in '|'.join(diag1)): return 10000000
        if('O|O|O|O' in '|'.join(diag1)): return -10000000
        if('X|X|X|X' in '|'.join(diag2)): return 10000000
        if('O|O|O|O' in '|'.join(diag2)): return -10000000

    #Parcours les 4 diagonales restantes
    for j in range(2):
        diag1 = []
        diag2 =[]
        a = 0
        b = 11
        for i in range(j+1,6):
            if(a<=4):
                diag1.append(grille[a][i])
                a+=1
            if(b>=7):
                diag2.append(grille[b][i])
                b=b-1
        if('X|X|X|X' in '|'.join(diag1)): return 10000000
        if('O|O|O|O' in '|'.join(diag1)): return -10000000
        if('X|X|X|X' in '|'.join(diag2)): return 10000000
        if('O|O|O|O' in '|'.join(diag2)): return -10000000
    
    return val

def minimax(grille, tour_IA,alpha, beta,profondeur):
    if TerminalTest(grille) or profondeur ==0:
        if(TerminalTest(grille)): return None,Utility2(grille)*(profondeur+1)
        else : return None,UtilityPlus(grille,'X')*(profondeur+1)
    
    if tour_IA:
        value = -math.inf
        col = Actions(grille)[0]
        for a in Actions(grille):
            bestVal = minimax(Result(grille,a,'X'),False,alpha,beta, profondeur-1)[1]
            if (bestVal >value):
                value = bestVal
                col = a
            alpha = max(alpha,value)
            if(alpha>=beta):
                return col,value
        return col,value

    else:
        value = math.inf
        col = Actions(grille)[0]
        for a in Actions(grille):
            bestVal = minimax(Result(grille,a,'O'),True,alpha,beta, profondeur-1)[1]
            if(bestVal<value):
                value = bestVal
                col = a
            beta = min(beta,value)
            if (alpha>=beta):
                return col,value
        return col,value
    
def Jouer(IA_commence):
    grille=Initial()
    coup = 0
    if(IA_commence):
        t=time.time()
        col,score = minimax(grille,True,-math.inf,math.inf,4)
        print(round(time.time()-t,3))
        grille = Result(grille,col,'X')
        coup+=1
    while(TerminalTest(grille)!=True and coup<72):
        Afficher(grille)
        print("\n")
        rep=eval(input("Position en colonne : "))
        while(rep-1 not in Actions(grille)):
            print("Impossible")
            rep=eval(input("Position en colonne : "))
        grille=Result(grille,rep-1,'O')
        coup+=1
        if(TerminalTest(grille)): break
        else:
            print("Chargement...")
            t=time.time()
            col,score = minimax(grille,True,-math.inf,math.inf,4)
            print(round(time.time()-t,3))
            grille = Result(grille,col,'X')
            coup+=1
            print("L'IA a joué en "+str(col+1))
    print("\n")
    Afficher(grille)
    print("\n")
    print("Fin de partie")
            






