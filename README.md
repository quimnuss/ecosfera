# ecosfera

Ecosystem in a bottle python simulation

# prerequisites

## third party modules required

`pip install bokeh`

## optional

Install jupyter to use the jupyter notebook

`pip install jupyterlab`

# running

you can run the default world with:

`python ecosfera.py`

it will generate an interctive resource graph as html as well as output
a log of birth and death in the console.

you can run the jupyter with:

`jupyter-lab`

and then select the `Ecosfera.ipynb` notebook

You can run all the steps to load the code and run the default world. It should
output this graph:

![Ecosfera Default World Graph](images/ecosfera_default_jupyter.png?raw=true "Ecosfera Default World")

If you want to change the initial conditions, do so on step 2 and rerun that step

Alternativelly, you can also change the initial conditions of the python script
[modifying the world_slected in worldLibrary.py](https://github.com/quimnuss/ecosfera/blob/master/worldLibrary.py#L4)
