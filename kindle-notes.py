#!/usr/bin/env python3
# coding: utf-8
# creado por: Antonio Russoniello

import sys
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, NoEscape, NewPage, Command
from pylatex.utils import bold
import pylatex.config as cf
from os import listdir, remove, path
import shutil

notes = []
file_name = "My Clippings.txt"

def file_read():
	f = open(file_name, mode='r')
	libro = True
	for l in f:
		if (libro):
			titulo = l.replace('\n', '').strip()
			t_char = titulo.find('(')			
			autor = titulo[t_char+1:-1]
			titulo = titulo[:t_char-1]
			titulo = titulo.replace('\ufeff','')

		else:
			if ( l[0:14] != '- Tu subrayado' and l[0:13] != '- Tu marcador' and l != '==========\n' and l != '\n'):
				l.replace('\ufeff', '')
				coleccion = {"titulo": titulo, "autor": autor, "nota": l.replace('\n', '').strip()}
				notes.append(coleccion)
		libro = False
		if (l == '==========\n'):
			libro = True

def show_entries():
	for n in notes:
		print("++++++++++++++++++++++++++++")
		print(n.get("titulo"),"--", n.get("autor"))	
		print(n.get("nota"))

def total_entries():
	print("total de entradas:",len(notes))

def find_notes_author(author):
	print("Buscar por Autor:",author.upper())
	count = 0
	for n in notes:
		tmp = n.get("autor").lower()
		tmp = tmp.find(author.lower())
		if (tmp >= 0):
			count += 1	
			print("\033[92m--------------------------------------")
			print("\033[94m" + str(count) + '.',"Libro:",n.get("titulo"), "\u279c", n.get("autor").upper())	
			print("\033[36m\u00ab", n.get("nota"),"\u00bb")

def find_notes_title(title):
	print("Buscar por palabra clave:",title.lower())
	count = 0
	for n in notes:
		tmp = n.get("titulo").lower()
		tmp = tmp.find(title.lower())
		if (tmp >= 0):
			count += 1	
			print("\033[92m--------------------------------------")
			print("\033[94m" + str(count) + '.',"Libro:",n.get("titulo"), "\u279c", n.get("autor").upper())	
			print("\033[36m\u00ab", n.get("nota"),"\u00bb")

def show_notes_key_word(word):
	print("Buscar por palabra clave:",word.lower())
	count = 0
	for n in notes:
		tmp = n.get("nota").lower()
		tmp = tmp.find(word.lower())
		if (tmp >= 0):
			count += 1	
			print("\033[92m--------------------------------------")
			print("\033[94m" + str(count) + '.',"Libro:",n.get("titulo"), "\u279c", n.get("autor").upper())	
			print("\033[36m\u00ab", n.get("nota"),"\u00bb")

def get_notes_key_word(word):
	print("Buscar por palabra clave:",word.lower())
	count = 0
	output_msg = ''	
	for n in notes:
		tmp = n.get("nota").lower()
		tmp = tmp.find(word.lower())
		if (tmp >= 0):
			count += 1
			output_msg += str(count) + '. ' + "\\underline{libro}: " + n.get("titulo") + " --> " + n.get("autor").upper() + "\n\r"
			output_msg += n.get("nota") + "\n\r"
	return output_msg

def latex_out(k_word, text):
    escape = False
    content_separator = "\n"
    cf.active = cf.Version1(indent=False)
    doc = Document()
    doc.preamble.append(Command('title', 'Palabra clave: ' + k_word))
    doc.preamble.append(Command('author', 'Autores varios'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(text))
    doc.generate_pdf(k_word, clean_tex=True)	        

def books_dict():
	unique = {}
	for n in notes:
		unique[n.get("titulo")] = n.get("autor")
	#print(unique)
	return unique

def books_list():
	unique = []
	for n in notes:
		unique.append(n.get("titulo") + " \u279c (" + n.get('autor') + ")")
	#print(unique)
	unique = set(unique)
	return unique

def authors_list():
	unique = []
	for n in notes:
		unique.append(n.get("autor"))
	#print(unique)
	unique = set(unique)
	return unique

#################################################################

file_read() # poblar diccionario con las notas del archivo kindle

if (len(sys.argv) == 1):
	print("solo indique un nombre de autor para la busqueda o bien:")
	print("-b <libro> para libro especifico")
	print("-n <palabra> para buscar notas por palabra clave")	
	print("-a para una lista de autores")		
	print("-l para una lista de libros")
	print("-p <palabra_clave> en Beta")	

else:
	if (sys.argv[1] == '-l'):
		count = 0
		books_l = books_list()
		books_l = list(books_l)
		books_l.sort()
		for b in books_l:
			count += 1
			print(count, b)

	elif (sys.argv[1] == '-a'):
		count = 0
		authors = authors_list()
		authors = list(authors)
		authors.sort()
		for a in authors:
			count += 1			
			print(count,a)		

	elif (sys.argv[1] == '-b'):
		book_key = sys.argv[2]
		find_notes_title(book_key)

	elif (sys.argv[1] == '-n'):
		key_word = sys.argv[2]
		show_notes_key_word(key_word)

	# crear archivo pdf para cada entrada con palabra clave
	elif (sys.argv[1] == '-p'):
		if len(sys.argv) == 3 and sys.argv[2] != '':
			key_word = sys.argv[2]			
			text = get_notes_key_word(key_word)
			if (text !=''):
				print("creando archivo -> " + key_word + ".pdf")
				latex_out(key_word, text)
				res = path.isfile('./pdf_output/' + key_word + '.pdf')
				if res:
					remove('./pdf_output/' + key_word + '.pdf')					
				shutil.move(key_word + '.pdf','./pdf_output/')										
			else:
				print("palabra no encontrada")
		else:
			print("indique palabra clave")

	elif sys.argv[1] == '-t': # funcíon en beta para probar busqueda de portadas
		author = sys.argv[2]
		book = sys.argv[3]
		print(listdir(calibre_path + author + '/' + book))

	else:
		author_key = sys.argv[1]
		find_notes_author(author_key)

