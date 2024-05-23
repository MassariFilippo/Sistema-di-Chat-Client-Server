import socket
import threading

# Lista per tenere traccia dei client connessi
clients = []
usernames = []

# Funzione per gestire la trasmissione dei messaggi
def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except Exception as e:
                print(f"Errore durante l'invio del messaggio: {e}")
                clients.remove(client)

# Funzione per gestire i client connessi
def handle_client(client, address):
    print(f"Connessione stabilita con {address}")
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except Exception as e:
            print(f"Errore nella connessione con {address}: {e}")
            break
    
    print(f"Connessione chiusa con {address}")
    clients.remove(client)
    client.close()

# Funzione principale per avviare il server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server avviato su porta 5555")

    while True:
        client, address = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

if __name__ == "__main__":
    start_server()
