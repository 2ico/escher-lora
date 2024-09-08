import streamlit as st
import fal_client
from PIL import Image
import requests
from io import BytesIO

def generate_image(topic: str):
    step_1_prompt = f"{topic}"


    handler = fal_client.submit(
        "fal-ai/flux-lora",
        arguments={
            "prompt": step_1_prompt,
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "num_images": 1,
            "strength": 0.85,
            "image_size": "portrait_4_3",
        },
    )

    result = handler.get()
    print(result)

    step_1_image_url = result["images"][0]["url"]
    print(f"step 1 image url: {step_1_image_url}")

    handler2 = fal_client.submit(
        "fal-ai/flux-lora/image-to-image",
        arguments={
            "prompt": f"{topic} in the style of wxexcher in black and white",
            "num_inference_steps": 40,
            "guidance_scale": 4, # NB changed this 3.5->4
            "num_images": 1,
            "enable_safety_checker": True,
            "output_format": "jpeg",
            "image_url": step_1_image_url,
            "strength": 0.8,
            "loras": [
                {
                    "path": "https://storage.googleapis.com/fal-flux-lora/3afe13e9e58e4b40a1ecb89e81e364d2_pytorch_lora_weights.safetensors",
                    "scale": 1.8
                }
            ],
        },
    )

    result2 = handler2.get()
    print(result2)
    out_image = result2["images"][0]["url"]
    return out_image

# st.title("Escher Flux LoRA")
# # st.write(
# #     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# # )
# topic = st.text_input(label="Prompt")
# submit_button = st.button(label="Generate image", on_click=lambda: generate_image(topic, image_empty))
# image_empty = st.empty()

# Streamlit UI components
st.title('Escher Painting Generator')
st.markdown("""M.C. Escher is known globally for his intricate and mathematically inspired artwork, Escher masterfully blended infinite loops, impossible scenarios, and visual puzzles that captivate and challenge the mind.
Escher's work often depicted realistic scenes from Italy and the Netherlands, places he lived and traveled. Unfortunately, his explorations were confined to Europe, leaving many of the world's wonders unillustrated by his unique perspective.""")
prompt = st.text_input('Enter a prompt for the image generator:')

if st.button('Generate Image'):
    with st.spinner("Generating image"):
        url = generate_image(prompt)
        # print(url)
        response = requests.get(url)
        color_image = Image.open(BytesIO(response.content))    
        # Convert the image to black and white
        bw_image = color_image.convert('L')  # 'L' mode is for grayscale
        
    st.image(image=bw_image, caption="Generated Image", use_column_width=True)


# st.text("Some examples:")
# st.image()