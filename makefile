#------------------------------- /usr/bin/g++-7 -------------------------------#
#------------------------------- coding: utf-8 --------------------------------#
# Criado por: Jean Marcelo Mira Junior
# Versão: 1.0
# Criado em: 08/03/2021
# Sistema operacional: Linux - Ubuntu 20.04.1 LTS
# Objetivo: estabelecer um padrão de Makefile
#------------------------------------------------------------------------------#

all: packages run

packages:
	sudo apt-get update
	pip3 install spade
	sudo apt-get update
	sudo apt-get upgrade

run:
	python3 main.py

