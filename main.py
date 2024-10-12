import telebot
from geopy.distance import geodesic

# Token do bot
TOKEN = '8008284040:AAF8lUdalNszINj90KHI97So7TdwqNIHmfo'

bot = telebot.TeleBot(TOKEN)

cidade_escolhida = ""
categoria_escolhida = ""
preco_min = ""
preco_max = ""
km_minimo = ""
km_maximo = ""
ano_min = ""
ano_max = ""
marca_escolhida = ""
cambio_escolhido = ""

cidades = {
    "Americana - SP": (-22.7377, -47.3331),
    "Ananindeua - PA": (-1.3641, -48.3721),
    "Anápolis - GO": (-16.3281, -48.9534),
    "Araçatuba - SP": (-21.2076, -50.4323),
    "Araraquara - SP": (-21.7948, -48.1756),
    "Salvador - BA": (-12.9714, -38.5014),
    "Barreiras - BA": (-12.1462, -44.9964),
    "Barueri - SP": (-23.5057, -46.8799),
    "Bauru - SP": (-22.3145, -49.0587),
    "Campinas - SP": (-22.9099, -47.0626),
    "Canoas - RS": (-29.9173, -51.1835),
    "Caruaru - PE": (-8.2848, -35.9696),
    "Cascavel - PR": (-24.9555, -53.4553),
    "Lages - SC": (-27.815, -50.3264),
    "Macapá - AP": (0.0345, -51.0694),
    "Maceió - AL": (-9.6658, -35.735),
    "Manaus - AM": (-3.1190, -60.0217),
    "Marabá - PA": (-5.3811, -49.1324),
    "Marília - SP": (-22.2171, -49.9501),
    "Maringá - PR": (-23.4205, -51.9331),
    "Mauá - SP": (-23.6678, -46.4613),
    "Natal - RN": (-5.7945, -35.211),
    "Palmas - TO": (-10.2491, -48.3243),
    "Santarém - PA": (-2.4385, -54.6996),
    "Taguatinga - DF": (-15.8366, -48.0575),
    "Taubaté - SP": (-23.0269, -45.5556),
    "Aparecida de Goiânia - GO": (-16.8198, -49.2469),
    "Brasília - DF": (-15.7942, -47.8822),
    "Chapecó - SC": (-27.1000, -52.6166),
    "Franca - SP": (-20.5352, -47.4015),
    "Gravataí - RS": (-29.9425, -50.9914),
    "Guarapuava - PR": (-25.3902, -51.4622),
    "Guarulhos - SP": (-23.4542, -46.5336),
    "Ipatinga - MG": (-19.4683, -42.536),
    "Itabuna - BA": (-14.7882, -39.2806),
    "Itaguaí - RJ": (-22.8527, -43.7759),
    "Itajaí - SC": (-26.9101, -48.6705),
    "Osasco - SP": (-23.5328, -46.791),
    "Goiânia - GO": (-16.6869, -49.2648),
    "Cuiabá - MT": (-15.6014, -56.0979),
    "Indaiatuba - SP": (-23.0885, -47.208),
    "Piracicaba - SP": (-22.7338, -47.6476),
    "São Paulo - SP": (-23.5505, -46.6333),
    "Cabo Frio - RJ": (-22.8894, -42.0281),
    "Campina Grande - PB": (-7.2291, -35.8808),
    "Campo Grande - MS": (-20.4697, -54.6201),
    "Pato Branco - PR": (-26.229, -52.6706),
    "Santa Maria - RS": (-29.6842, -53.8069),
    "Santo André - SP": (-23.663, -46.5383),
    "São Carlos - SP": (-22.0074, -47.8901),
    "São Gonçalo - RJ": (-22.8268, -43.0635),
    "São José - SC": (-27.5969, -48.6172),
    "São Leopoldo - RS": (-29.754, -51.1492),
    "São Luís - MA": (-2.5387, -44.2825),
    "Várzea Grande - MT": (-15.6458, -56.1322),
    "Fortaleza - CE": (-3.7172, -38.5434),
    "Contagem - MG": (-19.9317, -44.0537),
    "Dourados - MS": (-22.2231, -54.805),
    "Ji-Paraná - RO": (-10.8777, -61.9321),
    "Linhares - ES": (-19.3946, -40.0641),
    "Serra - ES": (-20.121, -40.3072),
    "Sobral - CE": (-3.6904, -40.3499),
    "Uberaba - MG": (-19.7477, -47.9381),
    "Florianópolis - SC": (-27.5954, -48.548),
    "Imperatriz - MA": (-5.5268, -47.4914),
    "Jundiaí - SP": (-23.1855, -46.8978),
    "Pelotas - RS": (-31.7654, -52.3371),
    "Sorocaba - SP": (-23.5015, -47.4526),
    "Uberlândia - MG": (-18.9128, -48.2754),
    "Blumenau - SC": (-26.9194, -49.0661),
    "Limeira - SP": (-22.5646, -47.4015),
    "Vitória - ES": (-20.3155, -40.3128),
    "Boa Vista - RR": (2.8235, -60.6758),
    "João Pessoa - PB": (-7.115, -34.8641),
    "Praia Grande - SP": (-24.0058, -46.402),
    "Curitiba - PR": (-25.4284, -49.2733),
    "Criciúma - SC": (-28.6775, -49.3697),
    "Londrina - PR": (-23.304, -51.1696),
    "Teresina - PI": (-5.0919, -42.8034),
    "Campos dos Goytacazes - RJ": (-21.762, -41.3181),
    "Caxias do Sul - RS": (-29.1629, -51.1792),
    "Jaboatão dos Guararapes - PE": (-8.112, -35.0145),
    "Jaraguá do Sul - SC": (-26.4854, -49.0663),
    "Lauro de Freitas - BA": (-12.8943, -38.3247),
    "Petrolina - PE": (-9.3887, -40.5027),
    "Nova Iguaçu - RJ": (-22.7555, -43.4603),
    "Vila Velha - ES": (-20.3297, -40.292),
    "São Bernardo do Campo - SP": (-23.6914, -46.5646),
    "São Caetano do Sul - SP": (-23.6229, -46.5548),
    "São José dos Campos - SP": (-23.2237, -45.9009),
    "Ponta Grossa - PR": (-25.0916, -50.1619),
    "Volta Redonda - RJ": (-22.5231, -44.1041),
    "Juazeiro do Norte - CE": (-7.2127, -39.3157),
    "São José do Rio Preto - SP": (-20.8113, -49.3758),
    "Porto Alegre - RS": (-30.0346, -51.2177),
    "Ribeirão Preto - SP": (-21.1699, -47.8099),
    "Feira de Santana - BA": (-12.2664, -38.9663),
    "Rio das Ostras - RJ": (-22.5174, -41.945),
    "Montes Claros - MG": (-16.7282, -43.8578),
    "Mogi das Cruzes - SP": (-23.5208, -46.1853),
    "Vitória da Conquista - BA": (-14.8615, -40.8445),
    "Rio de Janeiro - RJ": (-22.9068, -43.1729),
    "Duque de Caxias - RJ": (-22.7859, -43.3044)
}


