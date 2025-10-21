import telebot
from dotenv import load_dotenv
from api_service import FusionBrainAPI
import os
import time


load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, """Hello, im a picture generating bot, write me  /generate followed by the prompt you want to generate an image for, to 
know my commands write /help!""")
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.reply_to(message, """/generate <prompt> - Generate an image based on the given prompt.
                             /help - shows this help message""")

@bot.message_handler(commands=['generate'])
def gen(message):
    
    prompt = " ".join(message.text.split()[1:])
    if prompt == "":
        bot.send_chat_action(message.chat.id, action='typing')
        bot.send_message(message.chat.id,"You have to write /generate and write the prompt(with space in between the command and the prompt), please try again")
    else:
        
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv('FB_API_KEY'), os.getenv('FB_SECRET_KEY'))
        bot.send_chat_action(message.chat.id, action='typing')
        generating = bot.send_message(message.chat.id, 'Image generation has started, this might take a while...')
        bot.send_chat_action(message.chat.id, action='upload_photo')
        try:
            
            bot.send_chat_action(message.chat.id, action='upload_photo' )
            pipeline_id = api.get_pipeline()
            img = api.generate(prompt, pipeline_id)
            
            files = api.check_generation(img)
            if not files:
                bot.reply_to(message, "Image generation failed, please try again or contact support.")
                
            else:
                bot.send_chat_action(message.chat.id, action='upload_photo')
                api.save_image(files[0], 'result.png')
                bot.send_chat_action(message.chat.id, action='upload_photo')
                bot.send_message(message.chat.id, 'Image generated successfully!:')
                bot.delete_message(message.chat.id, generating.message_id)
                with open('result.png', 'rb') as photo: 
                    bot.send_photo(message.chat.id, photo)
                    time.sleep(1)
                os.remove('result.png')
                
        except Exception as e:
            bot.send_message(message.chat.id, f'Error in generating:{e}')


bot.infinity_polling()