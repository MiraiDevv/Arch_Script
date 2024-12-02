# Arch Linux Installation Script

This script automates the installation of Arch Linux using the `archinstall` library. 

## Requirements

- Arch Linux live ISO environment
- Internet connection
- Python 3.x
- `archinstall` package (included in recent Arch Linux ISOs)

## Usage

1. Boot into the Arch Linux live environment
2. Clone this repository or download the script
3. Run the script with root privileges:
```bash
sudo python install_arch.py
```

## Features

- Automated disk partitioning
- System locale and timezone configuration
- User account creation
- Basic package installation
- Network configuration

## Note

Please review the configuration in the script before running it. You may want to modify:
- Disk partitioning scheme
- Locale and timezone
- Username and password
- Package selection

⚠️ **Warning**: This script will format the selected disk. Make sure you have backups of any important data.
