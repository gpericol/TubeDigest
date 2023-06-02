# TubeDigest

TubeDigest is a Python program that transforms YouTube videos into concise, digestible summaries. It utilizes YouTube's API and various text summarization techniques to generate summaries based on video subtitles.

## Requirements

- Python 3
- Dependencies: youtube_transcript_api, openai, tiktoken

## Installation

1. Clone this repository: `git clone https://github.com/your_username/TubeDigest.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Ensure you have obtained the necessary API key from Google Cloud Console and replace the placeholder `api_key` in the `config_real.py` file with your actual API key.

2. Run the program by executing the following command:

`python tube_digest.py <video_url_or_code> [-f] [-d]`

   - `<video_url_or_code>`: The URL or code of the YouTube video for which you want to generate a summary.
   - `-f` or `--force` (optional): Download the subtitles and create summaries even if they are already present in the database, overwriting them.
   - `-d` or `--delete` (optional): Remove the data related to the video from the database.

3. The program will create a summary of the video and store it in the database. If the subtitles and summaries already exist in the database, the program will output the path to the existing summary file. If the `-f` flag is provided, the program will overwrite the existing data with new subtitles and summaries.

4. The generated summaries are stored in the database along with additional information about the video.
