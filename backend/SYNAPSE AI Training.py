#SYNAPSE AI Training File
#Creating embeddings from EEG readings using CNNs

import os
import glob
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import StandardScaler
from scipy.fftpack import fft
from scipy.signal import welch
import pywt
import chromadb
import random

DATA_DIR = "/content/sample_data"   #CHANGE TO ACTUAL PATH
EPOCHS = 100
BATCH_SIZE = 8
LR = 1e-3
EMBEDDING_DIM = 300
SAMPLING_RATE = 256   # Muse 2 256 Hz
WAVELET = 'db4'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Our 4 different thoughts, widely varying in terms of emotions and meaning
THOUGHT_LABELS = [
    "dhp", #1 - Doctor Helps Patient - Thoughts of care, empathy, concern
    "sab", #2 - Sister argues with brother - Thoughts of conflict, frustration
    "fbh", #3 - Fire burns house - Thoughts of emergency, fear, rapid reaction
    "cfm", #4 - Child cries for mother - Thoughts of sadness and distress
    "null" #5 To account for no thoughts
]

def bandpass_filter_dummy(eeg_array, low=0.5, high=40, sfreq=256):
    """
    Placeholder for bandpass filtering. For real usage, apply MNE or SciPy filters.
    eeg_array shape: (num_channels, num_samples)
    """
    # This function just returns the input for now.
    return eeg_array

