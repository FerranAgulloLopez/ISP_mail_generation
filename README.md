# ISP Mail Generation
This repository belongs to Adrián Tormos, Josu Yeregi and Ferran Agulló. It comes from the subject ISP of the MAI Master of the UPC. It contains the implementation for all the components regarding the infrastructure of our project. Check the full report of the final delivery for a description of the components and the overall architecture.

## Structure
The repository contains three directories: data, development and production. The data directory contains the datasets we have used in the project along the scripts for extracting and preprocessing them. The development contains the code for the two steps of the development environment: the summarization and the fine tuning of the generator. The generator fine tuning has been performed with Google Colab to be able to have the enough resources for loadng and training one of the versions of GPT2. Lastly, the production directory contains the code for the two components of the production environment: the web page and the API.

Follows a list with the description of the repository contents:
- data/: directory containing the used datasets and data processing scripts
    - datasets/: directory containing the used datasets
        - extracted/: directory containing the extracted datasets
            - bc3/: the extracted dataset from the bc3 corpus
            - enron/: the extracted dataset from the enron corpus
        - summarized/: directory containing the summarized datasets
            - bc3/: the summarized datasets from the bc3 corpus
                - t5-large: the summarized dataset using the t5-large model
                - pegasus-xsum: the summarized dataset using the pegasus model
    - extraction_scripts/: directory containing the scripts used for processing the data
        - bc3_email_corpus_dataset_extractor.py: script for extracting and processing the dataset from the bc3 corpus
        - enron_dataset_extractor: script for extracting and processing the dataset from the enron dataset
- development/: directory containing the code for the development environment
    - summarizer: directory containing the code for summarizing the datasets
    - generator_fine_tuning: directory containing the code for fine tuning the generator
- production/: directory containing the code for the production environment
    - api/: directory containing the code for the API components
    - web/: directory containing the code for the web page
    
## Usage
Follows a list with the description of how to use each of the executable components:
- bc3_dataset_extractor (data/extraction_scripts/bc3_email_corpus_dataset_extractor.py):
    - run: 
        - input params:
            - data_directory: path to the input data directory of the raw bc3 corpus
            - output_directory: path to the output directory
        - command: python3 bc3_email_corpus_dataset_extractor.py --data_directory data_directory --output_directory output_directory
- enron_dataset_extractor (data/extraction_scripts/enron_dataset_extractor.py.py):
    - set up: change the variables inside the script as desired
    - run: python3 enron_dataset_extractor.py
- generator_fine_tuning (development/generator_fine_tuning/generator_fine_tune.ipynb): copy the script file inside Google Colab. Follow the guide described inside the script and change the config parameters inside the code as desired.
- summarizer (development/summarizer/summarizer.py):
    - set up: install with pip the python packages that are specified in the requirement.txt file along the script -> pip3 install -r requirements.txt
    - run:
        - input params:
            - pretrained_model: the pretrained model to use from HuggingFace
            - min_length: the minimum length of the output summarization
            - max_length: the maximum length of the output summarization
            - repetition_penalty: the penalty to repeating tokens in the output summarization
        - command: python3 summarizer.py --pretrained-mode pretrained_model --min-length min_length --max-length max_length --repetition-penalty repetition_penalty
- web (production/web):
    - in plain OS
        - set up: install php
        - variables:
            - ip: IP to use
            - port: port to use
        - command: php -S ip:port
    - with docker: using the Dockerfile that is along the web files
        - variables:
            - docker_image_name: name of the docker image
            - docker_container_name: name of the docker container
            - port: port to use
        - build image: sudo docker build -t docker_image_name .
        - run image: sudo docker run -p port:port --name docker_container_name docker_image_name
    - with Kubernetes/Openshift: using the configuration files that are inside the manifests directory
        - variables:
            - namespace: namespace to use
        - set up: 
            - create namespace -> kubectl create namespace namespace
            - create image: create the docker image with the steps shown before
            - upload image: upload the image to a docker repository, public or private (OpenShift comes with one, you can make use of it)
            - update repository image: change the line 19 of the deployment.yaml file with the url of the docker image from the selected repository
            - select port: we are using the port 8001 in the configuration files but it can be changed
        - run: apply the configuration files
            - kubectl apply -f deployment.yaml
            - kubectl apply -f service.yaml
- api (production/api): ... (pre -> put model in place)


## License
Free use of this software is granted under the terms of the Apache License 2.0

