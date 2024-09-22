import argparse
from pyswip import Prolog
from openai import OpenAI
from os import getenv
import weave

# Initialize Weave tracing
weave.init("wb_customer_knowledge_graph")


def build_knowledge_graph(content_file):
    # Read content from the file
    with open(content_file, "r") as file:
        content = file.read()

    # Use OpenRouter with OpenAI API to generate structured output for the knowledge graph
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )
    response = client.chat.completions.create(
        # model="meta-llama/llama-3.1-405b-instruct",
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Create a knowledge graph in prolog language for marketing based on the following content: {content}",
            },
        ],
        # max_tokens=131000,
        # temperature=0.5,
    )

    # Parse the response to extract the knowledge graph
    # graph_data = response.choices[0].message.content.strip()
    graph_data = response.choices[0].message.content
    prolog_code = extract_prolog_code(graph_data)
    print("Prolog Code:\n", prolog_code)
    test_prolog_graph(prolog_code)

    # Use Weave to trace the graph creation process
    with weave.trace("build_knowledge_graph"):
        # Here you would parse the graph_data into a structured format
        # For demonstration, let's assume graph_data is already structured
        graph = parse_graph_data(graph_data)

    return graph
    # return graph_data


def parse_graph_data(graph_data):
    # Dummy function to parse graph data
    # Replace with actual parsing logic
    return graph_data


def output_graph_prolog(graph):
    # Convert the graph to Prolog format
    prolog_output = ""
    for node, connections in graph.items():
        for connection in connections:
            prolog_output += f"{connection['type']}({node}, {connection['target']}).\n"
    return prolog_output


def extract_prolog_code(graph_data):
    """Extracts the Prolog code from the response."""
    start = graph_data.find("```prolog")
    end = graph_data.find("```", start + 1)
    if start != -1 and end != -1:
        return graph_data[start + len("```prolog") : end].strip()
    return ""


def test_prolog_graph(prolog_code):
    """Runs a Prolog query to test the graph."""
    prolog = Prolog()
    # Assert each line of the Prolog code separately
    for line in prolog_code.splitlines():
        if line.strip():  # Ensure the line is not empty
            prolog.assertz(line.strip())

    print("Testing Prolog graph...")
    # Check if a specific fact exists
    query_result = list(prolog.query("company(canva)"))
    if query_result:
        print("Test passed: 'company(canva).' exists in the Prolog graph.")
    else:
        print("Test failed: 'company(canva).' does not exist in the Prolog graph.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a knowledge graph for marketing."
    )
    parser.add_argument(
        "content", nargs="?", default="content.html", help="The content file to process"
    )
    args = parser.parse_args()

    # Build the knowledge graph
    graph = build_knowledge_graph(args.content)

    # Output the graph in Prolog format
    prolog_output = output_graph_prolog(graph)
    print(prolog_output)
