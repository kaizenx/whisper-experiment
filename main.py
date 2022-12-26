from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# import whisper

# model = whisper.load_model("base")
# result = model.transcribe("audio.mp3")
# print(result["text"])