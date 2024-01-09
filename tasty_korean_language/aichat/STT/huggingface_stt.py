import librosa
from transformers import (
    AutoFeatureExtractor,
    AutoModelForCTC,
    AutoTokenizer,
    Wav2Vec2Processor
)
import unicodedata
from transformers.pipelines import AutomaticSpeechRecognitionPipeline

def hg_stt(audio):
    
    # audip_path에 audio 파일 넣으면 될 듯 한데 자세히는 모르겠습니다. librosa가 wav파일 있는 링크주면 자동으로 리샘플링해서
    # 로우데이터로 바꿔주는 건데 작업하시면서 확인하셔야 할 것 같습니다.
    audio_path = "C:/Users/user/Downloads/131.인공지능 학습을 위한 외국인 한국어 발화 음성 데이터/01.데이터_new_20220719/2.Validation/원천데이터/VS_4. 중국어/5. 한국문화II/CN50QA286_CN0476_20211014.wav"

    
    # 모델과 토크나이저, 예측을 위한 각 모듈들을 불러옵니다.
    model = AutoModelForCTC.from_pretrained("42MARU/ko-spelling-wav2vec2-conformer-del-1s")
    feature_extractor = AutoFeatureExtractor.from_pretrained("42MARU/ko-spelling-wav2vec2-conformer-del-1s")
    tokenizer = AutoTokenizer.from_pretrained("42MARU/ko-spelling-wav2vec2-conformer-del-1s")

    processor = Wav2Vec2Processor(
        feature_extractor=feature_extractor, tokenizer=tokenizer
    )

    # 실제 예측을 위한 파이프라인에 정의된 모듈들을 삽입.
    asr_pipeline = AutomaticSpeechRecognitionPipeline(
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=-1,
    )

    # 음성파일을 불러오고 resamling
    raw_data, _ = librosa.load(audio_path, sr=16000)
    pred = asr_pipeline(inputs=raw_data)["text"]

    # 모델이 자소 분리 유니코드 텍스트로 나오므로, 일반 String으로 변환해줄 필요가 있습니다.
    result = unicodedata.normalize("NFC", pred)
    
    return result