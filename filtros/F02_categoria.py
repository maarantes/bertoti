import telebot
from filtros.F03_preco import request_preco_min

# Função para pedir a categoria
def request_category(bot, message, cidade_escolhida):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    # Criar os botões de categoria
    button1 = telebot.types.KeyboardButton("Hatch")
    button2 = telebot.types.KeyboardButton("Sedan")
    button3 = telebot.types.KeyboardButton("SUV")
    button4 = telebot.types.KeyboardButton("Picape")
    button5 = telebot.types.KeyboardButton("Minivan")
    button6 = telebot.types.KeyboardButton("Furgão")
    button_skip = telebot.types.KeyboardButton("Pular")

    # Adicionar os botões ao teclado
    markup.add(button1, button2, button3, button4, button5, button6, button_skip)

    bot.send_message(message.chat.id, "(2/7) Categoria de Carro\nAgora, escolha uma categoria:", reply_markup=markup)

    # Passando cidade_escolhida como argumento para a próxima função
    bot.register_next_step_handler(message, lambda msg: handle_category(bot, msg, cidade_escolhida))

# Função para lidar com a escolha da categoria
def handle_category(bot, message, cidade_escolhida):
    try:
        global categoria_escolhida
        if message.text == "Pular":
            bot.reply_to(message, "Entendi. Vamos para o próximo filtro.")
            categoria_escolhida = ""
        else:
            tipo_escolhido = message.text.upper()
            categoria_escolhida = tipo_escolhido
        
        # Passando cidade_escolhida e categoria_escolhida como argumentos
        request_preco_min(bot, message, cidade_escolhida, categoria_escolhida)

    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")
