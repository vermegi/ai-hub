from sseclient import SSEClient
import requests
import json
import os

class ConversationOrchestrator:
    def __init__(self, s=None):
        '''
        `s` is a session state that is stored to `self.session`.
        '''
        self.seesion = s
    
    def init_conversation(self):
        '''
        This is used to initialize `self.session`
        '''
        pass

    def run_user_query(self, user_question: str):
        '''
        `run_user_query` is an iterable yielding assistant's answer tokens.
        `user_question` is a string holding the user question to be answered.
        Any state content should be managed within `self.session`
        '''
        pass

class PF_Orchestrator(ConversationOrchestrator):
    def __init__(self, s):
        
        self.pf_endpoint_name=os.environ.get("PF_ENDPOINT_NAME")
        self.pf_deployment_name=os.environ.get("PF_DEPLOYMENT_NAME")
        self.pf_endpoint_key=os.environ.get("PF_ENDPOINT_KEY")
        
        if self.pf_endpoint_name is None or self.pf_endpoint_key is None:
             raise Exception("Prompt Flow end_point or key not provided!")
        
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.pf_endpoint_key),"Accept": "text/event-stream, application/json"}
        
        if s is None:
            raise Exception("Session is required")
        # self.session = s
        super().__init__(s)
        self.init_conversation()  
    
    def init_conversation(self):
        self.session['history']=[]
        
    def run_user_query(self, user_question):             
        
        body = {
            "question": user_question,
            "chat_history": self.session['history'],
        }

        response = requests.post(self.pf_endpoint_name, json=body, headers=self.headers, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type')
        assistant_answer = ''
        if "text/event-stream" in content_type:
            client = SSEClient(response)
            for event in client.events():
                dct = json.loads(event.data)
                answer_delta = dct.get('answer')
                if answer_delta:
                    yield answer_delta
                    assistant_answer += answer_delta
        else:
             pass
        
        self.session['history'].append({
            "inputs": {
                "question": user_question,
            },
            "outputs": {
                    "answer": assistant_answer,
            }
        })
