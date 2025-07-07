# Evaluate UV Package Manager

## Advantages for us

- can install the newest python versions
- all done in virtual envs
- even installed apps are kept in venvs
- very fast
- dependencies can be kept up-to-date easier

## Try using it on BBB

```Shell
sudo apt update
sudo apt dist-upgrade
sudo apt install cmake build-essential
```

```Shell
# curl -LsSf https://astral.sh/uv/install.sh | sudo sh
# uv self update
sudo pip install uv --upgrade --break-system-packages

source $HOME/.local/bin/env

uv python list
# cpython-3.11.2-linux-armv7-gnu    /usr/bin/python3.11
uv python install 3.13 --reinstall
# installs cpython-3.13.2-linux-armv7-gnu
uv venv -p 3.13
# creates a usable venv for py313
uv pip install /opt/shepherd/software/python-package -p 3.13
# fails with ram-explosion, several packages are build in parallel
uv pip install numpy -p 3.13 # v2.2.4, 110 min (previously 240min?)
uv pip install zstandard -p 3.13  # v0.23, 21 min
sudo apt install hdf5-tools libhdf5-dev # or libhdf5-103, the two installed did the trick
uv pip install h5py -p 3.13  # v3.13, 54 min
uv pip install gevent -p 3.13  # v2024.11.1, 35 min
uv pip install pyzmq -p 3.13  # v26.4.0, 25 min
uv pip install pydantic click -U -p 3.13  #
uv pip install shepherd-core -U -p 3.13  # 1 min
uv pip install psutil msgpack -p 3.13  # 2 min

source /opt/shepherd/software/python-package/.venv/bin/activate
```

run in venv:

```shell
cd
uv venv
source /home/jane/.venv/bin/activate

# in .bashrc
. "$HOME/.local/bin/env"
. "$HOME/.venv/bin/activate"
```


help with cleaning up uv [is here](https://docs.astral.sh/uv/getting-started/features/#utility) and also [removing it completely](https://docs.astral.sh/uv/getting-started/installation/#uninstallation)

```Shell
uv cache prune
# or complete clean
uv cache clean
```

~~Still an [open bug](https://github.com/astral-sh/uv/issues/6873) in uv (v0.4.15, 2024-09-23)~~
-> resolved in uv 0.4.29

```Shell
>>  uv pip install /opt/shepherd/software/python-package -p 3.13
Resolved 48 packages in 1.11s
Installed 48 packages in 2.54s
 + annotated-types==0.7.0
 + certifi==2024.8.30
 + charset-normalizer==3.4.0
 + chromalog==1.0.5
 + click==8.1.7
 + colorama==0.4.6
 + colored-traceback==0.4.2
 + dnspython==2.7.0
 + email-validator==2.2.0
 + future==1.0.0
 + gevent==24.10.3
 + greenlet==3.1.1
 + h5py==3.12.1
 + idna==3.10
 + intelhex==2.3.0
 + intervaltree==3.1.0
 + invoke==2.2.0
 + msgpack==1.1.0
 + msgpack-numpy==0.4.8
 + numpy==2.1.2
 + packaging==24.1
 + plumbum==1.9.0
 + psutil==6.1.0
 + pwntools-elf-only==4.12.3.dev0
 + pydantic==2.9.2
 + pydantic-core==2.23.4
 + pyelftools==0.31
 + pygments==2.18.0
 + pyserial==3.5
 + python-dateutil==2.9.0.post0
 + python-periphery==1.1.2
 + pyyaml==6.0.2
 + pyzmq==26.2.0
 + requests==2.32.3
 + rpyc==6.0.1
 + setuptools==75.3.0
 + shepherd-core==2024.9.1
 + shepherd-sheep==0.8.3 (from file:///opt/shepherd/software/python-package)
 + six==1.16.0
 + sortedcontainers==2.4.0
 + tqdm==4.66.6
 + typing-extensions==4.12.2
 + unix-ar==0.2.1
 + urllib3==2.2.3
 + zerorpc==0.6.3
 + zope-event==5.0
 + zope-interface==7.1.1
 + zstandard==0.23.0
```

It works!

```Shell
(python-package) root@sheep0:/opt/shepherd/software/python-package# shepherd-sheep -v --version blink
Shepherd-Sheep v0.8.3
Python v3.13.0 (main, Oct 16 2024, 02:57:06) [GCC 6.3.0 20170516]
Click v8.1.7
Blinks LEDs IO & EMU next to Target-Ports for 30 s
```

But it's slower than the bundled py-version:

```Shell
sudo python3 -X importtime -c 'from shepherd_core.data_models.task import EmulationTask' 2> importtime.log
# native
# 11.7 s on v2024.8.2, pydantic 2.9.0, core 2.23.2
#  8.8 s on v2025.2.2, pydantic 2.11.2, core 2.33.1
# with UV
# 18.7 s on v2024.9.1, pydantic 2.9.2, core 2.23.4 - python 3.13.0 via uv 0.4.29
# 13.1 s on v2025.2.2, pydantic 2.11.2, core 2.33.1 - python 3.13.2 via uv 0.6.12

```
