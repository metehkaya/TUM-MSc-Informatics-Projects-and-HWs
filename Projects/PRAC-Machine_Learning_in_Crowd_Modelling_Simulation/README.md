# Final Project

### Setup

Installation steps:

1. Create conda venv with python 3.6 version: conda create -n manifold_env python=3.6 -y

2. Activate venv: conda activate manifold_env

3. Install packages 

	- Packages for megaman: conda install --channel=conda-forge -y pip nose coverage cython numpy scipy scikit-learn pyflann pyamg h5py plotly
	
	- Packages to run notebooks: conda install jupyter notebook & conda install matplotlib
	
	- [Optional] Packages to run notebook word2vec_partial_data: conda install seaborn gensim

4. Clone megaman: git clone https://github.com/mmp2/megaman.git

5. Go into repository and install: python setup.py install

6. [Optional] Download GoogleNews-vectors-negative300.bin.gz from [Google Code Archive](https://code.google.com/archive/p/word2vec/) or [Drive](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g).
