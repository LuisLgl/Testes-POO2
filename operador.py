import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")  # Exibe a resposta do suporte
            else:
                break
        except:
            break

def send_messages(client_socket):
    while True:
        question = input("Digite sua dúvida: ")
        if question.lower() == "atendimento concluido":
            client_socket.send("atendimento concluido".encode())
            break
        client_socket.send(f"Financeiro:{question}".encode())  # Exemplo de enviar para área Financeiro

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.send("cliente".encode())  # Informando ao servidor que é um cliente

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()
