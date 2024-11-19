from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM

# Function to generate application letter using Ollama model
def generate_application_letter(name, p_info, position, comp_name, comp_desc, offer):
    try:
        # Define the template for the prompt
        template = (
            "Generate an application letter on behalf of: '{name}' - '{p_info}' "
            "to apply for the position {position} at the following company: '{comp_name}'. "
            "This is a description of the company: '{comp_desc}'. "
            "And this is the actual job offer text: {offer}. "
            "Write an application letter to the company. "
            "Focus on where skills and strengths of the applicant match the requirements "
            "of the position and be creative here. Use the language of the offer for the application letter."
        )

        # Create a ChatPromptTemplate with the provided template
        prompt = ChatPromptTemplate.from_template(template)

        # Fill in the template with the provided values
        filled_prompt = prompt.format_prompt(
            name=name,
            p_info=p_info,
            position=position,
            comp_name=comp_name,
            comp_desc=comp_desc,
            offer=offer,
        )

        # Initialize the Ollama model
        model = OllamaLLM(model="gemma2:27b")

        # Create a simple chain with the prompt and the model
        chain = filled_prompt | model

        # Generate the application letter
        response = chain.run()

        # Return the generated letter
        return response
    except Exception as e:
        print("Ollama Model Error", f"Failed to generate application letter.\nError: {e}")
        return None
