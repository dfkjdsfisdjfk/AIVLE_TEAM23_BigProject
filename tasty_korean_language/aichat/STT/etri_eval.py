import json
import urllib3
import json
import base64
import librosa
import numpy as np

def etri_eval(origin_text:str,audio,key:str):
    # openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation" # 영어
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어

    accessKey = key
    languageCode = "korean"
    script = origin_text


    pcm = (librosa.load(audio, sr=16000)[0] * 32767).astype(np.int16)
    audioContents = base64.b64encode(pcm).decode('utf8')

    requestJson = {   
        "argument": {
            "language_code": languageCode,
            "script": script,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    # print("[responseCode] " + str(response.status)) # 응답 코드 필요하다면 사용
    # print("[responBody]")
    # print(str(response.data,"utf-8"))
    
    result = json.loads(response.data)['return_object']['score']
    # print(json.loads(response.data))
    
    return result