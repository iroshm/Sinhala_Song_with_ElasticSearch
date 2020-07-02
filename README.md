# Sinhala_Song_with_ElasticSearch
Project to search songs in sinhala using Elasticsearch and python 

## Setup

### Requirements
1. Install python 3 and pip version 3
2. Install required packages
      a.) elasticsearch
      b.) tkinter
      c.) kibana

## Run

### Method 1(Recommended)
#### If you are using virtual environment(Recommended - pycharm virtual environment)
1. Go to this link and download sinlin tokenizer. ``` https://github.com/ysenarath/sinling  ``` 
2. Copy ```sinling``` folder to packagers. ```ElasticSearch\venv\Lib\site-packages```
3. Run ElasticSearch locally on your computer( port - ```9200```)
3. Connect to the ElasticSeacrh 
4. If you need to fill text files in the root directory run the ```file_generator.py``` file
5. Run ```advanced_search.py```

### Method 2
#### If you are run directly
Steps-
1. Create new folder named `bin` in root path
2. Download [`stat.split.pickle`](https://github.com/ysenarath/sinling/releases/download/v0.1-alpha/stat.split.pickle) to the `bin` folder
3. Import required tools from the `sinling` module in your desired project 
(you may have to append this project path to your path environment variable)
4. Run ElasticSearch locally on your computer( port - ```9200```)
5. Connect to the ElasticSeacrh 
6. If you need to fill text files in the root directory run the ```file_generator.py``` file
7. Run ```advanced_search.py``
