import replicate
import dotenv
dotenv.load_dotenv()

input = {
    "style": "realistic_image/b_and_w",
    "prompt": "a portrait photo of a short haired fat dachshund"
}

output = replicate.run(
    "recraft-ai/recraft-20b",
    input=input
)
with open("output.webp", "wb") as file:
    file.write(output.read())