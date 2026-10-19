import FreeSimpleGUI as fsg
from chat_view import ChatView
from chat_message import ChatMessage
import config

def format_messages(messages=[]):
    if messages:
        output = ""
        for message in messages:
            output += f"{message.username}: {message.text}\n"

        return output

def run():
    username = fsg.popup_get_text("Enter a name", "Live Chat")

    if not username:
        return

    view = ChatView()

    messages = ChatMessage.all()
    view.update_messages(format_messages(messages))


    while True:
        event, values = view.read(timeout=config.POLL_RATE)

        if event == fsg.WIN_CLOSED:
            break

        if event == "__TIMEOUT__":
            messages = ChatMessage.all()
            view.update_messages(format_messages(messages))

        if event == "Send":
            text = values["-CHAT-"]

            if text:
                ChatMessage(username, text).save()
                view.clear_input()
                messages = ChatMessage.all()
                view.update_messages(format_messages(messages))

    view.close()


if __name__ == "__main__":
    run()