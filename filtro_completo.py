import telebot

def filtro_completo(bot, message, cidade_escolhida, categoria_escolhida, preco_min, preco_max, km_minimo, km_maximo, ano_min, ano_max, marca_escolhida, cambio_escolhido):

    categoria_filtro_01 = f"/{categoria_escolhida}" if categoria_escolhida else ""
    categoria_filtro_02 = f"?categorias={categoria_escolhida}" if categoria_escolhida else ""
    parte_cidade = f"&cidade=" if categoria_escolhida else  f"?cidade="

    ano_filtro = f"/de.{ano_min}/ate.{ano_max}" if ano_min is not None else ""
    ano_filtro_02 = f"&anoDe={ano_min}&anoAte={ano_max}" if ano_min is not None else ""

    # Permitir que o valor 0 seja considerado válido
    preco_filtro = f"&PrecoDe={preco_min}&PrecoAte={preco_max}" if preco_min is not None and preco_max is not None else ""
    km_filtro = f"&KmDe={km_minimo}&KmAte={km_maximo}" if km_minimo is not None and km_maximo is not None else ""

    marca_filtro_01 = f"&marca1={marca_escolhida}" if marca_escolhida else ""
    marca_filtro_02 = f"/{marca_escolhida}" if marca_escolhida else ""
    cambio_filtro = f"&Cambios={cambio_escolhido}" if cambio_escolhido else ""

    filtro_completo_url = (f"https://seminovos.localiza.com{categoria_filtro_01}/carros/{cidade_escolhida}{marca_filtro_02}"
                           f"{ano_filtro}{categoria_filtro_02}{parte_cidade}{cidade_escolhida}"
                           f"{marca_filtro_01}{ano_filtro_02}"
                           f"{preco_filtro}{km_filtro}{cambio_filtro}")

    bot.send_message(message.chat.id, f"Filtro completo: {filtro_completo_url}")