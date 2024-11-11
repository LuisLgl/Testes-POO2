import socket
import threading

clients = []
managers = {"Financeiro": None, "Logistica": None, "Atendimento": None}
messages = []  # Lista para armazenar todas as mensagens trocadas

def handle_client(client_socket, address):
    global clients, managers
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                # Se a mensagem for "atendimento concluído", encerra a conexão
                if message.lower() == "atendimento concluido":
                    client_socket.send("Atendimento encerrado. Até logo!".encode())
                    break
                
                # Registra a mensagem no histórico do servidor
                messages.append(f"[Cliente {address[0]}:{address[1]}] Pergunta: {message.strip()}")
                area, question = message.split(":", 1)  # Extrai a área e a pergunta
                if area in managers and managers[area]:
                    # Encaminha a pergunta para o gerente da área correspondente
                    managers[area].send(f"[Cliente {address[0]}:{address[1]}] Pergunta: {question.strip()}".encode())
                    client_socket.send(f"[Sucesso] Sua dúvida foi enviada para o gerente de {area}.".encode())
                else:
                    client_socket.send(f"[Erro] Nenhum gerente disponível para {area} no momento.".encode())
            else:
                break
        except Exception as e:
            print(f"[Erro] {e}")
            clients.remove(client_socket)
            break
    client_socket.close()

def handle_manager(manager_socket, area):
    global messages
    print(f"[Servidor] Gerente de {area} conectado.")
    
    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                # Registra a resposta do gerente no histórico do servidor
                messages.append(f"[{area} Gerente] Resposta: {message.strip()}")
                
                # Envia a resposta para todos os clientes conectados dessa área
                for client in clients:
                    client.send(f"[{area} Gerente] Resposta: {message.strip()}".encode())
                
                # Envia uma confirmação para o gerente de que a resposta foi enviada
                manager_socket.send("Mensagem enviada para os clientes.".encode())
            else:
                break
        except Exception as e:
            print(f"[Erro] {e}")
            managers[area] = None
            break
    manager_socket.close()

def start_server():
    global managers
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(10)
    print("Servidor rodando na porta 5555...\n")

    while True:
        client_socket, address = server.accept()
        print(f"Nova conexão de {address[0]}:{address[1]}")

        role = client_socket.recv(1024).decode()
        if role in managers:  # É um gerente para uma área específica
            managers[role] = client_socket
            print(f"Gerente de {role} conectado.")
            client_socket.send(f"[Suporte Conectado] O gerente de {role} está agora disponível.".encode())
            manager_thread = threading.Thread(target=handle_manager, args=(client_socket, role))
            manager_thread.start()
        else:  # É um cliente
            clients.append(client_socket)
            print("Cliente conectado.")
            client_socket.send("[Suporte] Conectado. Aguardando sua dúvida.".encode())
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    start_server()
