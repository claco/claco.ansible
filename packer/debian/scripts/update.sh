#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

apt-get -y update
apt-get -yq upgrade
apt-get -y clean autoclean
apt-get -y autoremove

unset DEBIAN_FRONTEND

rm -rf /var/lib/{apt,dpkg,cache,log}/
rm -rf /tmp/*
rm -rf /var/log/apt/*
rm -rf /var/apt/cache/*
rm -rf /var/lib/apt

