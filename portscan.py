import socket
import threading
from time import sleep
from tqdm import tqdm

THREAD_LIMIT = 10
SEMAPHORE = threading.Semaphore(THREAD_LIMIT)

def check_port(ip, port, open_ports, progress_bar, delay):
    with SEMAPHORE:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        result = sock.connect_ex((ip, port))

        if result == 0:
            open_ports.append(port)
        sock.close()
        progress_bar.update(1)
        sleep(delay)

def port_scan(ip, ports, delay):
    open_ports = []
    threads = []

    with tqdm(total=len(ports), desc="Escaneando", unit="porta") as progress_bar:
        for port in ports:
            thread = threading.Thread(target=check_port, args=(ip, port, open_ports, progress_bar, delay))
            threads.append(thread)
            thread.start()

            if len(threads) >= THREAD_LIMIT:
                for thread in threads:
                    thread.join()
                threads = []

        for thread in threads:
            thread.join()

    return open_ports

if __name__ == "__main__":
    url = input("Digite o IP ou URL alvo: ")

    try:  
        target_ip = socket.gethostbyname(url)
    except socket.gaierror:
        print("Erro: URL ou IP inválidos")
        exit()

    start_port = int(input("Digite a porta inicial: "))
    end_port = int(input("Digite a porta final: "))
    delay = float(input("Digite o tempo de espera entre conexões: "))

    ports = list(range(start_port, end_port + 1))
    open_ports = port_scan(target_ip, ports, delay)

    if open_ports:
        print(f"Portas abertas em {target_ip}: {open_ports}")
    else:
        print("Nenhuma porta aberta encontrada.")