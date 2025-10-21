import json
import base64
from io import BytesIO
import time
import requests
from  dotenv import load_dotenv
from PIL import Image
import os


class FusionBrainAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        #print(data)
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024): # images = 1 , width = 1024, height = 1024
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)



#if __name__ == '__main__':
    #load_dotenv()
    #api = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv('FB_API_KEY'), os.getenv('FB_SECRET_KEY'))
    #pipeline_id = api.get_pipeline()
    #uuid = api.generate("a family gathering in armenia with a sceneray of ararat at Sevan river with Barbecue", pipeline_id)
    #files = api.check_generation(uuid)
    #with open('result.txt', 'w', encoding='utf-8') as f:
        #f.write(files[0])

       # new function for decoding base64 and saving the pic 
    def save_image(self, base64_str, file_path):
        decoded_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(decoded_data))
        image.save(file_path)
        print(f"image saved to {file_path}")

def gen_img(prompt,size=None):
    load_dotenv()
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv('FB_API_KEY'), os.getenv('FB_SECRET_KEY'))
    try:
        
        pipeline_id = api.get_pipeline()
        if size:
            width, height = size
            img = api.generate(prompt,pipeline_id,width=width, height=height)
        else:
            img = api.generate(prompt,pipeline_id)
        files = api.check_generation(img)
        if not files:
            return 'Error generating image'
        else:
            return files[0]
    except Exception as e:
        return f'Error {str(e)}'

#size = (768, 576)
#img = gen_img('mount ararat with flag of armenia', size)
#with open('result.txt', 'w', encoding='utf-8') as f:
    #f.write(img)
    
#Don't forget to specify exactly YOUR_KEY and YOUR_SECRET.