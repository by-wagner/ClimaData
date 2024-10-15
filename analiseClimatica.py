import csv
from datetime import datetime
import matplotlib.pyplot as plt


# Funções de carregamento e validação de dados

def carregar_dados(nome_arquivo):
    """
    Carrega os dados do arquivo CSV.

    Decisões:
    1. Ignora a primeira linha (cabeçalho) do arquivo.
    2. É realizado uma conversão de strings vazias para 0 ou None evitando erros.
    3. É utilizado um dicionário para cada registro facilitando acesso aos dados.
    """
    dados = []
    with open(nome_arquivo, 'r') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)
        for linha in leitor:
            data = datetime.strptime(linha[0], '%d/%m/%Y')
            registro = {
                'data': data,
                'precip': float(linha[1]) if linha[1] else 0,
                'maxima': float(linha[2]) if linha[2] else None,
                'minima': float(linha[3]) if linha[3] else None,
                'horas_insol': float(linha[4]) if linha[4] else 0,
                'temp_media': float(linha[5]) if linha[5] else None,
                'um_relativa': float(linha[6]) if linha[6] else None,
                'vel_vento': float(linha[7]) if linha[7] else 0
            }
            dados.append(registro)
    return dados


def validar_mes(mes):
    return 1 <= mes <= 12


def validar_ano(ano):
    return 1961 <= ano <= 2016


# Funções de análise de dados

def visualizar_intervalo(dados, data_inicio, data_fim, tipo_dado):
    """
    Exibe os dados no intervalo selecionado.

    Decisões:
    1. Formata a saída para melhor legibilidade.
    2. Permiti a visualização de diferentes tipos de dados.
    """
    print("\nDados no intervalo selecionado:")

    if tipo_dado == 1:
        print(
            f"{'Data':<12}{'Precip(mm)':>10}{'Máx(°C)':>9}{'Mín(°C)':>9}{'Insol(h)':>10}{'Méd(°C)':>9}{'UR(%)':>8}{'Vel.Vento(m/s)':>15}")
        print("-" * 82)
        for dado in dados:
            if data_inicio <= dado['data'] <= data_fim:
                print(
                    f"{dado['data'].strftime('%d/%m/%Y'):<12}{dado['precip']:10.1f}{dado['maxima']:9.1f}{dado['minima']:9.1f}{dado['horas_insol']:10.1f}{dado['temp_media']:9.1f}{dado['um_relativa']:8.1f}{dado['vel_vento']:15.1f}")

    elif tipo_dado == 2:
        print(f"{'Data':<12}{'Precipitação(mm)':>18}")
        print("-" * 30)
        for dado in dados:
            if data_inicio <= dado['data'] <= data_fim:
                print(f"{dado['data'].strftime('%d/%m/%Y'):<12}{dado['precip']:18.1f}")

    elif tipo_dado == 3:
        print(f"{'Data':<12}{'Máxima(°C)':>12}{'Mínima(°C)':>12}{'Média(°C)':>12}")
        print("-" * 48)
        for dado in dados:
            if data_inicio <= dado['data'] <= data_fim:
                print(
                    f"{dado['data'].strftime('%d/%m/%Y'):<12}{dado['maxima']:12.1f}{dado['minima']:12.1f}{dado['temp_media']:12.1f}")

    elif tipo_dado == 4:
        print(f"{'Data':<12}{'Umidade Relativa(%)':>20}{'Vel. Vento(m/s)':>18}")
        print("-" * 50)
        for dado in dados:
            if data_inicio <= dado['data'] <= data_fim:
                print(f"{dado['data'].strftime('%d/%m/%Y'):<12}{dado['um_relativa']:20.1f}{dado['vel_vento']:18.1f}")


def mes_mais_chuvoso(dados):
    """
    Encontra o mês mais chuvoso.

    Decisão:
    Usa um dicionário para somar a precipitação por mês/ano.
    """
    precipitacao_mensal = {}
    for dado in dados:
        chave = (dado['data'].year, dado['data'].month)
        precipitacao_mensal[chave] = precipitacao_mensal.get(chave, 0) + dado['precip']

    mes_max = max(precipitacao_mensal, key=precipitacao_mensal.get)
    return mes_max, precipitacao_mensal[mes_max]


def media_temperatura_minima(dados, mes, ano_inicio, ano_fim):
    """
    Calcula a média da temperatura mínima para um mês específico ao longo dos anos.

    Decisão:
    Ignora os dados nulos (None) ao calcular a média.
    """
    medias = {}
    for ano in range(ano_inicio, ano_fim + 1):
        temps = [d['minima'] for d in dados if
                 d['data'].year == ano and d['data'].month == mes and d['minima'] is not None]
        if temps:
            medias[f"{mes:02d}/{ano}"] = sum(temps) / len(temps)
    return medias


def gerar_grafico_temperaturas(medias):
    """Gera um gráfico de barras com as médias de temperatura."""
    anos = list(medias.keys())
    temperaturas = list(medias.values())

    plt.figure(figsize=(12, 6))
    plt.bar(anos, temperaturas, color='skyblue')
    plt.title('Média de Temperatura Mínima por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Função principal

def main():
    nome_arquivo = 'data/Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv'
    dados = carregar_dados(nome_arquivo)

    while True:
        print("\nEscolha uma opção:")
        print("1. Visualizar intervalo de dados")
        print("2. Encontrar mês mais chuvoso")
        print("3. Calcular média de temperatura mínima")
        print("4. Sair")

        try:
            opcao = int(input("Digite sua escolha (1-4): "))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if opcao == 1:
            try:
                ano_inicio = int(input("Digite o ano inicial: "))
                mes_inicio = int(input("Digite o mês inicial (1-12): "))
                ano_fim = int(input("Digite o ano final: "))
                mes_fim = int(input("Digite o mês final (1-12): "))

                if not (validar_ano(ano_inicio) and validar_ano(ano_fim) and
                        validar_mes(mes_inicio) and validar_mes(mes_fim)):
                    raise ValueError("Datas inválidas")

                data_inicio = datetime(ano_inicio, mes_inicio, 1)
                data_fim = datetime(ano_fim, mes_fim, 28)

                tipo_dado = int(
                    input("Escolha o tipo de dado (1-Todos, 2-Precipitação, 3-Temperatura, 4-Umidade/Vento): "))
                if tipo_dado not in [1, 2, 3, 4]:
                    raise ValueError("Tipo de dado inválido")

                visualizar_intervalo(dados, data_inicio, data_fim, tipo_dado)
            except ValueError as e:
                print(f"Entrada inválida: {e}")

        elif opcao == 2:
            mes_max, precipitacao_max = mes_mais_chuvoso(dados)
            print(f"\nMês mais chuvoso: {mes_max[1]}/{mes_max[0]} com {precipitacao_max:.2f}mm de precipitação")

        elif opcao == 3:
            try:
                mes = int(input("Digite o mês para análise (1-12): "))
                if not validar_mes(mes):
                    raise ValueError("Mês inválido")

                medias = media_temperatura_minima(dados, mes, 2006, 2016)
                print("\nMédias de temperatura mínima:")
                for ano, media in medias.items():
                    print(f"{ano}: {media:.2f}°C")

                gerar_grafico_temperaturas(medias)

                media_geral = sum(medias.values()) / len(medias)
                print(f"\nMédia geral da temperatura mínima de {mes}/2006-2016: {media_geral:.2f}°C")
            except ValueError as e:
                print(f"Entrada inválida: {e}")

        elif opcao == 4:
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()