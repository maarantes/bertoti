import spacy
from spacy.matcher import Matcher
import telebot
from filtro_completo import filtro_completo
from filtros.F01_localizacao import request_location, register_location_handler

# Token do bot
TOKEN = "8008284040:AAF8lUdalNszINj90KHI97So7TdwqNIHmfo"
bot = telebot.TeleBot(TOKEN)

# Carregando o modelo de português do spaCy
nlp = spacy.load("pt_core_news_sm")

# Criando um matcher para capturar preços, anos e quilometragem
matcher = Matcher(nlp.vocab)

# Padrões para capturar preços com o símbolo R$ (ex.: "R$50.000", "R$50000", "R$50.000,00", "R$50 000", etc.)
matcher.add("PRECO", [
    [{"TEXT": "R$"}, {"LIKE_NUM": True}, {"IS_PUNCT": True}, {"LIKE_NUM": True}],  # Exemplo: R$50.000
    [{"TEXT": "R$"}, {"LIKE_NUM": True}, {"IS_PUNCT": False}, {"LIKE_NUM": True}],  # Exemplo: R$50000
    [{"TEXT": "R$"}, {"LIKE_NUM": True}, {"IS_PUNCT": False}],  # Exemplo: R$50000
    [{"TEXT": "R$"}, {"LIKE_NUM": True}, {"TEXT": ","}, {"LIKE_NUM": True}],  # Exemplo: R$50,000
    [{"TEXT": "R$"}, {"LIKE_NUM": True}, {"IS_SPACE": True}, {"LIKE_NUM": True}],  # Exemplo: R$50 000
])

# Padrões para capturar anos (ex.: "2018", "de 2018 a 2022")
matcher.add("ANO", [[{"LIKE_NUM": True}],
                    [{"TEXT": "de"}, {"LIKE_NUM": True}, {"TEXT": "a"}, {"LIKE_NUM": True}]])

# Padrões para capturar quilometragem (ex.: "30.000 km", "30000 km", "30.000 km até 50.000 km")
matcher.add("KM", [
    [{"LIKE_NUM": True}, {"TEXT": "km"}],  # Exemplo: 30.000 km
    [{"LIKE_NUM": True}, {"TEXT": "mil"}],  # Exemplo: 30 mil
    [{"LIKE_NUM": True}, {"TEXT": "km"}, {"TEXT": "até"}, {"LIKE_NUM": True}, {"TEXT": "km"}]  # Exemplo: 30.000 km até 50.000 km
])

# Função para formatar a cidade e o estado
def formatar_cidade_estado(cidade_estado):
    partes = cidade_estado.split(" - ")
    if len(partes) == 2:
        cidade = partes[0].strip().lower().replace(" ", "-")
        estado = partes[1].strip().lower()
        return f"{estado}-{cidade}"
    return cidade_estado.lower().replace(" ", "-")

# Função para extrair filtros de uma mensagem
def extrair_filtros(frase):
    doc = nlp(frase)
    filtros = {
        "cidade": None,
        "marca": None,
        "categoria": None,
        "preco_min": None,
        "preco_max": None,
        "ano_min": None,
        "ano_max": None,
        "cambio": None,
        "quilometragem": None,
        "km_minimo": None,
        "km_maximo": None
    }

    # Extração de entidades
    for ent in doc.ents:
        if ent.label_ == "LOC":  # Localização
            filtros["cidade"] = ent.text
        elif ent.label_ == "ORG":  # Marca
            filtros["marca"] = ent.text

    # Extração de palavras-chave
    for token in doc:
        if token.text.lower() in ["suv", "sedan", "hatch"]:
            filtros["categoria"] = token.text
        elif token.text.lower() in ["automático", "manual"]:
            filtros["cambio"] = token.text

    # Aplicar o Matcher para preços, anos e quilometragem
    matches = matcher(doc)
    for match_id, start, end in matches:
        match = doc[start:end]
        if nlp.vocab.strings[match_id] == "PRECO":
            valores = match.text.replace("R$", "").replace(".", "").replace(",", "").replace(" ", "").split()
            if len(valores) == 2: 
                filtros["preco_min"], filtros["preco_max"] = valores
            elif len(valores) == 1:  
                filtros["preco_min"] = valores[0]

        elif nlp.vocab.strings[match_id] == "ANO":
            valores = match.text.split()
            if len(valores) == 4:
                filtros["ano_min"], filtros["ano_max"] = valores[1], valores[3]

        elif nlp.vocab.strings[match_id] == "KM":
            # Se for um intervalo de quilometragem
            if "até" in match.text:
                valores = match.text.split(" até ")
                filtros["km_minimo"] = valores[0].replace("km", "").strip()
                filtros["km_maximo"] = valores[1].replace("km", "").strip()
            else:
                filtros["quilometragem"] = match.text.replace("km", "").strip()

    # Formatar a cidade antes de passar para o filtro
    if filtros["cidade"]:
        filtros["cidade"] = formatar_cidade_estado(filtros["cidade"])

    return filtros

