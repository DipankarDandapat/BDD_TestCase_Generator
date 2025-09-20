import os
import autogen
from autogen import AssistantAgent, UserProxyAgent



# Configuration for OpenAI
config_list = [{
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY")
}]

llm = {"config_list": config_list, "temperature": 0.1}

def write_bdd_feature(requirement: str, feature_name: str = "GeneratedFeature") -> str:
    """
    Tool function to generate BDD feature file from requirement
    """
    prompt = f"""
You are an elite QA engineer specializing in Behavior-Driven Development. Create a comprehensive Gherkin feature file for:

{requirement}

CRITICAL RULES - MUST FOLLOW ALL:

1. STRUCTURE:
   - Begin with a clear `Feature:` definition that summarizes the requirement
   - If applicable, add a `Background:` section for common setup steps
   - Use proper Gherkin formatting and indentation throughout

2. SCENARIO DESIGN:
   - Write descriptive scenario titles that explain the specific behavior being tested
   - Each scenario must include proper Given, When, Then steps with logical flow
   - Use Scenario Outline when data variations exist with clear column headers
   - Provide at least 2-3 rows of meaningful example data for Scenario Outlines

3. TEST COVERAGE:
   - Cover happy path/success cases thoroughly
   - Include edge cases (boundary values, empty inputs, large inputs)
   - Add error scenarios (invalid inputs, system failures, forbidden actions)
   - Consider security, performance, and usability aspects where relevant

4. TAGGING & ORGANIZATION:
   - Tag every scenario with @automated @regression
   - Add @positive for successful paths and @negative for error/edge cases
   - Include @smoke for critical path scenarios

5. STEP QUALITY:
   - Use clear, business-readable language understandable by non-technical stakeholders
   - Make steps reusable and parameterized where appropriate
   - Ensure all scenarios are independently executable and verifiable

6. OUTPUT REQUIREMENT:
   - Output ONLY the complete feature file content in proper Gherkin syntax
   - No extra commentary, explanations, or chat messages
   - Ensure the file is ready for immediate use with Cucumber/SpecFlow

Remember: Focus on business behavior and user value rather than implementation details.
Each scenario should represent a single, complete behavior that can be automated.
"""

    try:
        # Create OpenAI wrapper and generate response
        client = autogen.OpenAIWrapper(**llm)
        reply = client.create(
            messages=[{"role": "user", "content": prompt}]
        )
        feature = reply.choices[0].message.content
        
        # Write to file
        file_name = f"{feature_name}.feature"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(feature)
        
        return file_name
    except Exception as e:
        raise Exception(f"Failed to generate BDD feature: {str(e)}")

# Create UserProxyAgent
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config={"work_dir": "output", "use_docker": False},
)

# Create BDD Writer Agent
bdd_writer = AssistantAgent(
    name="BDD_TEST_CASE_CREATOR",
    system_message="""You are a BDD Test Case Creator. 
    When you receive a requirement, call the write_bdd_feature function to generate a comprehensive BDD feature file.
    After generating the feature file, reply with TERMINATE.""",
    llm_config=llm,
)

# Register the tool function
autogen.register_function(
    write_bdd_feature,
    caller=bdd_writer,
    executor=user_proxy,
    description="Turn requirement into *.feature file with comprehensive BDD scenarios"
)

