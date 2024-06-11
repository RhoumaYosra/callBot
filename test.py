from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

path="C:/Users/rh.yosra/AppData/Local/Programs/Python/Python310/Lib/site-packages/TTS/.models.json"
model_manager = ModelManager(path)
model_path , config_path , model_item = model_manager.download_model("tts_models/en/ljspeech/tactorn2-DDC")

syn =Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path
    )

text=" I AM A TEXT REEDED BY COMPUTER"

outputs=syn.tts(text) 
syn.save_wav(outputs,"adio.wav")