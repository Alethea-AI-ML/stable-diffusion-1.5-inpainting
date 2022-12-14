# In this file, we define download_model
# It runs during container build time to get model weights built into the container

from diffusers import StableDiffusionInpaintPipeline
import os
import torch

def download_model():
    # do a dry run of loading the huggingface model, which will download weights at build time
    #Set auth token which is required to download stable diffusion model weights
    HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")

    #     lms = LMSDiscreteScheduler(
    #         beta_start=0.00085, 
    #         beta_end=0.012, 
    #         beta_schedule="scaled_linear"
    #     )
    model = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting",revision="fp16",torch_dtype=torch.float16, use_auth_token=HF_AUTH_TOKEN)

if __name__ == "__main__":
    download_model()