# Função de boas-vindas
@bot.message_handler(commands=["start"])
def send_welcome(message):
    nome_usuario = message.from_user.first_name
    file_id = "AgACAgEAAxkDAAICm2cK5i32HYjNGHarjEQ0e3F4sWDRAALJrDEbIMFYRAOkwenIeTeZAQADAgADeQADNgQ"
    
    bot.send_photo(
        message.chat.id, 
        file_id, 
        caption=f"Olá, {nome_usuario}! Escolha como deseja continuar:\n\n1. Pesquisa por Categoria e Localização Atual\n2. Descrever sua pesquisa detalhadamente"
    )

# Aguardar a resposta do usuário para escolher o fluxo
@bot.message_handler(func=lambda message: message.text in ["1", "2"])
def escolher_fluxo(message):
    if message.text == "1":
        # Fluxo Tradicional
        bot.send_message(message.chat.id, "Você escolheu o Pesquisa por Categoria e Localização Atual. Vamos começar filtrando os carros da Localiza!")
        request_location(bot, message)  # Pedindo localização no fluxo tradicional
    elif message.text == "2":
        # Fluxo de Linguagem Natural (com Spacy)
        bot.send_message(message.chat.id, "Você escolheu o Pesquisa detalhada. Digite o que procura, e eu vou filtrar os carros para você.")

# Processar mensagens para extrair filtros e usar o filtro_completo (caso o fluxo natural seja escolhido)
@bot.message_handler(func=lambda message: message.text and message.text not in ["1", "2"])
def process_message(message):
    filtros = extrair_filtros(message.text)

    # Formatando a mensagem de filtros para uma visualização mais amigável
    filtros_formatados = ""

    if filtros["cidade"]:
        filtros_formatados += f"Cidade: {filtros['cidade']}\n"
    if filtros["marca"]:
        filtros_formatados += f"Marca: {filtros['marca']}\n"
    if filtros["categoria"]:
        filtros_formatados += f"Categoria: {filtros['categoria']}\n"
    
    # Preço
    if filtros["preco_min"] and filtros["preco_max"]:
        filtros_formatados += f"Preço: R${filtros['preco_min']} - R${filtros['preco_max']}\n"
    elif filtros["preco_min"]:
        filtros_formatados += f"Preço mínimo: R${filtros['preco_min']}\n"
    elif filtros["preco_max"]:
        filtros_formatados += f"Preço máximo: R${filtros['preco_max']}\n"
    
    # Quilometragem
    if filtros["km_minimo"] and filtros["km_maximo"]:
        filtros_formatados += f"Quilometragem: {filtros['km_minimo']} km - {filtros['km_maximo']} km\n"
    elif filtros["km_minimo"]:
        filtros_formatados += f"Quilometragem mínima: {filtros['km_minimo']} km\n"
    elif filtros["km_maximo"]:
        filtros_formatados += f"Quilometragem máxima: {filtros['km_maximo']} km\n"
    
    # Ano
    if filtros["ano_min"] and filtros["ano_max"]:
        filtros_formatados += f"Ano: {filtros['ano_min']} - {filtros['ano_max']}\n"
    elif filtros["ano_min"]:
        filtros_formatados += f"Ano mínimo: {filtros['ano_min']}\n"
    elif filtros["ano_max"]:
        filtros_formatados += f"Ano máximo: {filtros['ano_max']}\n"
    
    # Câmbio
    if filtros["cambio"]:
        filtros_formatados += f"Câmbio: {filtros['cambio']}\n"

    # Enviar a mensagem formatada para o usuário
    bot.reply_to(message, f"Filtros identificados:\n\n{filtros_formatados.strip()}")

    # Chamando a função filtro_completo com os filtros extraídos
    if filtros:
        filtro_completo(
            bot,
            message,
            cidade_escolhida=filtros["cidade"],
            categoria_escolhida=filtros["categoria"],
            preco_min=filtros["preco_min"],
            preco_max=filtros["preco_max"],
            km_minimo=filtros.get("km_minimo", None),
            km_maximo=filtros.get("km_maximo", None),
            ano_min=filtros["ano_min"],
            ano_max=filtros["ano_max"],
            marca_escolhida=filtros["marca"],
            cambio_escolhido=filtros["cambio"],
        )


register_location_handler(bot)

if __name__ == "__main__":
    bot.polling()
