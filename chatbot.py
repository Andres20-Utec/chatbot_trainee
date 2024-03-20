import spacy
import es_core_news_sm
nlp = es_core_news_sm.load()
#Instalando bibliotecas necesarias
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jellyfish
import nltk
nltk.download('punkt')
import warnings
warnings.filterwarnings('ignore')

#Función para encontrar la raiz de las palabras
def raiz(palabra):
    radio=0
    palabra_encontrada=palabra
    file = open('lista_verbos.txt','r')
    lista_verbos = [element.strip('\n') for element in file.readlines()]
    for word in lista_verbos:
        confianza = jellyfish.jaro_winkler_similarity(palabra,word)
        if (confianza>=0.93 and confianza>=radio):
            radio=confianza
            palabra_encontrada=word
    return palabra_encontrada

#Función para tratar los textos
def tratamiento_texto(texto):
    trans = str.maketrans('áéíóú','aeiou')
    texto = texto.lower()
    texto = texto.translate(trans)
    texto = " ".join(texto.split())
    return texto

#Función para reemplazar el final de una palabra por 'r'
def reemplazar_terminacion(palabra):
    patron = r"(es|me|as|te|ste)$"
    nueva_palabra = re.sub(patron, "r", palabra)
    return nueva_palabra.split()[0]

#Función para adicionar o eliminar tokens
def revisar_tokens(texto, tokens):
    if len(tokens)==0:
        if [x for x in ['Chapter Data Engineering', 'CDE', 'Chapter Data Engineering '] if x in tratamiento_texto(texto)]: tokens.append('Chapter Data Engineering')
        elif [x for x in ['DAC', 'datos altamente críticos'] if x in tratamiento_texto(texto)]: tokens.append('datos altamente críticos')
        elif [x for x in ['on premise', 'arquitectura actual'] if x in tratamiento_texto(texto)]: tokens.append('datos altamente críticos')
    else:
        elementos_a_eliminar = ["cual", "que", "quien", "cuanto", "donde", "cuando", "como"]
        if 'hablame' in texto and 'hablar' in tokens: tokens.remove('hablar')
        elif 'cuentame' in texto and 'contar' in tokens: tokens.remove('contar')
        elif 'hago' in texto and 'hacer' in tokens: tokens.remove('hacer')
        elif 'entiendes' in texto and 'entender' in tokens: tokens.remove('entender')
        elif 'platicame' in texto and 'platicar' in tokens: tokens.remove('platicar')
        elif 'sabes' in texto and 'saber' in tokens: tokens.remove('saber')
        tokens = [x.replace('datar','data').replace('datos','dato') for x in tokens if x not in elementos_a_eliminar]
    return tokens

#Función para devolver los tokens normalizados del texto
def normalizar(texto):
    tokens=[]
    tokens=revisar_tokens(texto, tokens)
    if 'elprofealejo' in tokens:
        texto = ' '.join(texto.split()[:15])
    else:
        texto = ' '.join(texto.split()[:25])

    doc = nlp(texto)
    with open("diccionario_irregulares.json", "r") as archivo:
        diccionario_irregulares = json.load(archivo)
    file = open('lista_verbos.txt','r')
    lista_verbos = [element.strip('\n') for element in file.readlines()]
    for t in doc:
        lemma=diccionario_irregulares.get(t.text, t.lemma_.split()[0])
        lemma=re.sub(r'[^\w\s+\-*/]', '', lemma)
        if t.pos_ in ('VERB','PROPN','PRON','NOUN','AUX','SCONJ','ADJ','ADV','NUM') or lemma in lista_verbos:
            if t.pos_=='VERB':
                lemma = reemplazar_terminacion(lemma)
                tokens.append(raiz(tratamiento_texto(lemma)))
            else:
                tokens.append(tratamiento_texto(lemma))

    tokens = list(dict.fromkeys(tokens))
    tokens = list(filter(None, tokens))
    tokens = revisar_tokens(texto, tokens)
    return tokens


def obtener_lista_frases_normalizadas():
    lista_documentos = ["respuestas.txt"]
    documento_txt = ''
    for documento in lista_documentos:
        with open(documento, "r", encoding="utf-8") as archivo_txt:
            lector_txt = archivo_txt.read()
            for fila in lector_txt:
                documento_txt += fila
    documento =  documento_txt
    lista_frases = nltk.sent_tokenize(documento,'spanish')
    lista_frases_normalizadas = [' '.join(normalizar(x)) for x in lista_frases]
    return lista_frases, lista_frases_normalizadas


#Función para devolver la respuesta de los documentos
def respuesta_documento(pregunta):
    pregunta = normalizar(pregunta)
    def contar_coincidencias(frase):
        #print(frase, ' :',sum(1 for elemento in pregunta if elemento in frase))
        return sum(1 for elemento in pregunta if elemento in frase)
    lista_frases, lista_frases_normalizadas = obtener_lista_frases_normalizadas()
    diccionario = {valor: posicion for posicion, valor in enumerate(lista_frases_normalizadas)}
    lista = sorted(list(diccionario.keys()), key=contar_coincidencias, reverse=True)[:6]
    if 'curso' not in pregunta: lista = [frase for frase in lista if 'curso' not in frase]
    lista.append(' '.join(pregunta))
    #for elemento in lista: print(elemento)
    TfidfVec = TfidfVectorizer(tokenizer=normalizar)
    tfidf = TfidfVec.fit_transform(lista)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    return req_tfidf, lista_frases[diccionario[lista[idx]]]


'''pregunta='funciones de un Data Scientist Leader según Manual de Gobierno de Modelos Analíticos de Auditoría'
print('Tokens Pregunta: ', normalizar(pregunta))
respuesta = respuesta_documento(pregunta)
print('Tokens Respuesta: ', normalizar(respuesta[1]))
print('Precisión: ', round(respuesta[0],2))
print(respuesta[1])'''