# Função para iniciar a conversa
@bot.message_handler(commands=['start'])

def send_welcome(message):
    nome_usuario = message.from_user.first_name
    
    # Certifique-se de que o file_id seja uma string (coloque-o entre aspas)
    file_id = "AgACAgEAAxkDAAICm2cK5i32HYjNGHarjEQ0e3F4sWDRAALJrDEbIMFYRAOkwenIeTeZAQADAgADeQADNgQ"
    
    # Enviar a imagem usando o file_id
    sent_message = bot.send_photo(message.chat.id, file_id, caption=f"Olá, {nome_usuario}! Hoje eu vou te ajudar a escolher o carro seminovo perfeito para você na Localiza Seminovos.")
    
    # Continuar o fluxo de solicitação de localização
    request_location(message)

# Função para pedir a localização do usuário
def request_location(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Enviar localização", request_location=True)
    markup.add(button_geo)
    bot.send_message(message.chat.id, "(1/7) Localização\nVamos começar a filtragem pela sua localização. Primeiro, vou procurar a cidade com uma unidade da Localiza mais próxima de você.")
    bot.send_message(message.chat.id, "Por favor, clique no botão abaixo para eu receber sua localização atual.\nLembrete: É necessário usar seu celular para enviar sua localização!", reply_markup=markup)

# Função para encontrar a cidade mais próxima
def find_nearest_city(user_location):
    nearest_city = None
    nearest_distance = float('inf')

    for city, coords in cidades.items():
        # Calcula a distância geodésica entre o usuário e a cidade
        distance = geodesic(user_location, coords).kilometers
        if distance < nearest_distance:
            nearest_city = city
            nearest_distance = distance

    return nearest_city, nearest_distance

def formatar_cidade_estado(cidade_estado):

    partes = cidade_estado.split(" - ")
    if len(partes) == 2:
        cidade = partes[0].strip().lower().replace(" ", "-")
        estado = partes[1].strip().lower()
        return f"{estado}-{cidade}"
    return cidade_estado.lower().replace(" ", "-")

# Função para lidar com a localização enviada pelo usuário
@bot.message_handler(content_types=['location'])
def handle_location(message):

    global cidade_escolhida

    nome_usuario = message.from_user.first_name

    if message.location is not None:
        user_location = (message.location.latitude, message.location.longitude)
        bot.reply_to(message, f"Recebi sua localização, {nome_usuario}." )
        
        # Encontrar a cidade mais próxima
        nearest_city, nearest_distance = find_nearest_city(user_location)
        bot.send_message(message.chat.id, f"A unidade Localiza mais próxima fica em {nearest_city}, a uma distância de {nearest_distance:.2f} km.", parse_mode='Markdown')
        cidade_escolhida = formatar_cidade_estado(nearest_city)
        request_category(message)

# Função para mostrar os botões de categoria
def request_category(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    # Criar os botões de categoria
    button1 = telebot.types.KeyboardButton('Hatch')
    button2 = telebot.types.KeyboardButton('Sedan')
    button3 = telebot.types.KeyboardButton('SUV')
    button4 = telebot.types.KeyboardButton('Picape')
    button5 = telebot.types.KeyboardButton('Minivan')
    button6 = telebot.types.KeyboardButton('Furgão')
    button_skip = telebot.types.KeyboardButton('Pular')

    # Adicionar os botões ao teclado
    markup.add(button1, button2, button3, button4, button5, button6, button_skip)

    bot.send_message(message.chat.id, "(2/7) Categoria de Carro\nAgora, escolha uma categoria:", reply_markup=markup)

# Função para lidar com a escolha da categoria
@bot.message_handler(func=lambda message: message.text in ['Hatch', 'Sedan', 'SUV', 'Picape', 'Minivan', 'Furgão', 'Pular'])

def handle_category(message):
    global categoria_escolhida
    if message.text == 'Pular':
        bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
        categoria_escolhida = ""
    else:
        tipo_escolhido = message.text.upper()
        categoria_escolhida = tipo_escolhido
    
    request_preco_min(message)

# Função para pedir o preço mínimo
def request_preco_min(message):

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton('Pular')
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(3/7) Preço Mínimo\nAgora, digite o preço mínimo:", reply_markup=markup)

    bot.register_next_step_handler(message, handle_preco_min)

# Função para lidar com o preço mínimo
def handle_preco_min(message):

    global preco_min

    if message.text  == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
        request_km_min(message)
        return

    try:
        preco_min = int(message.text.replace("R$", "").replace(",", "").strip())
        bot.reply_to(message, f"Preço mínimo definido: R$ {preco_min}")
        request_preco_max(message)  # Chama a função para pedir o preço máximo
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, handle_preco_min)  # Pede o preço mínimo novamente

# Função para pedir o preço máximo (não pode ser pulado)
def request_preco_max(message):
    bot.send_message(message.chat.id, "Agora, digite o preço máximo:")

    # Registra o próximo passo para lidar com o preço máximo
    bot.register_next_step_handler(message, handle_preco_max)

# Função para lidar com o preço máximo (obrigatório)
def handle_preco_max(message):

    global preco_max

    try:
        preco_max = int(message.text.replace("R$", "").replace(",", "").strip())  # Guarda o valor como inteiro
        
        # Verifica se o preço máximo é menor que o preço mínimo
        if preco_max <= preco_min:
            bot.reply_to(message, "O preço máximo deve ser maior que preço mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, handle_preco_max)  # Pede o preço máximo novamente
        else:
            bot.reply_to(message, f"Preço máximo definido: R${preco_max}")
            request_km_min(message)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número.")
        bot.register_next_step_handler(message, handle_preco_max)  # Pede o preço máximo novamente

# Função para pedir o KM mínimo
def request_km_min(message):

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton("Pular")
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(4/7) KMs Rodados\nDigite o KM mínimo:",  reply_markup=markup)

    # Registra o próximo passo para lidar com o KM mínimo
    bot.register_next_step_handler(message, handle_km_min)

# Função para lidar com o KM mínimo
def handle_km_min(message):

    global km_minimo

    if message.text == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
        request_ano_min(message)
        return

    try:
        km_minimo = int(message.text.replace("Km", "").replace(",", "").strip())  # Guarda o valor como inteiro
        bot.reply_to(message, f"KM mínimo definido: {km_minimo} Km")
        request_km_max(message)  # Chama a função para pedir o KM máximo
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, handle_km_min)  # Pede o KM mínimo novamente

# Função para pedir o KM máximo
def request_km_max(message):
    bot.send_message(message.chat.id, "Agora, digite o KM máximo:")

    # Registra o próximo passo para lidar com o KM máximo
    bot.register_next_step_handler(message, handle_km_max)

# Função para lidar com o KM máximo
def handle_km_max(message):

    global km_maximo

    try:
        km_maximo = int(message.text.replace("Km", "").replace(",", "").strip())  # Guarda o valor como inteiro
        
        # Verifica se o KM máximo é menor que o KM mínimo
        if km_maximo <= km_minimo:
            bot.reply_to(message, "O KM máximo deve ser maior que KM mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, handle_km_max)  # Pede o KM máximo novamente
        else:
            bot.reply_to(message, f"KM máximo definido: {km_maximo} Km")
            request_ano_min(message)  # Chama a função para finalizar o filtro de KM
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, handle_km_max)  # Pede o KM máximo novamente

# Função para pedir o ano mínimo
def request_ano_min(message):
    
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton('Pular')
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(5/7) Ano de Fabricação\nAgora, digite o ano mínimo:", reply_markup=markup)

    # Registra o próximo passo para lidar com o ano mínimo
    bot.register_next_step_handler(message, handle_ano_min)

# Função para lidar com o ano mínimo
def handle_ano_min(message):

    global ano_min

    if message.text == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
        request_marca(message)
        return

    try:
        ano_min = int(message.text.strip())
        bot.reply_to(message, f"Ano mínimo definido: {ano_min}")
        request_ano_max(message)  # Chama a função para pedir o ano máximo
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, handle_ano_min)  # Pede o ano mínimo novamente

