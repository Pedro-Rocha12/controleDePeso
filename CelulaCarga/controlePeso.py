import serial
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from tkinter import ttk
import math
from PIL import Image, ImageTk

# Configurações da porta serial
porta = 'COM8'  # Atualize com a sua porta COM correta
baud_rate = 57600

# Inicia a conexão serial
ser = serial.Serial(porta, baud_rate, timeout=1)

# Lista para armazenar os dados
dados = []
parar_leitura = False
peso_atual = 0

def enviar_comando(comando):
    ser.write(comando.encode())
    ser.flush()

def ler_serial():
    global parar_leitura, peso_atual
    while not parar_leitura:
        if ser.in_waiting > 0:
            linha = ser.readline().decode('utf-8').strip()
            if linha:
                print(linha)
                if "Leitura:" in linha:
                    # Filtra e exibe apenas as leituras de peso
                    peso = float(linha.split("Leitura: ")[1].split(" Kg")[0])
                    peso = max(0, min(peso, 20))  # Limita o peso entre 0 e 20
                    peso_atual = peso
                    dados.append(f"{peso:.2f} Kg")
                    atualizar_ponteiro(peso)
                    atualizar_valor(peso)
                elif linha == "Iniciado":
                    dados.clear()  # Limpa os dados anteriores ao iniciar
                elif linha == "Finalizado":
                    # Salva os dados em um arquivo .txt
                    salvar_dados()
                    parar_leitura = True

def iniciar_pesagem():
    enviar_comando('I')
    abrir_interface_pesos()

def finalizar_pesagem():
    global parar_leitura
    enviar_comando('F')
    parar_leitura = True
    salvar_dados()  # Chama salvar_dados antes de fechar a janela principal
    root.destroy()

def salvar_dados():
    if dados:
        # Abrir diálogo para salvar arquivo
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            with open(filepath, 'w') as file:
                for dado in dados:
                    file.write(dado + '\n')
            messagebox.showinfo("Informação", f"Dados salvos em '{filepath}'.")

def abrir_interface_pesos():
    global peso_canvas, ponteiro, valor_label
    peso_window = tk.Toplevel(root)
    peso_window.title("Pesos Atuais")
    peso_window.geometry("500x500")  # Define o tamanho da janela de pesos

    peso_canvas = Canvas(peso_window, width=400, height=400, bg='white')
    peso_canvas.pack(pady=20)

    # Desenhar o velocímetro (arco de 270 a 90 graus)
    peso_canvas.create_arc(50, 50, 350, 350, start=0, extent=180, style=tk.ARC, outline='black', width=2)
    
    # Linhas principais (com valores) a cada 1 kg
    for i in range(0, 41, 2):  # Aumenta o espaçamento entre os números
        valor = i * 0.5
        angle = 180 + (180 * (valor / 20))  # Ajusta o ângulo para distribuir ao longo do arco de 270 a 90 graus
        x1 = 200 + 130 * math.cos(math.radians(angle))
        y1 = 200 + 130 * math.sin(math.radians(angle))
        x2 = 200 + 160 * math.cos(math.radians(angle))
        y2 = 200 + 160 * math.sin(math.radians(angle))
        peso_canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
        peso_canvas.create_text(200 + 180 * math.cos(math.radians(angle)),
                                200 + 180 * math.sin(math.radians(angle)),
                                text=str(valor), font=("Helvetica", 10))

    # Linhas menores a cada 0.5 kg
    for i in range(1, 40, 2):
        valor = i * 0.5
        angle = 180 + (180 * (valor / 20))
        x1 = 200 + 145 * math.cos(math.radians(angle))
        y1 = 200 + 145 * math.sin(math.radians(angle))
        x2 = 200 + 160 * math.cos(math.radians(angle))
        y2 = 200 + 160 * math.sin(math.radians(angle))
        peso_canvas.create_line(x1, y1, x2, y2, fill='black', width=1)

    # Desenhar o ponteiro como um triângulo com uma base menor
    ponteiro = peso_canvas.create_polygon(200, 200, 198, 65, 202, 65, fill='red')

    # Label para exibir o valor atual
    valor_label = tk.Label(peso_window, text="Peso Atual: 0.0 Kg", font=("Helvetica", 16))
    valor_label.pack(pady=10)

def atualizar_ponteiro(peso):
    angle = 180 + (180 * (peso / 20))
    x = 200 + 140 * math.cos(math.radians(angle))
    y = 200 + 140 * math.sin(math.radians(angle))
    x1 = 200 + 10 * math.cos(math.radians(angle - 90))
    y1 = 200 + 10 * math.sin(math.radians(angle - 90))
    x2 = 200 + 10 * math.cos(math.radians(angle + 90))
    y2 = 200 + 10 * math.sin(math.radians(angle + 90))
    peso_canvas.coords(ponteiro, 200, 200, x1, y1, x, y, x2, y2)

def atualizar_valor(peso):
    valor_label.config(text=f"Peso Atual: {peso:.2f} Kg")

# Configurar a interface gráfica principal
root = tk.Tk()
root.title("Controle de Pesagem")
root.geometry("500x500")  # Define o tamanho da janela principal

# Carregar e exibir a imagem na primeira interface
img = Image.open("imagem/tenpestTest.png")  # Atualize o caminho para sua imagem
img = img.resize((200, 200), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)

panel = tk.Label(root, image=img)
panel.pack(pady=10)

# Exibir mensagem de inicialização
msg_inicial = tk.Label(root, text="Célula de carga - Peso", font=("Helvetica", 24, "bold"))
msg_inicial.pack(pady=20)

# Configurar frame para os botões
frame = tk.Frame(root)
frame.pack(pady=20)

# Função para exibir os botões após um atraso
def exibir_botoes():
    btn_iniciar.pack(side=tk.LEFT, padx=20)
    btn_finalizar.pack(side=tk.LEFT, padx=20)

# Estilizar botões usando ttk
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10)

# Configurar botões com ttk e atraso de 3 segundos
btn_iniciar = ttk.Button(frame, text="Iniciar", command=iniciar_pesagem, style='TButton')
btn_finalizar = ttk.Button(frame, text="Finalizar", command=finalizar_pesagem, style='TButton')

# Chamar exibir_botoes após 3000 milissegundos (3 segundos)
root.after(3000, exibir_botoes)

# Iniciar a thread para leitura contínua da porta serial
thread_leitura = threading.Thread(target=ler_serial)
thread_leitura.start()

# Iniciar o loop da interface gráfica
root.mainloop()

# Finalizar a leitura da porta serial quando a GUI for fechada
parar_leitura = True
thread_leitura.join()
ser.close()








