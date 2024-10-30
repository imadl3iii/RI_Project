import re
import math
import sys
import time
import json
import nltk 
from nltk import TweetTokenizer

def Extraction(file):
    #Lecture du fichier qui contient les documents
    CacmAll = open(file, "r")

    #lecture des lignes
    lines = CacmAll.readlines()

    #dictionnaire des documents {DocIDF:liste des lignes du document}
    DictDoc ={}

    #parcourt et separation par rapport au .I, .T et .W ignorer les autres champs
    #c'est plus facile d'utiliser la fonction while pour avancer ligne par ligne et 
    beginDictDoc = time.time()
    i=0
    while(i<len(lines)):
        #on recupere la ligne 
        line = lines[i]

        #si la ligne commence par .I on recupere l'identifiant du document 
        if(line.startswith('.I')):
            DocIDF = int(line.split()[1])
        
        #sinon si la liste commence par .T, on recupere les lignes du champ titre
        if(line.startswith('.T')):
            i+=1
            titre = ""
            
            #on ajoute les lignes tanqu'elles ne commencent pas par un des marqueur en prenant 
            # en compte l'identifiant et le saut de ligne
            while((i<len(lines)) and (re.findall('\.([TWBANX]\n|I [0-9]+\n)', lines[i]))==[]):
                titre = titre + " " + lines[i]
                i+=1
            DictDoc[DocIDF] = titre

            #on decremente la ligne afin de retourner au marqueur
            i-=1
        
        #sinon si la liste commence par .W, on recupere les lignes du champ resume
        if(line.startswith('.W')):
            i+=1
            resume = ""
            while((i<len(lines)) and (re.findall('\.([TWBANX]|I [0-9]+)', lines[i]))==[]):
                resume = resume +" "+lines[i]
                i+=1
            DictDoc[DocIDF] = DictDoc[DocIDF] + resume
            i-=1          
        i+=1
    time.sleep(1)
    endDictDoc = time.time()
    #print('temps de chargement de DictDoc est =' +str(endDictDoc-beginDictDoc)+'secondes')
    #print('taille de DictDoc en octet apres enregistrement ='+str(sys.getsizeof(DictDoc)))
    return DictDoc


# Eliminer les mots vides et la ponctuation

def Stopword_elimination(text,ponctuation_list,stopwords_list):
    word_list = []
    # Eliminer la punctuation
    for character in ponctuation_list:
        text = text.replace(character, ' ')

    # str -> list
    words = text.split()
    for word in words:
        if word.lower() not in stopwords_list:
            word_list.append(word.lower())
    return word_list

def ExtractionQuery(path,stopwords_list,ponctuation_list):
    queryfile = open(path, "r")

    #lecture des lignes
    lines = queryfile.readlines()

    #dictionnaire des querys {queryIDF:liste des lignes des query}
    DictQuery ={}

    #parcourt et separation par rapport au .I, .T et .W ignorer les autres champs
    #c'est plus facile d'utiliser la fonction while pour avancer ligne par ligne et 
    i=0
    while(i<len(lines)):
        #on recupere la ligne 
        line = lines[i]

        #si la ligne commence par .I on recupere l'identifiant du document 
        if(line.startswith('.I')):
            queryIDF = int(line.split()[1])
            DictQuery[queryIDF]=""
        
        #sinon si la liste commence par .T, on recupere les lignes du champ titre
        if(line.startswith('.T')):
            i+=1
            titre = ""
            
            #on ajoute les lignes tanqu'elles ne commencent pas par un des marqueur en prenant 
            # en compte l'identifiant et le saut de ligne
            while((i<len(lines)) and (re.findall('\.([TWBANX]\n|I [0-9]+\n)', lines[i]))==[]):
                titre = titre + " " + lines[i]
                i+=1
            DictQuery[queryIDF] = titre

            #on decremente la ligne afin de retourner au marqueur
            i-=1
        
        #sinon si la liste commence par .W, on recupere les lignes du champ resume
        if(line.startswith('.W')):
            i+=1
            resume = ""
            while((i<len(lines)) and (re.findall('\.([TWBANX]|I [0-9]+)', lines[i]))==[]):
                resume = resume +" "+lines[i]
                i+=1
            DictQuery[queryIDF] = DictQuery[queryIDF] + resume
            i-=1          
        i+=1 
    Query={}
    for key in DictQuery.keys():
        text=DictQuery[key]
        word_list=Stopword_elimination(text,ponctuation_list,stopwords_list)
        cleanWord_list = []
        for word in word_list:
            if word not in cleanWord_list:
                cleanWord_list.append(word)
        Query[key]=cleanWord_list
    #print(Query)
    return Query
    
