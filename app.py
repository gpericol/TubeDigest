from youtube_info import YoutubeInfo
from resume import Resume   
from db import DB

from config_real import *

def main():
    db = DB(video_id)
    YTI = YoutubeInfo(video_id)
    if not db.check_video():
        db.create_video()
        info = YTI.get_video_info()
        db.save_info(info)
    
    Res = Resume(api_key, system_prompt, tokens)
    subs = YTI.get_subs()
    
    # clean subtitles
    subs = " ".join(subs.split("\n"))
    # resume
    chunks_len = 10000
    chunks = Res.split_into_chunks(subs)
    
    while chunks_len > target_chunks:
        # create chunks    
        print(f"resuming {len(chunks)} / {target_chunks}")
        text = Res.resume_text(chunks)
        
        chunks = Res.split_into_chunks(text)
        chunks_len = len(chunks)

        db.save_content(f"{chunks_len}-{tokens}.txt", text)
        
    print(f"chunks: {chunks_len} of {target_chunks}")

if __name__ == "__main__":
    main()