import socket
import threading

def receive_messages(manager_socket):
    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                print(f"\n[Cliente] {message}")  # Exibe a mensagem do cliente
            else:
                break
        except:
            break

def send_messages(manager_socket):
    while True:
        response = input("Digite sua resposta: ")
        if response.lower() == "atendimento concluido":
            manager_socket.send("atendimento concluido".encode())
            break
        manager_socket.send(response.encode())

def start_manager():
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.connect(('localhost', 5555))

    print("Escolha a área de suporte que você gerenciará:")
    print("1. Financeiro")
    print("2. Logística")
    print("3. Atendimento")
    area_choice = input("Digite o número da área: ")

    areas = {"1": "Financeiro", "2": "Logistica", "3": "Atendimento"}
    area = areas.get(area_choice, "Invalido")

    if area == "Invalido":
        print("[Erro] Escolha inválida. Fechando conexão.")
        manager_socket.close()
        return

    manager_socket.send(area.encode())  # Informando ao servidor a área gerenciada

    print(f"\nVocê está gerenciando a área de {area}.\n")
    receive_thread = threading.Thread(target=receive_messages, args=(manager_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(manager_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_manager()
