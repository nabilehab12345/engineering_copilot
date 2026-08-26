import os
import streamlit as st
from pypdf import PdfReader
from core.agent import EngineeringAgent
from core.auto_learner import AutonomousLearner
from tools.web_learner import ingest_url_content

# ضبط مظهر وعنوان الصفحة
st.set_page_config(
    page_title="Robotics & Mechanical Engineering Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة المساعد ومحركات التعلم
@st.cache_resource
def load_system():
    agent = EngineeringAgent()
    learner = AutonomousLearner()
    return agent, learner

agent, learner = load_system()

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ Engineering Control Panel")
    st.caption("Universal Robotics & Machine Design AI")
    st.markdown("---")

    # 1. قسم رفع وتصنيف المراجع الهندسية
    st.subheader("📚 Ingest Textbooks & Papers")
    
    # اختيار التخصص الهندسي لتصنيف الكتاب بدقة
    categories = [
        "01_mechanical_design",
        "02_robotics_and_control",
        "03_mechatronics_and_bldc",
        "04_electrical_and_power",
        "05_materials_and_manufacturing",
        "06_thermal_and_hydraulics",
        "07_embedded_and_realtime",
        "08_automation_and_plc"
    ]
    selected_category = st.selectbox("Select Engineering Domain:", categories)
    uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"])

    if uploaded_pdf is not None:
        if st.button("📥 Index & Ingest to Vault", use_container_width=True):
            with st.spinner("Processing and chunking document..."):
                # حفظ الملف فيزيائياً في مجلده الصحيح
                save_dir = os.path.join("knowledge_vault", selected_category)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                file_save_path = os.path.join(save_dir, uploaded_pdf.name)
                with open(file_save_path, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())

                # قراءة وفهرسة الصفحات في ChromaDB
                reader = PdfReader(uploaded_pdf)
                chunks_count = 0
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and len(text.strip()) > 50:
                        chunks = [text[i:i+800] for i in range(0, len(text), 600)]
                        for c_idx, chunk in enumerate(chunks):
                            agent.rag.collection.upsert(
                                ids=[f"{uploaded_pdf.name}_p{idx+1}_c{c_idx}"],
                                documents=[chunk],
                                metadatas=[{
                                    "source": uploaded_pdf.name,
                                    "category": selected_category,
                                    "page": idx + 1
                                }]
                            )
                            chunks_count += 1
                st.success(f"✅ Ingested {chunks_count} passages into '{selected_category}'!")

    st.markdown("---")

    # 2. قسم التعلم من الروابط واليوتيوب
    st.subheader("🌐 Ingest Web & YouTube")
    url_input = st.text_input("Enter URL (Article or YouTube)")
    if st.button("🔗 Learn from Link", use_container_width=True):
        if url_input:
            with st.spinner("Ingesting content..."):
                res = ingest_url_content(url_input)
                if "content" in res and res["content"]:
                    agent.rag.collection.upsert(
                        ids=[f"url_{res['title'][:30]}"],
                        documents=[res["content"]],
                        metadatas=[{"source": res["title"], "category": "web_ingested", "page": 1}]
                    )
                    st.success(f"✅ Successfully ingested [{res['source_type']}]!")
                else:
                    st.error(f"❌ Error: {res.get('message')}")

    st.markdown("---")

    # 3. زر التعلم الذاتي التلقائي
    if st.button("🧠 Run Auto-Discovery (arXiv)", use_container_width=True):
        with st.spinner("Fetching latest global robotics research..."):
            learner.discover_and_learn()
            st.success("✅ Latest research papers ingested into ChromaDB!")

    st.markdown("---")
    
    # 4. زر مسح المحادثة وبدء جلسة جديدة
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# واجهة المحادثة الرئيسية
st.title("🤖 Engineering AI Copilot")
st.markdown("Your **Autonomous Senior Partner** for Mechanical Design, Robotics Kinematics, Electrical Control Panels, and Physics Simulation.")

# إدارة سجل الرسائل
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello Engineer! I am fully connected to your engineering libraries, ChromaDB vault, and calculation tools. How can I assist you today with CAD design, calculations, kinematics, or panel sizing?"
        }
    ]

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# إدخال سؤال جديد
if user_prompt := st.chat_input("Ask a calculation, CAD generation, kinematics derivation, or circuit design..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing and calculating with deterministic tools..."):
            response = agent.chat(user_prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})