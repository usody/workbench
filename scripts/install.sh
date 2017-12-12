#!/usr/bin/env bash
set -e
set -o pipefail
if  [[ $EUID > 0 ]]; then
    echo 'Execute as root' 1>&2
    exit
fi

# Where are the project files?
cd ${1:-'./..'}

echo 'Installing debian required packages...'
cat debian-requirements.txt | xargs apt install -y

echo 'Installing python packages...'
pip3 install -e . -r requirements.txt

echo 'Installing erwb command line...'
install -m 0755 scripts/erwb /usr/local/sbin/erwb
# Execution example: sudo erwb

echo 'Installing reciclanet scripts...'
echo 'Ensure you have performed git submodule init / git submodule update'
#git submodule init
#git submodule update
install -m 0755 reciclanet-scripts/instalar /usr/local/bin/erwb-install-image

echo Workbench installed!
