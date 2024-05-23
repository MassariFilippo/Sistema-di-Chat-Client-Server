import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Funzione per ricevere messaggi dal server
def receive_messages(client, text_area):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, message + '\n')
            text_area.config(state=tk.DISABLED)
            text_area.yview(tk.END)
        except Exception as e:
            print(f"Errore durante la ricezione del messaggio: {e}")
            break

# Funzione per inviare messaggi al server
def send_message(client, entry, client_name):
    message = entry.get()
    if message != "":
        formatted_message = f"{client_name}: {message}"
        client.send(formatted_message.encode('utf-8'))
        entry.delete(0, tk.END)

# Funzione per configurare la GUI del client
def start_client_gui():

    client_name = "Chat Client 2"
    
    # Connessione al server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    # Creazione della finestra principale
    root = tk.Tk()
    root.title(client_name)

    # Creazione della text area per visualizzare i messaggi
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Creazione del campo di input per inviare messaggi
    entry_frame = tk.Frame(root)
    entry_frame.pack(padx=10, pady=5, fill=tk.X)

    entry = tk.Entry(entry_frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    send_button = tk.Button(entry_frame, text="Invia", command=lambda: send_message(client, entry, client_name))
    send_button.pack(side=tk.RIGHT)

    # Thread per ricevere messaggi dal server
    receive_thread = threading.Thread(target=receive_messages, args=(client, text_area))
    receive_thread.start()

    # Avvio della GUI
    root.mainloop()

if __name__ == "__main__":
    start_client_gui()
