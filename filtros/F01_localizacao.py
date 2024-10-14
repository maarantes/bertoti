import telebot

from geopy.distance import geodesic
from cidades import cidades
from filtros.F02_categoria import request_category

# Função para pedir a localização do usuário
def request_location(bot, message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Enviar localização", request_location=True)
    markup.add(button_geo)
    bot.send_message(message.chat.id, "(1/7) Localização\nVamos começar a filtragem pela sua localização. Primeiro, vou procurar a cidade com uma unidade da Localiza mais próxima de você.")
    bot.send_message(message.chat.id, "Por favor, clique no botão abaixo para eu receber sua localização atual.\nLembrete: É necessário usar seu celular para enviar sua localização!", reply_markup=markup)

# Função para encontrar a cidade mais próxima
def find_nearest_city(user_location):
    nearest_city = None
    nearest_distance = float("inf")

    for city, coords in cidades.items():
        distance = geodesic(user_location, coords).kilometers
        if distance < nearest_distance:
            nearest_city = city
            nearest_distance = distance

    return nearest_city, nearest_distance

# Função para formatar a cidade e o estado
def formatar_cidade_estado(cidade_estado):
    partes = cidade_estado.split(" - ")
    if len(partes) == 2:
        cidade = partes[0].strip().lower().replace(" ", "-")
        estado = partes[1].strip().lower()
        return f"{estado}-{cidade}"
    return cidade_estado.lower().replace(" ", "-")

def register_location_handler(bot):
    @bot.message_handler(content_types=["location"])
    def location_handler(message):
        nome_usuario = message.from_user.first_name

        if message.location is not None:
            user_location = (message.location.latitude, message.location.longitude)
            bot.reply_to(message, f"Recebi sua localização, {nome_usuario}.")
            
            nearest_city, nearest_distance = find_nearest_city(user_location)
            cidade_escolhida = formatar_cidade_estado(nearest_city)
            
            bot.send_message(message.chat.id, f"A unidade Localiza mais próxima fica em {nearest_city}, a uma distância de {nearest_distance:.2f} km.")
            request_category(bot, message, cidade_escolhida)
