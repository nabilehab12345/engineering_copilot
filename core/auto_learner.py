import arxiv
from apscheduler.schedulers.background import BackgroundScheduler
from core.rag_engine import KnowledgeEngine

class AutonomousLearner:
    def __init__(self, topics: list = None):
        self.topics = topics or [
            "quadruped robot reinforcement learning",
            "brushless motor field oriented control",
            "sim-to-real robotics mujoco"
        ]
        self.rag = KnowledgeEngine()
        self.scheduler = BackgroundScheduler()

    def discover_and_learn(self):
        client = arxiv.Client()
        count = 0
        for topic in self.topics:
            search = arxiv.Search(query=topic, max_results=2, sort_by=arxiv.SortCriterion.SubmittedDate)
            for paper in client.results(search):
                doc_id = f"arxiv_{paper.entry_id.split('/')[-1]}"
                content = f"Title: {paper.title}\nSummary: {paper.summary}"
                self.rag.collection.upsert(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{"source": paper.title, "page": 1}]
                )
                count += 1
        print(f"\n🧠 [Auto-Learner] تم سحب واستيعاب {count} أبحاث جديدة من arXiv تلقائياً.")

    def start(self, hour: int = 3):
        self.scheduler.add_job(self.discover_and_learn, 'cron', hour=hour)
        self.scheduler.start()