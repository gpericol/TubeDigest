import os
import shutil
import json

class DB:
    def __init__(self, video_id, path="output/"):
        self.path = path
        self.video_id = video_id

    def check_video(self):
        folder_path = os.path.join(self.path, self.video_id)
        return os.path.isdir(folder_path)
    
    def create_video(self):
        folder_path = os.path.join(self.path, self.video_id)
        os.makedirs(folder_path, exist_ok=True)

    def save_info(self, data):
        file_path = os.path.join(self.path, self.video_id, 'info.json')
        if not os.path.isfile(file_path):
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

    def save_content(self, name, content):
        file_path = os.path.join(self.path, self.video_id, f"{name}")
        with open(file_path, "wb") as file:
            file.write(content.encode("UTF-8"))

    def delete_video(self):
        folder_path = os.path.join(self.path, self.video_id)
        shutil.rmtree(folder_path)