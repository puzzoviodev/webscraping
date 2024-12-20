import requests
import pandas as pd
import json
from datetime import datetime
import time

class StatusInvestScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://statusinvest.com.br'
        
    def buscar_acao(self, ticker):
        """
        Busca dados fundamentalistass de uma ação
        Args:
            ticker (str): Código da ação (ex: PETR4)
        """
        ticker = ticker.upper()
        
        try:
            # URL dos indicadores
            url_indicadores = f"{self.base_url}/acao/indicadores/{ticker}"
            
            # Headers específicos para a requisição
            headers = {
                **self.headers,
                'Accept': 'application/json',
                'Referer': f'{self.base_url}/acao/indicadores/{ticker}'
            }
            
            # Faz a requisição inicial para obter os dados básicos
            response = requests.get(url_indicadores, headers=headers)
            
            if response.status_code == 200:
                # URLs das APIs específicas
                urls = {
                    'indicadores': f'https://statusinvest.com.br/acao/indicatorhistoryvalue?ticker={ticker}&time=5',
                    'dividendos': f'https://statusinvest.com.br/acao/companytickerprovents?ticker={ticker}',
                    'balanço': f'https://statusinvest.com.br/acao/getbalancesheet?ticker={ticker}&type=1&years=5'
                }
                
                dados = self._extrair_dados(urls)
                return dados
                
            else:
                print(f"Erro ao acessar página: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao buscar dados: {str(e)}")
            return None
            
    def _extrair_dados(self, urls):
        """Extrai dados de todas as APIs necessárias"""
        dados = {}
        
        # Extrai indicadores
        response = requests.get(urls['indicadores'], headers=self.headers)
        if response.status_code == 200:
            dados['indicadores'] = self._processar_indicadores(response.json())
            
        # Extrai dividendos
        response = requests.get(urls['dividendos'], headers=self.headers)
        if response.status_code == 200:
            dados['dividendos'] = self._processar_dividendos(response.json())
            
        # Extrai balanço
        response = requests.get(urls['balanço'], headers=self.headers)
        if response.status_code == 200:
            dados['balanco'] = self._processar_balanco(response.json())
            
        return dados
        
    def _processar_indicadores(self, dados_json):
        """Processa os indicadores fundamentalistas"""
        indicadores = {}
        
        for indicador in dados_json:
            nome = indicador.get('key', '')
            valores = []
            
            for valor in indicador.get('values', []):
                valores.append({
                    'data': valor.get('date', ''),
                    'valor': valor.get('value', 0)
                })
                
            indicadores[nome] = valores
            
        return pd.DataFrame(indicadores)
        
    def _processar_dividendos(self, dados_json):
        """Processa o histórico de dividendos"""
        dividendos = []
        
        for div in dados_json:
            dividendos.append({
                'data_com': div.get('date', ''),
                'valor': div.get('value', 0),
                'tipo': div.get('type', ''),
                'data_pagamento': div.get('paymentDate', '')
            })
            
        return pd.DataFrame(dividendos)
        
    def _processar_balanco(self, dados_json):
        """Processa os dados do balanço patrimonial"""
        balanco = {}
        
        for item in dados_json:
            nome = item.get('key', '')
            valores = []
            
            for valor in item.get('values', []):
                valores.append({
                    'ano': valor.get('year', ''),
                    'valor': valor.get('value', 0)
                })
                
            balanco[nome] = valores
            
        return pd.DataFrame(balanco)
        
    def salvar_dados(self, dados, ticker):
        """Salva os dados em arquivos CSV"""
        data_atual = datetime.now().strftime("%Y%m%d")
        
        for tipo, df in dados.items():
            nome_arquivo = f"{ticker}_{tipo}_{data_atual}.csv"
            df.to_csv(nome_arquivo, index=False)
            print(f"Arquivo salvo: {nome_arquivo}")
            
    def analisar_dados(self, dados):
        """Realiza análise básica dos dados coletados"""
        analise = {}
        
        if 'indicadores' in dados:
            # Análise de indicadores
            df_ind = dados['indicadores']
            ultimos_valores = df_ind.iloc[-1]
            
            analise['indicadores'] = {
                'P/L': ultimos_valores.get('P/L', 0),
                'P/VP': ultimos_valores.get('P/VP', 0),
                'ROE': ultimos_valores.get('ROE', 0),
                'Margem_Liquida': ultimos_valores.get('Margem_Liquida', 0)
            }
            
        if 'dividendos' in dados:
            # Análise de dividendos
            df_div = dados['dividendos']
            
            analise['dividendos'] = {
                'total_ultimo_ano': df_div[df_div['data_com'] >= datetime.now().year]['valor'].sum(),
                'media_ultimos_12_meses': df_div['valor'].mean(),
                'quantidade_pagamentos': len(df_div)
            }
            
        return analise

def main():
    # Exemplo de uso
    scraper = StatusInvestScraper()
    
    # Lista de ações para análise
    acoes = ['PETR4', 'VALE3', 'ITUB4']
    
    for acao in acoes:
        print(f"\nAnalisando {acao}...")
        
        # Busca dados
        dados = scraper.buscar_acao(acao)
        
        if dados:
            # Salva dados
            scraper.salvar_dados(dados, acao)
            
            # Análise básica
            analise = scraper.analisar_dados(dados)
            
            print("\nResultados da análise:")
            print(json.dumps(analise, indent=2))
            
        # Espera entre requisições para evitar bloqueio
        time.sleep(2)

if __name__ == "__main__":
    main()
