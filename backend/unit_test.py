import query as query
from langchain_community.llms.ollama import Ollama

def print_green(text):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"{GREEN}{text}{RESET}")

def print_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def print_yellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")



def query_evaluate_answer(question:str,answer:str):

    EVAL_PROMPT="""
                Expected response:{Expected_response}
                Actual response:{actual_response}

                -----
                (Answer in true or false) , wether the (expected response) means the same as (Actual response)?
                your answer should contain the the word true if you think expected and actual response means the same thing
                and contain false if they mean something else, if the actual answer is a detailed explanation dumb it down to a simple yes or no and evaluate
               


                """

    response_text=query.query_rag(question)
    prompt=EVAL_PROMPT.format(
        Expected_response=answer,
        actual_response=response_text
    )
    model=Ollama(model='llama2-uncensored')
    evaluation=model.invoke(prompt)
    final_result=evaluation.strip().lower()
    if "true" in final_result:
        print_green(f"true {evaluation}")
        return True
    elif "false" in final_result:
        print_red(f"false {evaluation}")
        return False
    else:
        print_yellow(f"cannot resolve {evaluation}")
        return False
    
    
def Solar_storm_date():
    assert query_evaluate_answer(
        question="who wears the armband on the field",
        answer="captain"
    )
def who_works():
    assert query_evaluate_answer(
        question="can a goal keeper touch the ball with his hands outside the penalty area",
        answer="no"
    )
        
Solar_storm_date()
who_works()

