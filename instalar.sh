#!/bin/bash

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "Por favor, execute como root (sudo ./instalar.sh)"
    exit 1
fi

# Verifica se está no ambiente live do Arch
if [ ! -f /etc/arch-release ]; then
    echo "Este script deve ser executado no ambiente live do Arch Linux!"
    exit 1
fi

# Verifica conexão com a internet
if ! ping -c 1 archlinux.org &> /dev/null; then
    echo "Sem conexão com a internet. Por favor, configure sua conexão primeiro."
    exit 1
fi

# Atualiza o relógio do sistema
timedatectl set-ntp true

# Verifica se o Python e o archinstall estão instalados
if ! command -v python &> /dev/null || ! command -v archinstall &> /dev/null; then
    echo "Instalando dependências necessárias..."
    pacman -Sy --noconfirm python archinstall
fi

# Executa o script de instalação
echo "Iniciando a instalação do Arch Linux..."
python install_arch.py
