# 1 - 3.5 - Pergunta:
eu quero fazer um script para puxar informaçoes financeiras das acoes do mercado acionário brasileiro. Construa para mim o código em python onde eu posso selecionar qual acao eu quero buscar informacoes

# 1 - Resposta
Para criar um script em Python que permite buscar informações financeiras de ações do mercado acionário brasileiro, você pode usar a biblioteca `yfinance` para acessar dados do Yahoo Finance. Certifique-se de instalá-la primeiro usando o seguinte comando:

```bash
pip install yfinance
```

Aqui está um exemplo de código que permite que você selecione a ação que deseja buscar informações financeiras:

```python
import yfinance as yf

def buscar_informacoes_acao():
    # Solicita ao usuário que insira o símbolo da ação (por exemplo, PETR4.SA para Petrobras)
    simbolo_acao = input("Digite o símbolo da ação (ex: PETR4.SA): ")

    # Tenta obter os dados da ação
    try:
        acao = yf.Ticker(simbolo_acao)
        informacoes = acao.info

        # Exibe as informações disponíveis
        print("\nInformações financeiras para", simbolo_acao)
        for chave, valor in informacoes.items():
            print(f"{chave}: {valor}")

    except Exception as e:
        print(f"Erro ao buscar informações: {e}")

if __name__ == "__main__":
    buscar_informacoes_acao()
```

Este script solicitará ao usuário que insira o símbolo da ação desejada (por exemplo, PETR4.SA para Petrobras) e, em seguida, buscará e exibirá as informações financeiras disponíveis para essa ação.

Lembre-se de que a disponibilidade de informações pode variar e nem todas as ações terão todos os campos de dados. Certifique-se de lidar com exceções e erros adequadamente em seu código. Além disso, considere aprimorar o script para permitir que o usuário escolha quais informações específicas ele deseja buscar (por exemplo, preço das ações, volume de negociação, etc.).


# 2 - 3.5 - Pergunta:
eu quero modelar sazonalidades semanais, mensais e anuais utilizando senos e cossenos. Me dê o código a partir da coluna de datas ´Date´


# 2 - 3.5 - Resposta:
Para modelar sazonalidades semanais, mensais e anuais utilizando senos e cossenos em Python, você pode seguir os passos abaixo. Vou usar a biblioteca NumPy para realizar os cálculos trigonométricos e a biblioteca Matplotlib para plotar os resultados. Certifique-se de ter essas bibliotecas instaladas antes de executar o código.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Crie um DataFrame de exemplo com uma coluna de datas 'Date'
data = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
df = pd.DataFrame({'Date': data})

# Defina as frequências para as sazonalidades
frequencia_semanal = 1 / 7.0  # Sazonalidade semanal (1 semana)
frequencia_mensal = 1 / 30.44  # Sazonalidade mensal (média de dias em um mês)
frequencia_anual = 1 / 365.25  # Sazonalidade anual (média de dias em um ano, considerando anos bissextos)

# Calcule os senos e cossenos para as sazonalidades
df['Seno_Semanal'] = np.sin(2 * np.pi * frequencia_semanal * df.index)
df['Cosseno_Semanal'] = np.cos(2 * np.pi * frequencia_semanal * df.index)
df['Seno_Mensal'] = np.sin(2 * np.pi * frequencia_mensal * df.index)
df['Cosseno_Mensal'] = np.cos(2 * np.pi * frequencia_mensal * df.index)
df['Seno_Anual'] = np.sin(2 * np.pi * frequencia_anual * df.index)
df['Cosseno_Anual'] = np.cos(2 * np.pi * frequencia_anual * df.index)

# Plotar os senos e cossenos das sazonalidades
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Seno_Semanal'], label='Seno Semanal')
plt.plot(df['Date'], df['Cosseno_Semanal'], label='Cosseno Semanal')
plt.plot(df['Date'], df['Seno_Mensal'], label='Seno Mensal')
plt.plot(df['Date'], df['Cosseno_Mensal'], label='Cosseno Mensal')
plt.plot(df['Date'], df['Seno_Anual'], label='Seno Anual')
plt.plot(df['Date'], df['Cosseno_Anual'], label='Cosseno Anual')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.title('Sazonalidades Seno e Cosseno')
plt.legend()
plt.grid(True)
plt.show()
```

Neste exemplo, criamos um DataFrame de exemplo com uma coluna de datas e, em seguida, calculamos os valores de seno e cosseno para as sazonalidades semanal, mensal e anual com base no índice de datas. Por fim, plotamos os resultados usando o Matplotlib.

Este código gera gráficos das sazonalidades usando senos e cossenos para cada frequência. Você pode ajustar os valores de `frequencia_semanal`, `frequencia_mensal` e `frequencia_anual` conforme necessário para se adequarem aos seus dados e necessidades específicas.