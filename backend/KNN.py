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
import joblib
from google.cloud import storage
from datetime import datetime
import json

EMBEDDING_DIM = 300
SAMPLING_RATE = 256
WAVELET = 'db4'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

class EEGEmbeddingCNN(nn.Module):
    """
    Maps a feature vector of shape [batch_size, feature_dim] -> [batch_size, EMBEDDING_DIM]
    But we do a small 1D conv to mimic some "spatial" filter effect on the feature dimension.
    """
    def __init__(self, input_dim, embedding_dim=64):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.fc = nn.Linear(64 * input_dim, embedding_dim)

    def forward(self, x):
    #    # x: [batch_size, 1, feature_dim]
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        emb = self.fc(x)
        return emb

def embed_new_sample(eeg_array, model, scaler, device=DEVICE):
    """
    Convert raw EEG (4, num_samples) -> embedding (EMBEDDING_DIM,)
    following the same pipeline: bandpass -> features -> scale -> CNN
    """
    feat_vec = get_feature_vector(eeg_array)
    feat_vec_scaled = scaler.transform(feat_vec.reshape(1, -1))[0]
    model.eval()
    with torch.no_grad():
        t = torch.tensor(feat_vec_scaled, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
        emb = model(t)
    return emb.cpu().numpy().reshape(-1)


def query_chroma_for_embedding(embedding, collection, k=1):
    """
    Given an embedding, query the Chroma collection to find top-k matches.
    Returns Chroma's result dict, e.g. containing 'ids', 'metadatas', 'distances'
    """
    try:
        # Format query according to ChromaDB documentation
        query_emb = [embedding.tolist()]
        results = collection.query(
            query_embeddings=query_emb,
            n_results=k,
            include=['documents', 'metadatas', 'distances']
        )
        return results
    except Exception as e:
        print(f"Detailed query error: {str(e)}")
        return None

def query():
    """
    Example function to show how to embed a random EEG sample
    and retrieve the closest match from Chroma.
    """
    try:
        # 1) Load trained model & scaler
        print("Loading model and scaler...")
        if not os.path.exists("eeg_triplet_cnn.pth"):
            raise FileNotFoundError("Model file 'eeg_triplet_cnn.pth' not found!")
        if not os.path.exists("scaler_triplet.joblib"):
            raise FileNotFoundError("Scaler file 'scaler_triplet.joblib' not found!")
        
        # Calculate input_dim based on your feature extraction
        # Use exactly 2560 samples to match the training data
        test_eeg = np.random.randn(4, 2560)  # Changed from 256 to 2560 to match training
        test_features = get_feature_vector(test_eeg)
        input_dim = len(test_features)
        
        print(f"Calculated input dimension: {input_dim}")
        
        model_load = EEGEmbeddingCNN(input_dim=input_dim, embedding_dim=EMBEDDING_DIM)
        model_load.load_state_dict(torch.load("eeg_triplet_cnn.pth", map_location=DEVICE))
        model_load.to(DEVICE)
        scaler_load = joblib.load("scaler_triplet.joblib")
        print("Model and scaler loaded successfully!")

        # 2) Connect to Chroma
        print("Connecting to ChromaDB...")
        client = chromadb.HttpClient(
            ssl=True,
            host='api.trychroma.com',
            tenant='768c13d0-c1fb-4e76-bd7c-ae5c8732fe8d',
            database='synapse-ai',
            headers={'x-chroma-token': 'ck-6WFPYVNfYg9MZQsNLBzm8mJeoXt3xyMN26W3vh2TscJU'}
        )
        collection = client.get_or_create_collection(name="embeddings_eeg")
        print("Connected to ChromaDB successfully!")
        
        # Debug: Check collection info
        print(f"Collection name: {collection.name}")
        print(f"Collection count: {collection.count()}")
        

        # 3) Load and check CSV
        csv_path = 'cfm9.csv'
        print(f"Loading CSV file: {csv_path}")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file '{csv_path}' not found!")
        
        df = pd.read_csv(csv_path)
        channels = ["TP9", "AF7", "AF8", "TP10"]
        if not all(ch in df.columns for ch in channels):
            raise ValueError(f"CSV must contain columns {channels} for EEG data.")
        
        # Ensure we use exactly 2560 samples, just like in training
        df = df.iloc[:2560]  # Added this line to match training
        raw_eeg = df[channels].values.T
        print(f"Processing EEG data of shape: {raw_eeg.shape}")
        
        # 5) Generate and query embedding
        print("Generating embedding...")
        new_emb = embed_new_sample(raw_eeg, model_load, scaler_load, device=DEVICE)
        print(f"Embedding shape: {new_emb.shape}")  # Add this debug line
        print("Querying ChromaDB...")
        
        results = query_chroma_for_embedding(new_emb, collection, k=1)
        
        print("\nResults:")
        print("--------")
        if results and any(results.values()):  # Check if results contain any data
            print(f"Found matches:")
            if 'distances' in results:
                print(f"Distances: {results['distances']}")
            if 'metadatas' in results:
                print(f"Metadatas: {results['metadatas'][0][0]['thought_label']}")
        else:
            print("No matches found or empty results")
        
        if(results['metadatas'][0][0]['thought_label'] == 'cfm'):
            return 'Child cries for mother'
        elif(results['metadatas'][0][0]['thought_label'] == 'dhp'):
            return 'Doctor Helps Patient'
        elif(results['metadatas'][0][0]['thought_label'] == 'sab'):
            return 'Sister argues with brother'
        elif(results['metadatas'][0][0]['thought_label'] == 'fbh'):
            return 'Fire burns house' 
        else:
            return 'No specific thought pattern detected'
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def main():
    print("Starting main function...")
    result = query()
    print(result)
    print("Query completed.")
    print("Program finished.")
    
    try:
        # Initialize Google Cloud Storage with explicit credentials
        credentials_path = 'credentials.json'  # Make sure this file is in the same directory as KNN.py
        storage_client = storage.Client.from_service_account_json(credentials_path)
        
        bucket_name = 'synapse-ai-bucket'
        bucket = storage_client.bucket(bucket_name)

        # Create the data to store
        data = {
            'thought': result,
            'timestamp': datetime.now().isoformat()
        }

        # Create a unique blob name using the result and timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        blob_name = f"{result}_{timestamp}.json"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(
            json.dumps(data),
            content_type='application/json'
        )
        print(f"Successfully uploaded to {bucket_name}/{blob_name}")
        
    except Exception as e:
        print(f"Error uploading to Google Cloud Storage: {str(e)}")

if __name__ == "__main__":
    print("Script is being run directly")
    main()