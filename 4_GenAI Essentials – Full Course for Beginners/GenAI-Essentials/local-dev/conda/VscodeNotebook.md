```sh
conda install -c conda-forge ipykernal
conda deactivate
conda remove -n hello --all -y
conda create -n hello python=3.10.0 ipykernel -y
conda activate hello
```
