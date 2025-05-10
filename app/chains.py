import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile",
    temperature=0,
    api_key="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")
        
    def extract_jobs(self,cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED DATA FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped data is from the career's page of a website
            Your job is to extract the job posting and return them in JSON format containing the 
            following keys: "role","experience","skills" and "description".
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data':cleaned_text})
        try:  
           json_parser = JsonOutputParser()
           res = json_parser.parse(res.content)
        except OutputParserException: 
           raise OutputParserException("Context too big. Unable to parse jobs")
        return res if isinstance(res,list) else[res]

    def write_email(self, job, links):
      prompt_email = PromptTemplate.from_template(
        """
        #JOB DESCRIPTION:
        {job_description}
    
        #INSTRUCTION:
        You are Prasanna,a business development executive at Amazon.Amazon is an Product based company dedicated
        the seamless intergration of business processes through automated tools.
        Your job is to write a cold email to the client regarding the job mentioned above in fulfilling
        thier needs.
        Also add the most relevant ones from the following links to showcase the company's portfolio: {link_list}
        Remember you are Prasanna , BDE at Amazon , Banglore
        Make it more in a professional format
        Mention as writing email to Hiring Manager also mention my email : iamprasanna1@gmail.com
        Do not provide a preamble
        ### EMAIL (NO PREAMBLE):
        """ 
      )
      chain_email = prompt_email | self.llm
      res = chain_email.invoke({"job_description": str(job), "link_list": links})
      return res.content

if __name__ == "__main__": 
    print(os.getenv("API_KEY"))