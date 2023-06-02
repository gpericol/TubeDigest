import re
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup

class YoutubeInfo:
    def __init__(self, video_id):
        self.video_id = self._extract_video_id(video_id)
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"

    def _extract_video_id(self, url):
        video_id = None
        
        if "youtube.com" in url:
            match = re.search(r"watch\?v=([A-Za-z0-9_-]+)", url)
            if match:
                video_id = match.group(1)        
        else:
            match = re.search(r"([A-Za-z0-9_-]+)", url)
            if match:
                video_id = match.group(1)
        
        if video_id == None:
            raise Exception("Can't extract video_id")
        
        return video_id

    def _get_best_subtitles(self):
        transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)

        for transcript in transcript_list:
            return transcript.language_code
            
        raise Exception("No srt available")

    def get_subs(self):
        srt = YouTubeTranscriptApi.get_transcript(self.video_id, [self._get_best_subtitles()])

        if srt == None:
            raise Exception("No srt available")

        # clean text
        text = "\n".join(line["text"].strip() for line in srt)

        return text


    def get_video_info(self):
        r = requests.get(self.url)
        s = BeautifulSoup(r.text, "html.parser")
        title = s.find("title").text.replace("\n", "")
    
        author = s.find("span",itemprop="author")
        author_url = author.find("link",itemprop="url")['href']
        author_name = author.find("link",itemprop="name")['content']

        # returning the dictionary
        return {
            "title": title,
            "author_name": author_name,
            "author_url": author_url,
            "url": self.url,
            "video_id": self.video_id
        }