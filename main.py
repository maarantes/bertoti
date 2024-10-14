import telebot
from filtros.F01_localizacao import request_location, register_location_handler

# Token do bot
TOKEN = "8008284040:AAF8lUdalNszINj90KHI97So7TdwqNIHmfo"
bot = telebot.TeleBot(TOKEN)

# Função de boas-vindas
@bot.message_handler(commands=["start"])
def send_welcome(message):
    nome_usuario = message.from_user.first_name
    file_id = "AgACAgEAAxkDAAICm2cK5i32HYjNGHarjEQ0e3F4sWDRAALJrDEbIMFYRAOkwenIeTeZAQADAgADeQADNgQ"
    
    bot.send_photo(message.chat.id, file_id, caption=f"Olá, {nome_usuario}! Vamos começar filtrando os carros da Localiza.")
    request_location(bot, message)

register_location_handler(bot)

if __name__ == "__main__":
    bot.polling()
