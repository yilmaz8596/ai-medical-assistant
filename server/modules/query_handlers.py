
from ..logger import logger 

def query_chain(chain,user_input:str):
    logger.info(f"Received user input: {user_input}")
    try:
        logger.debug("Running the query chain...")
        result=chain.invoke({"query": user_input})
        response={
            "response": result["result"],
            "sources": [doc.metadata.get("source", "") for doc in result["source_documents"]]
        }
        logger.debug(f"Query chain result: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing the query: {str(e)}")
        raise e