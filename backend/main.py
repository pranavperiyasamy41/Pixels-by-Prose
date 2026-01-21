import io
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from diffusers import StableDiffusionPipeline
import torch
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# FORCE CPU for stability and space saving
device = "cpu"
dtype = torch.float32

print(f"🚀 Booting system on: {device.upper()}")

model_id = "nitrosocke/Arcane-Diffusion"

# Using local_files_only=False ensures it fixes any broken model files
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, 
    torch_dtype=dtype,
    use_safetensors=False 
)
pipe.to(device)

@app.get("/generate")
async def generate(prompt: str):
    refined_prompt = f"{prompt}, arcane style"
    # Keeping steps low (15) so the CPU doesn't take forever
    image = pipe(refined_prompt, num_inference_steps=15).images[0]
    
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return Response(content=buffer.getvalue(), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)