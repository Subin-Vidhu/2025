import gradio as gr
def update(name):
    return f"Welcome to Gradio, {name}!"

with gr.Blocks(theme="dark") as demo:
    gr.Markdown("Start typing below and then click **Run** to see the output.")
    with gr.Tab("Lion"):
        gr.Image("lion.jpg")
        gr.Button("New Lion")
    with gr.Tab("Tiger"):
        gr.Image("tiger.jpg")
        gr.Button("New Tiger")    
    with gr.Group():
        gr.Textbox(label="First")
        gr.Textbox(label="Last")
    with gr.Row():
        with gr.Column(scale=1):
            text1 = gr.Textbox()
            text2 = gr.Textbox()
        with gr.Column(scale=4):
            btn1 = gr.Button("Button 1")
            btn2 = gr.Button("Button 2")    
    with gr.Accordion("See Details"):
        gr.Markdown("lorem ipsum")
    with gr.Row():
        inp = gr.Textbox(placeholder="What is your name?")
        out = gr.Textbox()
    btn = gr.Button("Run")
    btn.click(fn=update, inputs=inp, outputs=out)

demo.launch()