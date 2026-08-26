from core.agent import EngineeringAgent
from core.auto_learner import AutonomousLearner
from tools.web_learner import ingest_url_content

def main():
    print("=" * 60)
    print("🤖 Engineering Copilot: Robotics & Machine Design AI")
    print("=" * 60)

    agent = EngineeringAgent()
    learner = AutonomousLearner()
    learner.start(hour=3)

    print("\n💡 Quick Commands:")
    print(" - Type 'scan' to index all PDFs in knowledge_vault folder.")
    print(" - Type 'learn: <URL>' to ingest web articles or YouTube videos.")
    print(" - Type 'auto' to fetch and index latest robotics papers from arXiv.")
    print(" - Type 'exit' to quit.\n")

    while True:
        try:
            prompt = input("👤 You: ").strip()
            if not prompt:
                continue
            if prompt.lower() in ["exit", "quit", "bye"]:
                learner.scheduler.shutdown()
                print("Goodbye!")
                break

            if prompt.lower() == "scan":
                print("⏳ Indexing documents...")
                print(agent.rag.ingest_pdfs())
                continue

            if prompt.startswith("learn:"):
                url = prompt.replace("learn:", "").strip()
                print(f"⏳ Ingesting URL: {url} ...")
                res = ingest_url_content(url)
                if "content" in res and res["content"]:
                    agent.rag.collection.upsert(
                        ids=[f"url_{res['title'][:30]}"],
                        documents=[res['content']],
                        metadatas=[{"source": res['title'], "page": 1}]
                    )
                    print(f"✅ Ingested content from [{res['source_type']}] successfully!")
                else:
                    print(f"❌ Error: {res.get('message')}")
                continue

            if prompt.lower() == "auto":
                learner.discover_and_learn()
                continue

            print("\n🤖 Copilot is thinking and calculating...")
            reply = agent.chat(prompt)
            print(f"\n{reply}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            learner.scheduler.shutdown()
            print("\nShutting down.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()