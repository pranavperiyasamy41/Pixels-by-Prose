import gradio as gr
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained("nitrosocke/Arcane-Diffusion", torch_dtype=torch.float16)
pipe.to("cuda") 

def cartoonify(prompt):
    image = pipe(prompt).images[0]
    return image

demo = gr.Interface(fn=cartoonify, inputs="text", outputs="image", title="Text to Cartoon Image Generator")

demo.launch()
