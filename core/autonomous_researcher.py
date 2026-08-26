import json
import arxiv
import trafilatura
import ollama
from core.rag_engine import KnowledgeEngine
from core.skill_manager import SkillManager

class AutonomousResearcher:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name
        self.rag = KnowledgeEngine()
        self.skills = SkillManager()

    def deep_research_and_synthesize(self, research_topic: str) -> dict:
        """
        1. تفكيك الموضوع والبحث في مصادر متعددة
        2. فلترة الأبحاث الرديئة وربط المفاهيم
        3. التدقيق والوعي الذاتي
        4. حفظ المهارة والنتائج لمنع النسيان
        """
        print(f"\n🔍 [1/4] تفكيك موضوع البحث والاتصال بمصادر الأبحاث: {research_topic}")
        client = arxiv.Client()
        search = arxiv.Search(query=research_topic, max_results=3, sort_by=arxiv.SortCriterion.Relevance)
        
        extracted_findings = []
        for paper in client.results(search):
            extracted_findings.append({
                "title": paper.title,
                "summary": paper.summary[:600],
                "url": paper.pdf_url
            })

        print("🧠 [2/4] فلترة المعلومات وربط المفاهيم الهندسية...")
        synthesis_prompt = f"""
        Analyze these research papers for topic '{research_topic}':
        {json.dumps(extracted_findings)}
        
        Tasks:
        1. Extract the core mathematical equations and state-of-the-art methods.
        2. Filter out weak or unverified claims.
        3. Connect these findings to practical mechanical and robotics implementation.
        """
        
        synthesis_response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        synthesized_text = synthesis_response['message']['content']

        print("🛡️ [3/4] إجراء الفحص الذاتي والمراقبة الهندسية (Self-Critique)...")
        critique_prompt = f"""
        Review your own engineering synthesis below. Check for physical realism, unit consistency, and manufacturing feasibility.
        Synthesis: {synthesized_text}
        
        Output an enhanced, flawless engineering recommendation and action plan.
        """
        final_critique = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": critique_prompt}]
        )
        flawless_knowledge = final_critique['message']['content']

        print("💾 [4/4] حفظ المعرفة في قاعدة البيانات الدائمة ومكتبة المهارات...")
        # حفظ المعرفة في الذاكرة الدائمة حتى لا ينساها أبداً
        doc_id = f"research_{research_topic.replace(' ', '_')[:30]}"
        self.rag.collection.upsert(
            ids=[doc_id],
            documents=[flawless_knowledge],
            metadatas=[{"source": research_topic, "page": 1}]
        )

        return {
            "status": "success",
            "topic": research_topic,
            "synthesized_knowledge": flawless_knowledge,
            "papers_analyzed": len(extracted_findings)
        }