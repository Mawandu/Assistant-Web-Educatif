import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import re

def clean_text(text: str) -> str:
    """Nettoie le texte extrait du PDF."""
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = '\n'.join(line.strip() for line in text.split('\n'))
    return text.strip()

def extract_pages_from_pdf(file_path: str) -> List[Dict]:
    """Extrait le contenu de chaque page et son numéro."""
    doc = fitz.open(file_path)
    pages_content = []
    
    for page_num, page in enumerate(doc):
        raw_text = page.get_text()
        cleaned_text = clean_text(raw_text)
        if len(cleaned_text.strip()) > 50: 
            pages_content.append({
                "page_number": page_num + 1,
                "content": cleaned_text
            })
        else:
            print(f"⚠️  Page {page_num + 1} ignorée (trop courte)")
    
    print(f"✅ {len(pages_content)} pages extraites du PDF")
    return pages_content

def split_text_into_chunks(pages: List[Dict]) -> List[Dict]:
    """Découpe le texte de chaque page en morceaux en conservant les métadonnées."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,        
        chunk_overlap=300,      
        length_function=len,
        separators=[
            "\n\n\n",          
            "\n\n",             
            "\n",               
            ". ",               
            " ",                
            ""
        ]
    )
    
    all_chunks = []
    chunk_global_index = 0
    
    for page in pages:
        page_num = page["page_number"]
        chunks_on_page = text_splitter.split_text(page["content"])
        
        for local_idx, chunk_text in enumerate(chunks_on_page):
            if len(chunk_text.strip()) < 100:  
                print(f"⚠️  Chunk ignoré (trop court) - Page {page_num}")
                continue
            all_chunks.append({
                "text": chunk_text.strip(),
                "metadata": {
                    "page": page_num,
                    "chunk_index_on_page": local_idx,
                    "global_chunk_index": chunk_global_index,
                    "chunk_length": len(chunk_text)
                }
            })
            chunk_global_index += 1
    
    print(f"✅ {len(all_chunks)} chunks créés au total")
    if all_chunks:
        avg_length = sum(c["metadata"]["chunk_length"] for c in all_chunks) / len(all_chunks)
        print(f"📊 Longueur moyenne des chunks : {avg_length:.0f} caractères")  
    return all_chunks
def preview_chunks(chunks: List[Dict], n: int = 3):
    """Affiche les n premiers chunks pour vérifier la qualité du découpage."""
    print(f"\n🔍 Aperçu des {min(n, len(chunks))} premiers chunks :\n")
    
    for i, chunk in enumerate(chunks[:n]):
        text = chunk["text"]
        meta = chunk["metadata"]
        
        print(f"--- Chunk #{i+1} (Page {meta['page']}) ---")
        print(f"Longueur : {meta['chunk_length']} caractères")
        print(f"Texte (100 premiers caractères) : {text[:100]}...")
        print()