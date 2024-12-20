import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AnaliseFundamentalista:
    def __init__(self):
        # Dados fundamentalistas das PETR4 (exemplo com dados históricos)
        self.dados_fundamentalistas = {
            'ano': [2019, 2020, 2021, 2022, 2023],
            'lucro_liquido': [40.1, 7.1, 106.7, 188.3, 124.7],  # em bilhões
            'receita_liquida': [302.2, 281.5, 452.7, 640.9, 603.3],
            'ebitda': [129.2, 52.9, 234.9, 339.3, 262.4],
            'divida_liquida': [317.9, 284.5, 58.7, -57.6, -82.8],
            'patrimonio_liquido': [299.1, 311.3, 350.5, 389.2, 401.5],
            'fcf': [30.2, 28.1, 101.5, 122.8, 89.4],  # Free Cash Flow
            'dividendos': [10.7, 1.8, 101.4, 215.8, 72.4]
        }
        
        # Dados de mercado atuais
        self.dados_mercado = {
            'cotacao_atual': 35.82,
            'num_acoes': 13.04,  # em bilhões
            'valor_mercado': 467.0,  # em bilhões
            'volume_diario_medio': 1.8,  # em bilhões
            'setor': 'Petróleo e Gás',
        }
        
        # Valores de referência para indicadores
        self.valores_referencia = {
            'P/L': {
                'otimo': {'min': 0, 'max': 10},
                'bom': {'min': 10, 'max': 15},
                'regular': {'min': 15, 'max': 20},
                'alto': {'min': 20, 'max': float('inf')},
                'descricao': 'Preço em relação ao lucro. Quanto menor, mais barata a ação.'
            },
            'P/VP': {
                'otimo': {'min': 0, 'max': 1},
                'bom': {'min': 1, 'max': 2},
                'regular': {'min': 2, 'max': 3},
                'alto': {'min': 3, 'max': float('inf')},
                'descricao': 'Preço em relação ao valor patrimonial. Abaixo de 1 indica ação negociada abaixo do patrimônio.'
            },
            'Margem_EBITDA': {
                'ruim': {'min': 0, 'max': 15},
                'regular': {'min': 15, 'max': 25},
                'bom': {'min': 25, 'max': 35},
                'otimo': {'min': 35, 'max': float('inf')},
                'descricao': 'Indica eficiência operacional. Quanto maior, melhor.'
            },
            'Margem_Liquida': {
                'ruim': {'min': 0, 'max': 10},
                'regular': {'min': 10, 'max': 20},
                'bom': {'min': 20, 'max': 30},
                'otimo': {'min': 30, 'max': float('inf')},
                'descricao': 'Lucratividade final. Quanto maior, melhor.'
            },
            'ROE': {
                'ruim': {'min': 0, 'max': 10},
                'regular': {'min': 10, 'max': 15},
                'bom': {'min': 15, 'max': 20},
                'otimo': {'min': 20, 'max': float('inf')},
                'descricao': 'Retorno sobre patrimônio. Maior que 15% é considerado bom.'
            },
            'Dividend_Yield': {
                'baixo': {'min': 0, 'max': 3},
                'regular': {'min': 3, 'max': 6},
                'bom': {'min': 6, 'max': 10},
                'otimo': {'min': 10, 'max': float('inf')},
                'descricao': 'Rendimento de dividendos. Acima de 6% é considerado bom.'
            },
            'Divida_Liquida_EBITDA': {
                'otimo': {'min': float('-inf'), 'max': 1},
                'bom': {'min': 1, 'max': 2.5},
                'regular': {'min': 2.5, 'max': 3.5},
                'alto': {'min': 3.5, 'max': float('inf')},
                'descricao': 'Capacidade de pagar dívidas. Menor que 2.5 é considerado saudável.'
            },
            'FCF_Yield': {
                'baixo': {'min': 0, 'max': 5},
                'regular': {'min': 5, 'max': 10},
                'bom': {'min': 10, 'max': 15},
                'otimo': {'min': 15, 'max': float('inf')},
                'descricao': 'Rendimento do fluxo de caixa livre. Acima de 10% é considerado bom.'
            }
        }

    def avaliar_indicador(self, nome, valor):
        """Avalia um indicador com base nos valores de referência"""
        if nome not in self.valores_referencia:
            return "Sem referência"
            
        referencias = self.valores_referencia[nome]
        for classificacao, limites in referencias.items():
            if classificacao != 'descricao':
                if limites['min'] <= valor < limites['max']:
                    return classificacao
                    
        return "Não classificado"

    def calcular_indicadores(self):
        """Calcula e avalia os indicadores fundamentalistas"""
        df = pd.DataFrame(self.dados_fundamentalistas)
        ultimo_ano = df.iloc[-1]
        
        indicadores = {}
        for nome, formula in {
            'P/L': lambda: self.dados_mercado['valor_mercado'] / ultimo_ano['lucro_liquido'],
            'P/VP': lambda: self.dados_mercado['valor_mercado'] / ultimo_ano['patrimonio_liquido'],
            'Margem_EBITDA': lambda: (ultimo_ano['ebitda'] / ultimo_ano['receita_liquida']) * 100,
            'Margem_Liquida': lambda: (ultimo_ano['lucro_liquido'] / ultimo_ano['receita_liquida']) * 100,
            'ROE': lambda: (ultimo_ano['lucro_liquido'] / ultimo_ano['patrimonio_liquido']) * 100,
            'Dividend_Yield': lambda: (ultimo_ano['dividendos'] / self.dados_mercado['valor_mercado']) * 100,
            'Divida_Liquida_EBITDA': lambda: ultimo_ano['divida_liquida'] / ultimo_ano['ebitda'],
            'FCF_Yield': lambda: (ultimo_ano['fcf'] / self.dados_mercado['valor_mercado']) * 100
        }.items():
            valor = formula()
            indicadores[nome] = {
                'valor': valor,
                'avaliacao': self.avaliar_indicador(nome, valor),
                'descricao': self.valores_referencia[nome]['descricao']
            }
        
        return indicadores

    def gerar_relatorio_detalhado(self):
        """Gera um relatório detalhado com avaliação dos indicadores"""
        indicadores = self.calcular_indicadores()
        
        print("\n=== ANÁLISE FUNDAMENTALISTA PETR4 ===\n")
        print("INDICADORES PRINCIPAIS:\n")
        
        for nome, info in indicadores.items():
            print(f"{nome}:")
            print(f"  Valor: {info['valor']:.2f}")
            print(f"  Avaliação: {info['avaliacao']}")
            print(f"  Referência: {info['descricao']}")
            print("  Faixas de Referência:")
            
            for classificacao, limites in self.valores_referencia[nome].items():
                if classificacao != 'descricao':
                    if limites['max'] == float('inf'):
                        print(f"    - {classificacao}: > {limites['min']}")
                    else:
                        print(f"    - {classificacao}: {limites['min']} a {limites['max']}")
            print()
        
        return indicadores

    def visualizar_indicadores_radar(self):
        """Cria um gráfico radar dos indicadores normalizados"""
        indicadores = self.calcular_indicadores()
        
        # Normalização dos valores para escala 0-1
        valores_norm = {}
        for nome, info in indicadores.items():
            valor = info['valor']
            ref = self.valores_referencia[nome]
            
            # Definir limites para normalização
            if nome in ['P/L', 'P/VP', 'Divida_Liquida_EBITDA']:
                # Indicadores onde menor é melhor
                max_val = ref['alto']['min']
                min_val = ref['otimo']['min']
                valores_norm[nome] = 1 - min(1, max(0, (valor - min_val) / (max_val - min_val)))
            else:
                # Indicadores onde maior é melhor
                max_val = ref['otimo']['min']
                min_val = ref['ruim']['min'] if 'ruim' in ref else ref['baixo']['min']
                valores_norm[nome] = min(1, max(0, (valor - min_val) / (max_val - min_val)))
        
        # Criar gráfico radar
        categorias = list(valores_norm.keys())
        valores = list(valores_norm.values())
        
        angles = [n / float(len(categorias)) * 2 * np.pi for n in range(len(categorias))]
        valores += valores[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        ax.plot(angles, valores)
        ax.fill(angles, valores, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categorias)
        ax.set_title('Avaliação dos Indicadores (Normalizado)')
        
        return fig

# Exemplo de uso
if __name__ == "__main__":
    analise = AnaliseFundamentalista()
    relatorio = analise.gerar_relatorio_detalhado()
    
    # Gerar visualização
    analise.visualizar_indicadores_radar()
    plt.show()
