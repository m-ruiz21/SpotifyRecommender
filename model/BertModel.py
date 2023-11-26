from transformers import BertTokenizer
from transformers import BertModel
from sklearn.model_selection import train_test_split
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup
from torch.nn.utils.clip_grad import clip_grad_norm
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader

import torch.nn as nn
import numpy as np
import re
import pandas as pd
import torch

#-------------------------Tokenization-------------------------#

df = pd.read_csv('./data/playlist_features_filtered.csv', delimiter=',', index_col=0)


# tokenize the playlist names 
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

encoded_playlist_names = tokenizer(text = df.name.to_list(),        
                           add_special_tokens=True,
                           padding = 'max_length',
                           truncation = 'longest_first',
                           max_length = 300,
                           return_attention_mask = True)

input_ids = encoded_playlist_names['input_ids']
attention_masks = encoded_playlist_names['attention_mask']

# put data into numpy arrays
names = np.array(input_ids)
input_ids = np.array(input_ids)
attention_masks = np.array(attention_masks)
labels = df[
        ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","time_signature","valence"]
    ].to_numpy()


#formatting the input
test_size = 0.1
seed = 42
train_inputs, test_inputs, train_labels, test_labels = \
            train_test_split(input_ids, labels, test_size=test_size, 
                             random_state=seed)
train_masks, test_masks, _, _ = train_test_split(attention_masks, 
                                        labels, test_size=test_size, 
                                        random_state=seed)

#scale the label scores
score_scaler = StandardScaler()
score_scaler.fit(train_labels)

train_labels = score_scaler.transform(train_labels)
test_labels = score_scaler.transform(test_labels)

batch_size = 32

def create_dataloaders(inputs, masks, labels, batch_size):
    input_tensor = torch.tensor(inputs)
    mask_tensor = torch.tensor(masks)
    labels_tensor = torch.tensor(labels)
    dataset = TensorDataset(input_tensor, mask_tensor, 
                            labels_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, 
                            shuffle=True)
    return dataloader

train_dataloader = create_dataloaders(train_inputs, train_masks, 
                                      train_labels, batch_size)
test_dataloader = create_dataloaders(test_inputs, test_masks, 
                                     test_labels, batch_size)


#-------------------------Model-------------------------#

#implement the model in pytorch
class BertRegressor(nn.Module):

    def __init__(self, drop_rate = 0.2, freeze_bert = False):
        super(BertRegressor, self).__init__()
        D_in, D_out = 768, 1

        self.bert = \
            BertModel.from_pretrained('bert-base-uncased')
        
        self.regressor = nn.Sequential(
            nn.Dropout(drop_rate),
            nn.Linear(D_in, D_out)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids = input_ids,
                            attention_mask = attention_mask)
        class_label_output = outputs[1]
        outputs = self.regressor(class_label_output)
        return outputs
    
model = BertRegressor(drop_rate = 0.2)

#-------------------------Training-------------------------#

#setting up the training env
if torch.cuda.is_available():       
    device = torch.device("cuda")
    print("Using GPU.")
else:
    print("No GPU available, using the CPU instead.")
    device = torch.device("cpu")
model.to(device)

#define the adam optimizer with a 5e-5 learning rate
optimizer = AdamW(model.parameters(), lr = 5e-5, eps = 1e-8)

#number of epochs
epochs = 5

#total steps
total_steps = len(train_dataloader) * epochs
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps = 0, num_training_steps = total_steps)
loss_fn = nn.MSELoss()

#training loop
def train(model, optimizer, scheduler, loss_function, epochs,
          train_dataloader, test_dataloader, device, clip_value = 2):
    for epoch in range(epochs):
        best_loss = 1e10
        model.train()
        for step, batch in enumerate(train_dataloader):
            batch_inputs, batch_masks, batch_labels = tuple(t.to(device) for t in batch)
            model.zero_grad()
            outputs = model(batch_inputs, batch_masks)
            loss = loss_function(outputs.squeeze(), batch_labels.squeeze())
            loss.backward()
            clip_grad_norm(model.parameters(), clip_value)
            optimizer.step()
            scheduler.step()
    return model

model = train(model, optimizer, scheduler, loss_fn, epochs, train_dataloader, device, clip_value= 2)