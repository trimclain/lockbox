.ONESHELL:
SHELL := /bin/bash
# Remove "Entering directory" messages
MAKEFLAGS += --no-print-directory

# has to be the first target
all: distrocheck
	@make software
	@# Create venv
	@if [[ ! -d ".venv" ]]; then \
		echo "Creating .venv..."; \
		$(CREATE_VENV); \
		echo "Done";\
	else \
		echo ".venv already exists"; \
	fi

HAS_APT := $(shell if command -v apt > /dev/null 2>&1; then echo true; fi)
HAS_PACMAN := $(shell if command -v pacman > /dev/null 2>&1; then echo true; fi)
SUPPORTED := $(or $(HAS_APT), $(HAS_PACMAN))
ifneq ($(SUPPORTED), true)
distrocheck:
	@echo "Your distro is not supported. Please refer to manual installation." && exit 1
else
distrocheck:
	@:
endif

ifeq ($(HAS_APT),true)
INSTALL_PIP := sudo apt install -y python3-pip
INSTALL_TK := sudo apt install -y python3-tk
# we mean else if here, but we always run distrocheck anyways
else
INSTALL_PIP := sudo pacman -S --noconfirm --needed python-pip
INSTALL_TK := sudo pacman -S --noconfirm --needed tk
endif

HAS_UV := $(shell if command -v uv > /dev/null 2>&1; then echo true; fi)
ifeq ($(HAS_UV),true)
	CREATE_VENV := uv venv
	INSTALL_REQS_VENV := uv pip install cryptography
else
	CREATE_VENV := python3 -m venv venv
	INSTALL_REQS_VENV := python3 -m pip install cryptography
endif

help: distrocheck
	@echo "Run 'make' to create the venv"
	@echo "Run 'make reqs' to install requirements"
	@echo "Run 'make install' install Lockbox"
	@echo "Run 'make uninstall' to uninstall Lockbox"

software: distrocheck
	@# Install pip
	@if [[ ! -f /usr/bin/pip3 ]]; then \
		echo "Installing python3-pip..."; \
		$(INSTALL_PIP)
	else \
		echo "pip3 is already installed"; \
	fi
	@# Install venv (on arch it comes with python)
	@if [[ "$(HAS_APT)" == "true" ]]; then \
		# if ! python3 -c "import venv" &>/dev/null; then
		if [[ ! -d /usr/lib/python$$(python3 -c "import platform; print(platform.python_version()[:-2])")/venv/ ]]; then \
			echo "Installing python3-venv..."; \
			sudo apt install -y python3-venv; \
		fi; \
	else \
		echo "venv is already installed"; \
	fi
	@# Install tkinter
	if ! python3 -c "import tkinter" &>/dev/null; then
		echo "Installing tkinter..."; \
		$(INSTALL_TK)
	else \
		echo "tkinter is already installed"; \
	fi

reqs: distrocheck
	@# Install requirements
	if ! python3 -c "import cryptography" &>/dev/null; then
		if [[ -n "$$VIRTUAL_ENV" ]]; then \
			echo "Installing cryptography module into venv..."; \
			$(INSTALL_REQS_VENV); \
			echo "Done"; \
		else \
			echo "Installing cryptography module..."; \
			if [[ "$(HAS_APT)" == "true" ]]; then \
				sudo apt install -y python3-cryptography; \
			elif [[ "$(HAS_PACMAN)" == "true" ]]; then \
				sudo pacman -S --noconfirm --needed python-cryptography; \
			fi; \
		fi; \
	else \
		echo "cryptography module is already installed"; \
	fi

install: distrocheck
	@make software
	@make reqs
	@echo "Installing Lockbox to ~/.local/bin..."
	@mkdir -p ~/.local/bin
	@rm -f ~/.local/bin/lockbox
	@echo -e "#!/usr/bin/env bash\npushd $$(pwd) > /dev/null && ./main.py && popd > /dev/null" > ~/.local/bin/lockbox
	@chmod +x ~/.local/bin/lockbox
	@echo "Lockbox was successfully installed"

uninstall: distrocheck
	@# Delete the executable in .local/bin
	@if [[ -f ~/.local/bin/lockbox ]]; then \
		echo "Uninstalling Lockbox from .local/bin..."; \
		rm -f ~/.local/bin/lockbox; \
		echo "Lockbox was successfully uninstalled"; \
	else \
		echo "Lockbox is already uninstalled"; \
	fi

.PHONY: all distrocheck help software reqs install uninstall
