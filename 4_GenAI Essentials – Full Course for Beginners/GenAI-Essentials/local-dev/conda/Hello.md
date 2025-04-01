## Hello Example

Here we are creating our hello env.
We install pandas in our hello env.
We observe which packages are installed hello.
We observe which packsages are installed in base
We can use python binary to execute the python in the context of conda
check what binary is being loaded.

```sh
conda create -n hello python 3.10.0 -y
conda activate
conda install -c conda-forge pandas
pip list
conda deactivate
pip list
conda activate hello
python app.py
whereis python
whereis python3
pip install -r requirements.txt 
```