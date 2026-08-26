import trafilatura
from youtube_transcript_api import YouTubeTranscriptApi

def ingest_url_content(url: str) -> dict:
    try:
        if "youtube.com" in url or "youtu.be" in url:
            video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("youtu.be/")[1].split("?")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ar'])
            return {
                "source_type": "youtube",
                "title": f"YouTube_{video_id}",
                "content": " ".join([e['text'] for e in transcript])
            }
        else:
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded, include_tables=True)
            return {
                "source_type": "webpage",
                "title": url.split("//")[-1].split("/")[0],
                "content": text
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}