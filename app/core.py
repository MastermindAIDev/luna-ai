from app.ui import build_interface

__version__ = "0.6.1"


def launch():
    interface = build_interface()
    interface.launch(server_name="0.0.0.0", server_port=8080, share=True)