def extract_fft_features(eeg_array):
    """
    EEG -> FFT -> frequency domain
    eeg_array: (num_channels, num_samples)
    returns: np.array of shape (*,) feature vector
    """
    feats = []
    for channel in eeg_array:
        fft_vals = np.abs(fft(channel))
        half_spectrum = fft_vals[: len(channel)//2]
        feats.append(half_spectrum)
    return np.hstack(feats)

def extract_psd_features(eeg_array, sfreq=256):
    """
    EEG -> Power Spectral Density (Welch)
    returns: np.array of shape (*,) feature vector
    """
    feats = []
    for channel in eeg_array:
        freqs, psd = welch(channel, fs=sfreq, nperseg=sfreq//2)
        feats.append(psd)
    return np.hstack(feats)

def extract_wavelet_features(eeg_array, wavelet='db4'):
    """
    EEG -> Discrete Wavelet Transform
    We take mean(abs(coeffs)) for each sub-band
    returns: np.array of shape (*,) feature vector
    """
    feats = []
    for channel in eeg_array:
        coeffs = pywt.wavedec(channel, wavelet=wavelet, level=4)
        # e.g., mean absolute value of each sub-band
        wavelet_sub_feats = [np.mean(np.abs(c)) for c in coeffs]
        feats.append(np.array(wavelet_sub_feats))
    return np.hstack(feats)

def get_feature_vector(eeg_array):
    """
    Combines multiple transforms into a single feature vector
    eeg_array: shape (num_channels, num_samples)
    """
    # 1) Filter
    filtered = bandpass_filter_dummy(eeg_array)

    # 2) Extract
    fft_f     = extract_fft_features(filtered)
    psd_f     = extract_psd_features(filtered, sfreq=SAMPLING_RATE)
    wavelet_f = extract_wavelet_features(filtered, wavelet=WAVELET)

    # 3) Concatenate
    feature_vector = np.hstack([fft_f, psd_f, wavelet_f])
    return feature_vector

##############################################################################
# 2. Triplet Dataset + Sampler
##############################################################################

class EEGTripletDataset(Dataset):
    """
    For triplet loss, we need anchor, positive, negative
    - anchor, positive come from same thought label
    - negative from different thought label
    We'll store:
      self.features[thought_label] -> list of feature vectors
    We randomly sample triplets at each iteration.
    """
    def __init__(self, feature_dict):
        """
        feature_dict: {label_str: [feature_vector, feature_vector, ...], ...}
        """
        super().__init__()
        self.feature_dict = feature_dict
        self.labels = list(feature_dict.keys())

        # Flatten out for indexing if needed, but we'll do custom sampling.
        self.total_samples = 0
        for lbl in self.labels:
            self.total_samples += len(feature_dict[lbl])

    def __len__(self):
        return 999999  # We'll do random sampling each time, effectively infinite

    def __getitem__(self, idx):
        """
        Randomly pick anchor label, then pick anchor + positive from same label,
        negative from a different label.
        """
        anchor_label = random.choice(self.labels)
        positives = self.feature_dict[anchor_label]
        if len(positives) < 2:
            # Edge case if there's only 1 sample for this label
            # we need at least 2 for anchor/positive
            # pick a label that has >=2 samples
            anchor_label = random.choice([lbl for lbl in self.labels
                                          if len(self.feature_dict[lbl]) >= 2])
            positives = self.feature_dict[anchor_label]

        anchor_pos = random.sample(positives, 2)
        anchor_feat = anchor_pos[0]
        positive_feat = anchor_pos[1]

        # negative label
        neg_label = random.choice([lbl for lbl in self.labels if lbl != anchor_label])
        negative_feat = random.choice(self.feature_dict[neg_label])

        # Return anchor, positive, negative
        return anchor_feat, positive_feat, negative_feat, anchor_label, anchor_label, neg_label

class EEGEmbeddingCNN(nn.Module):
    """
    Maps a feature vector of shape [batch_size, feature_dim] -> [batch_size, EMBEDDING_DIM]
    But we do a small 1D conv to mimic some "spatial" filter effect on the feature dimension.
    """
    def __init__(self, input_dim, embedding_dim=64):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.fc = nn.Linear(input_dim * 64, embedding_dim)

    def forward(self, x):
        # x: [batch_size, 1, feature_dim]
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        # flatten
        x = x.view(x.size(0), -1)
        emb = self.fc(x)  # [batch_size, embedding_dim]
        return emb

def triplet_loss_fn(anchor, positive, negative, margin=1.0):
    """
    anchor, positive, negative: [batch_size, embedding_dim]
    We'll use TripletMarginLoss from PyTorch for convenience
    """
    criterion = nn.TripletMarginLoss(margin=margin, p=2)
    return criterion(anchor, positive, negative)

def main():
    # Step A: Gather CSVs + Build Feature Dict
    #    feature_dict[label_str] = list of feature_vector (np arrays)
    feature_dict = {lbl: [] for lbl in THOUGHT_LABELS}

    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    print(f"Found {len(csv_files)} CSV files in {DATA_DIR}")

    # Read each CSV and figure out the label
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        # 1) Identify label. Either from a column or from filename
        base = os.path.basename(csv_file)
        found_label = None
        for lbl in THOUGHT_LABELS:
            if lbl in base:
                found_label = lbl
                break

        # If you keep the label in the CSV as a column "label", you can do:
        # found_label = df["label"].iloc[0]

        if not found_label:
            print(f"Warning: no label found for {csv_file}, skipping")
            continue

        # 2) Construct raw EEG array, shape (num_channels, num_samples)
        # Let's assume columns [time, TP9, AF7, AF8, TP10], ignoring time:
        # Adjust as needed
        channels = ["TP9", "AF7", "AF8", "TP10"]
        if not all(ch in df.columns for ch in channels):
            print(f"Warning: {csv_file} missing some channels. Skipping.")
            continue
        df = df.iloc[:2560]
        raw_eeg = df[channels].values.T  # shape = (4, num_samples)

        # 3) Extract features
        feats = get_feature_vector(raw_eeg)

        # 4) Store in dict
        feature_dict[found_label].append(feats)

    # Flatten + scaling
    # We'll gather all features to fit a scaler, then re-assign them.
    all_feats = []
    for lbl in THOUGHT_LABELS:
        for f in feature_dict[lbl]:
            all_feats.append(f)
    all_feats = np.array(all_feats)
    print("All feats shape (unscaled):", all_feats.shape)

    # Fit scaler
    scaler = StandardScaler()
    scaler.fit(all_feats)

    # Apply scaler
    for lbl in THOUGHT_LABELS:
        scaled_list = []
        for f in feature_dict[lbl]:
            f_scaled = scaler.transform(f.reshape(1, -1))[0]
            scaled_list.append(f_scaled)
        feature_dict[lbl] = scaled_list

    # Step B: Create Triplet Dataset & DataLoader
    dataset = EEGTripletDataset(feature_dict)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Step C: Build CNN Model
    input_dim = all_feats.shape[1]
    model = EEGEmbeddingCNN(input_dim=input_dim, embedding_dim=EMBEDDING_DIM).to(DEVICE)

    optimizer = optim.Adam(model.parameters(), lr=LR)


    # Step D: Training Loop (Triplet)
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        num_batches = 0

        for batch_idx, data in enumerate(dataloader):
            # data has anchor_feat, positive_feat, negative_feat, ...
            anchor_f, pos_f, neg_f, lblA, lblP, lblN = data
            # anchor_f shape: [batch_size, feature_dim] in numpy
            anchor_f = anchor_f.float().to(DEVICE)
            pos_f = pos_f.float().to(DEVICE)
            neg_f = neg_f.float().to(DEVICE)

            # Reshape for CNN input: [batch_size, 1, feature_dim]
            anchor_f = anchor_f.unsqueeze(1)
            pos_f    = pos_f.unsqueeze(1)
            neg_f    = neg_f.unsqueeze(1)

            optimizer.zero_grad()

            # Forward
            anchor_emb = model(anchor_f)
            pos_emb    = model(pos_f)
            neg_emb    = model(neg_f)

            # Triplet Loss
            loss = triplet_loss_fn(anchor_emb, pos_emb, neg_emb, margin=1.0)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

            # Just limit the epoch size so it doesn't go infinite
            if batch_idx > 50:
                break

        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/num_batches:.4f}")

    # Step E: Save the model + scaler
    torch.save(model.state_dict(), "eeg_triplet_cnn.pth")
    import joblib
    joblib.dump(scaler, "scaler_triplet.joblib")

    print("Finished training. Model + scaler saved.")

    print("Storing embeddings in ChromaDB...")
    model.eval()

    # 1) Initialize a local Chroma client (in-memory) or persistent if you want:
    #    For a persistent approach, set `persist_directory`.
    client = chromadb.HttpClient(ssl=True,host='api.trychroma.com',
                                 tenant='768c13d0-c1fb-4e76-bd7c-ae5c8732fe8d',
                                 database='synapse-ai',headers={ 'x-chroma-token': 'ck-2o6DKm7Da85kWCo31guqQVhSktjN1Kg4WPm3N68XtJEX'}
)

    torch.save(model.state_dict(), "eeg_triplet_cnn.pth")
    joblib.dump(scaler, "scaler_triplet.joblib")


    # 2) Create or get collection
    collection = client.get_or_create_collection(name="embeddings_eeg")

    # 3) Convert each sample to an embedding + store in Chroma
    doc_ids     = []
    doc_metadatas  = []
    doc_embeddings = []

    _counter = 0
    for lbl in THOUGHT_LABELS:
        for f_scaled in feature_dict[lbl]:
            # convert to embedding
            ft = torch.tensor(f_scaled, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                emb = model(ft)  # shape = [1, EMBEDDING_DIM]
            embedding_vec = emb.cpu().numpy().reshape(-1).tolist()

            # We'll store label as metadata, ID is unique
            doc_ids.append(f"{lbl}_{_counter}")
            doc_metadatas.append({"thought_label": lbl})
            doc_embeddings.append(embedding_vec)
            _counter += 1

    # Now add them to Chroma
    collection.add(
        embeddings=doc_embeddings,
        metadatas=doc_metadatas,
        ids=doc_ids
    )

    # If you want to persist to disk, call client.persist() if needed
    print("Embeddings stored in ChromaDB collection 'eeg_embeddings'.")
    print("Done!")



if __name__ == "__main__":
    main()