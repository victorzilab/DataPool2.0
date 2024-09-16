int sensor1 = A0;   // Pino do primeiro sensor
int sensor2 = A1;   // Pino do segundo sensor

// Variáveis globais para armazenar dados dos sensores
int data1, data2;  
int freq = 1000;    // Frequência de coleta de dados em milissegundos

void setup(){
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}


void loop() {
  // Lê os valores dos sensores
  data1 = analogRead(sensor1);
  data2 = analogRead(sensor2);

  // Envia os valores dos sensores para o monitor serial
  Serial.print("Sensor1: ");
  Serial.print(data1);
  Serial.print(" | Sensor2: ");
  Serial.println(data2);

  // Aguarda o intervalo definido antes da próxima leitura
  delay(freq);
}
