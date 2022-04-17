import sys
from PyQt5 import uic, Qt, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog, QErrorMessage, QMessageBox, QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import os
import time
from datetime import datetime
from functools import partial
import pwinput
import json

class Model():

	# En esta parte se cargan todos los datos del archivo JSON con los ajustes del usuario

	def __init__(self):

		# El archivo (settings.json) debe estar siempre a la vista del usuario.

		with open("settings.json") as self.file:
			self.data = json.load(self.file)

	def ajustes_funcionales(self):

		rutas_automaticas = self.data["Functions"]["Routes"]["Automatic_routes"]
		one_file = self.data["Functions"]["Files"]["One_file"]
		nombre_desencriptado = self.data["Functions"]["Files"]["Decrypted_name"]
		nombre_encriptado = self.data["Functions"]["Files"]["Encrypted_name"]

		return one_file, nombre_desencriptado, nombre_encriptado, rutas_automaticas

	def ajustes_apariencia(self):

		grupo_tema = self.data["Appearance"]["Theme"]

		return grupo_tema

class View():

	def __init__(self):

		self.app = QApplication(sys.argv)
		self.encrypter = self.encryterGUI()
		self.encrypter.show()
		sys.exit(self.app.exec_())

	class encryterGUI(QMainWindow):

		def __init__(self):

			# Lo que hacen estas 2 variables es dividir los 2 tipos de rutas para automatizar todo
			self.filename_encriptar = os.path.expanduser('~')
			self.filename_desencriptar = os.path.expanduser('~')

			self.ruta_modelo = Controller.comprobar_tema()
			self.ruta_modelo = self.ruta_modelo[0]

			try:
				basePath = sys._MEIPASS
			except Exception:
				basePath = os.path.abspath(".")

			bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
			gui_ruta = os.path.join(bundle_dir, self.ruta_modelo)

			# INIT
			super().__init__()

			uic.loadUi(gui_ruta, self)

			self.label_copynombre = self.label_copynombre
			self.label_copycodigo = self.label_copycodigo
			self.label_copyfecha = self.label_copyfecha
			self.label_copyruta = self.label_copyruta

			self.label_copynombre_2 = self.label_copynombre_2
			self.label_copycodigo_2 = self.label_copycodigo_2
			self.label_copyfecha_2 = self.label_copyfecha_2
			self.label_copyruta_2 = self.label_copyruta_2

			self.definir_eventos()

		def definir_eventos(self):

			self.label_ruta.setText(self.filename_encriptar)
			self.label_ruta_2.setText(self.filename_desencriptar)

			self.boton_buscar.clicked.connect(partial(self.boton_buscar_funcion, 1))
			self.boton_buscar_2.clicked.connect(partial(self.boton_buscar_funcion, 2))
			self.boton_encriptar.clicked.connect(self.boton_encriptar_funcion)
			self.boton_desencriptar.clicked.connect(self.boton_desencriptar_funcion)
			self.boton_ajustes.clicked.connect(self.boton_ajustes_funcion)

		def boton_buscar_funcion(self, tipo):

			if tipo == 1:

				self.filename_encriptar = QFileDialog.getOpenFileName(self, 'Abrir Archivo','C:\\',"Archivos de texto (*.txt *.py *.js)")
				self.filename_encriptar = self.filename_encriptar[0]

				if self.filename_encriptar == "":

					self.filename_encriptar = os.path.expanduser('~')
					self.label_ruta.setText(self.filename_encriptar)

				else:

					self.label_ruta.setText(self.filename_encriptar)

			if tipo == 2:

				self.filename_desencriptar = QFileDialog.getOpenFileName(self, 'Abrir Archivo','C:\\',"Archivos de texto (*.txt *.py *.js)")
				self.filename_desencriptar = self.filename_desencriptar[0]

				if self.filename_desencriptar == "":

					self.filename_desencriptar = os.path.expanduser('~')
					self.label_ruta_2.setText(self.filename_desencriptar)

				else:

					self.label_ruta_2.setText(self.filename_desencriptar)

		def boton_encriptar_funcion(self):

			if self.filename_encriptar == os.path.expanduser('~'):

				self.ejecutar_dialogo("ERROR (104-1)", "Ruta erronea o incompleta.")

			else:

				self.controlador = Controller.encrypterFunctions(self, self.filename_encriptar)
				
				modo = "encriptar"
				self.controlador.iniciador(modo, "none")

				# Si la opcion de rutas automaticas esta en True
				
				self.filename_desencriptar = str(self.label_ruta_2.text())

		def boton_desencriptar_funcion(self):

			if self.filename_desencriptar == os.path.expanduser('~'):

				self.ejecutar_dialogo("ERROR (104-2)", "Ruta erronea o incompleta.")

			else:

				self.controlador = Controller.encrypterFunctions(self, self.filename_desencriptar)

				modo = "desencriptar"
				self.controlador.iniciador(modo, self.label_codigo.text())

		def boton_ajustes_funcion(self):

			ventana_ajustes = View.settingsGUI()
			ventana_ajustes = ventana_ajustes.exec_()

		def ejecutar_dialogo(self, titulo, texto):

			ventana_dialogo = View.dialogGUI(titulo, texto)
			ventana_dialogo = ventana_dialogo.exec_()

	class settingsGUI(QDialog):

		# Esta clase es la que representa al Ventana de tipo dialogo de ajustes.
		# Es un dialogo debido a que no se puede cerrar la ventna del fondo mientra este activo el dialogo.

		def __init__(self):

			self.ruta_modelo = Controller.comprobar_tema()
			self.ruta_modelo = self.ruta_modelo[1]

			try:
				basePath = sys._MEIPASS
			except Exception:
				basePath = os.path.abspath(".")

			bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
			gui_ruta = os.path.join(bundle_dir, self.ruta_modelo)

			super().__init__()

			uic.loadUi(gui_ruta, self)
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

			self.definir_eventos()

		def definir_eventos(self):

			self.controlador = Controller.settingsFunctions(self)
			self.controlador.organizar_contenido()

			# En este punto se declaran los eventos que se ejecutaran al iniciar la ventana.

			# Menu de funciones
			self.boton_revertir.clicked.connect(self.boton_revertir_funcion)
			self.boton_guardar.clicked.connect(self.boton_guardar_funcion)
			self.boton_revertir_2.clicked.connect(self.boton_revertir_funcion)
			self.boton_guardar_2.clicked.connect(self.boton_guardar_funcion)
			self.boton_reiniciar.clicked.connect(self.boton_reiniciar_funcion)
			self.boton_reiniciar_2.clicked.connect(self.boton_reiniciar_funcion)

			# Menu de apariencia
			self.opcion_oscuro.stateChanged.connect(self.deseleccionar_funcion)
			self.opcion_claro.stateChanged.connect(self.deseleccionar_funcion)
			self.opcion_normal.stateChanged.connect(self.deseleccionar_funcion)

		def boton_reiniciar_funcion(self):

			self.controlador = Controller.settingsFunctions(self)
			self.controlador.reiniciar_configuraciones()

		def boton_guardar_funcion(self):

			# Al presionar el boton guardar

			self.controlador = Controller.settingsFunctions(self)
			self.controlador.guardar_configuraciones()

		def boton_revertir_funcion(self):

			self.controlador = Controller.settingsFunctions(self)
			self.controlador.organizar_contenido()

		def deseleccionar_funcion(self, state):

			# Esta funcion sirve para que solo se pueda seleccionar una sola opcion

			# Si el estado es checked
			if state == Qt.Checked:

				# Si la opcion_oscuro es checked
				if self.sender() == self.opcion_oscuro:

					self.opcion_claro.setChecked(False)
					self.opcion_normal.setChecked(False)

				# Si la opcion_claro es checked
				elif self.sender() == self.opcion_claro:

					self.opcion_oscuro.setChecked(False)
					self.opcion_normal.setChecked(False)

				# Si la opcion_normal es checked
				elif self.sender() == self.opcion_normal:

					self.opcion_oscuro.setChecked(False)
					self.opcion_claro.setChecked(False)

		def ejecutar_dialogo(self, titulo, texto):

			ventana_dialogo = View.dialogGUI(titulo, texto)
			ventana_dialogo = ventana_dialogo.exec_()

	class dialogGUI(QDialog):

		def __init__(self, titulo, texto):

			self.tema = Controller.comprobar_tema()
			self.tema = self.tema[2]

			self.titulo = titulo
			self.texto = texto

			try:
				basePath = sys._MEIPASS
			except Exception:
				basePath = os.path.abspath(".")

			bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
			gui_ruta = os.path.join(bundle_dir, "ui_models/qtdialog.ui")

			super().__init__()

			uic.loadUi(gui_ruta, self)
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

			self.setWindowTitle(self.titulo)
			
			self.label_texto.setText(self.texto)
			self.boton_cerrar.clicked.connect(self.cerrar_ventana)

			self.organizar_contenido()

		def organizar_contenido(self):

			# En esta funcion se le da un color al texto dependiendo del fondo o tema.

			if self.tema == "oscuro":
				self.setStyleSheet("background-color: #000000;")
				self.label_texto.setStyleSheet("color: #f5f5f5;")
			if self.tema == "claro":
				self.setStyleSheet("background-color: #f5f5f5;")
				self.label_texto.setStyleSheet("color: #000000;")
			if self.tema == "normal":
				self.label_texto.setStyleSheet("color: #000000;")

		def cerrar_ventana(self):

			self.close()

