from youtube_info import YoutubeInfo
from resume import Resume   

from config_real import *

def main():
    YTI = YoutubeInfo(video_id)
    Res = Resume(api_key, system_prompt, tokens)
    print(YTI.get_video_info())
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

        with open(f"{chunks_len}-{tokens}.txt", "wb") as f:
            f.write(text.encode("UTF-8"))

        
    print(f"chunks: {chunks_len} of {target_chunks}")

if __name__ == "__main__":
    main()