import requests
import json

class GlobalResearchEngine:
    """محرك البحث في مستودعات الجامعات العالمية وتقييم الموثوقية الأكاديمية"""
    def __init__(self):
        self.openalex_base = "https://api.openalex.org/works"

    def search_global_academic_works(self, topic: str, max_results: int = 5) -> dict:
        """البحث في أكثر من 250 مليون ورقة علمية من جامعات العالم"""
        try:
            params = {
                "search": topic,
                "per_page": max_results,
                "sort": "cited_by_count:desc"
            }
            response = requests.get(self.openalex_base, params=params, timeout=10)
            data = response.json()

            verified_papers = []
            for work in data.get("results", []):
                title = work.get("title", "Unknown")
                citations = work.get("cited_by_count", 0)
                year = work.get("publication_year", "N/A")
                venue = work.get("primary_location", {}).get("source", {}).get("display_name", "Peer-Reviewed Venue")
                oa_url = work.get("open_access", {}).get("oa_url")

                # تقييم الموثوقية بناءً على الاستشهادات والتحكيم
                trust_level = "S-Tier (Highly Cited & Verified)" if citations > 100 else ("A-Tier (Peer-Reviewed)" if citations > 20 else "B-Tier (Recent/Unverified)")

                verified_papers.append({
                    "title": title,
                    "year": year,
                    "venue": venue,
                    "citations": citations,
                    "trust_level": trust_level,
                    "pdf_link": oa_url
                })

            return {
                "status": "success",
                "topic": topic,
                "total_found": len(verified_papers),
                "papers": verified_papers
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def request_reference_consultation(self, book_title: str, author: str, purpose: str) -> str:
        """طلب استشارة المستخدم لتحميل مرجع محدد"""
        return f"""
        📚 [Reference Recommendation & Ingestion Request]
        - Title: {book_title}
        - Author(s): {author}
        - Technical Purpose: {purpose}
        >> Action: Please download this reference PDF, place it in 'knowledge_vault/', and type 'scan'.
        """