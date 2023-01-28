api = fortnite_api.FortniteAPI(api_key=fortnite_api_key, run_async=True)

async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Salut {user.first_name} !\r\nConfigure ton compte fortnite en exécutant \"/config <username>\"")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=context.args[20])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=handlers.helpHandler.get_help_msg(user))
    else:
        fortniteUsername = context.args[0]
        try:
            stats = await api.stats.fetch_by_name(fortniteUsername)
            print(stats.user.raw_data)
            print(stats.stats.all.overall.minutes_played)
            await bot.send_message(chat_id=group_chat_id, text=f'Parfait, {fortniteUsername} !')
            await bot.send_message(chat_id=group_chat_id, text=f'Voici ton nombre moyen de kills par partie : _{stats.stats.all.overall.kills_per_match}_', parse_mode='Markdown')
        except:
            await bot.send_message(chat_id=group_chat_id, text=f"Erreur lors de la récupération des informations.\r\nVeuillez vérifier le nom d'utilisateur et réessayer.")