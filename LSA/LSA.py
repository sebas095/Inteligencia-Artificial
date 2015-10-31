#implementacion LSA
# -*- encoding: utf-8 -*-
from __future__ import division
import re , pprint
from numpy import zeros, asarray, sum, where, average
from scipy.linalg import svd
from math import log

text = open('Textos/corazon_delator.txt', 'r').read()
#text = open('Textos/tunel.txt', 'r').read() 

#palabras que no aportan significado 
stopwords = ['un', 'una', 'unas', 'unos', 'uno', 'sobre', 'todo', 'también', 'tras', 'otro', 'algún', 'alguno', 'alguna', 'algunos', 'algunas',
			'ser', 'soy', 'es', 'eres', 'somos', 'son', 'estoy', 'esta', 'estamos', 'estan' , 'como', 'en', 'para', 'atras', 'porque', 'por qué', 
			'estado', 'estaba', 'ante', 'antes', 'siendo', 'ambos', 'pero', 'por', 'poder', 'puede', 'puedo', 'podemos', 'pueden', 'fui', 'fue', 
			'fuimos', 'fueron', 'hacer', 'hago', 'hace', 'hacemos', 'haceis', 'hacen', 'cada', 'fin', 'incluso', 'primero   desde', 'conseguir', 'consigo', 'consigue', 'consigues', 'conseguimos', 'consiguen',
			'ir', 'voy', 'va', 'vamos', 'vais', 'van', 'vaya', 'gueno', 'ha', 'tener', 'tengo', 'tiene', 'tenemos', 'teneis', 'tienen', 'el', 'la', 'lo', 'las', 'los', 'su', 'aqui', 'mio', 'tuyo',
			'ellos', 'ellas', 'nos', 'nosotros', 'vosotros', 'vosotras', 'si', 'dentro', 'solo', 'solamente', 'saber', 'sabes', 'sabe', 'sabemos', 'sabeis', 'saben', 'ultimo', 'largo',
			'bastante', 'haces', 'muchos', 'aquellos', 'aquellas', 'sus', 'entonces', 'tiempo', 'verdad', 'verdadero', 'verdadera   ', 'cierto', 'ciertos', 'cierta', 'ciertas', 'intentar', 'intento',
			'intenta', 'intentas', 'intentamos', 'intentais', 'intentan', 'dos', 'bajo', 'arriba', 'encima', 'usar', 'uso', 'usas', 'usa', 'usamos', 'usais', 'usan', 'emplear', 'empleo', 'empleas', 
			'emplean', 'ampleamos', 'empleais', 'valor', 'muy', 'era', 'eras', 'eramos', 'eran', 'modo', 'bien', 'cual', 'cuando', 'donde', 'mientras', 'quien', 'con', 'entre',
			'sin', 'trabajo', 'trabajar', 'trabajas', 'trabaja', 'trabajamos', 'trabajais', 'trabajan', 'podria', 'podrias', 'podriamos', 'podrian', 'podriais', 'yo', 'aquel']
ignorechars = ''',-:'!¡?¿"'''

