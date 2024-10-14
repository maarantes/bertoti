import telebot
from filtros.F06_marca import request_marca

# Função para pedir o ano mínimo
def request_ano_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_skip = telebot.types.KeyboardButton('Pular')
    markup.add(button_skip)

    bot.send_message(message.chat.id, "(5/7) Ano de Fabricação\nAgora, digite o ano mínimo:", reply_markup=markup)

    # Registra o próximo passo para lidar com o ano mínimo
    bot.register_next_step_handler(message, lambda msg: handle_ano_min(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo))

# Função para lidar com o ano mínimo
def handle_ano_min(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo):
    try:
        if message.text == "Pular":
            bot.reply_to(message, "Entendi. Vamos para o próximo passo.")
            request_marca(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, None, None) 
            return

        ano_min = int(message.text.strip())  # Guarda o valor como inteiro
        bot.reply_to(message, f"Ano mínimo definido: {ano_min}")
        request_ano_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_ano_min(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo))  # Pede o ano mínimo novamente

# Função para pedir o ano máximo
def request_ano_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min):
    bot.send_message(message.chat.id, "Agora, digite o ano máximo:")

    # Registra o próximo passo para lidar com o ano máximo
    bot.register_next_step_handler(message, lambda msg: handle_ano_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min))

# Função para lidar com o ano máximo
def handle_ano_max(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min):
    try:
        ano_max = int(message.text.strip())  # Guarda o valor como inteiro

        # Verifica se o ano máximo é menor que o ano mínimo
        if ano_max < ano_min:
            bot.reply_to(message, "O ano máximo deve ser maior ou igual ao ano mínimo. Por favor, insira um novo valor.")
            bot.register_next_step_handler(message, lambda msg: handle_ano_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min))  # Pede o ano máximo novamente
        else:
            bot.reply_to(message, f"Ano máximo definido: {ano_max}")
            request_marca(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max)
    except ValueError:
        bot.reply_to(message, "Valor inválido. Por favor, insira um número válido.")
        bot.register_next_step_handler(message, lambda msg: handle_ano_max(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min))  # Pede o ano máximo novamente