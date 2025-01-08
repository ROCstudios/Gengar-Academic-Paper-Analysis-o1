from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# Placeholder imports (Replace with your actual module imports)
from analysis import AnalysisResult
from completions import chat_with_gpt, clean_json_string
from analysis import (
    extract_text_from_pdf, LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT,
    CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT,
    FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT
)

@dataclass
class AnalysisMetadata:
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    pdf_name: str = ""
    analysis_type: str = ""  # e.g., "logical", "methodical", etc.

@dataclass
class ComprehensiveAnalysis:
    pdf_name: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    logical_analysis: Optional[AnalysisResult] = None
    methodical_analysis: Optional[AnalysisResult] = None
    calculation_analysis: Optional[AnalysisResult] = None
    data_analysis: Optional[AnalysisResult] = None
    citation_analysis: Optional[AnalysisResult] = None
    formatting_analysis: Optional[AnalysisResult] = None
    plagiarism_analysis: Optional[AnalysisResult] = None
    ethical_analysis: Optional[AnalysisResult] = None

    def get_total_error_count(self) -> int:
        total = 0
        for analysis in [
            self.logical_analysis,
            self.methodical_analysis,
            self.calculation_analysis,
            self.data_analysis,
            self.citation_analysis,
            self.formatting_analysis,
            self.plagiarism_analysis,
            self.ethical_analysis
        ]:
            if analysis and hasattr(analysis, 'summary'):
                total += int(analysis.summary.errorCount)
        return total

    def to_dict(self) -> dict:
        return {
            'pdf_name': self.pdf_name,
            'timestamp': self.timestamp,
            'analyses': {
                'logical': self.logical_analysis.to_dict() if self.logical_analysis else None,
                'methodical': self.methodical_analysis.to_dict() if self.methodical_analysis else None,
                'calculation': self.calculation_analysis.to_dict() if self.calculation_analysis else None,
                'data': self.data_analysis.to_dict() if self.data_analysis else None,
                'citation': self.citation_analysis.to_dict() if self.citation_analysis else None,
                'formatting': self.formatting_analysis.to_dict() if self.formatting_analysis else None,
                'plagiarism': self.plagiarism_analysis.to_dict() if self.plagiarism_analysis else None,
                'ethical': self.ethical_analysis.to_dict() if self.ethical_analysis else None
            },
            'total_errors': self.get_total_error_count()
        }

    @staticmethod
    def from_dict(data: dict) -> 'ComprehensiveAnalysis':
        return ComprehensiveAnalysis(
            pdf_name=data['pdf_name'],
            timestamp=data['timestamp'],
            logical_analysis=AnalysisResult.from_dict(data['analyses']['logical']) if data['analyses']['logical'] else None,
            methodical_analysis=AnalysisResult.from_dict(data['analyses']['methodical']) if data['analyses']['methodical'] else None,
            calculation_analysis=AnalysisResult.from_dict(data['analyses']['calculation']) if data['analyses']['calculation'] else None,
            data_analysis=AnalysisResult.from_dict(data['analyses']['data']) if data['analyses']['data'] else None,
            citation_analysis=AnalysisResult.from_dict(data['analyses']['citation']) if data['analyses']['citation'] else None,
            formatting_analysis=AnalysisResult.from_dict(data['analyses']['formatting']) if data['analyses']['formatting'] else None,
            plagiarism_analysis=AnalysisResult.from_dict(data['analyses']['plagiarism']) if data['analyses']['plagiarism'] else None,
            ethical_analysis=AnalysisResult.from_dict(data['analyses']['ethical']) if data['analyses']['ethical'] else None
        )

class MongoDBStorage:
    def __init__(
            self, 
            uri="mongodb+srv://adrian:bEhG0HKts4oKcKGa@gengar-1k-research.0k4v4.mongodb.net/?retryWrites=true&w=majority&appName=Gengar-1k-Research", 
            db_name="analysis_db", 
            collection_name="comprehensive_analyses"
    ):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def test_connection(self):
        try:
            # Connect the client to the server and ping to confirm connection
            self.client.admin.command({"ping": 1})
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")

    def save_comprehensive_analysis(self, analysis: ComprehensiveAnalysis) -> str:
        """Save a comprehensive analysis to MongoDB."""
        analysis_dict = analysis.to_dict()
        result = self.collection.insert_one(analysis_dict)
        return str(result.inserted_id)

    def get_analysis(self, pdf_name: str) -> Optional[ComprehensiveAnalysis]:
        """Retrieve a specific analysis by PDF name from MongoDB."""
        result = self.collection.find_one({"pdf_name": pdf_name})
        if result:
            return ComprehensiveAnalysis.from_dict(result)
        return None

    def update_analysis(self, pdf_name: str, analysis_type: str, result: AnalysisResult):
        """Update a specific analysis in MongoDB."""
        field_name = f"analyses.{analysis_type}"
        self.collection.update_one(
            {"pdf_name": pdf_name},
            {"$set": {field_name: result.to_dict()}}
        )

    def delete_analysis(self, pdf_name: str):
        """Delete a specific analysis by PDF name."""
        self.collection.delete_one({"pdf_name": pdf_name})

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
