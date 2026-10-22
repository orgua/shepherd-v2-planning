# Enabling the Crypto-Module

## OpenSSL Benchmark

```text
time openssl speed -evp aes-128-cbc

⇾ Benchmark of disabled module is ~3s
    Doing aes-128-cbc for 3s on 16 size blocks: 5618835 aes-128-cbc's in 2.94s
    Doing aes-128-cbc for 3s on 64 size blocks: 1886183 aes-128-cbc's in 2.98s
    Doing aes-128-cbc for 3s on 256 size blocks: 517655 aes-128-cbc's in 2.98s
    Doing aes-128-cbc for 3s on 1024 size blocks: 132735 aes-128-cbc's in 2.97s
    Doing aes-128-cbc for 3s on 8192 size blocks: 16702 aes-128-cbc's in 2.99s
    Doing aes-128-cbc for 3s on 16384 size blocks: 8359 aes-128-cbc's in 2.98s
⇾ Benchmark of enabled is <<1.00s (CPU-Time)
    Doing aes-128-cbc for 3s on 16 size blocks: 410104 aes-128-cbc's in 0.38s
    Doing aes-128-cbc for 3s on 64 size blocks: 348184 aes-128-cbc's in 0.28s
    Doing aes-128-cbc for 3s on 256 size blocks: 37545 aes-128-cbc's in 0.02s
    Doing aes-128-cbc for 3s on 1024 size blocks: 25658 aes-128-cbc's in 0.01s
    Doing aes-128-cbc for 3s on 8192 size blocks: 5663 aes-128-cbc's in 0.01s
    Doing aes-128-cbc for 3s on 16384 size blocks: 4040 aes-128-cbc's in 0.01s

# compact benchmark:
openssl speed -elapsed -evp aes-128-cbc aes-192-cbc aes-256-cbc
openssl speed -elapsed -evp aes-128-ctr aes-192-ctr aes-256-ctr
openssl speed -elapsed -evp aes-128-gcm aes-256-gcm des-ede3-cbc chacha20-poly1305

The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes  16384 bytes

aes-128-cbc      30229.13k    40065.07k    43963.48k    45118.46k    45378.22k    45416.45k  ⇾ Insecure
aes-192-cbc      26305.07k    33554.03k    36051.20k    36890.97k    37188.95k    37191.68k  ⇾ Insecure
aes-256-cbc      24307.25k    30221.35k    32434.60k    33024.34k    33161.22k    33166.68k  ⇾ Insecure

aes-128-ctr      24565.01k    36514.28k    41899.95k    47885.31k    49993.05k    50173.27k
aes-192-ctr      22875.85k    32318.14k    35530.50k    40397.14k    42265.26k    42341.72k
aes-256-ctr      21166.89k    29006.49k    30876.16k    35073.37k    36560.90k    36580.01k

aes-128-gcm      21461.14k    28427.01k    31007.74k    34032.30k    34802.35k    34794.15k
aes-256-gcm      18821.07k    23611.90k    24569.51k    27030.19k    27661.65k    27634.35k

des-ede3-cbc      5420.43k     5722.56k     5799.77k     5807.45k     5829.97k     5821.78k
chacha20-poly    22729.05k    52835.75k    96532.65k   107768.83k   112194.90k   112361.47k
                 128-cbc        chacha     chacha      chacha       chacha         chacha

# real test:
scp -o Cipher=chacha20-poly1305@openssh.com ./rec.2.h5 10.0.0.52:/home/hans/
# TI-Website about CryptoModule and performance on this CPU: https://processors.wiki.ti.com/index.php/AM335x_Crypto_Performance
# TI-Support shows that Module also handles basic compression: https://e2e.ti.com/support/processors/f/791/t/349219?AM335x-Hardware-Crypto-Engine
# TODO: change packet size for scp, try basic compression and fastest cipher for module
```

## Add Driver for CPU Crypto-Module

```text
# compile and add Cryptodev module / https://github.com/cryptodev-linux/cryptodev-linux
# Manual1: https://lauri.võsandi.com/2014/07/cryptodev.html
# Manual2: https://datko.net/2013/10/03/howto_crypto_beaglebone_black/

cd ~/
wget https://github.com/cryptodev-linux/cryptodev-linux/archive/cryptodev-linux-1.10.tar.gz
tar zxf cryptodev-linux-1.10.tar.gz
cd crypt...
make
sudo make install
sudo depmod -a                      # ⇾ register
sudo modprobe cryptodev             # ⇾ insert
lsmod                               # ⇾ check, /dev/crypto now available
add cryptodev to /etc/modules       # ⇾ permanent
sudo sh -c 'echo cryptodev /etc/modules'
```

