#include <HX711.h> // adiciona a biblioteca ao código

// configuração dos pinos para o módulo HX711
const int PINO_DT = 3;
const int PINO_SCK = 2;

const int TEMPO_ESPERA = 1000; // declaração da variável de espera

HX711 escala; // declaração do objeto escala na classe HX711 da biblioteca

float fator_calibracao = 51333; // pre-definição da variável de calibração

char comando; // declaração da variável que irá receber os comandos para alterar o fator de calibração

bool inicializado = false; // variável para armazenar o estado do sistema

void setup() {
  // mensagens do monitor serial
  Serial.begin(57600);
  Serial.println("Célula de carga - Calibração de Peso");
  Serial.println("Comandos: I = Iniciar, F = Finalizar, R = Reiniciar");

  escala.begin(PINO_DT, PINO_SCK); // inicialização e definição dos pinos DT e SCK dentro do objeto ESCALA

  // realiza uma média entre leituras com a célula sem carga
  float media_leitura = escala.read_average();
  Serial.print("Média de leituras com Célula sem carga: ");
  Serial.print(media_leitura);
  Serial.println();

  escala.tare(); // zera a escala
}

void loop() {
  if (Serial.available()) {
    comando = Serial.read();
    if (comando == 'I') {
      inicializado = true;
      Serial.println("Iniciado");
    }
    if (comando == 'F') {
      inicializado = false;
      Serial.println("Finalizado");
      delay(500); // pequeno atraso para evitar problemas de debounce
    }
    if (comando == 'R') {
      inicializado = false;
      Serial.println("Reiniciado");
      delay(500); // pequeno atraso para evitar problemas de debounce
      inicializado = true;
      Serial.println("Iniciado");
    }
    if (comando == 'n') fator_calibracao -= 1;
    if (comando == 'm') fator_calibracao += 1;
    if (comando == 'v') fator_calibracao -= 10;
    if (comando == 'b') fator_calibracao += 10;
    if (comando == 'x') fator_calibracao -= 100;
    if (comando == 'c') fator_calibracao += 100;
  }

  if (inicializado) {
    escala.set_scale(fator_calibracao); // ajusta a escala para o fator de calibração

    // verifica se o módulo está pronto para realizar leituras
    if (escala.is_ready()) {
      // mensagens de leitura no monitor serial
      float peso = escala.get_units();
      Serial.print("Leitura: ");
      Serial.print(peso, 3); // retorna a leitura da variável escala em Quilos
      Serial.print(" Kg");
      Serial.print(" \t Fator de Calibração = ");
      Serial.print(fator_calibracao);
      Serial.println();

      // enviar dados em formato CSV
      Serial.print(peso, 3);
      Serial.println(",Kg");
    } else {
      Serial.print("HX-711 ocupado");
    }
  }
  
  delay(TEMPO_ESPERA);
}


