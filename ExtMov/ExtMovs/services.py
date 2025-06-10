# ARQUIVO: seu_app/services.py

import csv
from datetime import datetime
from decimal import Decimal
from .models import ExtratoMovimentacao

def processar_extrato_csv(arquivo_csv):
    """
    Processa um arquivo CSV de extrato e salva CADA LINHA como um registro no banco de dados.
    Evita duplicatas usando uma chave composta (produto, data, documento).
    Retorna uma tupla (total_processado, total_criado, total_atualizado, erros).
    """
    erros = []
    linhas_processadas = 0
    criados_count = 0
    atualizados_count = 0
    
    leitor_csv = csv.reader(arquivo_csv, delimiter=';')
    
    try:
        header = next(leitor_csv)
    except StopIteration:
        return 0, 0, 0, ["Arquivo CSV está vazio"]

    for numero_linha, linha in enumerate(leitor_csv, start=2):
        try:
            if not any(field.strip() for field in linha):
                continue

            if len(linha) < 12:
                erros.append(f"Linha {numero_linha}: Número de colunas insuficiente.")
                continue

            # Extração e limpeza dos dados da linha
            loja = linha[0].strip()
            movimentacao = linha[1].strip() # Documento (NF, etc.)
            local = linha[2].strip()
            data_lancamento_str = linha[3].strip()
            data_movimento_str = linha[4].strip()
            codigo_produto = int(linha[5].strip())
            descricao_produto = linha[6].strip()
            
            # Limpeza de valores numéricos (usando Decimal para precisão)
            # Obs: Adaptei para converter para Decimal e depois para Integer no modelo, se necessário.
            # Se seus campos no modelo forem DecimalField, melhor ainda.
            # Corrigido: Salvar como Decimal para corresponder ao modelo
            saldo_anterior = Decimal(linha[9].replace(',', '.'))
            qtd_movimentada = Decimal(linha[10].replace(',', '.'))
            saldo_atual = Decimal(linha[11].replace(',', '.'))

            data_lancamento = datetime.strptime(data_lancamento_str, '%d/%m/%Y').date()
            data_movimento = datetime.strptime(data_movimento_str, '%d/%m/%Y').date()

            # Cria ou atualiza o registro no banco de dados
            # A chave única é a combinação de produto, data e o documento da movimentação
            obj, created = ExtratoMovimentacao.objects.update_or_create(
                codigo_produto=codigo_produto,
                data_movimento=data_movimento,
                movimentacao=movimentacao,
                defaults={
                    'loja': loja,
                    'local': local,
                    'data_lancamento': data_lancamento,
                    'descricao_produto': descricao_produto,
                    'saldo_anterior': saldo_anterior,
                    'qtd_movimentada': qtd_movimentada,
                    'saldo_atual': saldo_atual,
                }
            )
            
            if created:
                criados_count += 1
            else:
                atualizados_count += 1
            
            linhas_processadas += 1

        except Exception as e:
            erros.append(f"Linha {numero_linha}: Erro ao processar - {str(e)}")
            continue

    return linhas_processadas, criados_count, atualizados_count, erros