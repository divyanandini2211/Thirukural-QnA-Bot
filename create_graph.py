# Step 1: Import the necessary libraries
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, URIRef

# --- CONFIGURATION ---
# The name of your input CSV file.
# We are using the full path to make sure the file is found.
# The 'r' before the string is important!
CSV_FILE_NAME = r"C:\Users\Divya Nandhini\Downloads\Thirukural project - Sheet1 (1).csv"

# The name of the output file where the knowledge graph will be saved.
OUTPUT_GRAPH_FILE = "kural_knowledge_graph.ttl"
# --------------------


# Step 2: Define our Namespaces for the graph
# This creates clean, readable URIs for our data
BASE = Namespace("http://example.org/kural/")
ONT = Namespace("http://example.org/ontology#") # Ontology namespace

# Step 3: Create an empty graph
g = Graph()

# Bind the prefixes to the graph for cleaner output
g.bind("kural", BASE)
g.bind("ont", ONT)


# Step 4: Read the data from your CSV file
try:
    # Notice there are spaces around the column names in your file name.
    # Let's adjust the column names in the code to match perfectly.
    df = pd.read_csv(CSV_FILE_NAME)
    print(f"Successfully loaded '{CSV_FILE_NAME}'. Processing {len(df)} Kurals...")

    # Step 5: Loop through each row of the CSV file
    for index, row in df.iterrows():
        # --- Get data from each column ---
        # We use .strip() to remove any accidental extra spaces
        kural_id = str(row['Kural_ID']).strip()
        theme_text = str(row['Theme']).strip().replace(' ', '_') # Replace spaces for a clean URI
        virtue_text = str(row['Virtue']).strip().replace(' ', '_')
        emotion_text = str(row['Emotion']).strip().replace(' ', '_')

        # --- Create the main URI for this Kural ---
        # This will be something like: http://example.org/kural/305
        kural_uri = BASE[kural_id]

        # --- Add the triples (connections) to the graph ---

        # 1. State that this URI is a Kural
        g.add((kural_uri, RDF.type, ONT.Kural))

        # 2. Add the Theme connection
        g.add((kural_uri, ONT.hasTheme, ONT[theme_text]))

        # 3. Add the Virtue connection
        g.add((kural_uri, ONT.promotesVirtue, ONT[virtue_text]))

        # 4. Add the Emotion connection
        g.add((kural_uri, ONT.evokesEmotion, ONT[emotion_text]))

        # 5. Add the text data (Literals) directly to the Kural
        g.add((kural_uri, ONT.tamilText, Literal(row['Tamil_Text'])))
        g.add((kural_uri, ONT.englishTranslation, Literal(row['English_Translation'])))
        g.add((kural_uri, ONT.modernScenario, Literal(row['Modern_Scenario'])))
        g.add((kural_uri, ONT.qaQuestion, Literal(row['QA_Question'])))
        g.add((kural_uri, ONT.qaAnswer, Literal(row['QA_Answer'])))
        g.add((kural_uri, ONT.ethicalFramework, Literal(row['Ethical_Framework'])))


    # Step 6: Save the entire graph to the output file
    g.serialize(destination=OUTPUT_GRAPH_FILE, format="turtle")

    print(f"\nSuccess! Knowledge graph has been created and saved as '{OUTPUT_GRAPH_FILE}'.")
    print("You can open this .ttl file with a text editor to see the structured data.")

except FileNotFoundError:
    print(f"\nERROR: Could not find the file at the path specified.")
    print(f"Please double-check that this path is exactly correct: {CSV_FILE_NAME}")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please check that your CSV file has the correct column headers (e.g., 'Kural_ID', 'Theme', etc.).")