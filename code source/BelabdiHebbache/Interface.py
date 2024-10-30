from re import S
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import ProjetRI
from ProjetRI import * 
import time
import nltk 
from nltk import re


#Récupération et prétraitements des données 
#récupération des champs .I, .T, .W
DictDoc = Extraction("cacm.all")

#Elémination des mots vide et récupération des terme
ponctuation_list = ['?', '.', '!', '<', '>', '}', '{', ':', '(', ')', '[', ']', '\"', ',', '-', "»", "«", '\'', '’',
                    '#', '+', '_', '-', '*', '/', '=','\"n', ';','$']

# ouverture du fichier common_words
stopwordsfile = "common_words"

# Récupération de la liste des mots vides
stopwords_list = open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

#récupérer le nombre de documents
N = list(DictDoc)[-1]

#ouverture du fichier query.txt et qrels.txt
queryfile = "query.text"
qrelsfile = "qrels.text"

dictQuery=ExtractionQuery(queryfile,stopwords_list,ponctuation_list)
dictQrels=ExtractionQrels(qrelsfile)
#inexedDict, allwords=creation_indexedDict(DictDoc,ponctuation_list,stopwords_list)
"""
#enregistrement de inexedDict 
tfinexedDict = open("myIndexedDictionary.json", "w")
json.dump(inexedDict,tfinexedDict)
tfinexedDict.close()
"""

#loading dictionary inexedDict
tfinexedDict = open("myIndexedDictionary.json", "r")
#beginindexedDict = time.time()
indexedDict = json.load(tfinexedDict)

#time.sleep(1)
#endindexedDict = time.time()
#print('taille de indexedDict en octet apres enregistrement ='+str(sys.getsizeof(indexedDict)))
#print('temps de chargement de indexedDict est =' +str(endindexedDict-beginindexedDict)+'secondes')


#création du fichier inverse 
""""
fichier_inverse=creation_fichierInverse(indexedDict,allwords)
print(fichier_inverse)
#enregistrement de ficier inverse
tf_inverse = open("fichierInverse.json", "w")
json.dump(fichier_inverse,tf_inverse)
tf_inverse.close()
"""
#loading dictionary fichier_inverse
tf_inverse = open("fichierInverse.json", "r")
#beginfichier_inverse =time.time()
fichier_inverse = json.load(tf_inverse)
#time.sleep(1)
#endfichier_inverse = time.time()
#print('temps de chargement de fichier_inverse  est =' +str(endfichier_inverse -beginfichier_inverse )+'secondes')
#print('taille de fichier_inverse en octet apres enregistrement ='+str(sys.getsizeof(fichier_inverse)))

