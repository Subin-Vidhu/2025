import gradio as gr

def image_classifier(inp1, inp2):
  print(inp1)
  return {'cat': 0.3, 'dog': 1.7}

inputs = [gr.Image(),'image']

demo = gr.Interface(
  fn=image_classifier, 
  inputs=inputs,
  outputs="label")
demo.launch(share=False)