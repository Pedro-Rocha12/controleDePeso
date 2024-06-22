# Controle de Pesagem com Arduino e Python

Este projeto permite controlar e visualizar leituras de uma célula de carga conectada a um Arduino usando uma interface gráfica em Python.

## Pré-requisitos

- **Python**: Certifique-se de ter o Python instalado. Você pode baixar e instalar a versão mais recente do Python em [python.org](https://www.python.org/downloads/).
- **pip**: Verifique se `pip` está instalado executando `pip --version`. Se `pip` não estiver instalado, siga as instruções em [pip documentation](https://pip.pypa.io/en/stable/installation/).
- **Arduino IDE**: Certifique-se de ter a IDE do Arduino instalada. Você pode baixar e instalar a Arduino IDE em [Arduino IDE](https://www.arduino.cc/en/software/).

## Materiais Utilizados

- **Arduino Nano**
- **Módulo HX711**
- **Célula de Carga**
- **Jumpers e Protoboard**
- **Computador com Python instalado**

## Bibliotecas Necessárias para o Arduino

No Arduino IDE, instale as seguintes bibliotecas:

- **HX711**: Para instalar, vá em Tools -> Manage Libraries e procure por "HX711" e instale a biblioteca de Bogde.

Ainda no Arduino IDE, certifique-se de selecionar o Arduino correto (Nano, Mini, etc) e a porta conectada (COM7, COM8, etc)

## Instalação de Dependências

Use o `pip` para instalar as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

## Executando o Programa

Primeiro abra o Arduino IDE
Para executar o programa, use o seguinte comando:
```bash
python controlePeso.py
```

## Uso
Iniciar a Pesagem:
Clique no botão `"Iniciar"` para começar a pesagem. Uma nova janela com o velocímetro será aberta.
Finalizar a Pesagem:
Clique no botão `"Finalizar"` para encerrar a pesagem e salvar os dados em um arquivo .txt.
