import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
load_dotenv()
os.getenv("groq_api_key")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,groq_api_key=os.getenv("groq_api_key"),model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            INSTRUCTION:
You are Saksham Goyal, a recent graduate from Ajay Kumar Garg Engineering College with a focus on DevOps Engineering and Machine Learning. Your skills and enthusiasm to learn and grow are a great fit for the role, and you are eager to contribute to the success of the team.

Your job is to write a cold email to the client regarding the job mentioned above, describing your capability as a fresher, and how your skills in DevOps and ML Engineering could be beneficial for their needs.

Also, add the most relevant portfolio pieces from the following links: {link_list}

Remember, you are Saksham Goyal, a fresher from Ajay Kumar Garg Engineering College. Do not provide a preamble.

EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content


if __name__ == "__main__":
    print(os.getenv("groq_api_key"))