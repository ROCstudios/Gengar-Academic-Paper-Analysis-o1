import os
from mongo import MongoDBStorage
from completions import chat_with_gpt, clean_json_string
from typing import Optional
from prompts import (
    LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT,
    CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT,
    FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT, BIG_BOY_SINGLE_PROMPT
)
from data_analysis import ComprehensiveAnalysis, AnalysisResult
from entry import extract_text_from_pdf

bulk_storage = MongoDBStorage()  # Initialize MongoDB storage
bulk_storage.test_connection()  # Test connection to MongoDB

upload_storage = MongoDBStorage(collection_name="uploads")
upload_storage.test_connection()

def get_pdf_analysis(pdf_name: str, text: str):
    mongo_id = analyze_single_pdf(pdf_name, text, upload_storage)
    return get_analysis_by_id(mongo_id)

def analyze_single_pdf(pdf_name: str, text: str, database: MongoDBStorage):
    
    # Perform all types of analysis
    prompts_and_types = [
        (LOGICAL_ERROR_PROMPT, "logical"),
        (METHODICAL_ERROR_PROMPT, "methodical"),
        (CALCULATIONL_ERROR_PROMPT, "calculation"),
        (DATA_ERROR_PROMPT, "data"),
        (CITATION_ERROR_PROMPT, "citation"),
        (FORMATTING_ERROR_PROMPT, "formatting"),
        (PLAGARISM_ERROR_PROMPT, "plagiarism"),
        (ETHICAL_ERROR_PROMPT, "ethical")
    ]

    comprehensive_analysis = ComprehensiveAnalysis(pdf_name=pdf_name)

    for prompt, analysis_type in prompts_and_types:
        completion = chat_with_gpt(prompt=prompt, pdf_content=text)
        print("****")
        print(completion)
        print("****\n")
        result = AnalysisResult.from_json(completion)

        setattr(comprehensive_analysis, f"{analysis_type}_analysis", result)

    # Save the comprehensive analysis to MongoDB
    mongo_id = database.save_comprehensive_analysis(comprehensive_analysis)
    return mongo_id

def bulk_analyze_pdfs(folder_path):
    """Analyze all PDFs in a given folder.
    
    Args:
        folder_path (str): Path to folder containing PDF files to analyze
    """
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            print(f"Checking {file}")
            
            # Check if analysis already exists in MongoDB
            existing_analysis = bulk_storage.collection.find_one({"pdf_name": file})
            if existing_analysis:
                print(f"Analysis for {file} already exists in MongoDB. Skipping...")
                continue

            print(f"Analyzing {file}")
            pdf_path = os.path.join(folder_path, file)
            text = extract_text_from_pdf(pdf_path)
            
            mongo_id = analyze_single_pdf(file, text, bulk_storage)
            print(f"Saved comprehensive analysis to MongoDB with ID: {mongo_id}")

def get_analysis_json(pdf_name: str) -> Optional[dict]:
    """Retrieve a specific analysis by PDF name and return it as a JSON/dict object."""
    result = bulk_storage.collection.find_one({"pdf_name": pdf_name})
    if result:
        # Remove MongoDB's _id field since it's not JSON serializable
        result.pop('_id', None)
        return result
    return None

def get_analysis_by_id(mongo_id: str) -> Optional[dict]:
    """Retrieve a specific analysis by MongoDB ID and return it as a JSON/dict object."""
    from bson.objectid import ObjectId
    result = bulk_storage.collection.find_one({"_id": ObjectId(mongo_id)})
    if result:
        # Remove MongoDB's _id field since it's not JSON serializable
        result.pop('_id', None)
        return result
    return None

def get_all_analyses():
    """Return all documents as a list."""
    cursor = bulk_storage.collection.find({})
    return [doc for doc in cursor]

def count_analyses():
    """Count total documents in collection."""
    return bulk_storage.collection.count_documents({})

def print_all_pdf_names():
    """Print just the PDF names of all documents."""
    cursor = bulk_storage.collection.find({}, {"pdf_name": 1})  # Only retrieve pdf_name field
    for doc in cursor:
        print(doc["pdf_name"])

def get_collective_scores() -> dict:
    """
    Queries all analyses and returns a JSON summary of error counts by type.
    Returns a dictionary with error types as keys and their total counts as values.
    """
    cursor = bulk_storage.collection.find({})
    
    # Initialize counters for each error type
    collective_scores = {
        "logical_errors": 0,
        "methodical_errors": 0,
        "calculation_errors": 0,
        "data_errors": 0,
        "citation_errors": 0,
        "formatting_errors": 0,
        "plagiarism_errors": 0,
        "ethical_errors": 0
    }
    
    # Map analysis types to their corresponding JSON fields
    analysis_types = {
        "logical": "logical",
        "methodical": "methodical",
        "calculation": "calculation",
        "data": "data",
        "citation": "citation",
        "formatting": "formatting",
        "plagiarism": "plagiarism",
        "ethical": "ethical"
    }
    
    # Count errors from each document
    for doc in cursor:
        for error_type, field_name in analysis_types.items():
            if 'analyses' in doc and field_name in doc['analyses'] and doc['analyses'][field_name]:
                analysis = doc['analyses'][field_name]
                if 'errors' in analysis and isinstance(analysis['errors'], list):
                    collective_scores[f"{error_type}_errors"] += len(analysis['errors'])
    
    return collective_scores

if __name__ == "__main__":
    #add bulk download pdfs
    # analyze_pdfs("downloaded_pdfs")
    # print(get_analysis_json("A_Balance_for_Fairness:_Fair_Distribution_Utilising_Physics_in_Games_of_Characteristic_Function_Form.pdf"))
    print(get_collective_scores())

