```sh
conda create -n serv python=3.10.0 ipykernel -y
conda install -c conda-forge jupyterlab
jupyter lab --no-browser --allow-root --ip 0.0.0.0
conda install -c conda-forge jupyterlab-git
conda install -c conda-forge catppuccin-jupyterlab
```
