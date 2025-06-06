# Defining and training custom atomstic machine learning model with metatensor and metatomic

This section contains multiple notebook that will teach you about
[metatensor](https://docs.metatensor.org/) and
[metatomic](https://docs.metatensor.org/metatomic). You'll learn how to handle
data stored with metatensor, and how to define a train custom machine learning
models with metatomic.

## Installation

Please follow the instructions below to setup a Python virtual environment
containing all the dependencies:

```bash
cd metatensor-metatomic/

python3 -m venv virtualenv
source ./virtualenv/bin/activate
pip install -U pip

pip install -r requirements.txt
jupyter notebook  # or `jupyter lab` if you prefer
```


## Running the tutorials

You should go through the different notebooks in this repository in order.
Everytime you see this icon

![task icon](img/clipboard.png)

This means you need to modify the code to make it work and make a small test
pass. All the modifications should only require basic Python knowledge, and no
specific PyTorch/metatensor/metatomic knowledge.
