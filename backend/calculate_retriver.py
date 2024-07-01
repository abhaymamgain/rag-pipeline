from langchain.retrievers.multi_vector import MultiVectorRetriever
calculated_variable:MultiVectorRetriever = None

def set_calculated_variable(value):
    global calculated_variable
    calculated_variable = value

def get_calculated_variable():
    global calculated_variable
    return calculated_variable