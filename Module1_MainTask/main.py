from bot_assistant import Bot


def main():
    bot = Bot()
    bot.greeting()
    bot.show_commands()
    bot.polling()
    
 
if __name__ == "__main__":
    main()
    