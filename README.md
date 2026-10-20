# Document Explorer

An interactive visual analytics tool for exploring a collection of text documents: grouping them into clusters, mapping how similar they are, and reading them side by side.

Built by **Deepthi Kavitha** for the Data Visualization course in the M.S. in Computer and Information Science program at the **University of Massachusetts Dartmouth**.

**Live site:** _add your GitHub Pages link here_

---

## What you can do

| Feature | What it does |
|---|---|
| **Cluster filters** | Tick or untick clusters in the bar at the top (it stays in place as you scroll). The document list, bubble chart and MDS plot all update together. |
| **Document list** | Documents grouped by cluster, with a count for each. Click a document to open it, or **Open All** to open a whole cluster. Drag a cluster's heading to reorder the clusters. |
| **Search** | Type in the search box to filter the document list by name. |
| **Document workspace** | Read the documents you opened side by side. Each has a **Close** button; **Reset Workspace** clears them all. The workspace is always as tall as the document list and scrolls inside. |
| **Cluster bubble chart** | Every document is a bubble, grouped and labeled by cluster. Hover for its name and cluster; click to open it and enlarge the bubble. |
| **MDS plot** | Documents placed by similarity (closer means more alike), colored by cluster. Hovering a point highlights the same document in the list; clicking opens it. |
| **Light and dark mode** | Opens in light mode; the **Dark Mode** button switches. |

---

## How it works

The analysis runs in Python ahead of time, and the website reads its results.

```
dataset/ (116 text files)
   │
   ▼  tokens.py: tokenizing, stop-word removal, stemming (NLTK),
   │              named-entity extraction for people, places, dates and organizations (spaCy)
   │
   ├─▶ filtered_extracted_entities.csv   entities found in each document
   └─▶ document_term_matrix.csv          116 documents × 700 entity terms
          │
          ▼  cluster_document.py: K-means clustering, k = 5 (scikit-learn)
          │
          └─▶ document_clusters.csv      cluster for each document
                 │
                 ▼  mds.py: multidimensional scaling on Euclidean distances (scikit-learn),
                 │          using the key-term counts in VAProject3.csv
                 │
                 └─▶ mds_data.json       x, y position and cluster for each document
```

`index.html` loads `document_clusters.csv` and `mds_data.json` with D3, and opens each document's text straight from the `dataset/` folder.

---

## Built with

- **D3.js v7:** bubble chart (force layout), MDS scatter plot, data loading
- **jQuery and jQuery UI:** document list, workspace and drag-to-reorder clusters
- **HTML and CSS:** pistachio theme in `theme.css` (light and dark), with headings in Playfair Display and body text in Poppins
- **Python:** pandas, NLTK, spaCy and scikit-learn for the text processing, clustering and MDS
- **GitHub Pages** for hosting

---

## Project structure

```
index.html                       The website: layout, styles and all interactive charts
theme.css                        Page colors for light and dark mode (chart colors are set in index.html)
dataset/                         The 116 text documents
tokens.py                        Text cleaning, entity extraction, document-term matrix
cluster_document.py              K-means clustering
mds.py                           MDS layout
document_term_matrix.csv         Entity counts per document (input to clustering)
filtered_extracted_entities.csv  People, places, dates and organizations per document
extracted_entities.csv           Cleaned text and entities per document
document_clusters.csv            Cluster for each document (used by the website)
VAProject3.csv                   Key-term counts per document (input to MDS)
mds_data.json                    MDS positions and clusters (used by the website)
```

---

## Run it locally

The page loads CSV, JSON and text files, which browsers block when a page is opened directly from your computer, so serve the folder with a small local web server:

```bash
# from the project folder
python -m http.server 8000
```

Then open **http://localhost:8000/index.html**. In VS Code you can instead right-click `index.html` and choose **Open with Live Server**.

An internet connection is needed, because D3, jQuery and the fonts load from the web.

### Re-running the analysis

```bash
pip install pandas nltk spacy scikit-learn
python -m spacy download en_core_web_sm
python tokens.py
python cluster_document.py
python mds.py
```

The scripts still contain the folder paths from where they were first run (for example `"569/Project 2/dataset"` in `tokens.py` and `"Source Code/document_term_matrix.csv"` in `cluster_document.py`). Change these to `dataset` and `document_term_matrix.csv` before running them from this folder.

---

## Findings and limitations

- **One large cluster.** 112 of the 116 documents fall into Cluster 1. Each of the other four clusters holds a single file: `CIA_docs.txt`, `DIA_docs.txt`, `FBI_docs.txt` and `NSA_docs.txt`. These appear to be combined files of each agency's reports, so they're far longer than the individual reports and K-means separates them out. Removing the combined files before clustering should give clusters that divide the individual reports more meaningfully.
- **MDS uses a few key terms.** The MDS layout is based on counts of seven terms in `VAProject3.csv` (america, london, paris, cia, fbi, abdul and martin), not the full 700-term matrix used for clustering. 63 of the 116 documents mention none of these terms, so they all land on the same spot. The 116 documents occupy only 35 distinct positions, and many points sit on top of each other.
- **K is fixed.** The number of clusters is set by hand (k = 5) rather than chosen by a measure such as the silhouette score.

---

## Author

**Deepthi Kavitha** · M.S. Computer and Information Science, University of Massachusetts Dartmouth
[LinkedIn](https://www.linkedin.com/in/deepthigokuldhas) · [GitHub](https://github.com/Deep-Visualization)
