import telebot
from dotenv import load_dotenv
from api_service import FusionBrainAPI
import os


load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Hello, im a picture generating bot, write me  /generate followed by the prompt you want to generate an image for, to 
                 know my commands write /help!""")
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """/generate <prompt> - Generate an image based on the given prompt.
                             /help - shows this help message""")

@bot.message_handler(commands=['generate'])
def gen(message):
    
    prompt = " ".join(message.text.split()[1:])
    if prompt == []:# not finished
        bot.send_message("You have to write /generate and write the prompt(with space in between the command and the prompt), please try again")
    else:
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv('FB_API_KEY'), os.getenv('FB_SECRET_KEY'))
        bot.send_message(message.chat.id, 'Image generation has started, this might take a while...')
        try:
            pipeline_id = api.get_pipeline()
            img = api.generate(prompt, pipeline_id)
            files = api.check_generation(img)
            if not files:
                bot.reply_to(message, "Image generation failed, please try again or contact support.")
            else:
                api.save_image(files[0], 'result.png')
                bot.send_message(message.chat.id, 'Image generated successfully!:')
                with open('result.png', 'rb') as photo: 
                    bot.send_photo(message.chat.id, photo)
        except Exception as e:
            bot.send_message(message, f'Error in generating:{e}')






    

    



    
    




        



bot.infinity_polling()