# Controle de Pesagem com Arduino e Python

Este projeto permite controlar e visualizar leituras de uma célula de carga conectada a um Arduino usando uma interface gráfica em Python.

## Pré-requisitos

- **Python**: Certifique-se de ter o Python instalado. Você pode baixar e instalar a versão mais recente do Python em [python.org](https://www.python.org/downloads/).
- **pip**: Verifique se `pip` está instalado executando `pip --version`. Se `pip` não estiver instalado, siga as instruções em [pip documentation](https://pip.pypa.io/en/stable/installation/).

## Instalação de Dependências

Use o `pip` para instalar as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

## Executando o Programa

Para executar o programa, use o seguinte comando:
```bash
python arduinoTeste.py
```

## Uso
Iniciar a Pesagem:
Clique no botão `"Iniciar"` para começar a pesagem. Uma nova janela com o velocímetro será aberta.
Finalizar a Pesagem:
Clique no botão `"Finalizar"` para encerrar a pesagem e salvar os dados em um arquivo .txt.
