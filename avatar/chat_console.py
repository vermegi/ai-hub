from dotenv import load_dotenv
import os 

load_dotenv()

module_name = os.environ.get("ORCHESTRATOR_MODULE")
class_name = os.environ.get("ORCHESTRATOR_CLASS")
try:
    module = __import__(module_name) 
    orchestrator_class = getattr(module, class_name) 
    orchestrator = orchestrator_class()
except Exception as e:
    print(f"\n\nCannot import {class_name} from {module_name}. The following exception was rised\n")
    raise e

user_question = "Hello! I'd like to ask a question about Woodgroove's product portfolio"
while user_question != 'bye':    
    stream = orchestrator.run_user_query(user_question=user_question)
    print("\nassistant: ", end='', flush=True)
    for tok in stream:
        print(tok, end='', flush=True)
    user_question = input("\n\nuser: ")
    
    
