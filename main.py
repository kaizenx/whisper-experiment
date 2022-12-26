from fastapi import FastAPI, File, UploadFile
import whisper
import aiofiles
import time
import os.path

app = FastAPI()
model = whisper.load_model('base')

@app.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file( file: UploadFile = File() ):
    if not file:
        return {"message": "No upload file sent"}
    else:
        results = []
        try:
            contents = await file.read()
            filename = str(int(time.time())) +"-"+ file.filename
            completeName = os.path.join("uploads/", filename)
            async with aiofiles.open(completeName, 'wb') as f:
                await f.write(contents)
            result = model.transcribe(completeName)
            results.append({
                'filename': filename,
                'transcript': result['text'],
            })
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            await file.close()

        return {'results': results}
