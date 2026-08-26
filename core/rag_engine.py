import os
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

class KnowledgeEngine:
    def __init__(self, vault_path: str = "knowledge_vault"):
        self.vault_path = vault_path
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="engineering_references",
            embedding_function=self.embedding_func
        )

    def ingest_pdfs(self):
        """فحص وقراءة جميع ملفات PDF داخل كافة المجلدات الفرعية وتصنيفها"""
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
            return "تم إنشاء مجلد knowledge_vault الرئيسي."

        total_chunks = 0
        indexed_files = []

        # المرور على كافة المجلدات الفرعية بعمق (Recursive Traversal)
        for root, dirs, files in os.walk(self.vault_path):
            category = os.path.basename(root)
            if category == "knowledge_vault":
                category = "general"

            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    try:
                        reader = PdfReader(file_path)
                        for idx, page in enumerate(reader.pages):
                            text = page.extract_text()
                            if text and len(text.strip()) > 50:
                                # تقسيم الصفحة لمقاطع مناسبة
                                chunks = [text[i:i+800] for i in range(0, len(text), 600)]
                                for c_idx, chunk in enumerate(chunks):
                                    doc_id = f"{file}_p{idx+1}_c{c_idx}"
                                    self.collection.upsert(
                                        ids=[doc_id],
                                        documents=[chunk],
                                        metadatas=[{
                                            "source": file,
                                            "category": category,
                                            "page": idx + 1
                                        }]
                                    )
                                    total_chunks += 1
                        indexed_files.append(f"{file} ({category})")
                    except Exception as e:
                        print(f"⚠️ تعذر قراءة الملف {file}: {e}")

        return f"✅ تمت فهرسة {total_chunks} مقطعاً بنجاح من {len(indexed_files)} ملفات موزعة على التخصصات."

    def search_knowledge(self, query: str, category: str = None, n_results: int = 3) -> str:
        """البحث الذكي الموجه بالتخصص لمنع التشتت"""
        where_filter = {"category": category} if category else None
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            if not results["documents"] or not results["documents"][0]:
                return "لم يتم العثور على مراجع مطابقة في قاعدة المعرفة."
            
            output = ""
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                output += f"\n[مرجع: {meta['source']} | التخصص: {meta['category']} | صفحة: {meta['page']}]\n{doc}\n"
            return output
        except Exception as e:
            return f"خطأ أثناء البحث في المراجع: {str(e)}"