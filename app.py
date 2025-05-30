
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from riemann_calculator import calcular_soma_riemann
from plotter import plotar_riemann

# Funções matemáticas predefinidas
FUNCOES_PREDEFINIDAS = {
    "x^2": lambda x: x**2,
    "x^3": lambda x: x**3,
    "sin(x)": lambda x: np.sin(x),
    "cos(x)": lambda x: np.cos(x),
    "e^x": lambda x: np.exp(x),
    "1/x (para x>0)": lambda x: 1/x if isinstance(x, (int, float)) and x!=0 else (np.vectorize(lambda val: 1/val if val !=0 else np.nan)(x) if isinstance(x, np.ndarray) else np.nan) ,
    "sqrt(x) (para x>=0)": lambda x: np.sqrt(x) if isinstance(x, (int,float)) and x>=0 else (np.vectorize(lambda val: np.sqrt(val) if val >=0 else np.nan)(x) if isinstance(x, np.ndarray) else np.nan),
    "x": lambda x: x,
    "5": lambda x: 5.0 if isinstance(x, (int, float)) else np.full_like(x, 5.0) # Função constante
}

class RiemannApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Visual de Somas de Riemann")
        self.root.geometry("900x700") # Tamanho da janela

        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para os controles (esquerda)
        controls_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Frame para o gráfico (direita)
        plot_frame = ttk.LabelFrame(main_frame, text="Gráfico", padding="10")
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Controles ---
        ttk.Label(controls_frame, text="Função f(x):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.func_var = tk.StringVar(value=list(FUNCOES_PREDEFINIDAS.keys())[0])
        self.func_combo = ttk.Combobox(controls_frame, textvariable=self.func_var,
                                       values=list(FUNCOES_PREDEFINIDAS.keys()), width=27)
        self.func_combo.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(controls_frame, text="Limite inferior (a):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.a_var = tk.StringVar(value="0")
        self.a_entry = ttk.Entry(controls_frame, textvariable=self.a_var, width=30)
        self.a_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        ttk.Label(controls_frame, text="Limite superior (b):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.b_var = tk.StringVar(value="1")
        self.b_entry = ttk.Entry(controls_frame, textvariable=self.b_var, width=30)
        self.b_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)

        ttk.Label(controls_frame, text="Número de retângulos (n):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.n_var = tk.StringVar(value="10")
        self.n_entry = ttk.Entry(controls_frame, textvariable=self.n_var, width=30)
        self.n_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)
        # Slider para n
        self.n_slider = ttk.Scale(controls_frame, from_=1, to=200, orient=tk.HORIZONTAL,
                                 command=self.atualizar_n_entry_do_slider)
        self.n_slider.set(10) # Valor inicial
        self.n_slider.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=2)


        ttk.Label(controls_frame, text="Método da Soma:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.metodo_var = tk.StringVar(value="medio")
        metodos = ["esquerdo", "medio", "direito"]
        for i, metodo in enumerate(metodos):
            rb = ttk.Radiobutton(controls_frame, text=metodo.capitalize(), variable=self.metodo_var, value=metodo)
            rb.grid(row=6+i, column=0, columnspan=2, sticky=tk.W, padx=5)

        self.calcular_button = ttk.Button(controls_frame, text="Calcular e Plotar", command=self.executar_calculo_e_plot)
        self.calcular_button.grid(row=9, column=0, columnspan=2, pady=20)

        self.area_label = ttk.Label(controls_frame, text="Área Aproximada: -")
        self.area_label.grid(row=10, column=0, columnspan=2, pady=10)

        # --- Configuração do Gráfico Matplotlib ---
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Bind do slider para atualizar n_var e executar
        self.n_slider.bind("<ButtonRelease-1>", self.executar_se_slider_mudou)


    def atualizar_n_entry_do_slider(self, valor_slider):
        # Atualiza o campo de entrada 'n' quando o slider é movido
        self.n_var.set(str(int(float(valor_slider)))) # Converte para float, depois int, depois str

    def executar_se_slider_mudou(self, event=None):
        # Chamado quando o slider é solto, para atualizar o gráfico
        self.executar_calculo_e_plot()

    def executar_calculo_e_plot(self):
        try:
            func_nome = self.func_var.get()
            func_matematica = FUNCOES_PREDEFINIDAS.get(func_nome)
            if func_matematica is None:
                messagebox.showerror("Erro", "Função selecionada não é válida.")
                return

            a = float(self.a_var.get())
            b = float(self.b_var.get())
            n = int(self.n_var.get())
            metodo = self.metodo_var.get()

            if n <= 0 :
                messagebox.showerror("Erro de Entrada", "O número de retângulos (n) deve ser maior que zero.")
                return
            if a >=b:
                messagebox.showerror("Erro de Entrada", "O limite inferior (a) deve ser menor que o superior (b).")
                return

            # Calcula a Soma de Riemann
            soma_aprox, x_r, y_r, delta_x_r = calcular_soma_riemann(func_matematica, a, b, n, metodo)

            # Atualiza o label da área
            self.area_label.config(text=f"Área Aproximada: {soma_aprox:.6f}")

            # Plota
            plotar_riemann(self.ax, func_matematica, a, b, n, metodo,
                           x_r, y_r, delta_x_r, soma_aprox)
            self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, verifique os valores de entrada.\nDetalhe: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RiemannApp(root)
    root.mainloop()