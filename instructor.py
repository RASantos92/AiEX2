from openai import OpenAI
from dotenv import load_dotenv
import os
from modelUtil import ModelUtil
load_dotenv()
class Instructor:
    MAX_TOKENS = 3000
    
    def __init__(self, 
                memory = [],
                system_role = {"role": "system", "content": "You are a expert language teacher. Your main goal is to help the user with vocabulary, pronunciation, grammar, and conversation practice. You should offer personalized guidance and exercises to enhance language proficiency. Start by asking the user what language they want to use and what specific aspect they would like to focus on first."}
                ):
        self.memory = memory
        self.system_role = system_role
        self.memory.append(self.system_role)
        self.client = OpenAI(api_key=os.getenv("myGptkey"))
    
    def talk(self):
            print(ModelUtil.makeAPICall(self.memory,self.client))
            while True:
                try:
                    prompt = input()
                    self.memory.append({"role":"user", "content": prompt})
                    response = ModelUtil.makeAPICall(self.memory, self.client)
                    self.memory.append({'role': 'system', 'content': response})
                    tokens_used = ModelUtil.get_total_tokens(self.memory)
                    if ModelUtil.get_total_tokens(self.memory) > Instructor.MAX_TOKENS:
                        ModelUtil.truncate_summarize_messages(self.memory, self.client)
                        print(self.memory)
                    print(response, "\n", "Here are the total tokens used so far:", tokens_used)
                except KeyboardInterrupt:
                    break