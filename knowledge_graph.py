import argparse
import subprocess
from openai import OpenAI
from os import getenv
import weave
import json
import asyncio
from weave.flow.scorer import MultiTaskBinaryClassificationF1

# Initialize Weave tracing
weave.init("knowledge_graph_project")


@weave.op
def build_knowledge_graph(content_file):
    # Read content from the file
    with open(content_file, "r") as file:
        content = file.read()

    # Use OpenRouter with OpenAI API to generate structured output for the knowledge graph
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )
    prolog_kg_format = """


    ### Types of Nodes (Prolog Format):

    - **Companies**: `company(Name).`
    - **Products and Services**: `product_service(Name).`
    - **Customers**: `customer(Name).`
    - **Customer Segments**: `customer_segment(Name).`
    - **Marketing Campaigns**: `marketing_campaign(Name).`
    - **Sales Representatives**: `sales_representative(Name).`
    - **Marketing Channels**: `marketing_channel(Name).`
    - **Competitors**: `competitor(Name).`
    - **Partners and Suppliers**: `partner_supplier(Name).`
    - **Market Segments**: `market_segment(Name).`
    - **Events and Conferences**: `event(Name).`
    - **Trends and Technologies**: `trend_technology(Name).`
    - **Geographic Locations**: `geographic_location(Name).`

    ### Types of Connections (Prolog Format):

    - **Offers**: `offers(Company, ProductService).`
    - **Purchases**: `purchases(Customer, ProductService).`
    - **Located In**: `located_in(Entity, GeographicLocation).` *(Entity can be a Company or Customer)*
    - **Targets**: `targets(MarketingCampaign, CustomerSegment).`
    - **Utilizes**: `utilizes(MarketingCampaign, MarketingChannel).`
    - **Competes With**: `competes_with(Company, Competitor).`
    - **Partners With**: `partners_with(Company, PartnerSupplier).`
    - **Belongs To**: `belongs_to(Customer, MarketSegment).`
    - **Attended By**: `attended_by(Event, Entity).` *(Entity can be a Company or Customer)*
    - **Influences**: `influences(TrendTechnology, MarketSegment).`
    - **Managed By**: `managed_by(SalesRepresentative, CustomerAccount).`
    - **Interacts On**: `interacts_on(Customer, SocialMediaPlatform).`
    - **Associated With**: `associated_with(ProductService, TrendTechnology).`

    Repeat this format for each type of connection to build the knowledge graph.

    Enclose this prolog language output in a single '''prolog ... '''. do not split the prolog program. this prolog program will be compiled by prolog

    Please create a knowledge graph with the following structure and present it in Prolog format. For each node type and connection type, use the specified Prolog predicates below. Ensure that the format is consistent throughout.


    """
    response = client.chat.completions.create(
        # model="meta-llama/llama-3.1-405b-instruct",
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Create a knowledge graph in prolog language for marketing based on the following format and content:\n ### format:\n{prolog_kg_format}\n\n\n###Content:\n{content}",
            },
        ],
        # max_tokens=131000,
        # temperature=0.5,
    )

    # # Parse the response to extract the knowledge graph
    # graph_data = response.choices[0].message.content.strip()
    graph_data = response.choices[0].message.content
    # graph_data = """
    # ```prolog
    # company(canva).
    # node(a).
    # node(b).
    # edge(a, b).
    # ```
    # """
    prolog_code = extract_prolog_code(graph_data)
    print("Prolog Code:\n", prolog_code)
    test_prolog_graph(prolog_code)

    # Dummy graph data for demonstration purposes
    # prolog_code = extract_prolog_code(graph_data)
    # print("Prolog Code:\n", prolog_code)
    # test_prolog_graph(prolog_code)
    # Test the Prolog graph directly with the code
    test_prolog_graph(prolog_code)

    # return graph
    return graph_data


def parse_graph_data(graph_data):
    # Dummy function to parse graph data
    # Replace with actual parsing logic
    return graph_data


@weave.op
def extract_prolog_code(graph_data):
    """Extracts the Prolog code from the response."""
    start = graph_data.find("```prolog")
    end = graph_data.find("```", start + 1)
    if start != -1 and end != -1:
        return graph_data[start + len("```prolog") : end].strip()
    return ""


class PrologGraphModel(weave.Model):
    prolog_code: str

    @weave.op()
    async def predict(self, query: str) -> dict:
        result = self.run_prolog_query(self.prolog_code, query)
        return {"exists": "true" in result}

    def run_prolog_query(self, prolog_code, query):
        with open("temp_prolog.pl", "w") as f:
            f.write(prolog_code)
        process = subprocess.Popen(
            ["swipl", "-s", "temp_prolog.pl", "-g", query, "-t", "halt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return stdout.decode().strip()
        else:
            return stderr.decode().strip()

# Initialize Weave evaluation
weave.init('knowledge_graph_evaluation')

# Create the model
model = PrologGraphModel(prolog_code="")

# Define the dataset and labels
queries = ["company(canva)", "competitor(adobe)", "partner_supplier(anyscale)"]
labels = [{"exists": True}, {"exists": False}, {"exists": False}]
examples = [{"id": str(i), "query": queries[i], "target": labels[i]} for i in range(len(queries))]

# Define a scoring function
@weave.op()
def existence_score(target: dict, model_output: dict) -> dict:
    return {'correct': target['exists'] == model_output['exists']}

# Run the evaluation
evaluation = weave.Evaluation(
    name='prolog_graph_eval',
    dataset=examples,
    scorers=[MultiTaskBinaryClassificationF1(class_names=["exists"]), existence_score],
)
print(asyncio.run(evaluation.evaluate(model)))


@weave.op
def old_test_prolog_graph(prolog_code):
    """Runs a Prolog query to test the graph."""

    def run_prolog_query(prolog_code, query):
        # Write the Prolog code to a temporary file
        with open("temp_prolog.pl", "w") as f:
            f.write(prolog_code)
        process = subprocess.Popen(
            ["swipl", "-s", "temp_prolog.pl", "-g", query, "-t", "halt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return stdout.decode().strip()
        else:
            return stderr.decode().strip()

    # Query Prolog
    print(
        "Checking if node 'canva' exists:",
        run_prolog_query(prolog_code, "company(canva)"),
    )


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
