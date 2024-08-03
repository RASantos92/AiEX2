from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import date

MAX_TOKENS = 3000

load_dotenv()
systemRole = {"role": "system", "content": "You are a expert language teacher. Your main goal is to help the user with vocabulary, pronunciation, grammar, and conversation practice. You should offer personalized guidance and exercises to enhance language proficiency. Start by asking the user what language they want to use and what specific aspect they would like to focus on first."}

client = OpenAI(api_key=os.getenv("myGptkey"))

def get_total_tokens(messages):
    # A simple approximation, use a more accurate method if needed
    return sum(len(message['content']) for message in messages)

def truncate_summarize_messages(messages):
    # Keep truncating older messages if the total token count exceeds MAX_TOKENS
    # Last user input
    lastUserInput = messages.pop()
    # Last system output
    lastSystemOutput = messages.pop()
    # Give instruction to summarize the conversation so far.
    summaryPrompt = messages.copy() 
    summaryPrompt.append({"role":"user", "content": "Please summarize this whole conversation in a maximum of 2 paragraphs. Really highlight the key points in the conversation to remember. Focus on user progress"})
    # This response should be the summary
    response = makeAPICall(summaryPrompt)
    
    # Replace the messages list with just the summary, lastSystemOutput, and lastUserInput
    messages = [{'role': 'system', 'content': response},lastSystemOutput,lastUserInput]


def makeAPICall(contextBox):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= contextBox
    )

    # Print confirmation
    print("Completion data saved to completion_data.json")
    return completion.choices[0].message.content

print("before the function")

def talk():
    messages = []
    messages.append(systemRole)
    print(makeAPICall(messages))
    while True:
        try:
            prompt = input()
            messages.append({"role":"user", "content": prompt})
            response = makeAPICall(messages)
            messages.append({'role': 'system', 'content': response})
            tokens_used = get_total_tokens(messages)
            if get_total_tokens(messages) > MAX_TOKENS:
                truncate_summarize_messages(messages)
                print(messages)
            print(response, "\n", "Here are the total tokens used so far:", tokens_used)
        except KeyboardInterrupt:
            break


talk()