import argparse
import re
import os
import json
import pandas as pd
import numpy as np
from nltk import sent_tokenize

from datasets import Dataset, load_dataset
from transformers import AutoTokenizer, GPT2LMHeadModel
from transformers import DataCollatorForLanguageModeling, TrainingArguments, Trainer


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_file',  type=str, help="Path to data file", required=True)
    parser.add_argument('--output_directory', type=str, help="Path to output directory where to save the model", required=True)
    return parser.parse_args()


def get_data(path: str):
    with open(path, 'r') as file:
        json_data = json.load(file)
    dummy_df = pd.DataFrame(json_data['mails'])
    data = '<BOS> ' \
            + ' [CONTEXT] ' + dummy_df['subject'] \
            + ' [SUMMARY] ' + dummy_df['extractive_summary'] \
            + ' [MAIL] ' + dummy_df['content'] \
            + ' <EOS>'
    return Dataset.from_dict({'text':data})


def main(data_file: str, output_directory: str):

    """Prepare the data"""
    data = get_data(data_file)

    #get the tokenizer and the model
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # define the special tokens
    special_tokens_dict = {'bos_token': '<BOS>',
                           'eos_token': '<EOS>',
                           'pad_token': '<PAD>',
                           'mask_token':'<MASK>'}
    num_added_toks = tokenizer.add_special_tokens(special_tokens_dict)
    model.resize_token_embeddings(len(tokenizer))

    # tokenize the whole dataset
    tokenize = lambda x: tokenizer(x['text'], padding='max_length', truncation=True, max_length=256)
    training_data = data.map(tokenize, batched=True, remove_columns=['text'])

    # define a data collator for language modelling
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer)


    """Training"""
    training_args = TrainingArguments(output_directory,
                                      overwrite_output_dir = True,
                                      fp16=True,
                                      num_train_epochs=100,
                                      per_device_train_batch_size=16,
                                      load_best_model_at_end = True,
                                      metric_for_best_model='loss')

    trainer = Trainer(model=model,
                      args=training_args,
                      train_dataset=training_data,
                      tokenizer=tokenizer,
                      data_collator=data_collator)

    train_result = trainer.train()
    trainer.save_model()


if __name__ == '__main__':
    # Get input params (data directory)
    args = parse_arguments()

    # Run main program
    main(args.data_file, args.output_directory)