def ExtractionQrels(path):
    qrelsfile = open(path, "r")

    #lecture des lignes
    lines = qrelsfile.readlines()
    Qrels={}
    i=0
    while(i<len(lines)):
        line = lines[i].split(" ")
        numQuery=int(line[0])
        if  numQuery not in Qrels.keys():
            list = []
            list.append(int(line[1]))
            Qrels[numQuery] = list
        else: 
            list.append(int(line[1]))
            Qrels[numQuery]=list
        i +=1
    #print(Qrels)
    return Qrels


def mot_freq(word_list):
    frequence_dict = {}
    list_mots_freqs=[]
    for word in word_list:
        if word not in frequence_dict:
            frequence_dict[word] = word_list.count(word)
            list_mots_freqs.append([word,word_list.count(word)])
    return list_mots_freqs

def dict_freq(word_list):
    frequence_dict = {}
    for word in word_list:
        if word not in frequence_dict:
            frequence_dict[word] = word_list.count(word)
    return frequence_dict

def creation_indexedDict(DictDoc,ponctuation_list,stopwords_list):
    inexedDict={}
    #allwords est une liste qui contient tous 
    # les terms de la collection sans redand
    global allwords
    allwords=[]
    for key in DictDoc.keys():
        text=DictDoc[key]
        word_list=Stopword_elimination(text,ponctuation_list,stopwords_list)
        for word in word_list:
             if word not in allwords:
                allwords.append(word)
        if key not in inexedDict.keys():
           inexedDict[key]=dict_freq(word_list)  
    return inexedDict, allwords



#la creation du dict indexé 


# cette fonction retourne un dictionnaire qui a pour clé le numero du document qui contient
# le mot word et la valeur la frequence du mot word dans ce document 
def dict_doc_freq(word,inexedDict):
    dic_doc_freq={}
    for i in inexedDict.keys():
        for j in inexedDict[i].keys():
            if j==word:
                if i not in dic_doc_freq.keys():
                    dic_doc_freq[i]=inexedDict[i].get(word)
    return dic_doc_freq


# cette fonction cree le fichier inversé 
def creation_fichierInverse(indexedDict,allwords):
    fichier_inverse={}
    for word in allwords:
          if word not in fichier_inverse:
             fichier_inverse[word] = dict_doc_freq(word,indexedDict)
    return fichier_inverse



#************************Fonctions d'accées**********************************
#pour un document donnée, retourner la liste des mots avec les fréquences 
def ReturnWords(indiceDocument,indexedDict):
    for i in indexedDict.keys():
        if(i == indiceDocument):
            return indexedDict[i]
    print("liste de mots-fréquences non trouvée")

#pour un terme donnée, retourner la liste des documents dont il apparait avec la fréquence
def ReturnDocs(terme,fichier_inverse):
    for i in fichier_inverse.keys():
        if (i == str(terme).lower()):
            return fichier_inverse[i]
    print("liste de documents-fréquences non trouvée")

  

#fonction 1 du modele vectoriel
def ProduitInterne(dj,requete,FichierInvrsePoids):
    produit = 0
    for terme in requete:
        produit = produit + FichierInvrsePoids[str(terme).lower()][dj]
    return produit

#fonction 2 du modele vectoriel
def CoefDeDice(dj, NewRequete,requete,documentWords,FichierInvrsePoids):
    produit = 2*ProduitInterne(dj, NewRequete,FichierInvrsePoids)
    somme = 0
    i = 0
    while(i<len(documentWords)):
        somme = somme+ math.pow(FichierInvrsePoids[str(documentWords[i]).lower()][dj],2)
        i+=1
    somme = somme + len(requete)
    return produit/somme