class LSA(object):
	
	def __init__(self, stopwords, ignorechars):
		self.stopwords = stopwords
		self.ignorechars = ignorechars
		self.wdict = {}
		self.dcount = 0     
		
	def parse(self, doc):
		'''
		El método parse toma un documento, se divide en palabras, elimina los caracteres ignorados y convierte
		todo en minúsculas por lo que las palabras pueden ser comparados con las palabras vacías. Si la palabra 
		es una palabra de parada, se ignora y pasar a la siguiente palabra. Si no es una palabra de parada, 
		ponemos la palabra en el diccionario, y también añadir el número actual a no perder de vista que 
		documenta la palabra aparece en.Los documentos que cada palabra aparece en se mantienen en una lista 
		asociada a esa palabra en el diccionario. Por ejemplo, ya que el libro palabra aparece en los títulos 3 y 4,
		tendríamos self.wdict ["libro"] = [3, 4] después de que todos los títulos se analizan.Después de procesar 
		todas las palabras del documento actual, aumentamos el número de documento en preparación para el 
		siguiente documento que se analiza.
		'''
		words = doc.split()
		for w in words:
			#Convierto cada palabra a minuscula e ignoro los signos de puntuacion, admiracion,etc
			w = w.lower().translate(None, self.ignorechars)
			if w in self.stopwords:
				continue
			elif w in self.wdict:
				#Por cada palabra repetida en el diccionario se crea una columna mas con valor dcount
				self.wdict[w].append(self.dcount)
			else:
				#se agrega cada palabra del texto como llave del diccionario y y valor dcoubt
				self.wdict[w] = [self.dcount]
		self.dcount += 1 
		
	def build(self):
		'''
		Una vez que todos los documentos se analizan, todas las palabras (claves de diccionario) que 
		se encuentran en más de 1 documento se extraen y ordenados, y una matriz se construye con el 
		número de filas (claves) igual al número de las palabras, y el número de columnas igual al 
		recuento de documentos. Por último, para cada palabra (clave) y el documento de par se incrementa 
		la celda matriz correspondiente.
		'''
		#se inicializa self.keys con todaslas palabras que tienen una frecuencia superior a uno
		self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
		self.keys.sort()
		#se crea un array inicializado con ceros
		self.A = zeros([len(self.keys), self.dcount])
		#Se llena la matriz A donde en cada celda estara la ocurrencia correspondiente a cada palabra
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i,d] += 1

	def calc(self):
		'''
		La matriz T nos da las coordenadas de cada palabra en nuestro "concepto" espacio, 
		la matriz Vt nos da las coordenadas de cada documento en nuestro "concepto" el espacio, 
		y la matriz S de valores singulares nos da una idea de cómo muchas dimensiones o "conceptos" que deben incluir.
		'''
		#se hace una descomposicon de los valores singulares
		self.U, self.S, self.Vt = svd(self.A)
		
	def TFIDF(self):
		'''
		TFIDF i, j = (N i, j / N *, j) * log (D / D i) donde:
		N i, j = el número de veces que la palabra i aparece en el documento j (el recuento de células original).
		N *, j = el número de total de palabras en el documento j (sólo tiene que añadir los recuentos en la columna j).
		D = el número de documentos (el número de columnas).
		D i = el número de documentos en los que la palabra i aparece (el número de columnas que no son cero en la fila i).
		En esta fórmula, las palabras que se concentran en algunos documentos se enfatizan (por la N i, j / N *, j ratio) 
		y palabras que sólo aparecen en unos documentos también se destacaron (por el log (D / D i) plazo) .
		'''
		#Se calcula una funcion de pesos para la matriz A
		#Suma por columnas
		WordsPerDoc = sum(self.A, axis=0)        
		#Suma por filas
		DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		rows, cols = self.A.shape
		for i in range(rows):
			for j in range(cols):
				self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])
				
	def printA(self):
		print 'Here is the count matrix'
		print self.A
		
	def printSVD(self):
		print 'Here are the singular values'
		print self.S
		print 'Here are the first 3 columns of the U matrix'
		print -1*self.U[:, 0:3]
		print 'Here are the first 3 rows of the Vt matrix'
		print -1*self.Vt[0:3, :]
	
	def get_summary(self, lista):
		index = [0]
		tmp = set()
		tmp.add(0)
		col = sum(self.Vt,axis=0)
		k = len(self.Vt)
		for i in range(len(col)):
			col[i] = float(col[i]/k) #promedio

		for kk in range(int(len(self.Vt)*0.20)):
			indice = 0
			maxi = -1
			for i in range(len(col)):
				if col[i] > maxi:
					maxi = col[i]
					indice = i
			index.append(indice)
			col[indice] = -1

		#Version beta
		#for i in range(int(len(self.Vt)*0.32)): #Un resumen que tendra 30% del texto original
			#for j in rangel(len(self.Vt[i])):

			#Forma 1:
			#aux = where (self.Vt[i] == self.Vt[i].max())[0][0]
			#if aux not in tmp:
				#index.append(aux)
				#tmp.add(aux)
			
			#Forma 2:
			# aux = where(self.Vt[i] >= average(self.Vt[i]))[0][0]
			# if aux not in tmp:
			# 	index.append(aux)
			# 	tmp.add(aux)
			
		for s in range(len(index)):
			print lista[index[s]]
			
def split_content_to_sentences(text0):
		text = text0.replace('\n', '. ')
		return text.split('. ')

#Tokenizacion del texto
content = split_content_to_sentences(text)

mylsa = LSA(stopwords, ignorechars)

for t in content:
	mylsa.parse(t)
	
mylsa.build()
mylsa.calc()
mylsa.get_summary(content)
#mylsa.printA()
#mylsa.printSVD()
#text.close()

