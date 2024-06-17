import os

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "..."
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

db = SQLDatabase.from_uri('trino://tigerbonzo@localhost:8080/chinook_database/public')
write_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)


chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke({"question": "What is the album name with id 4"}))