#fonction 3 du modele vectoriel
def Cosinus(dj, NewRequete,requete,documentWords,FichierInvrsePoids):
    produit = ProduitInterne(dj, NewRequete,FichierInvrsePoids)
    somme = 0
    i = 0
    while(i < len(documentWords)):
        somme = somme+ math.pow(FichierInvrsePoids[str(documentWords[i]).lower()][dj],2)
        i+=1
    return produit/math.sqrt(somme*len(requete))


#fonction 4 du modele vectoriel
def Jaccard(dj,NewRequete,requete,documentWords,FichierInvrsePoids):
    produit = ProduitInterne(dj, NewRequete,FichierInvrsePoids)
    somme = 0
    i = 0
    while(i < len(documentWords)):
        somme = somme+ math.pow(FichierInvrsePoids[str(documentWords[i]).lower()][dj],2)
        i+=1
    somme = somme+len(requete)-produit
    return produit/somme

#fonction qui retourne le nombre de document pertinents trouvés
def ListeDocPertientTrouv(ListeDocTrouv, ListeDocPertinent):
    ListeDocPertientTrouv=[]
    for document in ListeDocTrouv:
        if(document in ListeDocPertinent):
            ListeDocPertientTrouv.append(document)
    return ListeDocPertientTrouv


#calcul du rappel d'une requete donnée ==> nombre de documents pertinents trouvés/nombre de document pertinents total
def Rappel(ListeDocPertientTrouv, ListeDocPertinent):
    return len(ListeDocPertientTrouv)/len(ListeDocPertinent)

#calcul de précision d'un requete donnée ==> nombre de documents pertinents sélécionnés/nombre total de documents sélécionnés
def Precision(ListeDocPertientTrouv, ListeDocTrouv):
    return len(ListeDocPertientTrouv)/len(ListeDocTrouv)


#2**************************Modéle boolean************************************************
#we dont work with this version 
#Module de Representation des Document 
def MRD_bool(fichier_inverse):
    DictBool = {}
    for terme in fichier_inverse.keys():
        DictDocs = {}
        document = 1
        for document in dict(fichier_inverse[terme]).keys():
            DictDocs[document]=True
        DictBool.update({terme : DictDocs})
    return DictBool  
#Module de Representation des Requetes
def MRR_bool(requete):
    requete=requete.lower()
    print(requete)
    req = TweetTokenizer().tokenize(requete)
    print(req)
    return req
#Module d'Appariemment entre requete document 
def MA_bool(requete,N,DictBool):
    listDocsTrouv=[]
    for i in range(1,N+1):
        if(rsv(requete,i,DictBool)):
            listDocsTrouv.append(i)
    return listDocsTrouv

def rsv(req,doc,DictBool):
    result= eval("")
    return result
#récupérer le not d'une variable booleénne
def notVar(variable):
    if(variable == True):
        return False
    else :
        if(variable == False):
            return True

#fonction used 
def ModeleBooleen(Requete,Index,Stopword_list):    
    listeDoc=[]    
    Req=''
    for doc in Index: 
        document=dict()
        for mot in Index[doc]:
            document[mot]= Index[doc][mot]
        MotsReqNoisy=nltk.tokenize.word_tokenize(Requete)    
        MotsReq=[]
        for mot in MotsReqNoisy:
            if(mot.lower() not in ['and','or','(',')','not']): 
                if mot.lower() not in Stopword_list:
                   MotsReq.append(mot.lower())
            else:
                MotsReq.append(mot.lower())
        for mot in MotsReq:            
            Req=''
            if(mot.lower() not in ['and','or','(',')','not']): 
                if(mot.lower() not in  document):
                    MotsReq[MotsReq.index(mot)]=0
                else:
                    MotsReq[MotsReq.index(mot)]=1
        for el in MotsReq:
            Req=Req+' '+str(el)
        if(eval(Req)==1):
            listeDoc.append(doc)  
    return listeDoc; 


#*****************************************************************************************
# #3 Création d'un fichier inversé par pondération

