# Script de Instalação do Arch Linux

Este script automatiza a instalação do Arch Linux usando a biblioteca `archinstall`.

## Requisitos

- Ambiente live ISO do Arch Linux
- Conexão com a Internet
- Python 3.x
- Pacote `archinstall` (incluído nas ISOs recentes do Arch Linux)

## Como Usar

1. Inicialize no ambiente live do Arch Linux
2. Clone este repositório ou baixe o script
3. Execute o script com privilégios de root:
```bash
sudo python install_arch.py
```

## Funcionalidades

- Particionamento automático do disco
- Configuração de localização e fuso horário do sistema
- Criação de conta de usuário
- Instalação de pacotes básicos
- Configuração de rede

## Observação

Por favor, revise a configuração no script antes de executá-lo. Você pode querer modificar:
- Esquema de particionamento do disco
- Localização e fuso horário
- Nome de usuário e senha
- Seleção de pacotes

⚠️ **Aviso**: Este script irá formatar o disco selecionado. Certifique-se de fazer backup de dados importantes.
