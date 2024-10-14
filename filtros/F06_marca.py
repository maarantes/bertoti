import telebot
from filtros.F07_cambio import request_cambio

# Função para pedir a marca
def request_marca(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Criar os botões de marca
    marcas = ["Ford", "Volkswagen", "Fiat", "Jeep", "Renault", "Citroen", "Chevrolet", "Toyota", 
              "Nissan", "Hyundai", "Peugeot", "Mercedes-Benz", "Audi", "Volvo", "Mitsubishi", 
              "BMW", "Land Rover", "Honda", "Jaguar", "Chery", "BYD", "Pular"]

    # Adicionar os botões ao markup
    for i in range(0, len(marcas), 3):
        markup.add(*marcas[i:i+3])

    bot.send_message(message.chat.id, "(6/7) Marca\nAgora, escolha a marca do carro:", reply_markup=markup)

    bot.register_next_step_handler(
        message, 
        lambda msg: handle_marca(
            bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max
        )
    )

# Função para lidar com a escolha da marca
def handle_marca(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max):
    try:
        if message.text == "Pular":
            bot.reply_to(message, "Entendi. Vamos para o último filtro.")
            request_cambio(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, None)
        else:
            marca_escolhida = message.text
            request_cambio(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida)
    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")
