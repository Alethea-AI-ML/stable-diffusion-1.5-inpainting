import torch
from torch import autocast
from diffusers import StableDiffusionInpaintPipeline
import base64
from io import BytesIO
import os
from PIL import Image
import urllib.request

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model
    HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")
    
    # this will substitute the default PNDM scheduler for K-LMS  
    #lms = LMSDiscreteScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear")

    model = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting",revision="fp16",torch_dtype=torch.float16, use_auth_token=HF_AUTH_TOKEN).to("cuda")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    image = model_inputs.get('image', None)
    mask_image = model_inputs.get('mask_image', None)
    #image=Image.open(image)
    #mask_image=Image.open(mask_image)
    with urllib.request.urlopen(image) as url:
        image = Image.open(url)
    with urllib.request.urlopen(mask_image) as url1:
        mask_image = Image.open(url1)
    
    if prompt == None:
        return {'message': "No prompt provided"}
    
    # Run the model
    with autocast("cuda"):
        image = model(prompt=prompt, image=image, mask_image=mask_image).images[0]
    
    buffered = BytesIO()
    image.save(buffered,format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the results as a dictionary
    return {'image_base64': image_base64}
