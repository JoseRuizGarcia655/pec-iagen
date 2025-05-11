from crewai import LLM

def get_llm() -> LLM:
    """
    Function to get the LLM instance with the specified model and API key.

    Returns:
        LLM: An instance of the LLM class.
    """
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if load_dotenv(dotenv_path=".env"):
        print("Environment variables loaded successfully.")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("MODEL_GPT4")

        return LLM(
            model=model_name,
            api_key=openai_api_key,
            max_tokens=4096,
            verbose=False,
        )

    else:
        raise Exception("Failed to load environment variables. Please check your .env file.")
