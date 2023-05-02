import logging
import os
import bisector
from dotenv import load_dotenv
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto


load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


# Enable a basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration for the answer buttons
ANSWER_STATES = ["1","2"]
keyboard_answers = [
            [
                InlineKeyboardButton("\u2705", callback_data="1"),
                InlineKeyboardButton("\u274C", callback_data="2"),
            ]
        ]
reply_markup_answers = InlineKeyboardMarkup(keyboard_answers)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts a new guessing message
    """
    if(not "is_playing" in context.user_data):

        data = bisector.startInteraction()
        context = add_contextinfo(context, data)
        context.user_data["is_playing"] = True       
        
        await update.effective_message.reply_photo(data["mid_frame_url"], caption=f"Frame({data['mid_frame']}) Did the rocket launch yet?", reply_markup=reply_markup_answers)
    else:
        await update.effective_message.reply_text("Sorry but we are currently playing! \U0001F62C")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Controls buttons functionality
    """
    query = update.callback_query
    await query.answer()
    
    # Conditional to check if user pressed an answer button or the start again button
    if(query.data in ANSWER_STATES):

        if(query.data == "1"):
            test_result = True
        else:
            test_result = False

        data = bisector.bisectFrame(context.user_data["left_frame"],context.user_data["right_frame"], context.user_data["mid_frame"], test_result)
        context = add_contextinfo(context, data)      

        if (not data["bisect_status"]):
            await query.edit_message_media(media=InputMediaPhoto(media=data["mid_frame_url"], caption=f"Frame({data['mid_frame']}) Did the rocket launch yet?"), reply_markup=reply_markup_answers)
        else:
            context.user_data.pop("is_playing")

            # Configuration for the Start Again button
            keyboard = [ [ InlineKeyboardButton("Start Again \U0001F504", callback_data="3") ] ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_media(media=InputMediaPhoto(media=data["mid_frame_url"], caption=f"We found it! Rocket launch at frame {data['mid_frame']} \U0001F680"), reply_markup=reply_markup)           
    else:
        await start_command(update, context)
        
   
def add_contextinfo(context: ContextTypes.DEFAULT_TYPE, data) -> ContextTypes.DEFAULT_TYPE:
    """
    Stores frame information
    - `data` Dictionary containing the data to be stored
    """
    context.user_data["left_frame"] = data['left_frame']
    context.user_data["right_frame"] = data['right_frame']
    context.user_data["mid_frame"] = data['mid_frame']

    return context


if __name__ == "__main__":
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add /start command
    app.add_handler(CommandHandler("start", start_command))

    # Add button handler 
    app.add_handler(CallbackQueryHandler(button_handler))

    # Run bot
    app.run_polling()