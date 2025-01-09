from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import json
from multi_prompt_analysis_errors import Error, AnalysisResult

@dataclass
class DetailedSummary:
    title: str
    authors: str
    published: str
    errorCount: int
    logicalErrorCount: int
    methodicalErrorCount: int
    calculationErrorCount: int
    dataInconsistencyCount: int
    citationErrorCount: int
    formattingErrorCount: int
    ethicalErrorCount: int

    def to_dict(self) -> dict:
        """Convert DetailedSummary to dictionary format"""
        return {
            'title': self.title,
            'authors': self.authors,
            'published': self.published,
            'errorCount': self.errorCount,
            'logicalErrorCount': self.logicalErrorCount,
            'methodicalErrorCount': self.methodicalErrorCount,
            'calculationErrorCount': self.calculationErrorCount,
            'dataInconsistencyCount': self.dataInconsistencyCount,
            'citationErrorCount': self.citationErrorCount,
            'formattingErrorCount': self.formattingErrorCount,
            'ethicalErrorCount': self.ethicalErrorCount
        }

@dataclass
class CategoryAnalysis:
    errors: List[Error]

    def to_dict(self) -> dict:
        return {
            'errors': [error.to_dict() for error in self.errors]
        }

    @classmethod
    def from_dict(cls, data: dict):
        errors = [Error(**error_data) for error_data in data.get('errors', [])]
        return cls(errors=errors)

@dataclass
class DetailedAnalysisResult:
    summary: DetailedSummary
    logical: Optional[CategoryAnalysis] = None
    methodical: Optional[CategoryAnalysis] = None
    calculation: Optional[CategoryAnalysis] = None
    data_inconsistencies: Optional[CategoryAnalysis] = None
    citation: Optional[CategoryAnalysis] = None
    formatting: Optional[CategoryAnalysis] = None
    ethical: Optional[CategoryAnalysis] = None

    def to_dict(self) -> dict:
        return {
            'summary': self.summary.to_dict(),
            'logical': self.logical.to_dict() if self.logical else None,
            'methodical': self.methodical.to_dict() if self.methodical else None,
            'calculation': self.calculation.to_dict() if self.calculation else None,
            'data_inconsistencies': self.data_inconsistencies.to_dict() if self.data_inconsistencies else None,
            'citation': self.citation.to_dict() if self.citation else None,
            'formatting': self.formatting.to_dict() if self.formatting else None,
            'ethical': self.ethical.to_dict() if self.ethical else None
        }

    @classmethod
    def from_json(cls, json_data: List[dict]):
        summary_data = next(item['summary'] for item in json_data if 'summary' in item)
        summary = DetailedSummary(**summary_data)
        
        category_mapping = {
            'logical': next((item['logical'] for item in json_data if 'logical' in item), None),
            'methodical': next((item['methodical'] for item in json_data if 'methodical' in item), None),
            'calculation': next((item['calculation'] for item in json_data if 'calculation' in item), None),
            'data_inconsistencies': next((item['data_inconsistencies'] for item in json_data if 'data_inconsistencies' in item), None),
            'citation': next((item['citation'] for item in json_data if 'citation' in item), None),
            'formatting': next((item['formatting'] for item in json_data if 'formatting' in item), None),
            'ethical': next((item['ethical'] for item in json_data if 'ethical' in item), None)
        }

        return cls(
            summary=summary,
            **{k: CategoryAnalysis.from_dict(v) if v else None 
               for k, v in category_mapping.items()}
        )
