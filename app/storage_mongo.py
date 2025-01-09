import os
from app.api.mongo import MongoDBStorage
from app.api.completions import chat_with_gpt, clean_json_string
from app.data.multi_prompt_analysis_errors import (
    extract_text_from_pdf, LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT,
    CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT,
    FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT
)
from app.data.multi_prompt_analysis_errors import ComprehensiveAnalysis, AnalysisResult

def analyze_pdfs(folder_path):
    storage = MongoDBStorage()  # Initialize MongoDB storage
    storage.test_connection()  # Test connection to MongoDB

    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            print(f"Analyzing {file}")
            pdf_path = os.path.join(folder_path, file)
            text = extract_text_from_pdf(pdf_path)

            # Perform all types of analysis
            prompts_and_types = [
                (LOGICAL_ERROR_PROMPT, "logical"),
                # (METHODICAL_ERROR_PROMPT, "methodical"),
                # (CALCULATIONL_ERROR_PROMPT, "calculation"),
                # (DATA_ERROR_PROMPT, "data"),
                # (CITATION_ERROR_PROMPT, "citation"),
                # (FORMATTING_ERROR_PROMPT, "formatting"),
                # (PLAGARISM_ERROR_PROMPT, "plagiarism"),
                # (ETHICAL_ERROR_PROMPT, "ethical")
            ]

            comprehensive_analysis = ComprehensiveAnalysis(pdf_name=file)

            for prompt, analysis_type in prompts_and_types:
                completion = chat_with_gpt(prompt=prompt, pdf_content=text)
                print("****")
                print(completion)
                print("****")
                result = AnalysisResult.from_json(clean_json_string(completion))

                setattr(comprehensive_analysis, f"{analysis_type}_analysis", result)

            # Save the comprehensive analysis to MongoDB
            mongo_id = storage.save_comprehensive_analysis(comprehensive_analysis)
            print(f"Saved comprehensive analysis to MongoDB with ID: {mongo_id}")

if __name__ == "__main__":
    analyze_pdfs("downloaded_pdfs")
