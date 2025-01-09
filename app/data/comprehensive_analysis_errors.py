import os
from entry import extract_text_from_pdf
from api.dropbox_handler import download_pdfs_from_dropbox
from api.completions import chat_with_gpt
from api.completions import LOGICAL_ERROR_PROMPT, METHODICAL_ERROR_PROMPT, CALCULATIONL_ERROR_PROMPT, DATA_ERROR_PROMPT, CITATION_ERROR_PROMPT, FORMATTING_ERROR_PROMPT, PLAGARISM_ERROR_PROMPT, ETHICAL_ERROR_PROMPT
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class Error:
    errorCategory: str
    issue: str 
    implications: str
    recommendation: str

    def to_dict(self) -> dict:
        """Convert Error to dictionary format"""
        return {
            'errorCategory': self.errorCategory,
            'issue': self.issue,
            'implications': self.implications,
            'recommendation': self.recommendation
        }

@dataclass
class Summary:
    title: str
    authors: str
    published: str
    errorCount: int

    def to_dict(self) -> dict:
        """Convert Summary to dictionary format"""
        return {
            'title': self.title,
            'authors': self.authors,
            'published': self.published,
            'errorCount': self.errorCount
        }

@dataclass
class AnalysisResult:
    errors: List[Error]
    summary: Summary

    def to_dict(self) -> dict:
        """Convert AnalysisResult to dictionary format"""
        return {
            'errors': [error.to_dict() for error in self.errors],
            'summary': self.summary.to_dict()
        }

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        
        # Filter out unexpected keywords for Error objects
        errors = []
        for error_data in data['errors']:
            error_fields = {k: v for k, v in error_data.items() 
                          if k in Error.__annotations__}
            errors.append(Error(**error_fields))

        # Filter out unexpected keywords for Summary object
        summary_fields = {k: v for k, v in data['summary'].items()
                         if k in Summary.__annotations__}
        
        # Remove any newlines from pdf_name if it exists in summary
        if 'pdf_name' in summary_fields:
            summary_fields['pdf_name'] = summary_fields['pdf_name'].replace('\n', '')
            
        summary = Summary(**summary_fields)
        return cls(errors=errors, summary=summary)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)



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


