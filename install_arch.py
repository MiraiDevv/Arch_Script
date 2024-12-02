#!/usr/bin/env python3
import archinstall
import json
import sys
import os

def main():
    # Check if running as root
    if os.geteuid() != 0:
        print("Este script deve ser executado como root!")
        sys.exit(1)

    # Basic configuration
    config = {
        "keyboard-layout": "br-abnt2",  # Brazilian ABNT2 keyboard layout
        "mirror-region": ["Brazil", "United States", "Worldwide"],  # Multiple mirror regions
        "locale": "pt_BR",
        "encoding": "UTF-8",
        "timezone": "America/Sao_Paulo",
        "ntp": True,
    }

    # Mirror configuration
    mirrors = {
        "Brazil": {
            "https://mirror.ufscar.br/archlinux/$repo/os/$arch": True,
            "https://archlinux.c3sl.ufpr.br/$repo/os/$arch": True,
        },
        "United States": {
            "https://mirrors.mit.edu/archlinux/$repo/os/$arch": True,
            "https://mirrors.kernel.org/archlinux/$repo/os/$arch": True,
        },
        "Worldwide": {
            "https://mirror.rackspace.com/archlinux/$repo/os/$arch": True,
            "https://archlinux.uk.mirror.allworldit.com/archlinux/$repo/os/$arch": True,
        }
    }

    # Disk configuration
    disk_layouts = {
        "ssd": {  # For the 256GB SSD
            "config_type": "default",
            "partitions": [
                {
                    "mountpoint": "/boot",
                    "size": "512MiB",
                    "filesystem": "fat32",
                    "bootable": True
                },
                {
                    "mountpoint": "/",
                    "size": "50GiB",  # Root partition
                    "filesystem": "ext4"
                },
                {
                    "mountpoint": "/var",
                    "size": "30GiB",  # Logs and variable data
                    "filesystem": "ext4"
                },
                {
                    "mountpoint": "swap",
                    "size": "16GiB",  # Swap space
                    "filesystem": "swap"
                }
            ]
        },
        "hdd": {  # For the 2TB HDD
            "config_type": "default",
            "partitions": [
                {
                    "mountpoint": "/home",
                    "size": "100%",  # Use all available space
                    "filesystem": "ext4"
                }
            ]
        }
    }

    # Package selection
    packages = [
        "base",
        "base-devel",
        "linux",
        "linux-firmware",
        "networkmanager",
        "grub",
        "efibootmgr",
        "sudo",
        "vim",
        "git"
    ]

    try:
        # List available disks
        disks = archinstall.list_disks()
        if not disks:
            print("Nenhum disco encontrado!")
            return

        print("\nDiscos disponíveis:")
        for disk in disks:
            print(f"- {disk}")

        # Get user input for disk selection
        print("\nVocê tem dois discos disponíveis: um SSD de 256GB e um HDD de 2TB")
        print("O SSD será usado para o sistema (/, /boot, /var) e o HDD para /home")
        ssd_disk = input("\nDigite o dispositivo do SSD de 256GB (ex: /dev/sda): ").strip()
        hdd_disk = input("Digite o dispositivo do HDD de 2TB (ex: /dev/sdb): ").strip()

        if ssd_disk not in disks or hdd_disk not in disks:
            print("Disco inválido selecionado!")
            return
        if ssd_disk == hdd_disk:
            print("Você deve selecionar dois discos diferentes!")
            return

        # Get user credentials
        hostname = input("Digite o nome da máquina: ").strip()
        username = input("Digite o nome de usuário: ").strip()
        password = input("Digite a senha: ").strip()
        root_password = input("Digite a senha do root: ").strip()

        # Initialize disks
        ssd = archinstall.Disk(ssd_disk)
        hdd = archinstall.Disk(hdd_disk)
        
        print("\nLimpando os discos...")
        ssd.wipe()
        hdd.wipe()

        print("Particionando o SSD...")
        ssd_layout = ssd.partition_disk(disk_layouts["ssd"])
        
        print("Particionando o HDD...")
        hdd_layout = hdd.partition_disk(disk_layouts["hdd"])

        # Merge the layouts
        partition_layout = {**ssd_layout, **hdd_layout}

        # Configure mirrors
        print("\nConfigurando mirrors do Brasil, EUA e Worldwide...")
        archinstall.use_mirrors(mirrors)

        # Install base system
        with archinstall.Installer(
            partition_layout,
            hostname=hostname,
            base_packages=packages
        ) as installation:
            # Configure base system
            installation.mount_ordered_layout()
            installation.minimal_installation()

            # Set timezone and locale
            installation.set_timezone(config["timezone"])
            installation.set_locale(config["locale"], config["encoding"])

            # Configure network
            installation.enable_networking()
            
            # Configure bootloader
            installation.add_bootloader()

            # Create user account
            installation.user_create(username, password)
            installation.user_set_pw("root", root_password)

            # Add user to sudoers
            installation.arch_chroot("usermod -aG wheel " + username)
            installation.arch_chroot("""echo '%wheel ALL=(ALL) ALL' | EDITOR='tee -a' visudo""")

        print("\nInstalação concluída com sucesso!")
        print("Você pode reiniciar o sistema para iniciar seu novo Arch Linux.")
        
    except Exception as e:
        print(f"Ocorreu um erro durante a instalação: {str(e)}")
        return

if __name__ == "__main__":
    main()
