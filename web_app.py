# Step 1: Import the necessary libraries
import streamlit as st
from rdflib import Graph

# --- CONFIGURATION ---
# The name of our knowledge graph file
GRAPH_FILE = "kural_knowledge_graph.ttl"
# --------------------

# Step 2: Load the knowledge graph
# @st.cache_data is a special Streamlit command to load the data only once,
# making the app faster.
@st.cache_data
def load_knowledge_graph():
    """Loads the RDF graph from the file."""
    g = Graph()
    try:
        g.parse(GRAPH_FILE, format="turtle")
        return g
    except FileNotFoundError:
        return None

# Step 3: The function to find an answer (copied from our previous app)
def find_answer(graph, user_question):
    """Searches the graph for a question and returns the answer."""
    if graph is None:
        return None
        
    query = """
    PREFIX ont: <http://example.org/ontology#>
    PREFIX kural: <http://example.org/kural/>

    SELECT ?kural_id ?question ?answer ?translation
    WHERE {
        ?kural_node a ont:Kural .
        ?kural_node ont:qaQuestion ?question .
        ?kural_node ont:qaAnswer ?answer .
        ?kural_node ont:englishTranslation ?translation .
        BIND(REPLACE(STR(?kural_node), STR(kural:), "") AS ?kural_id)
    }
    """
    results = graph.query(query)
    
    user_keywords = set(user_question.lower().split())
    
    best_match = None
    highest_score = 0
    
    for row in results:
        question_in_graph = row.question.lower()
        score = sum(1 for keyword in user_keywords if keyword in question_in_graph)
        
        if score > highest_score:
            highest_score = score
            best_match = row
            
    return best_match

# --- Streamlit Web App Interface ---

# Load the graph
kural_graph = load_knowledge_graph()

# Set the title of the web page
st.title("🏛️ Thirukkural Q&A Bot")
st.write("Ask a question and get wisdom from the Thirukkural.")

# Check if the knowledge graph was loaded successfully
if kural_graph is None:
    st.error(f"Failed to load the knowledge graph file: '{GRAPH_FILE}'. Please make sure it's in the same folder.")
else:
    # Create a text input box for the user's question
    user_question = st.text_input("Your question:", placeholder="e.g., How should I react when someone hurts me?")

    # Create a button to submit the question
    if st.button("Get Answer"):
        if user_question:
            # If the user has typed a question, find the answer
            found_answer = find_answer(kural_graph, user_question)

            if found_answer:
                # If an answer is found, display it nicely
                st.subheader(f"Answer from Kural #{found_answer.kural_id}")
                st.markdown(f"**Kural:** *\"{found_answer.translation}\"*")
                st.markdown(f"**Answer:** {found_answer.answer}")
            else:
                # If no answer is found, show a message
                st.warning("Sorry, I couldn't find a clear answer for that in my knowledge base.")
        else:
            # If the user clicks the button without typing a question
            st.info("Please enter a question first.")