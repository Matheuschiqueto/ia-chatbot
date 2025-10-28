# 🤖 IA Chatbot - Análise de Dados

Projeto para análise de dados de perguntas e respostas do chatbot usando Python e Pandas.

## 📋 Descrição

Este projeto analisa as respostas dos usuários e os produtos sugeridos pelo chatbot consultor virtual. A solução importa e visualiza dados históricos, fornecendo análises detalhadas das preferências dos usuários e recomendações de produtos.

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
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## 🔧 Instalação

1. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Como Usar

Execute o script principal:

```bash
python importar_dados.py
```

O script irá:
- Importar o arquivo `base-dados.csv`
- Exibir informações gerais sobre os dados
- Mostrar os primeiros 5 registros
- Analisar a distribuição de produtos escolhidos
- Analisar detalhadamente todas as perguntas e respostas
- Correlacionar as 3 primeiras perguntas com os produtos escolhidos
- Exibir um resumo geral dos dados

## 📝 Formato dos Dados

O arquivo `base-dados.csv` contém dados do chatbot de consultoria de moedores de carne:
- **Ordem**: Número de ordem do registro
- **Nome + Nº**: Identificação do usuário
- **Perguntas**: Sobre finalidade, quantidade, voltagem, tipo de carne, preferências, espaço, orçamento, etc.
- **Produto escolhido**: A recomendação final baseada nas respostas

## 🐛 Solução de Problemas

**Erro: "Arquivo não encontrado"**
```bash
Certifique-se de estar na pasta do projeto ao executar o script
```

**Erro: "pandas não encontrado"**
```bash
pip install -r requirements.txt
```

**Erro de encoding**
O arquivo CSV usa encoding UTF-8. Verifique a codificação do arquivo se houver problemas.
