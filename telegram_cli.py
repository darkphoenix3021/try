from IPython import get_ipython
from IPython.display import display
# %%
!pip install python-telegram-bot
# %%
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Configuration ---
# IMPORTANT: Replace "YOUR_BOT_TOKEN_HERE" with the API token you got from BotFather.
BOT_TOKEN = "7618281554:AAFODuNEWf-CtUrp1Va5d0a0O8gTzba_cUk"

# Enable logging for the library to see potential issues
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Message Handling ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming text messages sent to the bot.
    It prints the message details to the CLI.
    """
    if update.message and update.message.text:
        user = update.message.from_user
        chat_id = update.message.chat_id
        text = update.message.text

        print(f"\n--- New Message ---")
        print(f"From: {user.first_name} {user.last_name or ''} (@{user.username or 'N/A'})")
        print(f"Chat ID: {chat_id}")
        print(f"Message: {text}")
        print(f"--------------------")
        # Re-print the input prompt character to make CLI usage smoother
        print("> ", end="", flush=True)
    else:
        # Handle other types of messages if needed, or ignore
        chat_id = update.message.chat_id if update.message else "Unknown"
        print(f"\nReceived a non-text message or an update without a message from Chat ID: {chat_id}. This CLI currently only processes text messages for replies.")
        print("> ", end="", flush=True)


# --- Main Application Logic ---
async def main() -> None:
    """
    Main function to set up and run the bot, and handle CLI input for sending replies.
    """
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE": # This check is now less likely to be true, but good to keep.
        print("ERROR: Please ensure a valid bot token is set in the BOT_TOKEN variable.")
        return

    print("Starting Telegram CLI Bot Client...")
    print("This tool will show messages sent to your bot and let you reply.")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the message handler for text messages (excluding commands)
    # This means any regular text message sent to your bot will be processed by `handle_message`
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # You could add handlers for other message types (photos, audio, etc.) if you want to log them.

    try:
        # Initialize, start the application and its updater
        await application.initialize()
        await application.start()
        await application.updater.start_polling() # Starts fetching updates from Telegram

        print("\nBot is now listening for messages.")
        print("Messages received by your bot will appear above.")
        print("\n--- CLI Commands ---")
        print("To reply: /reply <ChatID> <Your message text>")
        print("Example:  /reply 123456789 Hello from my CLI!")
        print("To exit:  /exit")
        print("--------------------")
        print("> ", end="", flush=True)

        # Loop to get input from the CLI user
        while True:
            try:
                # Use asyncio.to_thread to run input() in a separate thread,
                # allowing the bot's async event loop to continue running.
                cli_input = await asyncio.to_thread(input)

                if cli_input.lower().strip() == "/exit":
                    print("Exiting application...")
                    break

                elif cli_input.lower().strip().startswith("/reply "):
                    parts = cli_input.strip().split(" ", 2)
                    # Expected format: /reply CHAT_ID MESSAGE
                    if len(parts) == 3:
                        target_chat_id_str = parts[1]
                        message_to_send = parts[2]

                        try:
                            target_chat_id = int(target_chat_id_str)
                            await application.bot.send_message(chat_id=target_chat_id, text=message_to_send)
                            print(f"Reply sent to Chat ID {target_chat_id}: {message_to_send}")
                        except ValueError:
                            print("Error: Invalid Chat ID. It must be a number.")
                        except Exception as e:
                            print(f"Error sending message: {e}")
                    else:
                        print("Invalid reply format. Use: /reply <ChatID> <Your message text>")

                elif cli_input.strip() == "": # User just pressed Enter
                    pass # Do nothing, just reprint prompt

                else:
                    if cli_input.strip(): # If user typed something other than a known command
                        print("Unknown command. Available commands: /reply <ChatID> <message>, /exit")

                print("> ", end="", flush=True) # Re-print prompt after handling input

            except (KeyboardInterrupt, EOFError):
                print("\nExiting application due to user interruption...")
                break
            except Exception as e:
                logger.error(f"Error in CLI input loop: {e}", exc_info=True)
                print("An error occurred in the CLI. Check logs. Restarting prompt...")
                print("> ", end="", flush=True)


    except Exception as e:
        logger.error(f"Critical error during application setup or runtime: {e}", exc_info=True)
        print(f"A critical error occurred: {e}")
    finally:
        # Gracefully stop the updater and application
        if application.updater and application.updater.is_running:
            print("Stopping Telegram polling...")
            await application.updater.stop()
        if application.running: # application.running is a property in v20+
            print("Stopping application...")
            await application.stop()
        # In v20+, shutdown is separate
        print("Shutting down application components...")
        await application.shutdown()
        print("Application shut down.")

# In Jupyter/IPython, you can directly await the async function
# instead of using asyncio.run()
# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\nCLI Bot Client terminated by user.")
#     except RuntimeError as e:
#         if "Event loop is closed" in str(e):
#             print("\nEvent loop was closed. Exiting.")
#         else:
#             raise # Re-raise other RuntimeError exceptions

# Run the main async function directly in the Jupyter event loop
await main()