# la fonction dict_doc_poids retourne un dictionnaire des numero de document qui contient le mot 
# "word" ti associé a le poids du mot "word" dans ce document dj
def dict_doc_poids(word,inexedDict,fichier_inverse,N):
    #N est le nombre total des documents de la collection
    dic_doc_poids={}
    #on parcour tout les numeros de documents de 1 à 3204
    for i in inexedDict.keys():
        #on vérifi si le doc contient le mot word(ti) on parcourant ses mots 
        for j in inexedDict[i].keys():
            if j==word:
                if i not in dic_doc_poids.keys():
                    #on recupere la frequence du mot dans le docuement i  = dj
                    freq=inexedDict[i].get(word)
                    #on recupére la freq maximal dans le doc i = dj 
                    max=0
                    for y in inexedDict[i].values():
                        if y>max:
                            max=y
                    ni=len(fichier_inverse[word])
                    #on calcul ni avec le fichier inversé pour gagné du temps 
                    dic_doc_poids[i]=(freq/max)*math.log10( (N/ni)+1 )
    return dic_doc_poids


#cette fonction permet la creation du fichier inverse pondéré 
def creation_fichierInversePonderé(N,indexedDict,fichier_inverse,allwords):
    fichier_inverse_pondere={}
    for word in allwords:
          if word not in fichier_inverse_pondere:
             fichier_inverse_pondere[word] = dict_doc_poids(word,indexedDict,fichier_inverse,N)
    return fichier_inverse_pondere

#4**************************Modéle Vectoriel************************************************


#Module de Representation des Document 
def MRD_Vec(fichier_inverse_pondere):
    return fichier_inverse_pondere
       
 
#Module de Representation des Requetes
def MRR_Vec(text,Stopword_list):
    req=text.split()
    requete=[]
    for mot in req:
        if mot.lower() not in Stopword_list:
            if mot.lower() not in requete:
               requete.append(mot.lower())
    return requete
#Module d'Appariemment entre requete document 
def MA_Vec(fichier_inverse_pondere,indexed,requete,fonction):
    listDocSim=dict()
    if fonction == "ProduitInterne":
        for doc in indexed: 
            documentWords=list()
            for mot in indexed[doc]:
                documentWords.append(mot)
            NewReq=list()
            for mot in requete:
                if mot.lower() in documentWords:
                    NewReq.append(mot.lower())
            if(len(NewReq)>0):
               listDocSim[doc]=ProduitInterne(doc,NewReq,fichier_inverse_pondere)
        listDocSim=sorted(listDocSim.items(), key=lambda t: t[1])          
    elif fonction == "CoefDeDice":
        for doc in indexed: 
            documentWords=list()
            for mot in indexed[doc]:
                documentWords.append(mot)
            NewReq=list()
            for mot in requete:
                if mot in documentWords:
                    NewReq.append(mot)
            if(len(NewReq)>0):
               listDocSim[doc]=CoefDeDice(doc,NewReq,requete,documentWords,fichier_inverse_pondere) 
        listDocSim=sorted(listDocSim.items(), key=lambda t: t[1])          
    elif fonction == "Cosinus":
        for doc in indexed: 
            documentWords=list()
            for mot in indexed[doc]:
                documentWords.append(mot)
            NewReq=list()
            for mot in requete:
                if mot in documentWords:
                    NewReq.append(mot)
            if(len(NewReq)>0):
               listDocSim[doc]=Cosinus(doc,NewReq,requete,documentWords,fichier_inverse_pondere) 
        listDocSim=sorted(listDocSim.items(), key=lambda t: t[1])          
    elif fonction == "Jaccard":
        for doc in indexed: 
            documentWords=list()
            for mot in indexed[doc]:
                documentWords.append(mot)
            NewReq=list()
            for mot in requete:
                if mot in documentWords:
                    NewReq.append(mot)
            if(len(NewReq)>0):
               listDocSim[doc]=Jaccard(doc,NewReq,requete,documentWords,fichier_inverse_pondere)
        listDocSim=sorted(listDocSim.items(), key=lambda t: t[1])    
    return listDocSim



 