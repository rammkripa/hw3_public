import numpy as np
from segtok import tokenizer
import torch as th
from torch import nn

# Using a basic RNN/LSTM for Language modeling
class LanguageModel(nn.Module):
    def __init__(self, vocab_size, rnn_size, num_layers=1, dropout=0):
        super().__init__()
        
        # Create an embedding layer of shape [vocab_size, rnn_size]
        # Use nn.Embedding
        # That will map each word in our vocab into a vector of rnn_size size.
        self.embedding = nn.Embedding(num_embeddings = vocab_size, embedding_dim = rnn_size)

        # Create an LSTM layer of rnn_size size. Use any features you wish.
        # We will be using batch_first convention
        self.lstm = nn.LSTM(input_size = rnn_size, hidden_size = rnn_size, num_layers = num_layers)
        # LSTM layer does not add dropout to the last hidden output.
        # Add this if you wish.
        self.dropout = nn.Dropout(p = dropout)
        # Use a dense layer to project the outputs of the RNN cell into logits of
        # the size of vocabulary (vocab_size).
        self.output = nn.Linear(in_features = rnn_size, out_features = vocab_size)
        
    def forward(self,x):
        embeds = self.embedding(x)
        if (len(list(embeds.size())) == 2) :
            embeds = embeds.view(len(x), 1, -1)
        lstm_out, _ = self.lstm(embeds) #embeds.view(len(x), 1, -1)
        lstm_drop = self.dropout(lstm_out)
#         logits = your_code
        linear_output = self.output(lstm_drop)#lstm_out.view(len(x), -1))
        logits = linear_output
        return logits
