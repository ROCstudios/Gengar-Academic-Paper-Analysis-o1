from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json
import pickle
import os
from pathlib import Path
from app.data.multi_prompt_analysis_errors import AnalysisResult
from app.api.completions import chat_with_gpt, clean_json_string
from app.data.multi_prompt_analysis_errors import extract_text_from_pdf  
from app.data.multi_prompt_analysis_errors import LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT, CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT, FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT

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
                'logical': self.logical_analysis.to_json() if self.logical_analysis else None,
                'methodical': self.methodical_analysis.to_json() if self.methodical_analysis else None,
                'calculation': self.calculation_analysis.to_json() if self.calculation_analysis else None,
                'data': self.data_analysis.to_json() if self.data_analysis else None,
                'citation': self.citation_analysis.to_json() if self.citation_analysis else None,
                'formatting': self.formatting_analysis.to_json() if self.formatting_analysis else None,
                'plagiarism': self.plagiarism_analysis.to_json() if self.plagiarism_analysis else None,
                'ethical': self.ethical_analysis.to_json() if self.ethical_analysis else None
            },
            'total_errors': self.get_total_error_count()
        }

@dataclass
class AnalysisCollection:
    analyses: Dict[str, ComprehensiveAnalysis] = field(default_factory=dict)
    
    def add_analysis(self, pdf_name: str, analysis_type: str, result: AnalysisResult):
        if pdf_name not in self.analyses:
            self.analyses[pdf_name] = ComprehensiveAnalysis(pdf_name=pdf_name)
        
        # Set the appropriate analysis type
        setattr(self.analyses[pdf_name], f"{analysis_type}_analysis", result)

    def get_analysis(self, pdf_name: str) -> Optional[ComprehensiveAnalysis]:
        return self.analyses.get(pdf_name)

class AnalysisStorage:
    def __init__(self, storage_dir="analysis_outputs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.collection = AnalysisCollection()

    def save_comprehensive_analysis(self, analysis: ComprehensiveAnalysis):
        """Save all analyses for a single PDF"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{analysis.pdf_name}_{timestamp}_comprehensive.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis.to_dict(), f, indent=2)
        
        return filepath

    def save_collection(self):
        """Save the entire collection"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"complete_analysis_collection_{timestamp}.pkl"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.collection, f)
        
        return filepath

    def load_collection(self, filename):
        """Load a complete collection"""
        filepath = self.storage_dir / filename
        with open(filepath, 'rb') as f:
            self.collection = pickle.load(f)

def analyze_pdfs(folder_path):
    storage = AnalysisStorage()
    
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            print(f"Analyzing {file}")
            pdf_path = os.path.join(folder_path, file)
            text = extract_text_from_pdf(pdf_path)
            
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
            
            for prompt, analysis_type in prompts_and_types:
                completion = chat_with_gpt(prompt=prompt, pdf_content=text)
                print("****")
                print(completion)
                print("****")
                result = AnalysisResult.from_json(clean_json_string(completion))
                try:
                    storage.collection.add_analysis(file, analysis_type, result)
                    print(f"Completed {analysis_type} analysis for {file}")
                except Exception as e:
                    print(f"Error in {analysis_type} analysis for {file}: {e}")
            
            # Save comprehensive analysis for this PDF
            comprehensive = storage.collection.get_analysis(file)
            if comprehensive:
                filepath = storage.save_comprehensive_analysis(comprehensive)
                print(f"Saved comprehensive analysis to {filepath}")
    
    # Save the entire collection
    collection_path = storage.save_collection()
    print(f"Saved complete collection to {collection_path}")

if __name__ == "__main__":
    analyze_pdfs("downloaded_pdfs")
