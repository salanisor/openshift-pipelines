# ~~~
# cd ~/Downloads/

tar -xvf crc-linux-amd64.tar.xz 
# crc-linux-2.16.0-amd64/
# crc-linux-2.16.0-amd64/LICENSE
# crc-linux-2.16.0-amd64/crc

mkdir -p ~/local/bin

mv crc-linux-*-amd64/crc ~/local/bin/

export PATH=$HOME/local/bin:$PATH

crc version
# CRC version: 2.16.0+05b62a75
# OpenShift version: 4.12.9
# Podman version: 4.4.1

echo 'export PATH=$HOME/local/bin:$PATH' >> ~/.bashrc
# ~~~
