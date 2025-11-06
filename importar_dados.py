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
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import matplotlib.pyplot as plt
import numpy as np

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
        
        # Converte cada coluna categórica de X, preservando valores do replace
        for col in x_encoded.columns:
            # Verifica se ainda há strings após o replace
            tem_strings = x_encoded[col].apply(lambda x: isinstance(x, str)).any()
            
            if tem_strings:
                # Se ainda tiver strings, aplica LabelEncoder apenas nos valores string
                # Mantém os valores numéricos do replace intactos
                le = LabelEncoder()
                
                # Identifica quais são strings e quais são números
                mask_strings = x_encoded[col].apply(lambda x: isinstance(x, str))
                
                # Aplica LabelEncoder apenas nas strings
                valores_strings = x_encoded[col][mask_strings].astype(str)
                valores_encoded = le.fit_transform(valores_strings)
                
                # Cria uma cópia da coluna
                col_encoded = x_encoded[col].copy()
                
                # Substitui apenas os valores string pelos valores codificados
                col_encoded[mask_strings] = valores_encoded
                
                # Converte valores numéricos do replace para int (se necessário)
                mask_numericos = ~mask_strings
                if mask_numericos.any():
                    col_encoded[mask_numericos] = pd.to_numeric(col_encoded[mask_numericos], errors='coerce').astype(int)
                
                x_encoded[col] = col_encoded
                le_x[col] = le
                
                # Conta quantos foram convertidos pelo replace vs LabelEncoder
                num_replace = mask_numericos.sum() if mask_numericos.any() else 0
                num_labelencoder = mask_strings.sum()
                print(f"✓ Coluna '{col}': {num_replace} valores do replace + {num_labelencoder} valores do LabelEncoder")
            elif not pd.api.types.is_numeric_dtype(x_encoded[col]):
                # Se não tem strings mas não é numérico, força conversão
                x_encoded[col] = pd.to_numeric(x_encoded[col], errors='coerce')
                print(f"✓ Coluna '{col}' convertida para numérico (após replace)")
            else:
                # Já é numérico após replace
                x_encoded[col] = x_encoded[col].astype(int)
                print(f"✓ Coluna '{col}' já numérica após replace ({x_encoded[col].nunique()} valores únicos)")
        
        # Garante que todas as colunas de X sejam numéricas
        for col in x_encoded.columns:
            x_encoded[col] = pd.to_numeric(x_encoded[col], errors='coerce').astype(int)
        
        # Converte Y para numérico, preservando valores do replace
        y_series = pd.Series(y) if not isinstance(y, pd.Series) else y
        y_df = pd.DataFrame({'target': y_series})
        y_encoded = aplicar_replace(y_df)['target']
        
        # Verifica se ainda há strings após o replace
        tem_strings_y = y_encoded.apply(lambda x: isinstance(x, str)).any()
        
        if tem_strings_y:
            # Se ainda tiver strings, aplica LabelEncoder em TODOS os valores
            # (produtos não estão no mapeamento do replace)
            le_y = LabelEncoder()
            y_encoded = le_y.fit_transform(y_encoded.astype(str))
            # Converte para numpy array para garantir compatibilidade
            y_encoded = np.array(y_encoded, dtype=int)
            print(f"✓ Target convertido para numérico (LabelEncoder - {len(np.unique(y_encoded))} classes)")
        else:
            # Cria LabelEncoder para manter compatibilidade com visualização
            le_y = LabelEncoder()
            y_encoded = pd.to_numeric(y_encoded, errors='coerce').astype(int)
            # Converte para numpy array
            y_encoded = np.array(y_encoded, dtype=int)
            # Ajusta o LabelEncoder com os valores únicos de Y original
            le_y.fit(y.astype(str))
            print(f"✓ Target convertido para numérico (após replace - {len(np.unique(y_encoded))} classes)")
        
        # Validação cruzada usando TODAS as amostras
        print("\n" + "=" * 100)
        print("📊 VALIDAÇÃO CRUZADA (USANDO TODAS AS AMOSTRAS)")
        print("=" * 100)
        
        # Usa k-fold estratificado (k=5) para usar todas as amostras
        # Cada amostra será usada para treino e teste em diferentes iterações
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        clf_cv = tree.DecisionTreeClassifier()
        
        # Calcula acurácia média na validação cruzada
        cv_scores = cross_val_score(clf_cv, x_encoded, y_encoded, cv=cv, scoring='accuracy')
        print(f"✓ Validação cruzada (5-fold):")
        print(f"  - Acurácia média: {cv_scores.mean()*100:.2f}%")
        print(f"  - Desvio padrão: {cv_scores.std()*100:.2f}%")
        print(f"  - Acurácia por fold: {[f'{s*100:.1f}%' for s in cv_scores]}")
        
        # Predições da validação cruzada (cada amostra prevista quando estava no conjunto de teste)
        y_pred_cv = cross_val_predict(clf_cv, x_encoded, y_encoded, cv=cv)
        
        # Calcula acurácia geral
        accuracy_cv = accuracy_score(y_encoded, y_pred_cv)
        print(f"\n📊 Acurácia geral (todas as amostras): {accuracy_cv*100:.2f}%")
        
        # Gera matriz de confusão usando todas as amostras
        print("\n" + "=" * 100)
        print("📊 MATRIZ DE CONFUSÃO (VALIDAÇÃO CRUZADA)")
        print("=" * 100)
        cm = confusion_matrix(y_encoded, y_pred_cv)
        print("\nMatriz de Confusão (usando todas as 40 amostras):")
        print(cm)
        
        # Treina o modelo final com TODAS as amostras
        print("\n" + "=" * 100)
        print("🌳 TREINANDO MODELO FINAL COM TODAS AS AMOSTRAS")
        print("=" * 100)
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x_encoded, y_encoded)
        print(f"✅ Modelo final treinado com {len(x_encoded)} amostras!")
        
        # Visualiza matriz de confusão
        plt.figure(figsize=(12, 10))
        im = plt.imshow(cm, interpolation='nearest', cmap='Blues')
        plt.colorbar(im, label='Quantidade')
        plt.title('Matriz de Confusão - Validação Cruzada (40 amostras)', fontsize=16, pad=20)
        plt.ylabel('Valor Real', fontsize=12)
        plt.xlabel('Valor Previsto', fontsize=12)
        
        # Adiciona os valores na matriz
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                        horizontalalignment="center",
                        color="white" if cm[i, j] > thresh else "black",
                        fontsize=10)
        
        # Define os labels
        tick_marks = np.arange(len(le_y.classes_))
        plt.xticks(tick_marks, le_y.classes_, rotation=45, ha='right')
        plt.yticks(tick_marks, le_y.classes_)
        plt.tight_layout()
        plt.savefig('matriz_confusao.png', dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Matriz de confusão salva como 'matriz_confusao.png'")
        plt.close()
        
        # Relatório de classificação
        print("\n" + "=" * 100)
        print("📋 RELATÓRIO DE CLASSIFICAÇÃO")
        print("=" * 100)
        print("\nRelatório detalhado (Validação Cruzada - todas as amostras):")
        print(classification_report(y_encoded, y_pred_cv, target_names=le_y.classes_))
        
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
        
        return clf, le_y
        
    except Exception as e:
        print(f"❌ Erro ao treinar modelo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    # Importa os dados
    dataframe, x, y = importar_dados()
    
    # Treina e mostra a árvore de decisão se os dados foram importados com sucesso
    if x is not None and y is not None:
        clf, le_y = treinar_e_mostrar_arvore(x, y)
    
    print("\n" + "=" * 100)
    print("✅ IMPORTAÇÃO E TREINAMENTO CONCLUÍDOS!")
    print("=" * 100)
