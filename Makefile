SHELL := /bin/bash

OS := $(shell awk -F= '$$1=="ID" { print $$2 ;}' /etc/os-release)

ifeq ($(OS), ubuntu)
	INSTALL = sudo apt install -y
	INSTALL_PIP = $(INSTALL) python3-pip
	INSTALL_VENV = $(INSTALL) python3-venv
	INSTALL_TK = $(INSTALL) python3-tk
else
	INSTALL = sudo pacman -S --noconfirm --needed
	INSTALL_PIP = $(INSTALL) python-pip
	# venv comes installed with python on arch
	INSTALL_VENV = $(INSTALL) python
	INSTALL_TK = $(INSTALL) tk
endif

all: software
	@# Create venv
	@if [[ ! -d "venv" ]]; then echo "Creating venv..." && python3 -m venv venv && echo "Done";\
		else echo "venv already exists"; fi

help: ## Print this help menu
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

software: ## Install necessary software
	@# Install pip and venv
	@if [[ ! -f /usr/bin/pip3 ]]; then echo "Installing python3-pip..." && $(INSTALL_PIP);\
		else echo "pip3 is already installed"; fi
	@if [[ ! -d /usr/lib/python$$(python3 -c "import platform; print(platform.python_version()[:-2])")/venv/ ]];\
		then echo "Installing python3-venv..." && $(INSTALL_VENV);\
		else echo "venv is already installed"; fi
	@# Install tkinter
	@if [[ ! -d /usr/lib/python$$(python3 -c "import platform; print(platform.python_version()[:-2])")/tkinter/ ]];\
		then echo "Installing Tkinter..." && $(INSTALL_TK);\
		else echo "tkinter is already installed"; fi

reqs: ## Install requirements
	@# Install required modules
	@echo "Installing requirements..."
	@# pip install cryptography
	@pip install -r requirements.txt
	@echo "Done"

.PHONY: all help software reqs install uninstall
