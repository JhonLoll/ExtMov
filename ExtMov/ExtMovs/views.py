import io
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .services import processar_extrato_csv
from django.db.models import Sum, Q, Value
from django.db.models.functions import Coalesce

from ExtMovs.models import ExtratoMovimentacao

# Obter o modelo de usuário personalizado
User = get_user_model()

# Create your views here.

# View para a página inicial
@login_required
def index(request):
    return render(request, 'index.html')

# View para a página de login
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('extrato')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('signin')
        
    return render(request, 'login/signin.html')
        
# View para a página de cadastro
def signup(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar_senha = request.POST['confirmarsenha']

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não conferem. Tente novamente.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está em uso. Tente outro.')
            return redirect('signup')
        
        try:
            user = User.objects.create_user(email=email, nome=nome, password=senha)
            login(request, user)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('extrato')
        
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar usuário: {e}. Tente novamente.')
            return redirect('signup')
    
    return render(request, 'login/signup.html')

# View para o logout
def sair(request):
    logout(request)
    return redirect('signin')

# View para a página de extrato
@login_required
def extrato(request):
    movimentacoes_qs = ExtratoMovimentacao.objects.all()

    # Obter lista de lojas únicas para o filtro
    lojas_unicas = ExtratoMovimentacao.objects.order_by('loja').values_list('loja', flat=True).distinct()

    # Filtros (a lógica de filtro continua a mesma)
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    loja = request.GET.get('loja')
    codigo_produto = request.GET.get('productCode')

    if start_date:
        movimentacoes_qs = movimentacoes_qs.filter(data_movimento__gte=start_date)
    if end_date:
        movimentacoes_qs = movimentacoes_qs.filter(data_movimento__lte=end_date)
    if loja:
        movimentacoes_qs = movimentacoes_qs.filter(loja=loja)
    if codigo_produto:
        movimentacoes_qs = movimentacoes_qs.filter(codigo_produto__icontains=codigo_produto)

    # Ordenar as movimentações para exibição na tabela
    movimentacoes_ordenadas = movimentacoes_qs.order_by('-data_movimento') # Alterado para ordem descendente

    # Calcula os totais para os cards de resumo (baseado nas movimentações filtradas)
    # Total de Entradas (soma das quantidades positivas)
    total_entradas = movimentacoes_qs.filter(qtd_movimentada__gt=0).aggregate(soma=Sum('qtd_movimentada'))['soma'] or 0
    # Total de Saídas (soma das quantidades negativas, em valor absoluto)
    total_saidas_negativo = movimentacoes_qs.filter(qtd_movimentada__lt=0).aggregate(soma=Sum('qtd_movimentada'))['soma'] or 0
    total_saidas = abs(total_saidas_negativo)
    # Saldo Geral (soma líquida das movimentações)
    saldo_geral = movimentacoes_qs.aggregate(soma=Sum('saldo_atual'))['soma'] or 0
    
    context = {
        # Passamos a lista de movimentações filtradas e ordenadas para o template
        'movimentacoes': movimentacoes_ordenadas,
        'total_entradas': total_entradas, # Corrigido: Usar total_entradas
        'total_saidas': total_saidas,
        'saldo_geral': saldo_geral,
        'valores_filtro': request.GET,
        'lojas_unicas': lojas_unicas, # Passar lojas únicas para o filtro
    }
    
    return render(request, 'extrato/extrato.html', context)


# View para a página de upload de arquivo - CORRIGIDA
@login_required
def upload_extrato(request):
    if request.method == 'POST':
        # Verifica se um arquivo foi enviado
        if 'extratoFile' not in request.FILES:
            messages.error(request, 'Nenhum arquivo foi selecionado.')
            return redirect('extrato')

        arquivo_upado = request.FILES['extratoFile']

        # Validação do tipo de arquivo
        if not arquivo_upado.name.endswith('.csv'):
            messages.error(request, 'Formato de arquivo inválido. Por favor, envie um arquivo .csv')
            return redirect('extrato')
        
        try:
            # CORRIGIDO: Lê o conteúdo do arquivo uma vez e tenta diferentes encodings
            conteudo_arquivo = arquivo_upado.read()
            
            arquivo_decodificado = None
            encodings_para_tentar = ['utf-8', 'windows-1252', 'iso-8859-1', 'cp1252', 'latin-1']
            
            for encoding in encodings_para_tentar:
                try:
                    # Decodifica o conteúdo binário para string
                    conteudo_texto = conteudo_arquivo.decode(encoding)
                    # Cria um objeto StringIO para simular um arquivo
                    arquivo_decodificado = io.StringIO(conteudo_texto)
                    break  # Se chegou aqui, o encoding funcionou
                except (UnicodeDecodeError, UnicodeError):
                    continue
            
            if arquivo_decodificado is None:
                messages.error(request, 'Não foi possível decodificar o arquivo. Verifique o formato.')
                return redirect('extrato')
            
            # CORRIGIDO: Trata os 4 valores retornados pela função
            total, criados, atualizados, erros = processar_extrato_csv(arquivo_decodificado)

            # Exibe erros se houver
            if erros:
                for erro in erros[:5]:  # Mostra apenas os primeiros 5 erros
                    messages.warning(request, f'Aviso: {erro}')
                if len(erros) > 5:
                    messages.warning(request, f'... e mais {len(erros) - 5} erros.')

            if total > 0:
                messages.success(request, 
                    f'Importação concluída! {total} produtos processados '
                    f'({criados} criados, {atualizados} atualizados).'
                )
            else:
                messages.error(request, 'Nenhum produto foi processado. Verifique o formato do arquivo.')
        
        except Exception as e:
            messages.error(request, f'Ocorreu um erro durante o processamento do arquivo: {e}')
        
        return redirect('extrato')

    # Se alguém tentar acessar a URL via GET, apenas redireciona
    return redirect('extrato')
