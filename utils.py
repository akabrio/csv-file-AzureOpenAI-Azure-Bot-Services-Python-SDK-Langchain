import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from prompts import CSV_PROMPT_PREFIX,CSV_PROMPT_SUFFIX

import pandas as pd

from dotenv import load_dotenv
load_dotenv("credentials.env")

class CSVAgent:
    """Class for a CSVAgent"""

    name = "@csvagentt"
    description = "useful when querying a csv file.\n"
    
    def __init__(self):
       
        self.llm = AzureChatOpenAI(  
            openai_api_key=os.environ['AZURE_OPENAI_API_KEY'],  
            api_version=os.environ['AZURE_OPENAI_API_VERSION'],  
            azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],  
            deployment_name=os.environ['AZURE_OPENAI_MODEL_NAME'],  
            model_name=os.environ['AZURE_OPENAI_MODEL_NAME'],  
            temperature=0  
        )  
  
        self.memory = ConversationBufferWindowMemory(memory_key="conversation_memory", return_messages=True, k=5)
                  
  
    def _run(self, query: str) -> str:
        
        file_url = "./all-states-history.csv"
        df =pd.read_csv(file_url).fillna(value = 0)
        
        try:
            agent = create_csv_agent(self.llm, path=file_url,handle_parsing_errors=True,verbose=True,memory=self.memory)
            for i in range(5):
                try:
                    response = agent.run(CSV_PROMPT_PREFIX + query + CSV_PROMPT_SUFFIX) 
                except Exception as e:  
                    response = str(e)  
                    if 'Could not parse LLM output' in response:  
                        response = "Sorry, I couldn't understand your query. Please try again with a different query.Plese Note that I can only provide questions related to the CSV file i have access to"  
                    else:  
                        response = "Sorry, I encountered an error. Please try again later."  
            return response 
            
        except Exception as e:
            print(e)
            response = e
            return response
        
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("CSVTabularTool does not support async")