# Função para pedir o ano máximo (não pode ser menor que o mínimo)
def request_ano_max(message):
    bot.send_message(message.chat.id, "Agora, digite o ano máximo:")

    # Registra o próximo passo para lidar com o ano máximo
    bot.register_next_step_handler(message, handle_ano_max)

# Função para lidar com o ano máximo
def handle_ano_max(message):

    global ano_max, ano_min

    try:
        ano_max = int(message.text.strip())  # Guarda o valor como inteiro
        
        # Verifica se o ano máximo é menor que o ano mínimo
        if ano_max < ano_min:
            bot.reply_to(message, "O ano máximo deve ser maior ou igual ao ano mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, handle_ano_max)  # Pede o ano máximo novamente
        else:
            bot.reply_to(message, f"Ano máximo definido: {ano_max}")
            request_marca(message)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, handle_ano_max)  # Pede o ano máximo novamente

# Função para pedir a marca
def request_marca(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Criar os botões de marca
    marcas = ["Ford", "Volkswagen", "Fiat", "Jeep", "Renault", "Citroen", "Chevrolet", "Toyota", 
              "Nissan", "Hyundai", "Peugeot", "Mercedes-Benz", "Audi", "Volvo", "Mitsubishi", 
              "BMW", "Land Rover", "Honda", "Jaguar", "Chery", "BYD", "Pular"]

    # Adicionar os botões ao markup
    for i in range(0, len(marcas), 3):
        markup.add(*marcas[i:i+3])

    bot.send_message(message.chat.id, "(6/7) Marca\nAgora, escolha a marca do carro:", reply_markup=markup)

    bot.register_next_step_handler(message, handle_marca)

# Função para lidar com a escolha da marca
def handle_marca(message):

    global marca_escolhida
    
    if message.text == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o último passo.")
        request_cambio(message)
        return
    
    marca_escolhida = message.text  # Armazena a marca escolhida
    bot.reply_to(message, f"Você escolheu a marca {marca_escolhida}.")
    
    request_cambio(message)

def request_cambio(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Criar os botões de câmbio
    button1 = telebot.types.KeyboardButton('Automático')
    button2 = telebot.types.KeyboardButton('Manual')
    button3 = telebot.types.KeyboardButton('Pular')

    # Adicionar os botões ao markup
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Escolha o tipo de câmbio:", reply_markup=markup)

    bot.register_next_step_handler(message, handle_cambio)

# Função para lidar com a escolha do tipo de câmbio
def handle_cambio(message):
    
    global cambio_escolhido

    if message.text == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o último passo.")
        finalize_filtros(message)
        return
    
    cambio_escolhido = message.text  # Armazena o câmbio escolhido
    bot.reply_to(message, f"Você escolheu o câmbio {cambio_escolhido}.")
    
    # Agora finaliza o filtro com todas as escolhas feitas
    finalize_filtros(message)

# Função para finalizar e mostrar o filtro completo
def finalize_filtros(message):
    global cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida, cambio_escolhido

    categoria_filtro_01 = f"/{categoria_escolhida}" if categoria_escolhida else ""
    categoria_filtro_02 = f"?categorias={categoria_escolhida}" if categoria_escolhida else ""

    ano_filtro = f"/de.{ano_min}/ate.{ano_max}" if ano_min != "" else ""
    ano_filtro_02 = f"&anoDe={ano_min}&anoAte={ano_max}" if ano_min != "" else ""

    preco_filtro = f"&PrecoDe={preco_min}&PrecoAte={preco_max}" if preco_min != "" else ""
    km_filtro = f"&KmDe={km_minimo}&KmAte={km_maximo}" if km_minimo != "" else ""
    marca_filtro = f"&marca1={marca_escolhida}" if marca_escolhida else ""
    cambio_filtro = f"&Cambios={cambio_escolhido}" if cambio_escolhido else ""

    # Monta o filtro completo incluindo apenas os filtros que têm valores
    filtro_completo = (f"https://seminovos.localiza.com{categoria_filtro_01}/carros/{cidade_escolhida}"
                       f"{ano_filtro}{categoria_filtro_02}&cidade={cidade_escolhida}"
                       f"{marca_filtro}{ano_filtro_02}"
                       f"{preco_filtro}{km_filtro}{cambio_filtro}")

    # Envia o filtro completo ao usuário
    bot.send_message(message.chat.id, f"Filtro completo: {filtro_completo}")


# Mantém o bot rodando
if __name__ == '__main__':
    bot.polling()
