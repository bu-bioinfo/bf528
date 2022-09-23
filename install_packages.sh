#conda create -n bf550 python=3.9
#conda activate bf550
conda install -c conda-forge ruby=2.7.2 gxx_linux-64
pip install pandas snakemake ncbi-acc-download

gem install bundler

bundle install
