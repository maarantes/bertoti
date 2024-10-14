import telebot
from filtro_completo import filtro_completo

# Função para pedir o tipo de câmbio
def request_cambio(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Criar os botões de câmbio
    button1 = telebot.types.KeyboardButton('Automático')
    button2 = telebot.types.KeyboardButton('Manual')
    button3 = telebot.types.KeyboardButton('Pular')

    # Adicionar os botões ao markup
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "(7/7) Câmbio\nEscolha o tipo de câmbio:", reply_markup=markup)

    bot.register_next_step_handler(message, lambda msg: handle_cambio(bot, msg, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida))

# Função para lidar com a escolha do tipo de câmbio
def handle_cambio(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida):
    try:
        if message.text == "Pular":
            bot.reply_to(message, "Entendi. Vamos finalizar.")
            filtro_completo(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida, None)
        else:
            cambio_escolhido = message.text
            bot.reply_to(message, f"Você escolheu o câmbio {cambio_escolhido}.")
            filtro_completo(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida, cambio_escolhido)
    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")
