### Run the image as a container with a local folder as "work" folder,
### and one port exposed for access to Jupyter notebook (with browser
nvidia-docker run --runtime=nvidia -d -p 8887:8887 -v $HOME/code/jupyter-files/cell-counter:/my_data jupyter-cell-counter
#docker run --gpus '"device=0"' -d -p 8887:8887 -v $HOME/code/jupyter-files/cell-counter:/my_data jupyter-cell-counter
