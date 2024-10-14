import telebot
from filtros.F05_ano import request_ano_min

# Função para pedir o KM mínimo
def request_km_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton("Pular")
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(4/7) KMs Rodados\nDigite o KM mínimo:", reply_markup=markup)

    # Registra o próximo passo para lidar com o KM mínimo
    bot.register_next_step_handler(message, lambda msg: handle_km_min(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max))

# Função para lidar com o KM mínimo
def handle_km_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max):
    try:
        if message.text == "Pular":
            bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
            request_ano_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, None, None)
            return

        km_minimo = int(message.text.replace("Km", "").replace(",", "").strip())  # Guarda o valor como inteiro
        bot.reply_to(message, f"KM mínimo definido: {km_minimo} Km")
        request_km_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_km_min(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max))  # Pede o KM mínimo novamente

# Função para pedir o KM máximo
def request_km_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo):
    bot.send_message(message.chat.id, "Agora, digite o KM máximo:")

    # Registra o próximo passo para lidar com o KM máximo
    bot.register_next_step_handler(message, lambda msg: handle_km_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo))

# Função para lidar com o KM máximo
def handle_km_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo):
    try:
        km_maximo = int(message.text.replace("Km", "").replace(",", "").strip())  # Guarda o valor como inteiro

        # Verifica se o KM máximo é menor que o KM mínimo
        if km_maximo < km_minimo:
            bot.reply_to(message, "O KM máximo deve ser maior que o KM mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, lambda msg: handle_km_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo))  # Pede o KM máximo novamente
        else:
            bot.reply_to(message, f"KM máximo definido: {km_maximo} Km")
            request_ano_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_km_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo))  # Pede o KM máximo novamente