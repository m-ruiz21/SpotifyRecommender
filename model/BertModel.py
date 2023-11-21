from transformers import BertTokenizer
from preprocessing import preprocessing_pipeline
from transformers import BertModel

import torch.nn as nn
import numpy as np
import re
import pandas as pd
from preprocessing import preprocessing_pipeline

#-------------------------Tokenization-------------------------#

#NOTE : need a DF

#using the tokenizer from english bert
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

#max length can be 512 if needed but 300 is more efficient
encoded_corpus = tokenizer(text = df.cleaned_description.to_list(),
                           add_special_tokens=True,
                           padding = 'max_length',
                           truncation = 'longest_first',
                           max_length = 300,
                           return_attention_mask = True)

input_ids = encoded_corpus['input_ids']
attention_masks = encoded_corpus['attention_mask']

