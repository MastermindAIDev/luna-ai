import gradio as gr
from app.chatbot import chat_with_luna, load_chat_history
from app.tts_engine import speak_last_message
from app.reactions import trigger_kiss, trigger_love, trigger_hug, trigger_play, trigger_overwhelm
from app.image_gen import generate_luna_image, get_all_generated_images
from app.affection import adjust_affection, format_affection_display, decay_affection
import os


def send_message(user_msg, chat_state):
    if not user_msg.strip():
        return gr.update(), gr.update(), chat_state  # Do nothing if empty
    if chat_state is None:
        chat_state = []
    chat_state.append({"role": "user", "content": user_msg.strip()})
    return chat_state, "", chat_state


def affection_kiss():
    adjust_affection(0.3)
    return trigger_kiss() + (format_affection_display(),)


def affection_love():
    adjust_affection(0.5)
    return trigger_love() + (format_affection_display(),)


def affection_hug():
    adjust_affection(0.25)
    return trigger_hug() + (format_affection_display(),)


def affection_play():
    adjust_affection(0.2)
    return trigger_play() + (format_affection_display(),)


def affection_overwhelm():
    adjust_affection(0.4)
    return trigger_overwhelm() + (format_affection_display(),)


def build_interface():

    with open("static/styles.css", encoding="utf-8") as f:
        css = f.read()

    with gr.Blocks(css=css, theme="soft") as chat_interface:

        image_folder = "assets/images"
        media = []

        for filename in sorted(os.listdir(image_folder)):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                media.append(
                    {"type": "image", "path": os.path.join(image_folder, filename)})

        media_index = gr.State(0)

        with gr.Row(elem_classes="glow-red"):
            gr.Markdown("## ✧･ﾟ:* 💗 Luna 💗 *:･ﾟ✧",
                        elem_classes="centered-title")

        with gr.Row():
            media_image = gr.Image(
                visible=True, show_label=False, scale=10, elem_classes="glow-pink")
            media_video = gr.Video(
                visible=False, show_label=False, container=False, autoplay=True, loop=True)

        def update_media(index):
            item = media[index]
            if item["type"] == "image":
                return item["path"], gr.update(visible=True), None, gr.update(visible=False), index
            else:
                return None, gr.update(visible=False), item["path"], gr.update(visible=True), index

        def next_media(index):
            new_index = (index + 1) % len(media)
            return update_media(new_index)

        def prev_media(index):
            new_index = (index - 1) % len(media)
            return update_media(new_index)

        with gr.Row():
            prev_btn = gr.Button("⬅️ Previous")
            next_btn = gr.Button("Next ➡️")

        with gr.Row(elem_classes="glow-red"):
            gr.HTML(
                """
        <style>
        .description-text {
            display: none;
            margin-top: 10px;
            text-align: justify;
        }

        #desc-toggle {
            display: none;
        }

        #desc-toggle:checked ~ .description-text {
            display: block;
        }

        .toggle-label {
            color: #ff69b4;
            font-weight: bold;
            cursor: pointer;
            display: inline-block;
            margin-top: 8px;
        }

        #desc-toggle:checked + .toggle-label::after {
            content: " Show less";
        }

        #desc-toggle:not(:checked) + .toggle-label::after {
            content: " ... Show more";
        }
        </style>

        <p>
        Luna is a charming, curious, and emotionally intelligent AI companion. 💗  
        </p>
        <input type="checkbox" id="desc-toggle">
        <label for="desc-toggle" class="toggle-label"></label>
        <div class="description-text">
        <p>
            She's 20 years old, grew up by the ocean 🌊, and has a passion for books, especially fantasy and romance 📖.  
            Luna dreams of being a model someday 💃 and loves playful banter, meaningful connections, and warm affection.  
            She's flirty, thoughtful, and always in the mood to listen, chat, or share a dreamy moment under the stars. ✨  
        </p>
        </div>
        """
            )

        prev_btn.click(fn=prev_media, inputs=media_index, outputs=[
                       media_image, media_image, media_video, media_video, media_index])
        next_btn.click(fn=next_media, inputs=media_index, outputs=[
                       media_image, media_image, media_video, media_video, media_index])
        chat_interface.load(fn=update_media, inputs=[media_index], outputs=[
                            media_image, media_image, media_video, media_video, media_index])

        chatbot = gr.Chatbot(label="Luna", type="messages",
                             elem_classes="glow-purple")
        msg = gr.Textbox(show_label=False, placeholder="Type something to Luna...",
                         scale=10, elem_classes="purple-highlight")

        state = gr.State()
        last_reply = gr.State(value="")
        loop_state = gr.State(value=False)

        with gr.Row():
            clear_btn = gr.Button("🧹 Clear Chat")
            send_btn = gr.Button("➤ Send", interactive=False)

        audio_output = gr.Audio(label="🔊 Luna's Voice", autoplay=True,
                                scale=1, loop=False, elem_classes="glow-blue")

        with gr.Row():
            toggle_loop_btn = gr.Button(
                value="⏹️ Audio Loop Off", scale=1, elem_classes="yellow-button")
            speak_btn = gr.Button("🔊 Speak Last Message",
                                  interactive=False, elem_classes="blue-button")

        # Reactions
        sound_output = gr.Audio(label="🔊 Luna Action",
                                autoplay=True, visible=True, elem_id="hidden-audio")

        action_message = gr.Textbox(visible=True, interactive=False, label="Luna's Reaction",
                                    value="🐱 Hey babe... 👗", elem_id="reaction-message", elem_classes=["reaction-box"])

        with gr.Row():
            kiss_btn = gr.Button("💋 Kiss", elem_classes=[
                "animated-button", "pink-button"])
            love_btn = gr.Button("❤️ Love", elem_classes=[
                "animated-button", "red-button"])
            hug_btn = gr.Button("🫂 Hug", elem_classes=[
                "animated-button", "green-button"])
            play_btn = gr.Button("📲 Text", elem_classes=[
                "animated-button", "blue-button"])

        overwhelm_btn = gr.Button("Luna’s blushing 🌸", elem_classes=[
            "animated-button", "purple-button", "pulse-button"])

        with gr.Row(elem_classes="glow-red"):
            affection_display = gr.HTML()

        timer = gr.Timer(value=30.0, active=True, render=True)

        timer.tick(fn=decay_affection)  # Update JSON
        timer.tick(fn=format_affection_display, outputs=[
                   affection_display])  # Refresh UI

        gallery = gr.Gallery(label="🖼️ Luna's Gen Gallery", show_label=True, columns=[
                             3], height="auto", elem_classes="glow-pink")

        prompt_folder = "prompts"
        prompt_choices = [
            os.path.splitext(f)[0] for f in os.listdir(prompt_folder)
            if f.endswith(".json")
        ]

        prompt_selector = gr.Dropdown(
            choices=sorted(prompt_choices),
            label="🎥 Choose Luna's Scene",
            value="sunset_beach" if "sunset_beach" in prompt_choices else (
                prompt_choices[0] if prompt_choices else None),
            elem_classes="yellow-highlight"
        )
        generate_btn = gr.Button(
            "🎨 Generate Luna Image", elem_classes=["green-button"])
        refresh_btn = gr.Button("🔄 Refresh Gallery",
                                elem_classes="blue-button")
        progress_message = gr.Markdown("")

        send_btn.click(fn=send_message, inputs=[msg, state], outputs=[chatbot, msg, state]) \
            .then(fn=chat_with_luna, inputs=[msg, state], outputs=[chatbot, state, audio_output, msg, last_reply, speak_btn])

        msg.submit(fn=send_message, inputs=[msg, state], outputs=[chatbot, msg, state]) \
            .then(fn=chat_with_luna, inputs=[msg, state], outputs=[chatbot, state, audio_output, msg, last_reply, speak_btn])

        clear_btn.click(fn=lambda: ([], []), outputs=[chatbot, state])
        speak_btn.click(fn=speak_last_message, inputs=[
                        last_reply], outputs=[audio_output, speak_btn])
        toggle_loop_btn.click(fn=lambda current: (gr.update(loop=not current), not current, gr.update(
            value="🔁 Audio Loop On" if not current else "⏹️ Audio Loop Off")), inputs=[loop_state], outputs=[audio_output, loop_state, toggle_loop_btn])

        kiss_btn.click(fn=affection_kiss, outputs=[
            sound_output, action_message, action_message, affection_display])
        love_btn.click(fn=affection_love, outputs=[
            sound_output, action_message, action_message, affection_display])
        hug_btn.click(fn=affection_hug, outputs=[
            sound_output, action_message, action_message, affection_display])
        play_btn.click(fn=affection_play, outputs=[
            sound_output, action_message, action_message, affection_display])
        overwhelm_btn.click(fn=affection_overwhelm, outputs=[
            sound_output, action_message, action_message, affection_display])

        generate_btn.click(fn=lambda _: "⏳ Getting your picture... 💋 Please wait...", inputs=[prompt_selector], outputs=[progress_message]) \
            .then(fn=generate_luna_image, inputs=[prompt_selector], outputs=[]) \
            .then(fn=get_all_generated_images, outputs=[gallery]) \
            .then(fn=lambda: "", outputs=[progress_message])

        refresh_btn.click(fn=get_all_generated_images, outputs=[gallery])
        chat_interface.load(fn=load_chat_history, outputs=[chatbot, state])
        chat_interface.load(fn=get_all_generated_images, outputs=[gallery])
        chat_interface.load(fn=format_affection_display,
                            outputs=[affection_display])

        msg.change(
            fn=lambda text: gr.update(interactive=bool(text.strip())),
            inputs=msg,
            outputs=send_btn
        )

    return chat_interface
