# 🤖 IA Chatbot - Análise de Dados

Projeto para análise de dados de perguntas e respostas do chatbot usando Python e Pandas.

## 📋 Descrição

Este projeto visa analisar as respostas dos usuários e as máquinas sugeridas pelo chatbot consultor virtual. Inicialmente, o foco é importar e visualizar os dados históricos sem treinar modelos de IA.

## 🚀 Tecnologias

- **Python 3.x**
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Operações numéricas

## 📁 Estrutura do Projeto

```
ia-chatbot/
├── base-dados.csv          # Arquivo com dados históricos de perguntas/respostas
├── importar_dados.py       # Script principal para importar e analisar dados
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

## 🔧 Instalação

1. Certifique-se de ter Python 3.x instalado

2. Crie um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Como Usar

### Importar e Visualizar os Dados

Execute o script principal:

```bash
python importar_dados.py
```

O script irá:
- ✅ Importar o arquivo `base-dados.csv`
- 📊 Exibir informações gerais sobre os dados
- 🔍 Mostrar os primeiros registros
- 📈 Calcular estatísticas descritivas
- 📦 Analisar a distribuição de produtos escolhidos
- 📝 Mostrar detalhes das respostas de todas as perguntas
- 🔗 Analisar correlações entre respostas e produtos escolhidos
- 📊 Fornecer um resumo geral dos dados

## 📝 Formato dos Dados

O arquivo `base-dados.csv` contém dados reais do chatbot de consultoria de moedores de carne:
- **Ordem**: Número de ordem do registro
- **Nome + Nº**: Identificação do usuário
- **11 Perguntas**: Sobre finalidade, quantidade, voltagem, tipo de carne, preferências, locksup, espaço, orçamento, etc.
- **Produto escolhido**: A recomendação final baseada nas respostas

### Estrutura:

| Ordem | Nome | Pergunta 1 | Pergunta 2 | ... | Produto escolhido |
|-------|------|-----------|-----------|-----|------------------|
| 1 | Paulo1 | Uso doméstico | De 2 até 10 kg | ... | Moedor de carne caf 114 total inox |

## 🎯 Funcionalidades

### ✅ Implementado
- ✅ Importação de dados CSV usando pandas
- ✅ Visualização de informações básicas do dataset
- ✅ Análise estatística descritiva
- ✅ Distribuição de produtos escolhidos com percentuais
- ✅ Análise detalhada de todas as perguntas e respostas
- ✅ Análise de correlações entre respostas e produtos
- ✅ Resumo geral dos dados
- ✅ Suporte para colunas com nomes personalizados

### 🔜 Próximos Passos
- Visualizações gráficas (matplotlib, seaborn)
- Pré-processamento de dados para treinamento de modelo
- Implementação de modelo de classificação/recomendação (Decision Tree, Random Forest, etc.)
- API para fazer predições baseadas em respostas
- Interface web para visualizar análises

## 📊 Análises Disponíveis

O script `importar_dados.py` fornece:

1. **Informações Básicas**
   - Total de registros
   - Total de colunas
   - Estrutura do DataFrame

2. **Primeiros Registros**
   - Visualização dos primeiros 5 registros

3. **Estatísticas Descritivas**
   - Contagens, frequências, valores únicos

4. **Análise de Máquinas**
   - Total de máquinas únicas
   - Distribuição de recomendações

5. **Análise de Perguntas**
   - Distribuição de respostas por pergunta
   - Padrões nas escolhas dos usuários
   - Percentuais de cada resposta

6. **Análise de Correlação**
   - Relação entre respostas específicas e produtos escolhidos
   - Padrões de recomendação baseados em combinações de respostas

7. **Resumo Geral**
   - Total de respostas analisadas
   - Número de perguntas e produtos
   - Produto mais recomendado

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
**Solução**: Certifique-se de estar na pasta do projeto:
```bash
cd /home/matheus/Documentos/ia-chatbot
```

### Erro: "pandas não encontrado"
**Solução**: Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro de encoding
O arquivo CSV usa encoding UTF-8. Se houver problemas, verifique a codificação do arquivo.

## 📊 Exemplo de Saída

O script gera uma análise completa mostrando:
- Distribuição de todos os produtos escolhidos
- Análise detalhada de cada pergunta com percentuais
- Correlações entre as 3 primeiras perguntas e os produtos recomendados
- Resumo estatístico geral

## 📞 Desenvolvido por

Projeto desenvolvido para análise de dados do chatbot consultor virtual de moedores de carne.

---
**Versão**: 1.1.0  
**Status**: 🟢 Funcional  
**Última atualização**: Análise adaptada para dados reais de moedores de carne

