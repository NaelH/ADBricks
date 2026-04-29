#!/bin/bash

# install.sh
# Script d'installation de ADBricks
# 
# Auteur    :   NaelH
# Version   :   1.0.0
# Usage     :   sudo ./install.sh
#
# Dépendance : 
#   -   Internet
#   -   sudo
#   -   sha256sum
#
# Journal de bord :
#  29th april 2026 : Beginning of the project 

# variables
current=$( pwd )
packages="python3-pip python-is-python3 2to3"
suminstallator="7a66014db2eea98f968dc2c52984f668bc56d6a0dcefc0d6c93e68257bbe096a"
sumthisone=$( sha256sum "$current"/install.sh | cut -d ' ' -f1 )

# Fonctions

aide(){
    echo -e "\nUsage: sudo $0"
    echo -e "       install     Permet l'installation de ADBricks"
    echo -e "       iverb       Permet l'installation en mode textuel"
    echo -e "       help        Obtenir de l'aide"
    echo -e "       pull        Mise à jour de l'intégralité du projet\n"
    exit 0
}

erreur(){
    echo "Erreur : $1"
    exit -1
}

mise_a_jour(){
    git pull
    echo -e "\nMise à jour terminé\n"
    exit 0
}

# blindages

[ $# -ne 1 ] && erreur "Ce script prend en compte un argument."
[ "$1" == "-h" -o "$1" == "--help" -o "$1" == "help" ] && aide
[ "$1" == "pull" ] && mise_a_jour
[ $EUID -ne 0 ] && erreur "Ce script nécessite l'usage de droits administrateurs."


apt update 
apt install $packages 