class Controller():

	def __init__(self):

		model_class = Model()

		view_class = View()

	def comprobar_tema():

		# Hice una funcion global ya que el tema afecta a todas las ventanas.

		# En esta funcion se llaman a las funciones de la clase Model para llamar a las variables de (settings.json)
		model_class = Model()
		ajustes_funcionales = model_class.ajustes_funcionales()
		ajustes_apariencia = model_class.ajustes_apariencia()

		# Todas las variables de los ajustes tomadas del JSON (settings.json)
		grupo_tema = ajustes_apariencia

		ruta_main = ""
		ruta_ajustes = ""
		ruta_dialogos = ""

		if grupo_tema == 0:

			# Tema oscuro
			ruta_main = "ui_models/qtmain_dark.ui"
			ruta_ajustes = "ui_models/qtsettings_dark.ui"
			ruta_dialogos = "oscuro"

		if grupo_tema == 1:

			# Tema claro
			ruta_main = "ui_models/qtmain_light.ui"
			ruta_ajustes = "ui_models/qtsettings_light.ui"
			ruta_dialogos = "claro"

		if grupo_tema == 2:

			# Tema normal
			ruta_main = "ui_models/qtmain.ui"
			ruta_ajustes = "ui_models/qtsettings.ui"
			ruta_dialogos = "normal"

		return ruta_main, ruta_ajustes, ruta_dialogos

	class encrypterFunctions():

		def __init__(self, view, filename):

			self.variables_ajustes()

			# Se le pasa self.view para asi poder cambiar los labels de la parte visual
			self.view = view

			self.timenow = time.strftime("%p")
			self.now = datetime.now()

			self.diccionario_generado, self.lista_generada = self.letras_cifradas()

			self.lista_espaciada = ""

			for x in self.lista_generada:

				self.lista_espaciada = self.lista_espaciada + f"{x} "

			# Cabeceras constantes de los archivos encriptados o desencriptados
			self.texto = f"#ARCHIVO ENCRIPTADO / {self.now} {self.timenow}\n{self.lista_espaciada}\n\n"
			self.texto_desencriptado = f"#ARCHIVO DESENCRIPTADO / {self.now} {self.timenow}\n\n"

			"""
			En este punto no importa si se llama a las 2 variables de ruta debido a que siempre se va a
			ejecutar un proceso a la vez (encriptar o desencriptar) y esa variable self.filname cambia
			segun el proceso que se le indico al presionar el boton.
			"""

			self.filename = filename

		def iniciador(self, modo, lista):

			def comprobador():

				if modo == "encriptar" or modo == "desencriptar" or modo == "1" or modo == "2":

					if modo == "encriptar" or modo == "1":

						modo_encriptar()

					if modo == "desencriptar" or modo == "2":

						try:

							self.lista2 = lista.split()

							for i in range(len(self.lista2)):

								self.lista2[i] = int(self.lista2[i])

							modo_desencriptar(self.lista2)

						except:

							modo_desencriptar("none")
				else:

					self.view.ejecutar_dialogo("Error (101)", "Modo erroneo.")
					comprobador()

			def modo_encriptar():

				def agregando_texto():

					cantidad_letras = 0
					porcentaje_por_letra = 0
					subida_actual = 0

					# Zona de la Progress bar
					with open(f"{self.filename}", encoding = "utf-8") as f:

						# Esta parte es para el funcionamiento de la Progress Bar
						# Primero se lee la cantidad de letras que hay
						for line in f:
							for letter in line:
								cantidad_letras += 1

						# Si hay letras entonces se divide 100 entre la cantida de letras
						# Este porcentaje sera la cantidad que subira la prgress bar con cada letra
						if cantidad_letras != 0:

							porcentaje_por_letra = 100/cantidad_letras
							subida_actual = porcentaje_por_letra

							while int(subida_actual) != 101:

								self.view.progress_1.setValue(int(subida_actual))
								subida_actual += porcentaje_por_letra

					# Zona de encriptamiento
					with open(f"{self.filename}", encoding = "utf-8") as f:

						while True:

							c = f.read(1)

							if not c:

								self.view.ejecutar_dialogo("Aviso", "Encriptacion terminada.")
								self.view.progress_1.setValue(0)
								break

							letra_añadir = self.codificador_letra(c, self.diccionario_generado)
							self.texto += letra_añadir

				# Configuracion de la opcion ONE FILE (CHECKED = 1)
				if self.one_file == 0:

					# En este punto se pasa a configurar el nombre para solo dejar el encriptado
					nombre_con_extension = os.path.basename(self.filename)
					nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]
					solo_extension = os.path.splitext(nombre_con_extension)[1]
					
					nombre_sin_extension = nombre_sin_extension.replace(f"-{self.nombre_encriptado}", "")
					nombre_archivo_completo = f"{nombre_sin_extension}-{self.nombre_encriptado}{solo_extension}"
						
					archivo_con_ruta = self.filename.replace(nombre_con_extension, "")
					archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo

					# Este ciclo sirve para verificar si hay archivos con el mismo nombre existentes y le añade un numero si lo hay
					i = 0
					while os.path.exists(archivo_con_ruta):

						i+=1
						self.texto = f"#ARCHIVO ENCRIPTADO / {self.now} {self.timenow}\n{self.lista_espaciada}\n\n"
						nombre_archivo_completo = f"{nombre_sin_extension}-{self.nombre_encriptado}({i}){solo_extension}"
						archivo_con_ruta = self.filename.replace(nombre_con_extension, "") # Se deja solo la ruta del archivo
						archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo # Se une la ruta con el nombre arreglado

					else:
						self.texto = f"#ARCHIVO ENCRIPTADO / {self.now} {self.timenow}\n{self.lista_espaciada}\n\n"

					agregando_texto()

					file = open(archivo_con_ruta, "w")
					file.write(self.texto + os.linesep)
					file.close()

					if self.rutas_automaticas == 1:

						self.view.label_ruta_2.setText(archivo_con_ruta)

					self.view.label_copynombre.setText(nombre_archivo_completo)
					self.view.label_copycodigo.setText(self.lista_espaciada)
					self.view.label_copyfecha.setText(f"{self.now} - {self.timenow}")
					self.view.label_copyruta.setText(archivo_con_ruta)

				if self.one_file == 1:

					# En este punto se pasa a configurar el nombre para solo dejar el encriptado
					nombre_con_extension = os.path.basename(self.filename)
					nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]
					solo_extension = os.path.splitext(nombre_con_extension)[1]

					nombre_archivo_completo = f"{nombre_sin_extension}{solo_extension}"

					archivo_con_ruta = self.filename.replace(nombre_con_extension, "")
					archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo

					agregando_texto()

					file = open(archivo_con_ruta, "w")
					file.write(self.texto + os.linesep)
					file.close()

					if self.rutas_automaticas == 1:

						self.view.label_ruta_2.setText(archivo_con_ruta)

					self.view.label_copynombre.setText(nombre_archivo_completo)
					self.view.label_copycodigo.setText(self.lista_espaciada)
					self.view.label_copyfecha.setText(f"{self.now} - {self.timenow}")
					self.view.label_copyruta.setText(archivo_con_ruta)

				# Si el archivo json no se puede guardar en el .exe se debe hacer un error por si no se puede leer un dato. (EXE)

			def modo_desencriptar(lista_ordenador):

				def agregando_letras_desencriptadas(lista_ordenador):

					self.diccionario = ""

					# Variables para el diccionario
					contador = 0
					linea_lista = ""
					segunda_linea = ""

					# Variables para la progress bar
					cantidad_letras = 0
					porcentaje_por_letra = 0
					subida_actual = 0

					# Zona de la Progress bar
					with open(f"{self.filename}", encoding = "utf-8") as f:

						# Esta parte es para el funcionamiento de la Progress Bar
						# Primero se lee la cantidad de letras que hay
						for line in f:
							for letter in line:
								cantidad_letras += 1

						# Si hay letras entonces se divide 100 entre la cantida de letras
						# Este porcentaje sera la cantidad que subira la prgress bar con cada letra
						if cantidad_letras != 0:

							porcentaje_por_letra = 100/cantidad_letras
							subida_actual = porcentaje_por_letra

							while int(subida_actual) != 101:

								self.view.progress_2.setValue(int(subida_actual))
								subida_actual += porcentaje_por_letra

					with open(f"{self.filename}") as file:
								
						try:
							segunda_linea = file.readlines()[1]
						except:
							segunda_linea = "None"

						with open(f"{self.filename}") as f:

							# Desencriptar archivo
							while True:

								try:

									# C = Letra
									c = f.read(1)

									if c != "":
										contador+=1

									if not c:
											
										if contador == 0:

											self.view.ejecutar_dialogo("Aviso", "Archivo vacio.")
											break

										else:
											
											self.view.ejecutar_dialogo("Aviso", "Desencriptacion terminada.")
											self.view.progress_2.setValue(0)
											break

									# En este punto se evalua si la lista esta vacia para asi agarrar la segunda linea del archivo automaticamente
									if lista_ordenador == "none" or lista_ordenador == []:

										linea_lista = segunda_linea

										try:

											lista_total = linea_lista.split()

											for i in range(len(lista_total)):

												lista_total[i] = int(lista_total[i])

											lista_ordenador = lista_total

											self.diccionario = self.creador_diccionario_para_decifrar(lista_ordenador)

										# Si ningun proceso funciona el codigo sera incorrecto.
										except Exception as e:

											self.view.ejecutar_dialogo("Error (102-1)", "Codigo incorrecto.")
											break
									# Significa que el usuario si ingreso la lista o codigo.
									else:

										self.diccionario = self.creador_diccionario_para_decifrar(lista_ordenador)
								except:

									self.view.ejecutar_dialogo("Error (102-2)", "Codigo incorrecto.")
									break

								if self.diccionario == {}:

									self.view.ejecutar_dialogo("Error (102-3)", "Codigo incorrecto.")
									break

								letra_añadir = self.codificador_letra(c, self.diccionario)
								self.texto_desencriptado += letra_añadir

				if self.one_file == 0:

					# En este punto se pasa a dividir el nombre del archivo para dejar el desencriptado
					nombre_con_extension = os.path.basename(self.filename)
					nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]
					solo_extension = os.path.splitext(nombre_con_extension)[1]

					nombre_sin_extension = nombre_sin_extension.replace(f"-{self.nombre_encriptado}", "")

					archivo_con_ruta = self.filename.replace(nombre_con_extension, "")

					# Para saber la cantidad de archivos que hay para luego reemplazar el numero en el nombre.
					contador_cantidad = 1
					for filename in os.listdir(archivo_con_ruta):

						file = os.path.join(archivo_con_ruta, filename)
						
						# Si filename es un archivo
						if os.path.isfile(file):

							if self.nombre_encriptado in filename:
								contador_cantidad += 1

					nombre_sin_extension = nombre_sin_extension.replace(f"({contador_cantidad-2})", "") # Error por cada numero solo se esta quitando el 1

					nombre_archivo_completo = f"{nombre_sin_extension}-{self.nombre_desencriptado}{solo_extension}"

					archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo

					# Este ciclo sirve para verificar si hay archivos con el mismo nombre existentes y le añade un numero si lo hay
					i = 0
					while os.path.exists(archivo_con_ruta):
						i+=1
						self.texto_desencriptado = f"#ARCHIVO DESENCRIPTADO / {self.now} {self.timenow}\n\n"
						nombre_archivo_completo = f"{nombre_sin_extension}-{self.nombre_desencriptado}({i}){solo_extension}"
						archivo_con_ruta = self.filename.replace(nombre_con_extension, "")
						archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo

					else:
						self.texto_desencriptado = f"#ARCHIVO DESENCRIPTADO / {self.now} {self.timenow}\n\n"

					agregando_letras_desencriptadas(lista_ordenador)

					file = open(archivo_con_ruta, "w")
					file.write(self.texto_desencriptado + os.linesep)
					file.close()

					self.view.label_copynombre_2.setText(nombre_archivo_completo)
					self.view.label_copycodigo_2.setText(self.lista_espaciada)
					self.view.label_copyfecha_2.setText(f"{self.now} - {self.timenow}")
					self.view.label_copyruta_2.setText(archivo_con_ruta)

				if self.one_file == 1:

					# En este punto se pasa a configurar el nombre para solo dejar el encriptado
					nombre_con_extension = os.path.basename(self.filename)
					nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]
					solo_extension = os.path.splitext(nombre_con_extension)[1]

					nombre_archivo_completo = f"{nombre_sin_extension}{solo_extension}"

					archivo_con_ruta = self.filename.replace(nombre_con_extension, "")
					archivo_con_ruta = archivo_con_ruta + nombre_archivo_completo

					agregando_letras_desencriptadas(lista_ordenador)

					file = open(archivo_con_ruta, "w")
					file.write(self.texto_desencriptado + os.linesep)
					file.close()

					self.view.label_copynombre_2.setText(nombre_archivo_completo)
					self.view.label_copycodigo_2.setText(self.lista_espaciada)
					self.view.label_copyfecha_2.setText(f"{self.now} - {self.timenow}")
					self.view.label_copyruta_2.setText(archivo_con_ruta)

				# Si el archivo json no se puede guardar en el .exe se debe hacer un error por si no se puede leer un dato. (EXE)

			comprobador()

		def letras_cifradas(self):

			import random
			from random import randrange

			primera_lista = ["a", "á", "b", "c", "d", "e", "é", "f", "g", "h", "i", "í", "j", "k", "l", "m", "n", "ñ", "o", "ó", "p", "q", "r", "s", "t", "u", "ú", "ü", "v", "w", "x", "y", "z"]
			diccionario_letras = {"a": "", "á": "", "b": "", "c": "", "d": "", "e": "", "é": "", "f": "", "g": "", "h": "", "i": "", "í": "", "j": "", "k": "", "l": "", "m": "", "n": "", "ñ": "", "o": "", "ó": "", "p": "", "q": "", "r": "", "s": "", "t": "", "u": "", "ú": "", "ü": "", "v": "", "w": "", "x": "", "y": "", "z": ""}

			letras_abecedario = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32] # Incluidas las tildes

			lista_orden = []
			lista_usados = []

			def organizador():

				numero_posicion = random.choice(letras_abecedario)

				if numero_posicion in lista_usados:

					organizador()

				else:

					lista_usados.append(numero_posicion)

					letra_escogida = primera_lista[numero_posicion]

					lista_orden.append(numero_posicion)

					diccionario_letras[letra] = letra_escogida

				return diccionario_letras, lista_orden

			for letra in diccionario_letras:

				respuesta = organizador()

			return respuesta[0], respuesta[1]

		def codificador_letra(self, letra, diccionario):

			comprobacion_letra = letra.isalpha()

			letra_final = letra

			if comprobacion_letra == True:

				comprobador_mayuscula = letra.isupper()

				letra_minuscula = letra.lower()

				letra_encontrada = diccionario[letra_minuscula]

				if comprobador_mayuscula == True:

					letra_final = letra_encontrada.upper()

				else:

					letra_final = letra_encontrada

			else:

				letra_final = letra

			return letra_final

		def creador_diccionario_para_decifrar(self, lista):

			primera_lista = ["a", "á", "b", "c", "d", "e", "é", "f", "g", "h", "i", "í", "j", "k", "l", "m", "n", "ñ", "o", "ó", "p", "q", "r", "s", "t", "u", "ú", "ü", "v", "w", "x", "y", "z"]

			lista_prueba = lista

			diccionario_inicial = {}

			posicion_primera_lista = 0

			for numero in lista_prueba:

				letra_encontrada = primera_lista[numero]

				diccionario_inicial[f"{letra_encontrada}"] = ""

			for elemento in diccionario_inicial:

				diccionario_inicial[elemento] = primera_lista[posicion_primera_lista]

				posicion_primera_lista += 1

			return diccionario_inicial

		def variables_ajustes(self):

			# En esta funcion se llaman a las funciones de la clase Model para llamar a las variables de (settings.json)
			model_class = Model()
			ajustes_funcionales = model_class.ajustes_funcionales()
			ajustes_apariencia = model_class.ajustes_apariencia()

			# Todas las variables de los ajustes tomadas del JSON (settings.json)
			self.one_file = ajustes_funcionales[0]
			self.nombre_desencriptado = ajustes_funcionales[1]
			self.nombre_encriptado = ajustes_funcionales[2]
			self.rutas_automaticas = ajustes_funcionales[3]
			self.grupo_tema = ajustes_apariencia

	class settingsFunctions():

		def __init__(self, view):

			self.view = view

			try:
				basePath = sys._MEIPASS
			except Exception:
				basePath = os.path.abspath(".")

			self.bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
			self.json_ruta = os.path.join(self.bundle_dir, "settings.json")

		def guardar_configuraciones(self):

			# 0 = False / 1 = True
			# Opcion_tema = 2 / 2 = tema normal

			one_file = 0
			nombre_desencriptado = self.view.nombre_desencriptado.text()
			nombre_encriptado = self.view.nombre_encriptado.text()
			rutas_automaticas = 1
			opcion_tema = 2

			if self.view.one_file.isChecked():
				one_file = 1

			if self.view.rutas_automaticas.isChecked():
				rutas_automaticas = 1
			else:
				rutas_automaticas = 0

			# Ver el tema que ingreso el usuario
			if self.view.opcion_oscuro.isChecked():
				opcion_tema = 0
			if self.view.opcion_claro.isChecked():
				opcion_tema = 1
			if self.view.opcion_normal.isChecked():
				opcion_tema = 2

			# Simbolos que un archivo no puede recibir como nombre. (HILO)
			simbolos_erroneos = ['/', ':', '*', '?', '"', '<', '>', '|', '!', '@', '#', '$', '%', '&']
			errores_simbologia = 0

			# Se comprueba si uno de esos simbolos esta en la variable.
			for simbolo in simbolos_erroneos:
				if errores_simbologia == 0:
					if simbolo in nombre_desencriptado:
						errores_simbologia = 1
						self.view.ejecutar_dialogo("Error (103-1)", f"El nombre no puede tener: ( {simbolo} )")
						self.organizar_contenido()
					if simbolo in nombre_encriptado:
						errores_simbologia = 1
						self.view.ejecutar_dialogo("Error (103-2)", f"El nombre no puede tener: ( {simbolo} )")
						self.organizar_contenido()

			if errores_simbologia == 0:

				# Si el nombre no tiene alguno de esos simbolos se guardaran los cambios.
				document_json = {"Functions": {"Files": {"One_file": int(one_file), "Decrypted_name": str(nombre_desencriptado), "Encrypted_name": str(nombre_encriptado)}, "Routes": {"Automatic_routes": int(rutas_automaticas)}}, "Appearance": { "Theme": int(opcion_tema)}}

				# Lo que se hace aqui es guardar todos los cambios de las configuraciones.
				with open(self.json_ruta, 'w') as file:
					json.dump(document_json, file, indent = 4)

				self.view.ejecutar_dialogo("Aviso", "Cambios guardados correctamente.")

		def reiniciar_configuraciones(self):

			# Al presionar el boton reiniciar
			document_json = {"Functions": {"Files": {"One_file": 0,"Decrypted_name": "(desencriptado)","Encrypted_name": "(encriptado)"},"Routes": {"Automatic_routes": 1}},"Appearance": {"Theme": 2}}

			# Lo que se hace aqui es revertir todos los cambios del archivo (settings.json) para dejarlo como al principio.
			with open(self.json_ruta, 'w') as file:
				json.dump(document_json, file, indent = 4)

			# Se reconfigura el apartado grafico (labels, checkbox y demas).
			self.view.one_file.setChecked(False)
			self.view.nombre_desencriptado.setText("(desencriptado)")
			self.view.nombre_encriptado.setText("(encriptado)")
			self.view.opcion_oscuro.setChecked(False)
			self.view.opcion_claro.setChecked(False)
			self.view.opcion_normal.setChecked(True)
			self.view.rutas_automaticas.setChecked(True)

			self.view.ejecutar_dialogo("Aviso", "Cambios guardados correctamente.")

		def organizar_contenido(self):

			# En esta funcion se busca organizar automaticamente el contenido de la ventana ajustes

			# En esta funcion se llaman a las funciones de la clase Model para llamar a las variables de (settings.json)
			model_class = Model()
			ajustes_funcionales = model_class.ajustes_funcionales()
			ajustes_apariencia = model_class.ajustes_apariencia()

			# Todas las variables de los ajustes tomadas del JSON (settings.json)
			self.one_file = ajustes_funcionales[0]
			self.nombre_desencriptado = ajustes_funcionales[1]
			self.nombre_encriptado = ajustes_funcionales[2]
			self.rutas_automaticas = ajustes_funcionales[3]
			self.grupo_tema = ajustes_apariencia

			opcion_0 = False
			opcion_1 = False
			opcion_2 = False

			# Procesamiento de variables

			# Opcion de One File
			if self.one_file == 1:
				self.one_file = True
			else:
				self.one_file = False

			# Rutas automaticas
			if self.rutas_automaticas == 1:
				self.rutas_automaticas = True
			else:
				self.rutas_automaticas = False

			# Opciones de Tema
			if self.grupo_tema == 0:
				opcion_0 = True
				opcion_1 = False
				opcion_2 = False
			elif self.grupo_tema == 1:
				opcion_0 = False
				opcion_1 = True
				opcion_2 = False
			elif self.grupo_tema == 2:
				opcion_0 = False
				opcion_1 = False
				opcion_2 = True

			self.view.one_file.setChecked(self.one_file)
			self.view.nombre_desencriptado.setText(str(self.nombre_desencriptado))
			self.view.nombre_encriptado.setText(str(self.nombre_encriptado))
			self.view.opcion_oscuro.setChecked(opcion_0)
			self.view.opcion_claro.setChecked(opcion_1)
			self.view.opcion_normal.setChecked(opcion_2)
			self.view.rutas_automaticas.setChecked(self.rutas_automaticas)

if __name__ == '__main__':
	controller = Controller()

"""
v1.1

CAMBIOS (v1.1.0):

- Modelo MVC.
- Menu de ajustes.
- Rutas automaticas.
- Cambios de apariencia.
- Archivos automaticos.

CAMBIOS (v1.1.1):

- Barras de progreso.
- Solucion de error al encriptar letras con acentos.

ERRORES:

- ERROR (100): Errores de funcionamiento:

	- Error (101): Errores de modo
	- Error (102): Errores de codigo de desencriptacion
	- Error (103): Errores de nombre de archivo
	- Error (104): Errores de ruta 

- ERROR (200): Errores de apariencia:

	- Error (201): Error de apariencia no leida
"""