#!/usr/bin/env python3
# coding: utf-8
# creado por: Antonio Russoniello

from pylatex import Document, simple_page_number, NoEscape, Command
from pylatex.utils import bold
import pylatex.config as cf
from os import listdir, remove, path
import shutil
from datetime import date
import PySimpleGUI as sg

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
	msg = ""	
	for n in notes:
		note = n.get("nota").lower()
		tmp = note.find(word.lower())
		if (tmp >= 0):
			note_split = note.split(word)
			word_count = len(note_split)
			mark_words = ''
			for w in range(0,word_count - 1):
				mark_words = mark_words + note_split[w] + '[' + word + ']'
			note = mark_words + note_split[word_count - 1]
			count += 1	
			print("\033[92m--------------------------------------")
			print("\033[94m" + str(count) + '.',"Libro:",n.get("titulo"), "\u279c", n.get("autor").upper())	
			print("\033[36m\u00ab", note,"\u00bb")
			msg = msg + str(count) + '. ' + n.get("titulo").upper() + ' -> ' + n.get("autor").upper() + ': ' + '\n"'  + note + '"\n\n'
	return msg

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
	doc.preamble.append(Command('author', 'Autores Varios'))
	doc.preamble.append(Command('date', str(date.today().day) + '-' + str(date.today().month) + '-' + str(date.today().year)))
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

# Define the window's contents
layout = [  [sg.Text("Palabra clave?")],
			[sg.Input(), sg.Button('Buscar')],
			[sg.Button('Autores'), sg.Button('Libros'), sg.Button('PDF')],
		]

# Create the window
window = sg.Window('Kindle Notes Explorer', layout)
												
while True:
	event, values = window.read()
	#window['input'].bind("<Return>", "_Enter")	

	if event == 'Autores':
		count = 0
		authors = authors_list()
		authors = list(authors)
		authors.sort()
		text = ""
		for a in authors:
			count += 1			
			print(count,a)
			text = text + str(count) + '. ' + a + '\n' 
		sg.PopupScrolled(text, size=(70,20), title='Autores')    
	
	elif event == 'Libros':
		count = 0
		books_l = books_list()
		books_l = list(books_l)
		books_l.sort()
		text = ""
		for b in books_l:
			count += 1
			print(count, b)
			text =  text + str(count) + '. ' + b + '\n' 
		sg.PopupScrolled(text, size=(100,20), title='Libros')

	elif event == 'Buscar':
		large = len(values)
		key_word = ''
		for w in range(large):
			key_word = key_word + values[w]
		if key_word != "":		
			text = show_notes_key_word(key_word)
			if text != '':			
				sg.PopupScrolled(text, size=(100,20), title=values[0])

	elif event == 'PDF':
		key_word = values[0]			
		text = get_notes_key_word(key_word)
		if (text !=''):
			print("creando archivo -> " + key_word + ".pdf")
			latex_out(key_word, text)
			res = path.isfile('./pdf_output/' + key_word + '.pdf')
			if res:
				remove('./pdf_output/' + key_word + '.pdf')					
			shutil.move(key_word + '.pdf','./pdf_output/')
			print('archivo pdf creado')									
		else:
			print("palabra no encontrada")
	

	if event in (sg.WIN_CLOSED, 'Cancel'):
		break		
		
window.close()