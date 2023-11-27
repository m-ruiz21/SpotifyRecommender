from transformers import BertModel
import torch.nn as nn

class BertRegressor(nn.Module):

    def __init__(self, drop_rate = 0.2, freeze_bert = False):
        super(BertRegressor, self).__init__()
        D_in, D_out = 768, 13

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