import telebot

from filtros.F04_km_rodado import request_km_min

# Função para pedir o preço mínimo
def request_preco_min(bot, message, cidade_escolhida, categoria_escolhida):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton('Pular')
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(3/7) Preço Mínimo\nAgora, digite o preço mínimo:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: handle_preco_min(bot, msg, cidade_escolhida, categoria_escolhida))

# Função para lidar com o preço mínimo
def handle_preco_min(bot, message, cidade_escolhida, categoria_escolhida):
    if message.text == "Pular":
        bot.reply_to(message, "Entendi. Vamos para o próximo filtro.")
        request_km_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min=None, preco_max=None)
        return

    try:
        preco_min = int(message.text.replace("R$", "").replace(",", "").strip())
        request_preco_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_preco_min(bot, msg, cidade_escolhida, categoria_escolhida))  

# Função para pedir o preço máximo (não pode ser pulado)
def request_preco_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min):
    bot.send_message(message.chat.id, "Agora, digite o preço máximo:")

    # Registra o próximo passo para lidar com o preço máximo
    bot.register_next_step_handler(message, lambda msg: handle_preco_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min))

# Função para lidar com o preço máximo (obrigatório)
def handle_preco_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min):
    try:
        preco_max = int(message.text.replace("R$", "").replace(",", "").strip())  # Guarda o valor como inteiro

        # Verifica se o preço máximo é menor que o preço mínimo
        if preco_max <= preco_min:
            bot.reply_to(message, "O preço máximo deve ser maior que o preço mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, lambda msg: handle_preco_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min))  # Pede o preço máximo novamente
        else:
            # Passa as informações coletadas para o próximo filtro
            request_km_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_preco_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min))  # Pede o preço máximo novamente