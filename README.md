# DataPool2.0

DataPool 2.0
DataPool 2.0 é uma ferramenta CLI em Python para coletar dados de sensores conectados a um Arduino e monitorar a comunicação serial em tempo real.

Funcionalidades
Coleta de dados de sensores via comunicação serial com Arduino.
Monitoramento de dados em tempo real.
Armazenamento dos dados coletados em um arquivo CSV.
Requisitos
Arduino com código para leitura de sensores via pinos analógicos.
Python 3.x instalado no sistema.
Biblioteca Python pyserial.
Instalação
Clone o repositório:

bash
Copy code
git clone https://github.com/seu-usuario/datapool-2.0.git
cd datapool-2.0
Instale a biblioteca pyserial:

bash
Copy code
pip install pyserial
Carregue o código no seu Arduino para coleta de dados dos sensores:

cpp
Copy code
int sensor1 = A0;
int sensor2 = A1;

void setup(){
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}

void loop(){
  int data1 = analogRead(sensor1);
  int data2 = analogRead(sensor2);
  Serial.print("Sensor1: ");
  Serial.print(data1);
  Serial.print(" Sensor2: ");
  Serial.println(data2);
  delay(1000); // Intervalo de coleta de dados
}
Uso
Conecte o Arduino à porta serial do seu computador.

Execute o script Python e siga as instruções do CLI:

bash
Copy code
python datapool_cli.py
Funções Principais
Iniciar coleta de dados: Coleta um número de amostras dos sensores com um intervalo configurado e salva em um arquivo CSV.
Monitoramento serial: Monitora e exibe os dados recebidos do Arduino em tempo real.
Contribuição
Sinta-se à vontade para abrir uma issue ou enviar um pull request para melhorias.

