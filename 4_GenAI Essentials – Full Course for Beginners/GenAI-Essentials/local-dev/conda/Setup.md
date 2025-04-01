## Install Miniconda

https://docs.anaconda.com/miniconda/install/#quick-command-line-install

__Linux__
```sh
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -u -p ~/miniconda3
```

__Windows Command Prompt__
```sh
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

__Windows Powershell__
```sh
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe
```

__MacOS (M1 Version)__
```sh
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

__MacOS (Intel Version)__
```sh
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

All version URLs can be found here [`https://repo.anaconda.com/miniconda/`](https://repo.anaconda.com/miniconda/)

## Setup Miniconda

```sh
source ~/miniconda3/bin/activate
conda init --all   
```

## Create a new env

Create a new python env called hello, with python version 3.10.0

```sh
conda create --name hello python=3.10.0 -y
```

## Activate the env

```sh
conda activate hello
```

## Get Info about current enviroment

We can see things like where the python envs exists.
```sh
conda info
```

## Remove an env

```sh
conda deactivate
conda remove -n hello --all -y
```

### Optional (Manual Conda Activation)

Sometimes you won't want conda to always run the base environment automatically whenever you use your terminal, to set this on conda you need to update its config with this command.

```sh
conda config --set auto_activate_base false
```

After restarting your terminal you can manually activate and deactivate conda simply with the commands
```sh
conda activate # Sends you to the Base environment by default

conda deactivate # Takes your terminal out of the conda environment
```