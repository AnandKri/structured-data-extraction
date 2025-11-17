import warnings
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from util import Invoice, get_pdf_file_paths, schema
warnings.filterwarnings("ignore")

if __name__=="__main__":
    pdf_directory = r"./Sample PDFs"
    pdf_file_paths = get_pdf_file_paths(pdf_directory)

    llm = ChatOllama(model="llama3.2:1b-instruct-q8_0", temperature=0)
    
    df = pd.DataFrame(columns=["customerName", "address", "invoiceNumber", "invoiceDate", "amountDue"])

    for rel_path in pdf_file_paths:
        invoice = Invoice(rel_path)

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a highly accurate assistant. You must output ONLY valid JSON following the given format instructions."),
            ("human", "Please answer the following request and format the output as specified:\nRequest: {invoice_data}")
        ])

        prompt = prompt_template.invoke({
            "invoice_data": (
                "Extract required fields from the given text of an invoice document. "
                f"Document text: {invoice.text_data}"
            )
        })

        structured_output = llm.with_structured_output(schema).invoke(prompt.to_messages())
        print(structured_output)

        df = pd.concat([df, pd.DataFrame([structured_output])], ignore_index=True)
    
    df.to_excel("extracted_invoice_data.xlsx", index=False)
    print(df)