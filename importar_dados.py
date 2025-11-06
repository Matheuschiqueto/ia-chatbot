#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para importar dados do arquivo base-dados-atualizada.csv usando pandas.
Este script importa e exibe os dados da planilha removendo a coluna 'Perguntas'
"""

import pandas as pd
import os
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

def importar_dados():
    """
    Importa os dados do arquivo base-dados-atualizada.csv.
    """
    # Caminho do arquivo CSV
    arquivo_csv = 'base-dados-atualizada.csv'
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_csv):
        print(f"❌ Erro: Arquivo '{arquivo_csv}' não encontrado!")
        return None, None, None
    
    try:
        # Importa o CSV usando pandas
        df = pd.read_csv(arquivo_csv, encoding='utf-8')
        
        # Remove a coluna 'Perguntas' (identificador)
        df = df.drop(columns=['Perguntas'], errors='ignore')
        print("✓ Coluna 'Perguntas' removida")
        
        # Separa em x (features) e y (target)
        # y é a última coluna (coluna decisória)
        # x são todas as outras colunas
        y = df.iloc[:, -1]  # Última coluna
        x = df.iloc[:, :-1]  # Todas as colunas exceto a última
        
        print("=" * 100)
        print("✅ ARQUIVO IMPORTADO COM SUCESSO!")
        print("=" * 100)
        print(f"\n📊 Total de registros: {len(df)}")
        print(f"📋 Total de colunas: {len(df.columns)}")
        
        # Informações sobre x e y
        print("\n" + "=" * 100)
        print("📊 VARIÁVEIS X E Y")
        print("=" * 100)
        print(f"\nVariável X (Features): {len(x.columns)} colunas")
        print(f"Colunas em X: {list(x.columns)}")
        print(f"\nVariável Y (Target - {df.columns[-1]}):")
        print(y.value_counts())

        # Exibe todos os dados de X
        print("\n" + "=" * 100)
        print("📊 VARIÁVEL X - TODOS OS DADOS")
        print("=" * 100)
        print(x)

        # Exibe todos os dados de Y
        print("\n" + "=" * 100)
        print("📊 VARIÁVEL Y - TODOS OS DADOS")
        print("=" * 100)
        print(y)
        
        return df, x, y
        
    except Exception as e:
        print(f"❌ Erro ao importar arquivo: {str(e)}")
        return None, None, None

def aplicar_replace(dados):
    """
    Aplica replace para converter valores categóricos em números.
    """
    dados_replace = dados.copy()
    
    # Mapeamento completo de todos os valores encontrados na planilha
    mapeamentos = {
        # Sim/Não (aplica em todas as colunas Sim/Não)
        'Sim': 1,
        'Não': 2,
        
        # Finalidade: Para qual finalidade pretende usar o moedor?
        'Industrial': 1,
        'Comercial': 2,
        'Doméstico': 3,
        
        # Quantos quilos precisa moer por minuto?
        'Até 1Kg': 1,
        'Até 6.5Kg': 2,
        'Até 9Kg': 3,
        'Acima de 10Kg': 4,
        
        # Qual é a voltagem que pretende utilizar?
        '127V': 1,
        '220V': 2,
        'Trifásico': 3,
        
        # O que irá moer?
        'Embutidos': 1,
        'Carne, Frango': 2,
        'Diversos (Castanhas, Frutas, Graõs, Etc)': 3,
        
        # Qual é a faixa de orçamento?
        'Até R$ 2,500,00': 1,
        'Até R$ 15,000,00': 2,
        'Acima de R$ 15,000,00': 3,
        
        # Potência desejada
        'Até 0,25kW': 1,
        'Até 2,2kW': 2,
        'Até 5,5kW': 3,
        'Até 7,5kW': 4,
    }
    
    # Aplica replace em todas as colunas
    for col in dados_replace.columns:
        if dados_replace[col].dtype == 'object':
            # Aplica os mapeamentos
            for valor_original, valor_numerico in mapeamentos.items():
                dados_replace[col] = dados_replace[col].replace(valor_original, valor_numerico)
    
    return dados_replace

def treinar_e_mostrar_arvore(x, y):
    """
    Treina um modelo de árvore de decisão e visualiza a árvore.
    """
    try:
        # Converte dados categóricos para numéricos
        print("\n" + "=" * 100)
        print("🔧 CONVERTENDO DADOS PARA TREINAMENTO")
        print("=" * 100)
        
        # Aplica replace primeiro
        print("📝 Aplicando replace para valores conhecidos...")
        x_encoded = aplicar_replace(x)
        
        le_x = {}
        
        # Converte cada coluna categórica de X
        for col in x_encoded.columns:
            if x_encoded[col].dtype == 'object' or x_encoded[col].apply(lambda x: isinstance(x, str)).any():
                # Se ainda tiver strings, usa LabelEncoder para os valores restantes
                le = LabelEncoder()
                x_encoded[col] = le.fit_transform(x_encoded[col].astype(str))
                le_x[col] = le
                print(f"✓ Coluna '{col}' convertida para numérico")
            elif not pd.api.types.is_numeric_dtype(x_encoded[col]):
                # Garante que seja numérico
                x_encoded[col] = pd.to_numeric(x_encoded[col], errors='coerce')
                print(f"✓ Coluna '{col}' convertida para numérico (após replace)")
        
        # Converte Y para numérico
        y_series = pd.Series(y) if not isinstance(y, pd.Series) else y
        y_df = pd.DataFrame({'target': y_series})
        y_encoded = aplicar_replace(y_df)['target']
        
        # Se ainda tiver strings em Y, usa LabelEncoder
        if y_encoded.dtype == 'object' or y_encoded.apply(lambda x: isinstance(x, str)).any():
            le_y = LabelEncoder()
            y_encoded = le_y.fit_transform(y_encoded.astype(str))
            print(f"✓ Target convertido para numérico")
        else:
            # Cria LabelEncoder para manter compatibilidade com visualização
            le_y = LabelEncoder()
            y_encoded = y_encoded.astype(int)
            # Ajusta o LabelEncoder com os valores únicos de Y original
            le_y.fit(y.astype(str))
            print(f"✓ Target convertido para numérico (após replace)")
        
        # Treina o modelo
        print("\n" + "=" * 100)
        print("🌳 TREINANDO ÁRVORE DE DECISÃO")
        print("=" * 100)
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x_encoded, y_encoded)
        print("✅ Modelo treinado com sucesso!")
        
        # Visualiza a árvore
        print("\n" + "=" * 100)
        print("📊 VISUALIZANDO ÁRVORE DE DECISÃO")
        print("=" * 100)
        plt.figure(figsize=(20, 10))
        tree.plot_tree(clf, feature_names=x_encoded.columns, class_names=le_y.classes_, filled=True, rounded=True)
        
        # Salva a árvore como imagem
        plt.savefig('arvore_decisao.png', dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Árvore salva como 'arvore_decisao.png'")
        plt.close()  # Fecha a figura para economizar memória
        
        return clf
        
    except Exception as e:
        print(f"❌ Erro ao treinar modelo: {str(e)}")
        return None

if __name__ == "__main__":
    # Importa os dados
    dataframe, x, y = importar_dados()
    
    # Treina e mostra a árvore de decisão se os dados foram importados com sucesso
    if x is not None and y is not None:
        clf = treinar_e_mostrar_arvore(x, y)
    
    print("\n" + "=" * 100)
    print("✅ IMPORTAÇÃO E TREINAMENTO CONCLUÍDOS!")
    print("=" * 100)
