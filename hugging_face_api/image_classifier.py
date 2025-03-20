from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import pipeline

app = FastAPI()

# Load your Hugging Face model here
classifier = pipeline("image-classification")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Image Classification API!"}

@app.post("/classify/")
async def classify_image(file: UploadFile = File(...)):
    # Process the uploaded image and classify it
    contents = await file.read()
    # Use the classifier on the image contents
    results = classifier(contents)
    return JSONResponse(content={"results": results})
