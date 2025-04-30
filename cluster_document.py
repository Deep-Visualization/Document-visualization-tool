import pandas as pd
from sklearn.cluster import KMeans

# Load the document-term matrix
df = pd.read_csv("Source Code/document_term_matrix.csv", index_col=0)


# Extract document names and feature values
doc_names = df.index.tolist()
X = df.values

# Apply KMeans clustering
k = 5  # Change this number as needed
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# Get cluster labels
labels = kmeans.labels_

# Create DataFrame of document names and cluster labels
clustered_df = pd.DataFrame({
    "Document": doc_names,
    "Cluster": labels
})

# Save to CSV
clustered_df.to_csv("document_clusters.csv", index=False)

print("✅ Done! Saved clustering results to 'document_clusters.csv'")
