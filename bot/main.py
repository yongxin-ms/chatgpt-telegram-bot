import logging
import os

from dotenv import load_dotenv

from openai_helper import OpenAIHelper, default_max_tokens
from telegram_bot import ChatGPTTelegramBot


def main():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [
        value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(
            f'The following environment values are missing in your .env: {", ".join(missing_values)}')
        exit(1)

    # Setup configurations
    model = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    max_tokens_default = default_max_tokens(model=model)
    openai_config = {
        'api_type': os.environ.get('OPENAI_API_TYPE'),
        'api_version': os.environ.get('OPENAI_API_VERSION'),
        'api_base': os.environ.get('OPENAI_API_BASE'),
        'api_key': os.environ['OPENAI_API_KEY'],
        'deployment_id': os.environ.get('DEPLOYMENT_ID'),
        'show_usage': os.environ.get('SHOW_USAGE', 'false').lower() == 'true',
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'proxy': os.environ.get('PROXY', None),
        'max_history_size': int(os.environ.get('MAX_HISTORY_SIZE', 15)),
        'max_conversation_age_minutes': int(os.environ.get('MAX_CONVERSATION_AGE_MINUTES', 180)),
        'assistant_prompt': os.environ.get('ASSISTANT_PROMPT', 'You are a helpful assistant.'),
        'max_tokens': int(os.environ.get('MAX_TOKENS', max_tokens_default)),
        'n_choices': int(os.environ.get('N_CHOICES', 1)),
        'temperature': float(os.environ.get('TEMPERATURE', 1.0)),
        'image_size': os.environ.get('IMAGE_SIZE', '512x512'),
        'model': model,
        'presence_penalty': int(os.environ.get('PRESENCE_PENALTY', 0)),
        'frequency_penalty': int(os.environ.get('FREQUENCY_PENALTY', 0)),
    }

    telegram_config = {
        'token': os.environ['TELEGRAM_BOT_TOKEN'],
        'admin_user_ids': os.environ.get('ADMIN_USER_IDS', '-'),
        'allowed_user_ids': os.environ.get('ALLOWED_TELEGRAM_USER_IDS', '*'),
        'monthly_user_budgets': os.environ.get('MONTHLY_USER_BUDGETS', '*'),
        'monthly_guest_budget': float(os.environ.get('MONTHLY_GUEST_BUDGET', '100.0')),
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'proxy': os.environ.get('PROXY', None),
        'voice_reply_transcript': os.environ.get('VOICE_REPLY_WITH_TRANSCRIPT_ONLY', 'true').lower() == 'true',
        'ignore_group_transcriptions': os.environ.get('IGNORE_GROUP_TRANSCRIPTIONS', 'true').lower() == 'true',
        'group_trigger_keyword': os.environ.get('GROUP_TRIGGER_KEYWORD', ''),
        'token_price': float(os.environ.get('TOKEN_PRICE', 0.002)),
        'image_prices': [float(i) for i in os.environ.get('IMAGE_PRICES', "0.016,0.018,0.02").split(",")],
        'transcription_price': float(os.environ.get('TOKEN_PRICE', 0.002)),
    }

    # Setup and run ChatGPT and Telegram bot
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = ChatGPTTelegramBot(
        config=telegram_config, openai=openai_helper)
    telegram_bot.run()


if __name__ == '__main__':
    main()
