import torch
from torch.utils.data import TensorDataset, DataLoader
from flask import Flask, request, jsonify
from transformers import BertTokenizer
from BertRegressor import BertRegressor

# Create flask app
app = Flask(__name__)

# Defining model architecture and loading the trained weights
model = BertRegressor()
model.load_state_dict(torch.load('bert_model.pt'))
model.eval()

# Load the tokenizer and tokenize input text
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Set device to GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

@app.route("/")
def main():
    # Request the playlist name from the user
    return "Hello World!"

@app.route("/predict", methods=['POST'])
def predict_playlist():
    if request.method == 'POST':
        try:
            # get the playlist name from the JSON request
            request_data = request.json
            playlist_name = request_data.get('playlist_name', '')

            # Check if playlist_name is empty
            if not playlist_name:
                return jsonify({'error': 'Missing or empty "playlist_name" field'}), 400

            input_ids, attention_masks = prepare_inputs([playlist_name], tokenizer)
            
            dataloader = create_dataloaders(input_ids, attention_masks)
            output = predict(model, dataloader, device)

            labels = [
                'acousticness', 'danceability', 'duration_ms','energy', 
                'instrumentalness', 'key', 'liveness', 'loudness',
                'mode', 'speechiness', 'tempo', 'time_signature', 'valence'
            ]
            result = dict(zip(labels, output[0]))
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': f'Error processing JSON data: {str(e)}'}), 400
    else:
        return "Only POST requests are allowed for this endpoint."

# helper functions
def predict(model, dataloader, device):
    model.eval()
    output = []
    for batch in dataloader:
        batch_inputs, batch_masks = \
                                  tuple(b.to(device) for b in batch)
        with torch.no_grad():
            output += model(batch_inputs, 
                            batch_masks).tolist()
    return output

def create_dataloaders(inputs, masks, batch_size=13):
    input_tensor = torch.tensor(inputs)
    mask_tensor = torch.tensor(masks)
    dataset = TensorDataset(input_tensor, mask_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    return dataloader


def prepare_inputs(playlist_names, tokenizer):
    encoded_playlist_names = tokenizer(text=playlist_names, 
                                       add_special_tokens=True,
                                       padding='max_length',
                                       truncation='longest_first',
                                       max_length=300,
                                       return_attention_mask=True)
    
    input_ids = encoded_playlist_names['input_ids']
    attention_masks = encoded_playlist_names['attention_mask']
    return input_ids, attention_masks


if __name__ == '__main__':
    app.run(debug=True)