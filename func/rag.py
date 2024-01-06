import os
import shutil
import tempfile
import requests

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores.utils import DistanceStrategy
from langchain.text_splitter import CharacterTextSplitter

def download(args: dict):
    if not 'dir' in args:
        raise ValueError('require dir')

    if 'zip_url' in args:
        res = requests.get(args['zip_url'])
        print(len(res.content))

        with tempfile.NamedTemporaryFile(suffix=".zip") as t:
            with open(t.name, 'wb') as f:
                f.write(res.content)
        
            shutil.unpack_archive(t.name, f"rag/{args['dir']}")
    elif 'url' in args:
        os.makedirs(f"rag/{args['dir']}", exist_ok=True)
        res = requests.get(args['url'])

        filepath = f"rag/{args['dir']}/{os.path.basename(args['url'])}"
        with open(filepath, 'wb') as f:
            f.write(res.content)
    elif 'text' in args:
        os.makedirs(f"rag/{args['dir']}", exist_ok=True)

        filepath = f"rag/{args['dir']}/text.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(args['text'])

def docs_load(args: dict):
    loader = GenericLoader.from_filesystem(
        path=f"rag/{args['dir']}",
        glob="**/[!.]*",
        show_progress=True,
    )

    docs = loader.load()
    print(docs)
    return docs

def split(docs, args: dict):
    text_splitter = CharacterTextSplitter(
        separator='\n\n',
        chunk_size=args['chunk_size'],
        chunk_overlap=0,
        length_function=len
    )
    chunk_docs = text_splitter.create_documents([doc.page_content for doc in docs])
    print(chunk_docs)
    return chunk_docs

def vector(docs, args: dict):
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    vector_store = FAISS.from_documents(documents=docs,
                                        embedding=embeddings, 
                                        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
                                        normalize_L2=True)
    return vector_store

def vector_save(docs, args: dict):
    vector_store = vector(docs, args)
    folder_path = f"rag/{args['dir']}/vector"
    vector_store.save_local(folder_path=folder_path)

    return vector_store

def vector_load(args: dict):
    folder_path = f"rag/{args['dir']}/vector"
    if not os.path.exists(folder_path):
        raise ValueError(f"missing rag/{args['dir']}/vector")

    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    vector_store = FAISS.load_local(folder_path=folder_path,
                                    embeddings=embeddings, 
                                    distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
                                    normalize_L2=True)
    return vector_store

def search(vector_store, args: dict):
    results = vector_store.similarity_search_with_score(query=args['query'], k=args['k'])
    print(results)
    detail = []
    for r in results:
        detail.append([r[0].page_content, float(r[1])])
    return results[0][0].page_content, detail

def load_dirs():
    dirs = []
    for name in os.listdir('rag'):
        dirs.append(name)

    return dirs

def upload(dir, chunk_size, file):
    if not dir:
        raise ValueError('require dir')

    args = {
        'dir': dir,
        'chunk_size': int(chunk_size),
        }
    shutil.unpack_archive(file.name, f"rag/{args['dir']}")
    docs = docs_load(args)
    if args['chunk_size'] > 0:
        docs = split(docs, args)
    vector_save(docs, args)

    return f"saved rag/{args['dir']}"
