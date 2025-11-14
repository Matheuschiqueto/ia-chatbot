#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para treinar e salvar o modelo de árvore de decisão
"""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

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

def treinar_modelo():
    """Treina o modelo e salva em arquivos pickle"""
    print("📊 Carregando dados de treinamento...")
    
    # 1. Importar dados
    csv_path = os.path.join(os.path.dirname(__file__), 'base-dados-atualizada.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')
    df = df.drop(columns=['Perguntas'], errors='ignore')
    
    # 2. Dividir X e Y
    X = df.iloc[:, :-1]  # Features (todas exceto a última)
    y = df.iloc[:, -1]   # Target (última coluna)
    
    print(f"✅ Total de registros: {len(df)}")
    print(f"✅ Features: {len(X.columns)} colunas")
    print(f"✅ Classes: {y.nunique()} categorias\n")
    
    # 3. Converter dados categóricos para numéricos
    X_encoded = aplicar_replace(X)
    
    # Aplicar LabelEncoder nos valores que ainda são strings
    label_encoders = {}
    for col in X_encoded.columns:
        if X_encoded[col].dtype == 'object':
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X_encoded[col])
            label_encoders[col] = le
    
    # Converte Y (produtos) com LabelEncoder
    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(y)
    
    # 4. Treinar árvore de decisão
    print("🤖 Treinando modelo...")
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_encoded, y_encoded)
    
    # Calcular acurácia
    accuracy = clf.score(X_encoded, y_encoded)
    print(f"✅ Acurácia: {accuracy*100:.2f}%\n")
    
    # 5. Salvar modelo e encoders
    model_dir = os.path.dirname(__file__)
    
    # Salvar modelo
    model_path = os.path.join(model_dir, 'modelo.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)
    print(f"✅ Modelo salvo em: {model_path}")
    
    # Salvar encoders
    encoders_path = os.path.join(model_dir, 'encoders.pkl')
    with open(encoders_path, 'wb') as f:
        pickle.dump({
            'label_encoders': label_encoders,
            'y_encoder': le_y,
            'feature_names': list(X.columns)
        }, f)
    print(f"✅ Encoders salvos em: {encoders_path}")
    
    print("\n✅ Modelo treinado e salvo com sucesso!")
    return clf, label_encoders, le_y, X.columns

if __name__ == "__main__":
    treinar_modelo()

