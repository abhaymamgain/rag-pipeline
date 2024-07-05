
import llm_calls as lc
import query_partition as qc
import partition

queries = [
    "What is the amount for Project Design?",
    "How much is Development (Phase 1)?",
    "What is the cost of Development (Phase 2)?",
    "What is the amount for Development (Phase 3)?",
    "How much is Development (Phase 4)?",
    "What is the cost for Development (Integration Testing)?",
    "What is the amount for Testing and Deployment (Phase 1)?",
    "How much is Testing and Deployment (Phase 2)?",
    "What is the cost for Project Management?",
    "What is the amount for Documentation?",
    "What is the subtotal?",
    "What is the tax amount?",
    "What is the total amount?"
]

ground_truths = [
    "$5,000.00",
    "$1,500.00",
    "$1,500.00",
    "$1,500.00",
    "$1,500.00",
    "$1,000.00",
    "$1,000.00",
    "$1,000.00",
    "$1,000.00",
    "$500.00",
    "$15,000.00",
    "$1,050.00",
    "$16,050.00"
]

    
    
    
    




# Prompt to compare the ground truth and generated response
comparison_prompt_template = """
Ground Truth: {ground_truth}
Generated Response: {generated_response}

Do the (Ground Truth )and (Generated Response) mean the same thing objectively? Answer 'yes' or 'no' only.

"""

# Function to check semantic equivalence using the LLM
def check_semantic_equivalence(ground_truth, generated_response):
    prompt = comparison_prompt_template.format(
        ground_truth=ground_truth,
        generated_response=generated_response
    )
    response = lc.llm_generate(prompt)
    return response


def evaluate_semantic_equivalence(queries, ground_truths, generated_responses):
    results = []
    for query, ground_truth, generated_response in zip(queries, ground_truths, generated_responses):
        evaluation = check_semantic_equivalence(ground_truth, generated_response)
        results.append({
            'query': query,
            'ground_truth': ground_truth,
            'generated_response': generated_response,
            'evaluation': evaluation
        })
    return results
partition.process_store()
generated_responses=[]
for query in queries:
    res=qc.run(query)
    generated_responses.append(res)

evaluation_results = evaluate_semantic_equivalence(queries, ground_truths, generated_responses)

for result in evaluation_results:
    print(f"Query: {result['query']}")
    print(f"Ground Truth: {result['ground_truth']}")
    print(f"Generated Response: {result['generated_response']}")
    print(f"Evaluation: {result['evaluation']}")
    print("---------")



    