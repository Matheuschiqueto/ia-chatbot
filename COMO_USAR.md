# 🤖 Como Usar o Serviço de IA

Este guia explica como configurar e usar o serviço de predição de máquinas baseado em IA.

## 📋 Pré-requisitos

1. Python 3.x instalado
2. Ambiente virtual Python (recomendado)
3. Node.js instalado (para o servidor front-end)

## 🚀 Configuração

### 1. Instalar Dependências Python

```bash
cd ia-chatbot
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Treinar o Modelo

Primeiro, você precisa treinar o modelo de IA:

```bash
python train_model.py
```

Isso irá:
- Carregar os dados de treinamento de `base-dados-atualizada.csv`
- Treinar o modelo de árvore de decisão
- Salvar o modelo em `modelo.pkl`
- Salvar os encoders em `encoders.pkl`

### 3. Iniciar o Serviço de Predição

Em um terminal, inicie o serviço Flask:

```bash
python prediction_service.py
```

O serviço estará rodando em `http://localhost:5000`

### 4. Iniciar o Servidor Node.js

Em outro terminal, inicie o servidor do chatbot:

```bash
cd ../chatbot
npm start
```

O servidor estará rodando em `http://localhost:3000`

## 🧪 Testar o Serviço

### Teste de Health Check

```bash
curl http://localhost:5000/health
```

### Teste de Predição

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "finalidade": "Doméstico",
    "quantidade": "Até 1Kg",
    "voltagem": "127V",
    "tipo_material": "Carne, Frango",
    "facil_limpeza": "Sim",
    "ruido_importante": "Sim",
    "espaco_limitado": "Sim",
    "orcamento": "Até R$ 2,500,00",
    "remoagem": "Não",
    "potencia": "Até 0,25kW"
  }'
```

## 📝 Formato das Respostas

O serviço espera as seguintes respostas no formato correto:

- **finalidade**: `"Doméstico"`, `"Comercial"`, ou `"Industrial"`
- **quantidade**: `"Até 1Kg"`, `"Até 6.5Kg"`, `"Até 9Kg"`, ou `"Acima de 10Kg"`
- **voltagem**: `"127V"`, `"220V"`, ou `"Trifásico"`
- **tipo_material**: `"Carne, Frango"`, `"Embutidos"`, ou `"Diversos (Castanhas, Frutas, Graõs, Etc)"`
- **facil_limpeza**: `"Sim"` ou `"Não"`
- **ruido_importante**: `"Sim"` ou `"Não"`
- **espaco_limitado**: `"Sim"` ou `"Não"`
- **orcamento**: `"Até R$ 2,500,00"`, `"Até R$ 15,000,00"`, ou `"Acima de R$ 15,000,00"`
- **remoagem**: `"Sim"` ou `"Não"`
- **potencia**: `"Até 0,25kW"`, `"Até 2,2kW"`, `"Até 5,5kW"`, ou `"Até 7,5kW"`

## 🔧 Variáveis de Ambiente

Você pode configurar a URL do serviço Python usando a variável de ambiente:

```bash
export PYTHON_SERVICE_URL=http://localhost:5000
```

## 🐛 Solução de Problemas

### Erro: "Modelo não encontrado"

Execute `python train_model.py` para treinar e salvar o modelo.

### Erro: "Erro ao conectar com o serviço de IA"

Certifique-se de que o serviço Python está rodando em `http://localhost:5000`.

### Erro: "Respostas faltando"

Verifique se todas as 10 perguntas foram respondidas no chat.

## 📚 Estrutura dos Arquivos

```
ia-chatbot/
├── base-dados-atualizada.csv  # Dados de treinamento
├── train_model.py             # Script para treinar o modelo
├── prediction_service.py      # Serviço Flask para predições
├── modelo.pkl                 # Modelo treinado (gerado)
├── encoders.pkl               # Encoders salvos (gerado)
└── requirements.txt           # Dependências Python
```

