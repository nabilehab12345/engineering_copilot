import json
import ollama
from core.global_researcher import GlobalResearchEngine
from core.skill_manager import SkillManager
from core.rag_engine import KnowledgeEngine

class TrainingModeEngine:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name
        self.researcher = GlobalResearchEngine()
        self.skills = SkillManager()
        self.rag = KnowledgeEngine()

    def train_on_engineering_topic(self, topic: str) -> str:
        """
        تشغيل دورة تدريبية كاملة للمساعد على موضوع محدد:
        1. البحث في مصادر الأبحاث العالمية
        2. استخراج القوانين
        3. كتابة وتوثيق كود المهارة وحفظها
        """
        print(f"\n🎓 [Training Mode] بدء تدريب المساعد على: {topic}")
        
        # 1. البحث عن أحدث الأوراق العلمية الموثوقة
        print("📖 [1/3] البحث عن المراجع والأوراق المحكمة...")
        search_results = self.researcher.search_global_academic_works(topic, max_results=3)
        papers = search_results.get("papers_found", [])

        # 2. دراسة الأبحاث واستخراج القوانين البرمجية
        print("🧠 [2/3] استيعاب المنهجيات واستنتاج المعادلات الرياضية...")
        study_prompt = f"""
        You are in Autonomous Training Mode. Study these academic works on '{topic}':
        {json.dumps(papers)}
        
        Your Goal:
        1. Extract the primary engineering formulas and physical parameters.
        2. Write a verified, clean, reusable Python function implementing these formulas.
        3. Explain the physics and assumptions clearly in English.
        """
        
        study_response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": study_prompt}]
        )
        lesson_learned = study_response['message']['content']

        # 3. حفظ المهارة في مجلد المهارات الدائم
        print("💾 [3/3] حفظ المهارة الجديدة في مكتبة المهارات وقاعدة المعرفة...")
        skill_name = topic.lower().replace(" ", "_")[:25]
        self.skills.save_skill(
            skill_name=skill_name,
            description=f"Auto-trained skill for {topic}",
            python_code=lesson_learned
        )
        
        # حفظ المعرفة في قاعدة البيانات
        self.rag.collection.upsert(
            ids=[f"trained_{skill_name}"],
            documents=[lesson_learned],
            metadatas=[{"source": f"Training: {topic}", "page": 1}]
        )

        return f"✅ [Training Complete] Successfully mastered topic: '{topic}' and registered new permanent skill '{skill_name}'."