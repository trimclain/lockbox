SHELL := /bin/bash

OS := $(shell awk -F= '$$1=="ID" { print $$2 ;}' /etc/os-release)

ifeq ($(OS), ubuntu)
	INSTALL_PIP = sudo apt install -y python3-pip
	INSTALL_VENV = sudo apt install -y python3-venv
else
	INSTALL_PIP = sudo pacman -S --noconfirm --needed python-pip
	# venv comes installed with python on arch
	INSTALL_VENV = sudo pacman -S --noconfirm --needed python
endif

all:
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

reqs: ## Install requirements
	@# Install required modules
	@echo "Installing requirements..."
	@pip install -r requirements.txt
	@echo "Done"

.PHONY: all help software reqs install uninstall
