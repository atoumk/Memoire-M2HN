import os
import re
import streamlit as st
import pandas as pd
import cv2
import sys
from pathlib import Path

src = str(Path.cwd().resolve().parents[1]/ 'src')
sys.path.append(src)
from config.paths import  DATA, EXPERIMENTS, METADATA


image_dirs = [
    os.path.join(DATA, 'cleaned', 'doc_imgs_cleaned'),
    os.path.join(DATA, 'cleaned', 'obj_imgs_cleaned')
]


dataframe_dir = os.path.join(EXPERIMENTS, 'faiss_similarity', 'results')


def remove_last_padding(filename: str) -> str:
    """Remove the last 2-digit underscore padding from a filename before the extension."""
    base_name, ext = os.path.splitext(filename)
    base_name = re.sub(r'_(\d{2})$', '', base_name)
    return base_name + ext

def find_image_path(filename: str) -> str | None:
    """Try to locate the image in any of the configured image directories."""
    for d in image_dirs:
        candidate = os.path.join(d, filename)
        if os.path.exists(candidate):
            return candidate
    return None


df_docs_docs = pd.read_csv(os.path.join(dataframe_dir, "docs_within_docs.csv"))
df_objs_objs = pd.read_csv(os.path.join(dataframe_dir, "objs_within_objs.csv"))
df_doc2obj = pd.read_csv(os.path.join(dataframe_dir, "docs_to_objs.csv"))
df_obj2doc = pd.read_csv(os.path.join(dataframe_dir, "objs_to_docs.csv"))
df_cluster7 = pd.read_csv(os.path.join(dataframe_dir, "c7_within_c7.csv"))

corpus_map = {
    ("Docs", "Docs"): df_docs_docs,
    ("Docs", "Objects"): df_doc2obj,
    ("Objects", "Objects"): df_objs_objs,
    ("Objects", "Docs"): df_obj2doc,
    ("Cluster Test", "Cluster Test"): df_cluster7
}


st.title("Recherche de similarité")

# Corpus 
start_corpus = st.selectbox("Corpus de départ", ["Docs", "Objects", "Cluster Test"])
target_corpus = st.selectbox("Corpus d'arrivée", ["Docs", "Objects", "Cluster Test"])
top_k = st.slider("Nombre de résultats à afficher", min_value=1, max_value=20, value=10)

df_search = corpus_map[(start_corpus, target_corpus)]

# Search bar
query_file = st.text_input("Tapez le nom du fichier à rechercher:")
matches = df_search[df_search['query'].str.contains(query_file, case=False, na=False)]


if not matches.empty:
    selected_query = st.selectbox("Fichier trouvé:", matches['query'].tolist())
    row = matches[matches['query'] == selected_query].iloc[0]

    # Query 
    query_filename = remove_last_padding(selected_query)
    query_path = find_image_path(query_filename)

    st.subheader("Image choisie")
    if query_path is None:
        st.error(f"Fichier introuvable dans {len(image_dirs)} dossiers : {query_filename}")
    else:
        img = cv2.imread(query_path)
        if img is None:
            st.error(f"Impossible de lire l'image : {query_path}")
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img, use_container_width=True)

    # Top-K matches
    st.subheader(f"Top {top_k} correspondances")
    match_imgs = []
    for i in range(top_k):
        col_path_key = f"top{i}_path"
        if col_path_key in row and pd.notna(row[col_path_key]):
            match_filename = remove_last_padding(row[col_path_key])
            match_path = find_image_path(match_filename)
            if match_path:
                match_imgs.append(match_path)
            else:
                st.warning(f"Fichier manquant pour Top {i+1}: {match_filename}")

    cols = st.columns(5)
    for idx, path in enumerate(match_imgs):
        img_match = cv2.imread(path)
        if img_match is not None:
            img_match = cv2.cvtColor(img_match, cv2.COLOR_BGR2RGB)
            cols[idx % 5].image(img_match, caption=f"Top {idx+1}", use_container_width=True)
        else:
            cols[idx % 5].warning(f"Impossible de lire Top {idx+1}")
else:
    st.warning("Aucun fichier correspondant trouvé.")