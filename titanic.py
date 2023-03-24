import pandas as pd ; import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import pathlib
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import time

import os
#print(os.getcwd())
os.chdir('/home/coder/work/ensae-reproductibilite-application')

TrainingData = pd.read_csv('train.csv')
TestData = pd.read_csv('test.csv')
TrainingData = TrainingData.drop(columns = "PassengerId")
TestData = TestData.drop(columns = "PassengerId")

TrainingData.head()


## Valeurs manquantes

TrainingData.isnull().sum()

TestData.isnull().sum()

## Un peu d'exploration et de feature engineering

### Statut socioéconomique

fig, axes=plt.subplots(1,2, figsize=(12, 6)) #layout matplotlib 1 ligne 2 colonnes taile 16*8
fig1_pclass=sns.countplot(data=TrainingData, x ="Pclass",    ax=axes[0]).set_title("fréquence des Pclass")
fig2_pclass=sns.barplot(data=TrainingData, x= "Pclass",y= "Survived", ax=axes[1]).set_title("survie des Pclass")

### Genre

print(TrainingData['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0]).unique())


# Extraction et ajout de la variable titre
TrainingData['Title'] = TrainingData['Name'].apply( lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])
TestData['Title'] = TestData['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])

# Suppression de la variable Titre
TrainingData.drop(labels='Name', axis=1, inplace=True)
TestData.drop(labels='Name', axis=1, inplace=True)

#On note que Dona est présent dans le jeu de test à prédire mais dans les variables d'apprentissage on règle ca a la mano
TestData['Title'] = TestData['Title'].replace('Dona.', 'Mrs.')


fx, axes = plt.subplots(2, 1, figsize=(15, 10))
fig1_title = sns.countplot(data=TrainingData, x='Title', ax=axes[0]).set_title("Fréquence des titres")
fig2_title = sns.barplot(data=TrainingData, x='Title',y='Survived', ax=axes[1]).set_title("Taux de survie des titres")

### Age

sns.distplot(a= TrainingData['Age'].dropna(axis = 0),bins = 15,hist_kws={'rwidth'     :0.7}).set_title("distribution de l'age")

## Encoder les données imputées ou transformées.


TrainingData.head()

# Age
meanAge=round(TrainingData['Age'].mean())
TrainingData['Age'] = TrainingData['Age'].fillna(meanAge)
TestData['Age'] = TrainingData['Age'].fillna(meanAge)

# Sex, Title et Embarked
label_encoder_sex = LabelEncoder()
label_encoder_title = LabelEncoder()
label_encoder_embarked = LabelEncoder()
TrainingData['Sex'] = label_encoder_sex.fit_transform(TrainingData['Sex'].values)
TrainingData['Title'] = label_encoder_title.fit_transform(TrainingData['Sex'].values)
TrainingData['Embarked'] = label_encoder_embarked.fit_transform(TrainingData['Sex'].values)


TrainingData['Embarked'] = TrainingData['Embarked'].fillna('S')
TestData['Embarked'] = TestData['Embarked'].fillna('S')


TestData['Fare']=TestData['Fare'].fillna(TestData['Fare'].mean())

# Making a new feature hasCabin which is 1 if cabin is available else 0
TrainingData['hasCabin'] = TrainingData.Cabin.notnull().astype(int)
TestData['hasCabin'] = TestData.Cabin.notnull().astype(int)


TrainingData['Ticket_Len'] = TrainingData['Ticket'].apply(lambda x: len(x))
TestData['Ticket_Len'] = TestData['Ticket'].apply(lambda x: len(x))
TrainingData.drop(labels='Ticket', axis=1, inplace=True)
TestData.drop(labels='Ticket', axis=1, inplace=True)

## Transformation en `Array`

TrainingData.drop(labels='Cabin', axis=1, inplace=True)
TestData.drop(labels='Cabin', axis=1, inplace=True)
y = TrainingData.iloc[:, 0].values
X = TrainingData.iloc[:, 1:12].values

# Feature Scaling
scaler_x = MinMaxScaler((-1,1))
X = scaler_x.fit_transform(X)


# On _split_ notre _dataset_ d'apprentisage pour faire de la validation croisée une partie pour apprendre une partie pour regarder le score.
# Prenons arbitrairement 10% du dataset en test et 90% pour l'apprentissage.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Random Forest

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import pathlib
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier


#Ici demandons d'avoir 20 arbres
rdmf = RandomForestClassifier(n_estimators=20)
rdmf.fit(X_train, y_train)


#calculons le score sur le dataset d'apprentissage et sur le dataset de test (10% du dataset d'apprentissage mis de côté)
# le score étant le nombre de bonne prédiction
rdmf_score = rdmf.score(X_test, y_test)
rdmf_score_tr = rdmf.score(X_train, y_train)
print("{} % de bonnes réponses sur les données de test pour validation (résultat qu'on attendrait si on soumettait notre prédiction sur le dataset de test.csv)".format(round(rdmf_score*100)))
from sklearn.metrics import confusion_matrix
print("matrice de confusion")
confusion_matrix(y_test, rdmf.predict(X_test))

