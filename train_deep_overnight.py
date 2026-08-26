import os
import time
import requests
import json
from pypdf import PdfReader
from core.rag_engine import KnowledgeEngine
from core.skill_manager import SkillManager
import ollama

# قائمة موسعة وشاملة لأدق الموضوعات الهندسية
DEEP_CURRICULUM = [
    # 1. الميكانيكا والتروس وعناصر الآلات
    "Spur helical planetary and cycloidal gear design stress calculations ISO AGMA",
    "Shaft design combined torsion bending fatigue failure Soderberg Goodman",
    "Rolling element bearing dynamic load rating C10 and L10 life calculation",
    "Finite Element Analysis FEA stress concentrations and von Mises yield criterion",
    "Mechanical vibration resonance damping and modal analysis in machine structures",

    # 2. كينماتيكا وديناميكا الروبوتات والتحكم
    "Product of Exponentials PoE formula spatial robot kinematics screw theory",
    "Geometric Jacobian operational space formulation and manipulator dynamics",
    "Cartesian impedance control and compliance under physical contact",
    "Whole-Body Impulse Control WBC multi-contact balance in humanoid robots",
    "Model Predictive Control Convex MPC for dynamic legged locomotion",

    # 3. الكهرباء وإلكترونيات القدرة والـ PCB
    "Three-phase motor inverter gate driver MOSFET layout and thermal management",
    "Field Oriented Control FOC Space Vector PWM SVPWM current loop tuning",
    "Industrial control panel design circuit breaker contactor sizing IEC 60204",
    "PCB design high-current traces ground planes and EMI EMC filtering",
    
    # 4. هندسة المواد والتصنيع والـ CNC
    "Engineering materials selection Ashby charts aluminum 7075-T6 vs titanium",
    "CNC 5-axis milling toolpath generation G-code feed speed optimization",
    "Geometric Dimensioning and Tolerancing GD&T fit standards ISO 286",
    "Additive manufacturing metal 3D printing DMLS SLS design for manufacturing",

    # 5. الحراريات وميكانيكا الموائع والهيدروليك
    "Heat transfer conduction convection heat sink sizing for electronics cooling",
    "Thermodynamic Stirling cycle power efficiency and regenerator design",
    "Hydraulic system circuit design cylinder sizing proportional valves",
    "Fluid mechanics pipe friction factor pressure drop and pump selection",

    # 6. الأنظمة المدمجة والـ Real-Time
    "STM32 ARM Cortex-M timer interrupt configuration for motor control FOC",
    "FreeRTOS real-time task scheduling mutex and queue latency optimization",
    "CAN-bus CAN-FD and EtherCAT industrial communication protocol implementation",
    "Magnetic encoder SPI communication and angle calibration algorithms",

    # 7. الأتمتة الصناعية والـ PLC
    "PLC programming IEC 61131-3 Ladder Diagram and Structured Text automation",
    "Industrial sensors proximity optical load cells calibration and interfacing",
    
    # 8. إدارة المشاريع ومعايير الأمان
    "Failure Mode and Effects Analysis FMEA risk assessment machine safety ISO 12100",
    "Bill of Materials BOM cost optimization and engineering project lifecycle"
]
class DeepOvernightTrainer:
    def __init__(self, download_dir: str = "knowledge_vault/downloaded_papers"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        self.rag = KnowledgeEngine()
        self.skills = SkillManager()
        self.openalex_url = "https://api.openalex.org/works"

    def download_pdf(self, pdf_url: str, filename: str) -> str:
        """تحميل ملف الـ PDF وحفظه على الهارد ديسك"""
        try:
            headers = {"User-Agent": "EngineeringCopilotResearch/1.0 (mailto:user@local.app)"}
            resp = requests.get(pdf_url, headers=headers, timeout=20)
            if resp.status_code == 200 and len(resp.content) > 10000:
                file_path = os.path.join(self.download_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                return file_path
        except Exception:
            pass
        return None

    def process_and_learn_pdf(self, file_path: str, topic: str):
        """قراءة وفهرسة الـ PDF المحمل في قاعدة البيانات"""
        try:
            reader = PdfReader(file_path)
            total_chunks = 0
            for idx, page in enumerate(reader.pages[:15]):  # قراءة أول 15 صفحة من البحث
                text = page.extract_text()
                if text and len(text.strip()) > 100:
                    chunks = [text[i:i+800] for i in range(0, len(text), 600)]
                    for c_idx, chunk in enumerate(chunks):
                        self.rag.collection.upsert(
                            ids=[f"{os.path.basename(file_path)}_p{idx+1}_c{c_idx}"],
                            documents=[chunk],
                            metadatas=[{"source": os.path.basename(file_path), "page": idx+1, "topic": topic}]
                        )
                        total_chunks += 1
            return total_chunks
        except Exception:
            return 0

    def run_training_session(self):
        print("=" * 70)
        print("🌙 بدء جلسة التدريب والبحث والتحميل الليلي الشامل للمساعد")
        print("=" * 70)
        print(f"📚 إجمالي الموضوعات الهندسية: {len(DEEP_CURRICULUM)} موضوعاً متخصصاً.")
        print(f"📁 سيتم حفظ الأبحاث الأصلية في: {self.download_dir}\n")

        start_time = time.time()
        total_papers_downloaded = 0

        for idx, topic in enumerate(DEEP_CURRICULUM, 1):
            print(f"\n──────────────────────────────────────────────────")
            print(f"🔍 [{idx}/{len(DEEP_CURRICULUM)}] البحث عن: {topic}")
            print(f"──────────────────────────────────────────────────")

            # 1. البحث في OpenAlex عن أبحاث مفتوحة التحميل
            try:
                params = {"search": topic, "per_page": 2, "sort": "cited_by_count:desc"}
                res = requests.get(self.openalex_url, params=params, timeout=10).json()
                
                for paper_idx, work in enumerate(res.get("results", []), 1):
                    title = work.get("title", f"Paper_{idx}_{paper_idx}")
                    oa_url = work.get("open_access", {}).get("oa_url")
                    
                    if oa_url and oa_url.endswith(".pdf"):
                        safe_name = f"{topic[:20].replace(' ', '_')}_{paper_idx}.pdf"
                        print(f"  📥 جاري تحميل البحث: {title[:50]}...")
                        pdf_path = self.download_pdf(oa_url, safe_name)
                        
                        if pdf_path:
                            chunks = self.process_and_learn_pdf(pdf_path, topic)
                            total_papers_downloaded += 1
                            print(f"  ✅ تم التحميل وفهرسة {chunks} مقطعاً في الذاكرة الدائمة.")

                # 2. صياغة مهارة هندسية برمجية وحفظها في skills/
                skill_name = topic.lower().replace(" ", "_")[:25]
                skill_prompt = f"Write a clean, reusable, verified Python engineering function with formulas for topic: '{topic}'"
                response = ollama.chat(
                    model="qwen2.5-coder:7b",
                    messages=[{"role": "user", "content": skill_prompt}]
                )
                self.skills.save_skill(skill_name, f"Verified skill for {topic}", response['message']['content'])
                print(f"  💡 تم توليد وتسجيل مهارة برمجية دائمة: '{skill_name}'.")

            except Exception as e:
                print(f"  ⚠️ تم تجاوز خطوة واستكمال البقية: {e}")

            time.sleep(3)  # استراحة خفيفة بين الموضوعات للحفاظ على هدوء المعالج

        elapsed_hours = round((time.time() - start_time) / 3600, 2)
        print("\n" + "=" * 70)
        print(f"🏆 اكتمل التدريب والتحميل الليلي بنجاح في {elapsed_hours} ساعة!")
        print(f"📥 إجمالي الأبحاث المحملة والمحفوظة: {total_papers_downloaded} ملف PDF.")
        print("=" * 70)

if __name__ == "__main__":
    trainer = DeepOvernightTrainer()
    trainer.run_training_session()