import os
from pdf import extract_text_from_pdf
from dropbox_handler import download_pdfs_from_dropbox
from completions import chat_with_gpt
from completions import LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT, CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT, FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT

from dataclasses import dataclass
from typing import List
import json

@dataclass
class Error:
    errorCategory: str
    issue: str 
    implications: str
    recommendation: str

@dataclass
class Summary:
    title: str
    authors: str
    published: str
    errorCount: int

@dataclass
class AnalysisResult:
    errors: List[Error]
    summary: Summary

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        errors = [Error(**error) for error in data['errors']]
        summary = Summary(**data['summary'])
        return cls(errors=errors, summary=summary)

    def to_json(self):
        return json.dumps({
            'errors': [vars(error) for error in self.errors],
            'summary': vars(self.summary)
        }, indent=2)

analysis_results: List[AnalysisResult] = []

def analyze_pdfs(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            print(f"Analyzing {file}")
            # Check if file has already been analyzed
            if any(result.summary.title.lower() == file.lower().replace('.pdf', '') 
                  for result in analysis_results):
                print(f"Skipping {file} - already analyzed")
                continue

            # Extract text from PDF
            pdf_path = os.path.join(folder_path, file)
            text = extract_text_from_pdf(pdf_path)
            completion = chat_with_gpt(prompt = LOGICAL_ERROR_PROMPT, pdf_content = text)
            print(completion)
            # Parse the completion into AnalysisResult
            result = AnalysisResult.from_json(completion)
            analysis_results.append(result)
            print(f"Analysis complete for {file}")

if __name__ == "__main__":
    # download_folder = download_pdfs_from_dropbox()
    # analyze_pdfs(download_folder)
    analyze_pdfs("downloaded_pdfs")
