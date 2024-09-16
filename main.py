import serial
import struct
import csv
import time

class ArduinoLoggerCLI:
    def __init__(self, port, baudrate=19200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.logging = False
        self.n_samples = 0
        self.interval = 0
        self.pwm_value = 0
        self.data = []

    def send_command(self, n_samples, interval, pwm_value):
        self.ser.write(b'k')
        self.ser.write(struct.pack(">H", n_samples))
        self.ser.write(struct.pack(">H", interval))
        self.ser.write(struct.pack(">H", pwm_value))

    def start_logging(self, n_samples, interval, pwm_value):
        self.send_command(n_samples, interval, pwm_value)
        self.n_samples = n_samples
        self.interval = interval
        self.pwm_value = pwm_value
        self.data = []
        self.logging = True
        self.log_end_time = time.time() + (n_samples * interval / 1000)  # Tempo total do log em segundos
        print(f"Coletando {n_samples} amostras com intervalo de {interval} ms e PWM {pwm_value}...")

        while self.logging and len(self.data) < n_samples:
            if self.ser.in_waiting >= 2:
                raw_data = self.ser.read(2)
                value = struct.unpack(">H", raw_data)[0]
                self.data.append(value)
                self.display_data(value)
            
            self.update_timer()
            time.sleep(interval / 1000)  # Intervalo entre amostras

        print("\nColeta finalizada.")
        self.save_log("datalog.csv")
        print("Pronto para iniciar novamente.\n")

    def display_data(self, value):
        print(f"Dado recebido: {value}")

    def update_timer(self):
        if self.logging:
            remaining_time = max(0, self.log_end_time - time.time())
            print(f"Tempo restante: {int(remaining_time)} s", end='\r')

    def save_log(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amostra", "Valor"])
            for i, value in enumerate(self.data):
                writer.writerow([i + 1, value])
        print(f"Dados salvos em {filename}")

    def close(self):
        self.ser.close()
        print("Conexão serial fechada.")

    def monitor_serial(self):
        """ Função para monitorar a comunicação serial e exibir os dados em tempo real. """
        print("Iniciando monitoramento serial...")
        try:
            while True:
                if self.ser.in_waiting >= 2:
                    raw_data = self.ser.read(2)
                    value = struct.unpack(">H", raw_data)[0]
                    self.display_data(value)
                time.sleep(0.1)  # Ajuste o intervalo conforme necessário
        except KeyboardInterrupt:
            print("\nMonitoramento interrompido.")

def list_serial_ports():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def main():
    print("Detectando portas COM disponíveis...")
    available_ports = list_serial_ports()

    if len(available_ports) == 0:
        print("Nenhuma porta serial encontrada. Conecte o Arduino e tente novamente.")
        return

    print("Portas COM disponíveis:")
    for i, port in enumerate(available_ports):
        print(f"{i + 1}: {port}")

    port_index = int(input("Selecione a porta COM (número): ")) - 1
    selected_port = available_ports[port_index]

    print(f"Conectando ao Arduino na porta {selected_port}...")
    logger = ArduinoLoggerCLI(port=selected_port)

    while True:
        print("\nEscolha uma operação:")
        print("1. Iniciar log de dados")
        print("2. Monitorar comunicação serial")
        print("3. Fechar conexão e sair")

        option = input("Selecione uma opção (1/2/3): ")

        if option == '1':
            n_samples = int(input("Digite o número de amostras: "))
            interval = int(input("Digite o intervalo entre amostras (ms): "))
            pwm_value = int(input("Digite o valor PWM (0-255): "))  # Assumindo valor PWM no intervalo de 0 a 255
            logger.start_logging(n_samples, interval, pwm_value)
        elif option == '2':
            logger.monitor_serial()
        elif option == '3':
            logger.close()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
