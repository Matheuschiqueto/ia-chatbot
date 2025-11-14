#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço Flask para fazer predições usando o modelo treinado
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permitir requisições do front-end

# Caminhos dos arquivos
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, 'modelo.pkl')
ENCODERS_PATH = os.path.join(MODEL_DIR, 'encoders.pkl')

# Variáveis globais para o modelo
modelo = None
encoders = None
y_encoder = None
feature_names = None

def aplicar_replace(dados):
    """Converte valores categóricos para números usando mapeamento específico."""
    dados_encoded = dados.copy()
    
    # Mapeamento de valores categóricos para números
    mapeamentos = {
        # Sim/Não
        'Sim': 1,
        'Não': 2,
        
        # Finalidade
        'Industrial': 1,
        'Comercial': 2,
        'Doméstico': 3,
        
        # Capacidade (Kg por minuto)
        'Até 1Kg': 1,
        'Até 6.5Kg': 2,
        'Até 9Kg': 3,
        'Acima de 10Kg': 4,
        
        # Voltagem
        '127V': 1,
        '220V': 2,
        'Trifásico': 3,
        
        # Tipo de material
        'Embutidos': 1,
        'Carne, Frango': 2,
        'Diversos (Castanhas, Frutas, Graõs, Etc)': 3,
        
        # Orçamento
        'Até R$ 2,500,00': 1,
        'Até R$ 15,000,00': 2,
        'Acima de R$ 15,000,00': 3,
        
        # Potência
        'Até 0,25kW': 1,
        'Até 2,2kW': 2,
        'Até 5,5kW': 3,
        'Até 7,5kW': 4,
    }
    
    # Aplica o replace em todas as colunas
    for col in dados_encoded.columns:
        dados_encoded[col] = dados_encoded[col].replace(mapeamentos)
    
    return dados_encoded

def carregar_modelo():
    """Carrega o modelo e os encoders"""
    global modelo, encoders, y_encoder, feature_names
    
    if modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}. Execute train_model.py primeiro.")
        
        if not os.path.exists(ENCODERS_PATH):
            raise FileNotFoundError(f"Encoders não encontrados em {ENCODERS_PATH}. Execute train_model.py primeiro.")
        
        print("📦 Carregando modelo...")
        with open(MODEL_PATH, 'rb') as f:
            modelo = pickle.load(f)
        
        print("📦 Carregando encoders...")
        with open(ENCODERS_PATH, 'rb') as f:
            encoders_data = pickle.load(f)
            encoders = encoders_data['label_encoders']
            y_encoder = encoders_data['y_encoder']
            feature_names = encoders_data['feature_names']
        
        print("✅ Modelo carregado com sucesso!")
    
    return modelo, encoders, y_encoder, feature_names

def prever_produto(respostas):
    """
    Faz a predição do produto baseado nas respostas
    
    Args:
        respostas: dict com as respostas onde as chaves são os textos das perguntas:
        {
            'Para qual finalidade pretende usar o moedor?': 'Doméstico',
            'Quantos quilos precisa moer por minuto?': 'Até 1Kg',
            ...
        }
    
    Returns:
        str: Nome do produto recomendado
    """
    modelo, encoders, y_encoder, feature_names = carregar_modelo()
    
    # Garantir que as colunas estejam na ordem correta
    respostas_ordenadas = {col: respostas.get(col, '') for col in feature_names}
    
    # Criar DataFrame com as respostas na ordem correta
    dados = pd.DataFrame([respostas_ordenadas], columns=feature_names)
    
    # Aplicar replace
    dados_encoded = aplicar_replace(dados)
    
    # Aplicar LabelEncoder nas colunas que ainda são strings
    for col in dados_encoded.columns:
        if dados_encoded[col].dtype == 'object' and col in encoders:
            try:
                dados_encoded[col] = encoders[col].transform(dados_encoded[col])
            except ValueError:
                # Se o valor não estiver no encoder, usar o valor mais próximo
                dados_encoded[col] = 0
    
    # Fazer predição
    predicao_encoded = modelo.predict(dados_encoded)
    produto = y_encoder.inverse_transform(predicao_encoded)[0]
    
    return produto

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    try:
        carregar_modelo()
        return jsonify({
            'status': 'ok',
            'message': 'Serviço de predição está funcionando'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para fazer predição de produto"""
    try:
        data = request.json
        
        # Validar dados recebidos
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        # Mapear respostas do chat para o formato esperado
        # O formato esperado é um dict com as chaves correspondentes às perguntas
        respostas_formatadas = {
            'Para qual finalidade pretende usar o moedor?': data.get('finalidade', ''),
            'Quantos quilos precisa moer por minuto?': data.get('quantidade', ''),
            'Qual é a voltagem que pretende utilizar?': data.get('voltagem', ''),
            'O que irá moer?': data.get('tipo_material', ''),
            'Prefere modelo mais fácil de limpar?': data.get('facil_limpeza', ''),
            'Ruído é um fator importante?': data.get('ruido_importante', ''),
            'O espaço físico é limitado?': data.get('espaco_limitado', ''),
            'Qual é a faixa de orçamento?': data.get('orcamento', ''),
            'Deseja função de remoagem?': data.get('remoagem', ''),
            'Potência desejada': data.get('potencia', '')
        }
        
        # Verificar se todas as respostas foram fornecidas
        valores_vazios = [k for k, v in respostas_formatadas.items() if not v]
        if valores_vazios:
            return jsonify({
                'success': False,
                'message': f'Respostas faltando: {", ".join(valores_vazios)}'
            }), 400
        
        # Fazer predição
        produto_recomendado = prever_produto(respostas_formatadas)
        
        return jsonify({
            'success': True,
            'produto': produto_recomendado,
            'respostas': respostas_formatadas
        })
        
    except Exception as e:
        print(f"❌ Erro ao fazer predição: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao fazer predição: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando serviço de predição...")
    print(f"📁 Diretório do modelo: {MODEL_DIR}")
    
    # Tentar carregar o modelo na inicialização
    try:
        carregar_modelo()
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível carregar o modelo na inicialização: {e}")
        print("⚠️  O modelo será carregado na primeira requisição")
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)

