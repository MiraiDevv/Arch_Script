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

# Verifica e instala as dependências necessárias
echo "Verificando dependências..."
DEPS=("python" "archinstall" "git")
DEPS_TO_INSTALL=()

for dep in "${DEPS[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        echo "- $dep não encontrado"
        DEPS_TO_INSTALL+=("$dep")
    else
        echo "- $dep já instalado"
    fi
done

if [ ${#DEPS_TO_INSTALL[@]} -gt 0 ]; then
    echo "Instalando dependências necessárias..."
    pacman -Sy --noconfirm "${DEPS_TO_INSTALL[@]}"
fi

# Verifica se o script já está presente
if [ ! -f "install_arch.py" ]; then
    echo "Baixando script de instalação..."
    if ! git clone https://github.com/seu-usuario/Arch_Script.git /tmp/arch_script; then
        echo "Erro ao clonar o repositório!"
        exit 1
    fi
    cp /tmp/arch_script/install_arch.py .
    rm -rf /tmp/arch_script
fi

# Executa o script de instalação
echo "Iniciando a instalação do Arch Linux..."
python install_arch.py
