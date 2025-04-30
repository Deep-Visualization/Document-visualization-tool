import pandas as pd
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
import json

# Load MDS data
df = pd.read_csv('VAProject3.csv')
documentNames = df['Unnamed: 0']
X = df.drop(columns=['Unnamed: 0']).values

# Load cluster labels
cluster_df = pd.read_csv('document_clusters.csv')
cluster_dict = dict(zip(cluster_df['Document'], cluster_df['Cluster']))

# MDS computation
dissimilarities = pairwise_distances(X, metric='euclidean')
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
X_mds = mds.fit_transform(dissimilarities)

# Build output with clusters
mds_data = []
for doc, (x, y) in zip(documentNames, X_mds):
    cluster = int(cluster_dict.get(doc, -1))  # fallback to -1 if missing
    mds_data.append({
        "id": doc,
        "x": float(x),
        "y": float(y),
        "cluster": cluster
    })

# Save to JSON
with open("mds_data.json", "w") as f:
    json.dump(mds_data, f, indent=4)

print("✅ mds_data.json with cluster info saved!")
