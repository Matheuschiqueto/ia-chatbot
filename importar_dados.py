#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para importar dados do arquivo base-dados.csv usando pandas.
Este script faz uma análise das respostas dos usuários e dos produtos sugeridos.
"""

import pandas as pd
import os

def importar_dados():
    """
    Importa e analisa os dados do arquivo base-dados.csv.
    """
    # Caminho do arquivo CSV
    arquivo_csv = 'base-dados.csv'
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_csv):
        print(f"❌ Erro: Arquivo '{arquivo_csv}' não encontrado!")
        return None
    
    try:
        # Importa o CSV usando pandas
        df = pd.read_csv(arquivo_csv, encoding='utf-8')
        
        print("=" * 100)
        print("✅ ARQUIVO IMPORTADO COM SUCESSO!")
        print("=" * 100)
        print(f"\n📊 Total de registros: {len(df)}")
        print(f"📋 Total de colunas: {len(df.columns)}")
        
        # Exibe informações básicas do DataFrame
        print("\n" + "=" * 100)
        print("📋 ESTRUTURA DOS DADOS")
        print("=" * 100)
        print(f"\nColunas: {list(df.columns)}")
        
        # Exibe os primeiros registros
        print("\n" + "=" * 100)
        print("🔍 PRIMEIROS 5 REGISTROS")
        print("=" * 100)
        print(df.head())
        
        # Análise da coluna de produtos escolhidos
        if 'Produto escolhido' in df.columns:
            print("\n" + "=" * 100)
            print("📦 PRODUTOS ESCOLHIDOS")
            print("=" * 100)
            produtos = df['Produto escolhido'].value_counts()
            print(f"\nTotal de produtos únicos: {df['Produto escolhido'].nunique()}")
            print("\nDistribuição de produtos escolhidos:")
            for produto, count in produtos.items():
                percentual = (count / len(df)) * 100
                print(f"  • {produto}: {count} vezes ({percentual:.1f}%)")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao importar arquivo: {str(e)}")
        return None

def analisar_perguntas(df):
    """
    Faz uma análise detalhada das respostas dos usuários para cada pergunta.
    """
    if df is None:
        return
    
    print("\n" + "=" * 100)
    print("🔎 ANÁLISE DETALHADA DAS PERGUNTAS E RESPOSTAS")
    print("=" * 100)
    
    # Identifica colunas de perguntas (exclui Ordem, Nome e Produto escolhido)
    colunas_metadados = ['Ordem', 'Nome +  Nº', 'Produto escolhido']
    perguntas = [col for col in df.columns if col not in colunas_metadados]
    
    for pergunta in perguntas:
        print(f"\n{'=' * 100}")
        print(f"📝 {pergunta}")
        print('=' * 100)
        
        # Distribuição de respostas
        respostas = df[pergunta].value_counts()
        print("\nDistribuição de respostas:")
        for resposta, count in respostas.items():
            percentual = (count / len(df)) * 100
            print(f"  • {resposta}: {count} vezes ({percentual:.1f}%)")

def analisar_correlacao_produto_resposta(df):
    """
    Analisa correlação entre respostas e produtos escolhidos.
    """
    if df is None or 'Produto escolhido' not in df.columns:
        return
    
    print("\n" + "=" * 100)
    print("🔗 ANÁLISE: CORRELAÇÃO ENTRE RESPOSTAS E PRODUTOS")
    print("=" * 100)
    
    colunas_metadados = ['Ordem', 'Nome +  Nº', 'Produto escolhido']
    perguntas = [col for col in df.columns if col not in colunas_metadados]
    
    for pergunta in perguntas[:3]:  # Analisa apenas as 3 primeiras perguntas
        print(f"\n📊 {pergunta}")
        print("-" * 100)
        
        # Agrupa por resposta da pergunta e conta produtos escolhidos
        for resposta in df[pergunta].unique():
            subset = df[df[pergunta] == resposta]
            produtos_count = subset['Produto escolhido'].value_counts()
            
            print(f"\n  Quando responde '{resposta}' ({len(subset)} pessoas):")
            for produto, count in produtos_count.head(3).items():
                percentual = (count / len(subset)) * 100
                print(f"    → {produto}: {count}x ({percentual:.0f}%)")

def resumo_geral(df):
    """
    Exibe um resumo geral dos dados.
    """
    if df is None:
        return
    
    print("\n" + "=" * 100)
    print("📊 RESUMO GERAL")
    print("=" * 100)
    
    print(f"\n✓ Total de respostas analisadas: {len(df)}")
    print(f"✓ Número de perguntas: {len(df.columns) - 3}")  # Exclui Ordem, Nome e Produto
    print(f"✓ Número de produtos disponíveis: {df['Produto escolhido'].nunique()}")
    
    # Produto mais recomendado
    produto_mais_comum = df['Produto escolhido'].mode()[0]
    print(f"✓ Produto mais recomendado: {produto_mais_comum}")

if __name__ == "__main__":
    # Importa os dados
    dataframe = importar_dados()
    
    # Faz análises detalhadas
    analisar_perguntas(dataframe)
    analisar_correlacao_produto_resposta(dataframe)
    resumo_geral(dataframe)
    
    print("\n" + "=" * 100)
    print("✅ ANÁLISE CONCLUÍDA!")
    print("=" * 100)
