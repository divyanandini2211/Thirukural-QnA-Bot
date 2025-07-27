# Step 1: Import the necessary library
from rdflib import Graph

# --- CONFIGURATION ---
# The name of the knowledge graph file we want to load.
# Make sure this file is in the same folder as this script.
GRAPH_FILE = "kural_knowledge_graph.ttl"
# --------------------


# Step 2: Create a function to load the knowledge graph
def load_knowledge_graph(file_path):
    """Loads the RDF graph from the specified file."""
    g = Graph()
    try:
        g.parse(file_path, format="turtle")
        print("Knowledge graph loaded successfully.")
        return g
    except FileNotFoundError:
        print(f"ERROR: The file '{file_path}' was not found. Please make sure it's in the right folder.")
        return None

# Step 3: Create a function to find the answer to a question
def find_answer(graph, user_question):
    """Searches the graph for a question and returns the answer."""
    # SPARQL is the query language for RDF graphs.
    # This query looks for a Kural (?) that has a qaQuestion (?) and a qaAnswer (?).
    query = """
    PREFIX ont: <http://example.org/ontology#>
    PREFIX kural: <http://example.org/kural/>

    SELECT ?kural_id ?question ?answer ?translation
    WHERE {
        ?kural_node a ont:Kural .
        ?kural_node ont:qaQuestion ?question .
        ?kural_node ont:qaAnswer ?answer .
        ?kural_node ont:englishTranslation ?translation .
        
        # This part gets the Kural ID from the URI
        BIND(REPLACE(STR(?kural_node), STR(kural:), "") AS ?kural_id)
    }
    """
    
    # Execute the query
    results = graph.query(query)
    
    # --- Simple Keyword Matching Logic ---
    # Convert user question to lowercase and split into words
    user_keywords = set(user_question.lower().split())
    
    best_match = None
    highest_score = 0
    
    # Loop through all the Q&A pairs in our knowledge graph
    for row in results:
        question_in_graph = row.question.lower()
        
        # Very simple scoring: count how many user keywords are in the graph's question
        score = 0
        for keyword in user_keywords:
            if keyword in question_in_graph:
                score += 1
        
        # If this is the best score so far, store this result
        if score > highest_score:
            highest_score = score
            best_match = row
            
    return best_match


# --- Main Application Logic ---
if __name__ == "__main__":
    # Load the graph when the script starts
    kural_graph = load_knowledge_graph(GRAPH_FILE)
    
    if kural_graph:
        print("\n--- Thirukkural Q&A Bot ---")
        print("Ask a question about life or ethics (or type 'exit' to quit).")
        
        # Loop forever to keep asking for questions
        while True:
            # Get input from the user
            user_input = input("\nYour question: ")
            
            # Check if the user wants to exit
            if user_input.lower() == 'exit':
                print("Thank you for using the Kural Bot. Goodbye!")
                break
            
            # Find the best answer
            found_answer = find_answer(kural_graph, user_input)
            
            # Print the result in a clean format
            if found_answer:
                print("\n--- Answer from the Thirukkural ---")
                print(f"Based on Kural #{found_answer.kural_id}:")
                print(f"\nKural: \"{found_answer.translation}\"")
                print(f"\nAnswer: {found_answer.answer}")
                print("------------------------------------")
            else:
                print("\nSorry, I couldn't find a clear answer for that question in my knowledge base.")