import openai
import asyncio
import botConfig
import discord
from discord import app_commands


# Set your OpenAI API key here
openai.api_key = botConfig._Open_AI_Token()

# Maximum tokens per response and max questions per session
MAX_TOKENS = 150
MAX_QUESTIONS_PER_SESSION = 5

def setup(bot):
    @bot.tree.command(name="ask_ai", description="Ask OpenAI a question")
    async def ask_ai(interaction: discord.Interaction, question: str):
        # OpenAI interaction logic
        await interaction.response.send_message(f"OpenAI says: ...", ephemeral=True)

async def ask_chatgpt(question, conversation_history):
    """
    Sends a question to ChatGPT and returns the response.
    
    :param question: The user's question to ChatGPT.
    :param conversation_history: The conversation history to maintain context.
    :return: The response from ChatGPT or an error message if something goes wrong.
    """
    try:
        # Add user's question to the conversation history
        conversation_history.append({"role": "user", "content": question})

        # Call the OpenAI API to get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use another model if preferred
            messages=conversation_history,
            max_tokens=MAX_TOKENS  # Limit the number of tokens in the response
        )
        
        # Extract the answer and add it to the conversation history
        answer = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

async def handle_ai_session(ctx, initial_question):
    """
    Handles a session where the user can interact with ChatGPT.
    
    :param ctx: The context in which the command was invoked.
    :param initial_question: The initial question the user asked.
    """
    user_id = ctx.author.id
    conversation_history = []
    questions_asked = 0  # Counter for the number of questions in the session

    # Ask the initial question
    answer = await ask_chatgpt(initial_question, conversation_history)
    await ctx.send(answer)
    questions_asked += 1

    # Wait for follow-up questions
    while questions_asked < MAX_QUESTIONS_PER_SESSION:
        try:
            # Wait for the next message from the user
            message = await ctx.bot.wait_for('message', check=lambda m: m.author.id == user_id, timeout=300)
            
            # End session if the user sends the stop command
            if message.content.strip().lower() == "/ai-stop":
                await ctx.send("AI session ended.")
                break

            # Handle the next question and increment the counter
            answer = await ask_chatgpt(message.content, conversation_history)
            await message.channel.send(answer)
            questions_asked += 1

        except asyncio.TimeoutError:
            await ctx.send("AI session ended due to inactivity.")
            break
