#!/usr/bin/env python3

from lib.youtube_info import YoutubeInfo
from lib.resume import Resume   
from lib.db import DB
import argparse

from config_real import *

def process_arguments():
    parser = argparse.ArgumentParser(description="TubeDigest: transforms YouTube videos into concise, digestible summaries.")
    parser.add_argument('video', help='URL or video code of Youtube video')
    parser.add_argument('-f', '--force', action='store_true', help='Download the subtitles and create summaries even if they are already present in the database, overwriting them.', required=False)
    parser.add_argument('-d', '--delete', action='store_true', help='Remove the data related to the video.', required=False)

    return parser.parse_args()

def main(args):
    YTI = YoutubeInfo(args.video)
    video_id = YTI.video_id
    db = DB(video_id)
    
    if args.delete:
        if db.check_video():
            db.delete_video()
            print(f"[-] {video_id} deleted")
        else:
            print(f"[-] {video_id} doesn't exists")
        exit()
    
    if db.check_video() and not args.force:
        print(f"{db.get_path()}")
        exit()

    if db.check_video() and args.force:
        print(f"{video_id} exists and will be partially overwritten.")

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
        print(f"[+] Resuming from {len(chunks)} chunks to {target_chunks} chunks expected")
        text = Res.resume_text(chunks)
        
        chunks = Res.split_into_chunks(text)
        chunks_len = len(chunks)

        db.save_content(f"{chunks_len}-{tokens}.txt", text)
        
    print(f"[+] Best result is {chunks_len} chunks of {target_chunks} expected")
    print(f"{db.get_path()}")


if __name__ == "__main__":
    args = process_arguments()
    main(args)