## Force OpenSSL to use Crypto-Module-Hardware

**Note:** hard-coding openSSL-Version is stupidly insecure)

```Shell
# Check active OpenSSL Version
apt list --installed | grep openssl  # ⇾ check current version
openssl engine -t -c                 # ⇾ should contain devcrypto
openssl version -f                   # ⇾ should list -DHAVE_CRYPTODEV -DUSE_CRYPTDEV_DIGESTS

# Check what ssh & sshd is using
wheris -u sshd                       # ⇾ /usr/sbin/sshd
ldd /usr/sbin/sshd
    libcrypto is part of openssl
# ⇾ installed is /lib/arm-linux[...]/libcrypto.so.1.0.0 with 2 year old openSSL 1.1.1 (NOT current 1.1.1g)
# ⇾ current is /usr/local/lib/libcrypto.so.1.1

# compile openSSL with cryptodev-support
# Manual: https://wiki.openssl.org/index.php/Compilation_and_Installation

cd ~/
wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
wget -O openssl.tar.gz https://github.com/openssl/openssl/archive/OpenSSL_1_1_1g.tar.gz
tar zxf openssl.tar.gz                # ⇾ TODO: still unpacks to full name with version nr.
cd openssl...
./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared enable-devcryptoeng no-sse2 no-com --openssldir=/usr/local/ssl
perl configdata.pm --dump
make clean
make                                  # ⇾ TODO: this takes ~33min
sudo make install_sw                  # ⇾ will be in /usr/local/bin

# ubuntu has a strange behavior: local/bin is used, local/lib gets ignored, so dirty fixing it
# ⇾ add "/usr/local/lib" as first active line in /etc/ld.so.conf.d/arm-gnueabihf.conf

# /etc/ssl/openssl.cnf                #  ⇾ TODO: maybe add/uncomment crypto in [engine]-section, seems not to be needed

# Problem: new openSSL gives us libcrypto.so.1.1. but sshd demands libcrypto.so.1.0.0
cd /usr/local/lib
# sudo ln -s libcrypto.so.1.1 libcrypto.so.1.0.0
# sudo shutdown -r now
# sudo cp libcrypto.so.1.1 libcrypto.so.1.0.0
# ⇾ symlinks and copy do not help, sshd relies on old version

# bypass: compile old version of libcrypto.ssl of openssl, could fail for ssh because of ABI-changes
# readme: https://github.com/openssl/openssl/issues/4597
apt list --installed | grep sll           #  ⇾ shows 1.0.2n
cd ~/
wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_2n.tar.gz
tar zxf OpenSSL_1_0_2n.tar.gz
cd OpenSSL
./config -DHAVE_CRYPTODEV -DUSE_CRYPTODEV_DIGESTS shared enable-devcryptoeng no-sse2 no-com --openssldir=/usr/local/ssl
make build_generated && make libcrypto.a
sudo make install_sw
sudo cp /usr/local/ssl/lib/libcrypto.so.1.0.0 /usr/lib/arm-linux-gnueabihf/libcrypto.so.1.0.0
# ⇾ WORKS but is slow (see benchmark)

# TODO: openssl config option: no-comp, no-sslv3, -DOPENSSL_NO_HEARTBEATS
```

## Compile SSHd with support for new openSSL-Version

```Shell
# compile openSSH with openssl usage
# sources and readme: https://github.com/openssh/openssh-portable
# info: installed is v7.6p1-4
cd ~/
wget https://github.com/openssh/openssh-portable/archive/V_8_3_P1.tar.gz
tar zxf V_
cd
configure --help
./configure --with-pam
make
make tests
```

## SSH benchmark

```Shell
rsync -r -v --progress -e ssh ./rec.2.h5 hans@10.0.0.52:/home/hans/
#   3.7 - 4.7 MB/s at 45% cpu usage out-of-the-box
#   6.x - 7.0 MB/s at 66% cpu usage after optimizations
#   ⇾ similar results with "external" sd-card
#   ⇾ cpu has most likely no crypto, or does not use it
#   1.5 - 2.8 MB/s  with 50% usage
```
