
import openai
import asyncio
import botConfig
# Sätt din OpenAI API-nyckel här
# openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = botConfig._Open_AI_Token()

# Maximum tokens per response and max questions per session
MAX_TOKENS = 150
MAX_QUESTIONS_PER_SESSION = 5

# Funktion för att ställa en fråga till ChatGPT
async def ask_chatgpt(question, conversation_history):
    try:
        # Lägger till användarens fråga i konversationshistoriken
        conversation_history.append({"role": "user", "content": question})

        # Anropar OpenAI API för att få ett svar
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Du kan använda en annan modell om du vill
            messages=conversation_history,
            max_tokens=MAX_TOKENS  # Begränsar antalet tokens i svaret
        )
        
        # Får svaret från modellen och lägger till det i konversationshistoriken
        answer = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Funktion för att hantera en AI-session
async def handle_ai_session(ctx, initial_question):
    user_id = ctx.author.id
    conversation_history = []
    questions_asked = 0  # Räknare för antalet frågor i sessionen

    # Fråga initial fråga
    answer = await ask_chatgpt(initial_question, conversation_history)
    await ctx.send(answer)
    questions_asked += 1

    # Väntar på följdfrågor
    while questions_asked < MAX_QUESTIONS_PER_SESSION:
        try:
            # Väntar på nästa meddelande från användaren
            message = await ctx.bot.wait_for('message', check=lambda m: m.author.id == user_id, timeout=300)
            
            if message.content.strip().lower() == "./ai-stop":
                await ctx.send("AI-session avslutad.")
                break

            # Hantera nästa fråga och uppdatera räknaren
            answer = await ask_chatgpt(message.content, conversation_history)
            await message.channel.send(answer)
            questions_asked += 1

        except asyncio.TimeoutError:
            await ctx.send("AI-session avslutad på grund av inaktivitet.")
            break
