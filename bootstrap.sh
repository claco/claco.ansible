#!/usr/bin/env bash

set -e

sudo -v

if [ -x "$(command -v lsb_release)" ]; then
  DIST=`lsb_release -si`
else
  DIST=""
fi

################################################################################
# Installing minimal requirements (Ansible, Git, Make)
################################################################################
if [[ "$DIST" == "Ubuntu" ]]; then
  sudo apt -y update

  printf "Installing Python..."
  sudo apt-get -y install python3 python3-dev python3-apt python3-virtualenv python3-venv python3-wheel unzip aptitude
  echo "done"

  printf "Installing Ansible..."
  python3 -m venv --system-site-packages .venv
  source .venv/bin/activate
  pip install wheel
  pip install ansible
  echo "done"

  printf "Installing Git..."
  sudo apt-get -y install git
  echo "done"

  printf "Installing Make..."
  sudo apt-get -y install make
  echo "done"

elif [[ "$OSTYPE" == "darwin"* ]]; then
  brew install git
  brew install make
  brew install unzip

  virtualenv .venv
  source .venv/bin/activate
  pip install ansible

else
  echo "Unknown Operating System"
  exit 1
fi
