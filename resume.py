import openai
import tiktoken
import time
from concurrent.futures import ThreadPoolExecutor

class Resume:
    def __init__(self, api_key, system_prompt, tokens_per_chunk):
        openai.api_key = api_key
        self.system_prompt = system_prompt
        self.tokens_per_chunk = tokens_per_chunk

    def split_into_chunks(self, text):
        encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
        words = encoding.encode(text)
        chunks = []
        for i in range(0, len(words), self.tokens_per_chunk):
            chunks.append(' '.join(encoding.decode(words[i:i + self.tokens_per_chunk])))
        return chunks

    def call_openai_api(self, chunk):
        found = False
        
        while not found:
            try:
                start_time = time.time()
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": self.system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"{chunk}"
                        },
                    ],
                    max_tokens=self.tokens_per_chunk,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                end_time = time.time()
                found = True
                print(f"{int(end_time - start_time)}")
            except Exception as e:
                print(e)

        return response.choices[0]['message']['content'].strip()
    
    def resume_text(self, chunks):
        with ThreadPoolExecutor(max_workers=5) as executor:
            responses = list(executor.map(self.call_openai_api, chunks))

        text = " ".join(responses)
        return text