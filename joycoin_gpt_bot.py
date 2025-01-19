import g4f
from telebot import TeleBot
import os
import time

bot = TeleBot('7934431830:AAEWOvAQfq7LT72TMFRT5M_7mVmYssqiNOY')

SYSTEM_PROMPT = """
You are JoyCoinGPT bot assistant.
Your task is to help users with:
- How to earn coins
- How to use bot commands
- How referral system works
- Available earning methods
- How to withdraw earnings
- Rules and limitations
- Code help if errors occur

Ты также помогаешь пользователям с:
- как заработать монеты
- как использовать команды бота
- как работает реферальная система
- какие есть способы заработка
- как вывести заработанные средства
- правила и ограничения
- помощь с кодом при ошибках

RULE: Always respond in the same language as the user's question.
If user writes in English - respond in English.
If user writes in Russian - respond in Russian.

Format your responses using HTML tags (<b>, <i>, <code>, etc).
Give brief and clear answers."""

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, '<b>Привет! Я ассистент бота JoyCoinGPT. Задавайте любые вопросы о работе с ботом, и я помогу разобраться!</b>', parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message):    
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            stream=False
        )
        if response:
            formatted_response = response
            if '```' in response:
                code_blocks = response.split('```')
                formatted_response = code_blocks[0]  
                
                for i in range(1, len(code_blocks), 2):
                    if i < len(code_blocks):
                        code = code_blocks[i].strip()
                        if code.startswith('python'):
                            code = code[6:] 
                        formatted_response += f'<pre><code>{code}</code></pre>'
                        
                        if i + 1 < len(code_blocks):
                            formatted_response += code_blocks[i + 1]
            
            try:
                bot.send_message(message.chat.id, formatted_response, parse_mode='HTML')
            except:
                bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "<b>Извините, не удалось получить ответ. Попробуйте еще раз.</b>", parse_mode='HTML')
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "<b>Произошла ошибка. Попробуйте позже.</b>", parse_mode='HTML')

def bot_polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(15)

if __name__ == "__main__":
    bot_polling()