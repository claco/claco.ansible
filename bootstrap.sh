#!/usr/bin/env bash

set -eau pipefail

sudo -v

while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

if [ -x "$(command -v lsb_release)" ]; then
  DIST=`lsb_release -si`
else
  DIST=""
fi

PYTHON_VERSION="python3"
PYTHON_INTERPRETER=`which $PYTHON_VERSION`
PYTHON=$PYTHON_INTERPRETER
REPOSITORY="claco.ansible"
DIRECTORY="$HOME/Projects/$REPOSITORY"
VENV="$DIRECTORY/.venv"

################################################################################
# Clone Ansible Playbooks
################################################################################
if [[ ! -d $DIRECTORY/.git ]]; then
  echo "Cloning Playbooks..."
  mkdir -p $DIRECTORY
  pushd $DIRECTORY > /dev/null
  git clone https://github.com/claco/$REPOSITORY.git $DIRECTORY
  git remote set-url origin git@github.com:claco/$REPOSITORY.git
else
  echo "Ansible Playbooks already installed."
fi

if [[ "$DIST" == "Pop" ]]; then
  ################################################################################
  # Install Ansible
  ################################################################################
  if [ ! -f $VENV/bin/ansible-playbook ]; then
    echo "Installing Ansible..."

    sudo apt -y update
    sudo apt -y install python3 python3-venv
    $PYTHON -m venv $VENV
    $VENV/bin/pip install pip setuptools wheel --upgrade
    $VENV/bin/pip install ansible
  else
    echo "Ansible already installed."
  fi

elif [[ "$DIST" == "Manjaro-ARM" ]]; then
  ################################################################################
  # Install Ansible
  ################################################################################
  if [ ! -f $VENV/bin/ansible-playbook ]; then
    echo "Installing Ansible..."

    sudo pamac update
    sudo pamac install gcc make python python-virtualenv --no-confirm
    $PYTHON -m venv $VENV
    $VENV/bin/pip install pip setuptools wheel --upgrade
    $VENV/bin/pip install ansible
  else
    echo "Ansible already installed."
  fi

else
  export HOMEBREW_CASK_OPTS="--appdir=/Applications --fontdir=/Library/Fonts"


  ################################################################################
  # Command Line Tools
  ################################################################################
  if ! pkgutil --pkg-info=com.apple.pkg.CLTools_Executables &> /dev/null; then
    printf "Installing Command Line Tools..."
    xcode-select --install &> /dev/null || true
    while ! pkgutil --pkg-info=com.apple.pkg.CLTools_Executables &> /dev/null; do
      sleep 10
    done
  else
    echo "Command Line Tools already installed...skipping"
  fi

  ################################################################################
  # Homebrew (Interactive Install)
  ################################################################################
  if [ ! -f /usr/local/bin/brew ]; then
    echo "Installing Homebrew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install brew-cask-completion
    brew cask install caskroom/fonts/font-symbola
  else
    echo "Homebrew already installed...skipping"
  fi

  ################################################################################
  # Install Ansible
  ################################################################################
  if [ ! -f /usr/local/bin/ansible-playbook ]; then
    printf "Installing Ansible..."
    brew install ansible &> /dev/null
    echo "done"
  else
    echo "Ansible already installed...skipping"
  fi

  ################################################################################
  # Enable SSH Logins
  ################################################################################
  if [[ $(sudo systemsetup -getremotelogin) = *Off* ]]; then
    printf "Enabling Remote Login..."
    sudo systemsetup -setremotelogin on
    echo "done"
  else
    echo "Remote Login Enabled ...skipping"
  fi

  ################################################################################
  # Disable "Downloaded From The Internet" Open Prompts
  ################################################################################
  printf "Disabling Internet Download Warning..."
  defaults write com.apple.LaunchServices LSQuarantine -bool NO
  echo "done"
  echo

  echo "######################################"
  echo "Please reboot to have this take effect"
  echo "######################################"

fi

echo "Done."
