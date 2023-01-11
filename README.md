# This python program needs LTTOOLBOX. If you do not have it, install it using the below instructions.
curl -sS https://apertium.projectjj.com/apt/install-nightly.sh | sudo bash
sudo apt -f install apertium-all-dev
## To convert the .dix file into bin format using lt-comp
lt-comp Odia_apertium_morph_dict.dix Odia_apertium_morph_dict.bin
# How to run the code
## This code runs both at file or folder level, both on POS or chunk annotated file.
## if you are running the following program at only pos annotated data, set chunk value as 0
## if you are running the following program at only pos annotated data, set chunk value as 1
python odia_morph_analysis_using_lt_toolbox.py --input Sample-Input/ --output Sample-Output --dict Odia_apertium_morph_dict.bin --chunk 1
### Arguments for running the program
#### input: Input folder or file
#### output: Output folder or file
#### dict: Apertium morph dict in bin format
#### chunk: 0 (for POS Annotated data) or 1 (for POS Chunk Annotated data)
# Packages required for running the program
## Install pip using sudo apt install python3-pip
## pip install wxconv
# How to cite the morph dictionary
@inproceedings{jena2011developing,
  title={Developing oriya morphological analyzer using lt-toolbox},
  author={Jena, Itisree and Chaudhury, Sriram and Chaudhry, Himani and Sharma, Dipti M},
  booktitle={International Conference on Information Systems for Indian Languages},
  pages={124--129},
  year={2011},
  organization={Springer}
}
# You can also cite this repository if you directly use it.
