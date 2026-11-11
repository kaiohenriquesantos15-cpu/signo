
from flask import Flask, render_template, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Caminho do banco de dados na mesma pasta do app.py
DB_PATH = os.path.join(os.path.dirname(__file__), 'signos_final.db')

def init_db():
    """Cria a tabela automaticamente se ela não existir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # O tipo DATETIME é ideal para o DB Browser entender como data e hora
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            signo TEXT NOT NULL,
            data_cadastro DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def calcular_signo(data_str):
    """Calcula o signo a partir da string DD/MM/AAAA."""
    try:
        data = datetime.strptime(data_str, '%d/%m/%Y')
    except ValueError:
        return "Data Inválida"

    dia = data.day
    mes = data.month

    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19): return "Áries"
    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20): return "Touro"
    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20): return "Gêmeos"
    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22): return "Câncer"
    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22): return "Leão"
    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22): return "Virgem"
    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22): return "Libra"
    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21): return "Escorpião"
    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21): return "Sagitário"
    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19): return "Capricórnio"
    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18): return "Aquário"
    else: return "Peixes"

# Dados místicos para cada signo
DADOS_SIGNOS = {
    "Áries": {"palavras": "Coragem, Ação, Liderança", "texto": "Você é movido pela iniciativa e pela paixão de começar coisas novas.", "curiosidade": "Marte é o regente de Áries, o planeta da guerra e da energia."},
    "Touro": {"palavras": "Estabilidade, Prazer, Persistência", "texto": "Você valoriza a segurança e os prazeres sensoriais da vida.", "curiosidade": "Touro é regido por Vênus, o planeta do amor e da beleza."},
    "Gêmeos": {"palavras": "Comunicação, Curiosidade, Agilidade", "texto": "Sua mente é rápida e você adora trocar ideias e informações.", "curiosidade": "Mercúrio, o mensageiro dos deuses, rege Gêmeos."},
    "Câncer": {"palavras": "Emoção, Cuidado, Intuição", "texto": "Você tem uma conexão profunda com o lar e com as pessoas que ama.", "curiosidade": "A Lua rege Câncer, controlando as marés e as emoções."},
    "Leão": {"palavras": "Criatividade, Brilho, Generosidade", "texto": "Você nasceu para brilhar e expressar sua individualidade com calor.", "curiosidade": "O Sol é o regente de Leão, o centro do sistema solar."},
    "Virgem": {"palavras": "Análise, Perfeição, Serviço", "texto": "Você tem um olhar atento aos detalhes e busca a excelência em tudo.", "curiosidade": "Mercúrio também rege Virgem, mas aqui ele é mais analítico."},
    "Libra": {"palavras": "Harmonia, Parceria, Estética", "texto": "Você busca o equilíbrio e valoriza relacionamentos justos e belos.", "curiosidade": "Libra é o único signo representado por um objeto (a balança)."},
    "Escorpião": {"palavras": "Intensidade, Transformação, Mistério", "texto": "Você vive tudo com profundidade e tem uma capacidade incrível de regeneração.", "curiosidade": "Plutão e Marte regem Escorpião, trazendo poder e intensidade."},
    "Sagitário": {"palavras": "Liberdade, Expansão, Otimismo", "texto": "Você é um explorador nato, sempre em busca de novos horizontes.", "curiosidade": "Júpiter, o maior planeta, é o regente de Sagitário."},
    "Capricórnio": {"palavras": "Disciplina, Ambição, Estrutura", "texto": "Você constrói seu sucesso com paciência e trabalho duro.", "curiosidade": "Saturno, o senhor do tempo e das lições, rege Capricórnio."},
    "Aquário": {"palavras": "Inovação, Originalidade, Coletivo", "texto": "Você pensa fora da caixa e se preocupa com o futuro da humanidade.", "curiosidade": "Urano, o planeta das mudanças repentinas, rege Aquário."},
    "Peixes": {"palavras": "Sensibilidade, Imaginação, Compaixão", "texto": "Você tem uma conexão forte com o invisível e uma empatia profunda.", "curiosidade": "Netuno, o planeta dos sonhos e da ilusão, rege Peixes."}
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/cadastrar', methods=['POST'])
def index():
    resultado = None
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nasc = request.form.get('data_nascimento')
        
        if nome and data_nasc:
            signo = calcular_signo(data_nasc)
            info = DADOS_SIGNOS.get(signo, {"palavras": "Mistério", "texto": "Signo não identificado.", "curiosidade": "Consulte um astrólogo."})
            
            resultado = {
                "nome": nome,
                "signo": signo,
                "palavras": info["palavras"],
                "texto": info["texto"],
                "curiosidade": info["curiosidade"]
            }
            
            # AQUI GERA O DIA, HORA, MINUTO E SEGUNDO EXATOS
            agora = datetime.now()
            # Formato ISO: Ano-Mês-Dia Hora:Minuto:Segundo
            data_hora_cadastro = agora.strftime('%Y-%m-%d %H:%M:%S')
            
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO consultas (nome, data_nascimento, signo, data_cadastro) VALUES (?, ?, ?, ?)",
                    (nome, data_nasc, signo, data_hora_cadastro)
                )
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Erro ao salvar no banco: {e}")

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)
