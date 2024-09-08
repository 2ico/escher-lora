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

st.set_page_config(
        page_title="Escher-ifier",
)
st.title('Escher-ifier')
st.text('Escher Lithography Generator')
st.markdown("""M.C. Escher is known globally for his mathematically inspired artwork, blended infinite loops, and visual puzzles.""")
st.image("https://upload.wikimedia.org/wikipedia/en/a/a3/Escher%27s_Relativity.jpg", caption='Relativity by Escher (1953)')
st.markdown("""Some of Escher's work also depicted realistic scenes, from Italy and the Netherlands. 
Unfortunately, his explorations were confined to Europe, leaving many of the world's wonders unillustrated by his unique perspective.""")

st.text("NB It is recommended to use architectural subjects.")

prompt = st.text_input('Enter a prompt for the image generator:', placeholder="Colosseum in Rome")

if st.button('Create lithography'):
    with st.spinner("Generating image"):
        url = generate_image(prompt)
        # print(url)
        response = requests.get(url)
        color_image = Image.open(BytesIO(response.content))    
        # Convert the image to black and white
        bw_image = color_image.convert('L')  # 'L' mode is for grayscale
    st.text("Generated drawing:")
    st.image(image=bw_image, caption="Generated Image", use_column_width=True)


st.text("Some examples:")
st.image("./images/xBmqSXI-g8fF8SycpWh6L_bc8cecea79e04447a1672dd5752cebc5.jpg", caption='prompt: "Golden Gate bridge in San Francisco"')
st.image("./images/735617cebc82c72fa0b54b25129e2abaa2c48aad31df23ec850290c8.jpg", caption='prompt: "Colosseum in Rome"')