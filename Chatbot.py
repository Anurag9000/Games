import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from ollama import chat

with open("requests(Grok).txt", "a") as _:
    pass

conversations = {}
try:
    with open("requests(Grok).txt", "r") as file:
        for line in file:
            conversation_name, messages_str = line.strip().split(":", 1)
            conversations[conversation_name] = eval(messages_str)
except FileNotFoundError:
    pass

def start_chat():
    selected_name = ""
    messages = []

    def send_message(event=None):
        nonlocal messages, selected_name
        user_input = user_input_box.get("1.0", tk.END).strip()
        if user_input.lower() == "esc":
            root.quit()

        chat_display.config(state="normal")
        chat_display.insert(tk.END, "You: ", "user_tag")
        chat_display.insert(tk.END, f"{user_input}\n\n")
        chat_display.config(state="disabled")
        user_input_box.delete("1.0", tk.END)

        messages.append({"role": "user", "content": user_input})

        try:
            response = chat(
                model="llama3.2",
                messages=messages,
            )
            bot_reply = response["message"]["content"]
            chat_display.config(state="normal")
            chat_display.insert(tk.END, f"{selected_name}: ", "bot_tag")
            chat_display.insert(tk.END, f"{bot_reply}\n\n")
            chat_display.config(state="disabled")
            messages.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
            chat_display.config(state="normal")
            chat_display.insert(tk.END, "Error: ", "error_tag")
            chat_display.insert(tk.END, f"{str(e)}\n\n")
            chat_display.config(state="disabled")

        conversations[selected_name] = messages
        with open("requests(Grok).txt", "w") as file:
            for name, msgs in conversations.items():
                file.write(f"{name}:{msgs}\n")

    def shift_enter(event):
        user_input_box.insert(tk.INSERT, "\n")

    def select_conversation():
        nonlocal selected_name, messages
        if conversations:
            options = [f"{i+1}. {name}" for i, name in enumerate(conversations.keys())]
            options.append("0. Start a new conversation")
            choice = simpledialog.askinteger("Select Conversation", f"\n".join(options))

            if choice == 0:
                full_role = simpledialog.askstring("New Conversation", "Enter the role for the new conversation:")
                selected_name = full_role[:20].strip()
                initial_prompt = f"You are {full_role}."
                messages = [{"role": "system", "content": initial_prompt}]
            elif 1 <= choice <= len(conversations):
                selected_name = list(conversations.keys())[choice - 1]
                messages = conversations[selected_name]
                chat_display.config(state="normal")
                chat_display.delete("1.0", tk.END)
                for msg in messages:
                    if msg["role"] == "user":
                        chat_display.insert(tk.END, "You: ", "user_tag")
                        chat_display.insert(tk.END, f"{msg['content']}\n\n")
                    elif msg["role"] == "assistant":
                        chat_display.insert(tk.END, f"{selected_name}: ", "bot_tag")
                        chat_display.insert(tk.END, f"{msg['content']}\n\n")
                chat_display.config(state="disabled")
            else:
                messagebox.showerror("Error", "Invalid choice. Please try again.")
                select_conversation()
        else:
            messagebox.showinfo("No Conversations", "No existing conversations found. Starting a new one.")
            full_role = simpledialog.askstring("New Conversation", "Enter the role for the new conversation:")
            selected_name = full_role[:20].strip()
            initial_prompt = f"You are {full_role}."
            messages = [{"role": "system", "content": initial_prompt}]

    root = tk.Tk()
    root.title("Charecter AI")

    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", height=20, width=50)
    chat_display.tag_configure("user_tag", foreground="blue")
    chat_display.tag_configure("bot_tag", foreground="green")
    chat_display.tag_configure("error_tag", foreground="red")
    chat_display.pack(padx=10, pady=10)

    user_input_box = tk.Text(root, height=3, width=50)
    user_input_box.pack(padx=10, pady=(0, 10))
    user_input_box.bind("<Return>", send_message)
    user_input_box.bind("<Shift-Return>", shift_enter)

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack(pady=(0, 10))

    select_conversation()

    root.mainloop()

start_chat()
