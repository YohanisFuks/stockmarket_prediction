import pandas as pd
import numpy as np
import yfinance as yf

def construir_base(acao:str = 'PETR4.SA',
                            periodo:str = '5y')->pd.DataFrame:
    '''
    função para trazer informações volumétricas de cada ação passada no argumento.
    informações:
        dividendos
        splits
        DRE trimestral
        Balanço Patrimonial
        Fluxo de caixa
        Open
        High	
        Low	Close	
        Volume
    periodos { d - m - y }
    '''
    
    # Tenta obter os dados da ação
    try:
        acao = yf.Ticker(acao)
        historico = acao.history(period=periodo)
        #determinando os dados faltantes porque a bolsa nao opera
        historico['bolsa_opera'] = 1
        historico.reset_index(inplace = True)
        historico['Date'] = pd.to_datetime(historico['Date'].dt.date)
        historico = historico.groupby(pd.Grouper(key = 'Date',freq='D')).mean().reset_index()

        #feature engineering de datas
        historico['dow'] = historico['Date'].dt.day_of_week
        historico['trimestre_start'] = historico['Date'].dt.is_quarter_start
        historico['trimestre_end'] = historico['Date'].dt.is_quarter_end
        historico['trimestre'] = historico['Date'].dt.quarter
        historico['mes'] = historico['Date'].dt.month
        historico['ano'] = historico['Date'].dt.year
        historico['doy'] = historico['Date'].dt.day_of_year
        historico['inicio_mes'] = historico['Date'].dt.is_month_start
        historico['fim_mes'] = historico['Date'].dt.is_month_end
        historico['ano_eleitoral'] = eleicoes(historico)

        #feature engineering - sazonalidade
        #semanal
        historico['sin_semanal'] = np.sin(historico['dow'] * 2 * np.pi/7)
        historico['cos_semanal'] = np.cos(historico['dow'] * 2 * np.pi/7)

        #mensal
        historico['sin_mensal'] = np.sin(historico['mes'] * 2 * np.pi/12)
        historico['cos_mensal'] = np.cos(historico['mes'] * 2 * np.pi/12)

         #anual
        historico['sin_anual'] = np.sin(historico['doy'] * 2 * np.pi/365.25)
        historico['cos_anual'] = np.cos(historico['doy'] * 2 * np.pi/365.25)
        
        #feature engineering - autoregressivo
        #stds
        historico = desvio_padrao(historico)

        #rolling mean
        historico,n_drop = media_movel(historico)

        #limpar o dataframe
        historico = historico.iloc[n_drop:,]
        


        #financeiro:
        # - income statement
        quarterly_income_stmt = acao.quarterly_income_stmt #DRE trimestral

        # - balance sheeter
        quartly_balance_sheet = acao.quarterly_balance_sheet #Balanço Patrimonial trimestral

        # - cash flow statement
        quarterly_cashflow = acao.quarterly_cashflow #fluxo de caixa trimetral


        return historico, quarterly_income_stmt, quartly_balance_sheet,quarterly_cashflow

    except Exception as e:
        print(f"Erro ao buscar informações: {e}")
    


def eleicoes(base)->pd.Series:
    year_max = base['ano'].max()
    eleicoes = list(np.arange(start= 1998, stop = year_max + 12, step = 4))
    return base['ano'].isin(eleicoes)


def media_movel(historico:pd.DataFrame,
                janelas:list = [7,14,21,28,60,90,150]) ->pd.DataFrame:
        '''
        a partir de uma lista de janelas desejadas, cria as featuers de médias e o delta do atual
        com a feature criada
        retorna o dataframe e também a indicação de qual o window frame maior para dropar da base original
        '''
        for i in janelas:
            #criação das médias móveis
            historico['Open_ma_'+str(i)] = historico['Open'].rolling(window = i, min_periods = 1).mean().shift(7)
            historico['High_ma_'+str(i)] = historico['High'].rolling(window = i, min_periods = 1).mean().shift(7)
            historico['Low_ma_'+str(i)] = historico['Low'].rolling(window = i, min_periods = 1).mean().shift(7)
            historico['Close_ma_'+str(i)] = historico['Close'].rolling(window = i, min_periods = 1).mean().shift(7)
            historico['Volume_ma_'+str(i)] = historico['Volume'].rolling(window = i, min_periods = 1).mean().shift(7)
        
            #delta
            historico['Open_delta_ma_'+str(i)] = -historico['Open_ma_'+str(i)] + historico['Open']
            historico['High_delta_ma_'+str(i)] = -historico['High_ma_'+str(i)] + historico['High']
            historico['Low_delta_ma_'+str(i)] = -historico['Low_ma_'+str(i)] + historico['Low']
            historico['Close_delta_ma_'+str(i)] = -historico['Close_ma_'+str(i)] + historico['Close']
            historico['Volume_delta_ma_'+str(i)] = -historico['Volume_ma_'+str(i)] + historico['Volume']


        return historico, i


def desvio_padrao(historico:pd.DataFrame,
                janelas:list = [7,14,21,28,60,90,150]) ->pd.DataFrame:
        '''
        a partir de uma lista de janelas desejadas, cria as featuers de std
        '''
        for i in janelas:
            historico['Open_std_'+str(i)] = historico['Open'].rolling(window = i, min_periods = 1).std().shift(7)
            historico['High_std_'+str(i)] = historico['High'].rolling(window = i, min_periods = 1).std().shift(7)
            historico['Low_std_'+str(i)] = historico['Low'].rolling(window = i, min_periods = 1).std().shift(7)
            historico['Close_std_'+str(i)] = historico['Close'].rolling(window = i, min_periods = 1).std().shift(7)
            historico['Volume_std_'+str(i)] = historico['Volume'].rolling(window = i, min_periods = 1).std().shift(7)

        return historico