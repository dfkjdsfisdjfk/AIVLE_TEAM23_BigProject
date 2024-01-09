import librosa
from transformers import (
    AutoFeatureExtractor,
    AutoModelForCTC,
    AutoTokenizer,
    Wav2Vec2Processor
)
import unicodedata
from transformers.pipelines import AutomaticSpeechRecognitionPipeline
import nlptutti as metrics
import numpy as np

def hug_stt_acc(orgin_text:str,audio_file_path):

    model = AutoModelForCTC.from_pretrained("nooobedd/wav2vec_custom")
    feature_extractor = AutoFeatureExtractor.from_pretrained("nooobedd/wav2vec_custom")
    tokenizer = AutoTokenizer.from_pretrained("nooobedd/wav2vec_custom")

    processor = Wav2Vec2Processor(
        feature_extractor=feature_extractor, tokenizer=tokenizer
    )

    asr_pipeline = AutomaticSpeechRecognitionPipeline(
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=-1,
    )
    
    r, _ = librosa.load(audio_file_path, sr=16000)
    pred = asr_pipeline(inputs=r)["text"]


    result = unicodedata.normalize("NFC", pred)
    result = result.replace("<s>",'')
    result = result.replace("</s>",'')
    result = result.replace("<pad>",'')
    result = result.replace("<unk>",'')
    acc_hug = np.round(1 - metrics.get_cer(orgin_text, result)['cer'],2)
    
    return result, acc_hug