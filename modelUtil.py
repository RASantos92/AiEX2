class ModelUtil:

    @staticmethod
    def get_total_tokens(messages):
    # A simple approximation, use a more accurate method if needed
        return sum(len(message['content']) for message in messages)

    @staticmethod
    def truncate_summarize_messages(messages,client):
        # Keep truncating older messages if the total token count exceeds MAX_TOKENS
        # Last user input
        lastUserInput = messages.pop()
        # Last system output
        lastSystemOutput = messages.pop()
        # Give instruction to summarize the conversation so far.
        summaryPrompt = messages.copy() 
        summaryPrompt.append({"role":"user", "content": "Please summarize this whole conversation in a maximum of 2 paragraphs and a total of 2000 characters. Really highlight the key points in the conversation to remember. Focus on user progress"})
        # This response should be the summary
        response = ModelUtil.makeAPICall(summaryPrompt, client)
        
        # Replace the messages list with just the summary, lastSystemOutput, and lastUserInput
        messages = [{'role': 'system', 'content': response},lastSystemOutput,lastUserInput]

    @staticmethod
    def makeAPICall(contextBox, client):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= contextBox
        )
        # Print confirmation
        print("Completion data saved to completion_data.json")
        return completion.choices[0].message.content