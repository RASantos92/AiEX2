# Summary:
- This apprach of having a `message` array that you can pass to the APi to maintain context is a standard and effective way to maintain `context`. 
- With that being said, it is important to take memory and token limits into account. 
    - As the conversation continues, the messages array grows, and this could eventually hit the token limit imposed by the API, GPT-4 has a token limit of around 8,000 tokens.
    - This should be always taken in account, so to be a no brainer when moving forward.

## Efficiency and Improvements:
- Efficiency:
    - The approach is efficient in maintaining conversation context because the entire conversation history (as stored in the messages array) is passed to the model with each API call. This allows the model to generate responses that take into account the full context of the conversation.
- Improvement
    - ### Truncation: 
        - The plan is to set a MAX_TOKENS limit to 3,000.
            - Although the token limit is around 8,000 tokens 3,000 will be used, as the method to calculate tokens used will be a rough estimate.
        - Upon hitting the limit, a summarization of all messages will be generated and used as `memeory` or `context` by replacing messages with just the summary, last system output, and last user output.