#transformation du fichier inverse en module de representation boolean 
"""
DictBool=MRD_bool(fichier_inverse)
print(DictBool)
#enregistrement de ficier inverse
tf_DictBool = open("fichier_DictBool.json", "w")
json.dump(DictBool,tf_DictBool)
tf_DictBool.close()"""
"""
#loading dictionary DictBool
tf_DictBool = open("fichier_DictBool.json", "r")
#beginfichier_inverse =time.time()
DictBool = json.load(tf_DictBool)"""
"""
#création du fichier inverse pondéré
FichierInvrsePoids = creation_fichierInversePonderé(N,indexedDict,fichier_inverse,allwords)
#enregistrement
tf_inversePondere = open("fichierInversePondere.json", "w")
json.dump(FichierInvrsePoids,tf_inversePondere)
tf_inversePondere.close()
"""
#loading dictionary FichierInvrsePoids
tf_inversePondere = open("fichierInversePondere.json", "r")
#beginFichierInvrsePoids = time.time()
FichierInvrsePoids = json.load(tf_inversePondere)
#time.sleep(1)
#endFichierInvrsePoids = time.time()
#print('temps de chargement de FichierInvrsePoids  est =' +str(endFichierInvrsePoids -beginFichierInvrsePoids)+'secondes')
#print('taille de FichierInvrsePoids en octet apres enregistrement ='+str(sys.getsizeof(FichierInvrsePoids)))



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(690, 30, 481, 151))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.textEditRequeteBooleen = QtWidgets.QTextEdit(self.groupBox)
        self.textEditRequeteBooleen.setGeometry(QtCore.QRect(10, 50, 461, 41))
        self.textEditRequeteBooleen.setObjectName("textEditRequeteBooleen")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.ButtonRechercheBooleen = QtWidgets.QPushButton(self.groupBox)
        self.ButtonRechercheBooleen.setGeometry(QtCore.QRect(330, 100, 131, 41))
        self.ButtonRechercheBooleen.setObjectName("ButtonRechercheBooleen")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(690, 180, 481, 171))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.textEditRequeteVectoriel = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEditRequeteVectoriel.setGeometry(QtCore.QRect(10, 50, 461, 41))
        self.textEditRequeteVectoriel.setObjectName("textEditRequeteVectoriel")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ButtonRechercheVectoriel = QtWidgets.QPushButton(self.groupBox_2)
        self.ButtonRechercheVectoriel.setGeometry(QtCore.QRect(340, 100, 131, 41))
        self.ButtonRechercheVectoriel.setObjectName("ButtonRechercheVectoriel")
        self.comboBoxTypeFonctionAppa = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBoxTypeFonctionAppa.setGeometry(QtCore.QRect(10, 120, 161, 41))
        self.comboBoxTypeFonctionAppa.setObjectName("comboBoxTypeFonctionAppa")
        self.comboBoxTypeFonctionAppa.addItem("")
        self.comboBoxTypeFonctionAppa.addItem("")
        self.comboBoxTypeFonctionAppa.addItem("")
        self.comboBoxTypeFonctionAppa.addItem("")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 171, 31))
        self.label_3.setObjectName("label_3")
        self.ButtonEvaluationVectorielModel = QtWidgets.QPushButton(self.groupBox_2)
        self.ButtonEvaluationVectorielModel.setGeometry(QtCore.QRect(200, 100, 131, 41))
        self.ButtonEvaluationVectorielModel.setObjectName("ButtonEvaluationVectorielModel")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 0, 661, 351))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.textBrowserAfficheDocsTrouver = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowserAfficheDocsTrouver.setGeometry(QtCore.QRect(20, 30, 631, 311))
        self.textBrowserAfficheDocsTrouver.setObjectName("textBrowserAfficheDocsTrouver")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 350, 1151, 401))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 251, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(380, 20, 361, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(750, 25, 261, 21))
        self.label_6.setObjectName("label_6")
        self.textBrowserDocsPertinents = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowserDocsPertinents.setGeometry(QtCore.QRect(10, 60, 361, 331))
        self.textBrowserDocsPertinents.setObjectName("textBrowserDocsPertinents")
        self.textBrowserDocsPertSelected = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowserDocsPertSelected.setGeometry(QtCore.QRect(380, 60, 361, 331))
        self.textBrowserDocsPertSelected.setObjectName("textBrowserDocsPertSelected")
        self.textBrowserEvaluationResult = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowserEvaluationResult.setGeometry(QtCore.QRect(750, 60, 391, 331))
        self.textBrowserEvaluationResult.setObjectName("textBrowserEvaluationResult")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.ButtonRechercheBooleen.clicked.connect(lambda: boolean(self,indexedDict))
        self.ButtonRechercheVectoriel.clicked.connect(lambda: vectoriel(self,FichierInvrsePoids,indexedDict))
        self.ButtonEvaluationVectorielModel.clicked.connect(lambda: evaluation(self))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IHM pour les modeles de base de RI"))
        self.groupBox.setTitle(_translate("MainWindow", "Modéle booléen "))
        self.label.setText(_translate("MainWindow", "Requête"))
        self.ButtonRechercheBooleen.setText(_translate("MainWindow", "Recherche"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Modéle vectoriel"))
        self.label_2.setText(_translate("MainWindow", "Requête"))
        self.ButtonRechercheVectoriel.setText(_translate("MainWindow", "Recherche"))
        self.comboBoxTypeFonctionAppa.setItemText(0, _translate("MainWindow", "ProduitInterne"))
        self.comboBoxTypeFonctionAppa.setItemText(1, _translate("MainWindow", "CoefDeDice"))
        self.comboBoxTypeFonctionAppa.setItemText(2, _translate("MainWindow", "Cosinus"))
        self.comboBoxTypeFonctionAppa.setItemText(3, _translate("MainWindow", "Jaccard"))
        self.label_3.setText(_translate("MainWindow", "Fonction type:"))
        self.ButtonEvaluationVectorielModel.setText(_translate("MainWindow", "Evaluation"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Les documents trouvés "))
        self.groupBox_4.setTitle(_translate("MainWindow", "Evaluation du medéle vectoriel "))
        self.label_4.setText(_translate("MainWindow", "Documents pertinents"))
        self.label_5.setText(_translate("MainWindow", "Documents pertinents selectionné"))
        self.label_6.setText(_translate("MainWindow", "Resultats evaluation"))

def boolean(self,indexe):
    self.textBrowserAfficheDocsTrouver.clear()
    listDocs=[]
    req= self.textEditRequeteBooleen.toPlainText()
    if(req!=""):
        try:  
            listDocs=ModeleBooleen(req,indexe,stopwords_list)
            self.textBrowserAfficheDocsTrouver.clear()
            
            if(len(listDocs)>0):
                for element in listDocs:
                    self.textBrowserAfficheDocsTrouver.append("D "+str(element))
                    
                    #self.textBrowserAfficheDocsTrouver.itemDoubleClicked.connect(lambda: LectureItemDocs(self,Index))
            else:
                self.textBrowserAfficheDocsTrouver.append("Aucun document ne satisfait votre requête")
        except SyntaxError:
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez corriger le format de la requête")
            error.exec_()
    else:
        error=QtWidgets.QErrorMessage()
        error.showMessage("Veuillez écrire la requête")
        error.exec_() 

def vectoriel(self,FichierInvrsePoids,indexed):
    self.textBrowserAfficheDocsTrouver.clear()
    req= self.textEditRequeteVectoriel.toPlainText()
    requete=MRR_Vec(req,stopwords_list)
    fonction=self.comboBoxTypeFonctionAppa.currentText()
    if(req!=""):
        try:
            list_DocsSimilarite=MA_Vec(FichierInvrsePoids,indexed,requete,fonction)
            self.textBrowserAfficheDocsTrouver.clear()
            
            if(len(list_DocsSimilarite)>0):
                for element in reversed(list_DocsSimilarite):
                    self.textBrowserAfficheDocsTrouver.append("D "+str(element[0])+"    Similarité : "+str(element[1]))
            else:
                self.textBrowserAfficheDocsTrouver.append("Aucun document ne satisfait votre requête")
        except SyntaxError:
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez corriger le format de la requête")
            error.exec_()
    else:
        error=QtWidgets.QErrorMessage()
        error.showMessage("Veuillez écrire la requête")
        error.exec_() 

def evaluation(self):
    if(self.textEditRequeteVectoriel.toPlainText()!=""):
        try:
            Numreq = int(self.textEditRequeteVectoriel.toPlainText())
            requete = dictQuery[Numreq]
            print(requete)
            fonction=self.comboBoxTypeFonctionAppa.currentText()
            list_DocsSimilarite=MA_Vec(FichierInvrsePoids,indexedDict,requete,fonction)
            listDocselected = []
            S=0.12
            for element in reversed(list_DocsSimilarite):
                if(element[1]>= S):
                   listDocselected.append(int(element[0]))
            #limitation du T 
            T=50
            if(len(listDocselected)>T):
               print(str(len(listDocselected)))
               listDocselected=listDocselected[:T]
            print(listDocselected)
            DocPertinent = dictQrels[Numreq]
            print(DocPertinent)
            DocPertientTrouv=ListeDocPertientTrouv(listDocselected,DocPertinent)
            print(DocPertientTrouv)
            if(len(DocPertinent)>0):
               rappel=Rappel(DocPertientTrouv,DocPertinent)
            if(len(listDocselected)>0):
               precision=Precision(DocPertientTrouv,listDocselected)
            self.textBrowserDocsPertinents.clear()
            self.textBrowserDocsPertSelected.clear()
            self.textBrowserEvaluationResult.clear()
            if(len(DocPertientTrouv)>0):
                for doc in DocPertinent:
                     self.textBrowserDocsPertinents.append("D "+str(doc))
                for doc in DocPertientTrouv:
                     self.textBrowserDocsPertSelected.append("D "+str(doc))
                self.textBrowserEvaluationResult.append("Rappel ="+str(rappel))
                self.textBrowserEvaluationResult.append("Precision ="+str(precision))
            else:
                self.textBrowserDocsPertSelected.append("Aucun document pertinent selectionné ")
                self.textBrowserEvaluationResult.append("Rappel ="+str(0.0))
                self.textBrowserEvaluationResult.append("Precision ="+str(0.0))
        except SyntaxError:
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez entre un entier entre 01 et 64")
            error.exec_() 
    else:
        error=QtWidgets.QErrorMessage()
        error.showMessage("Veuillez entré le numéro de la requete (chiffre entre 01 ET 64)")
        error.exec_()     
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
