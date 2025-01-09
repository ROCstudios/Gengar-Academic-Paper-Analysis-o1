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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            errorCategory=data['errorCategory'],
            issue=data['issue'],
            implications=data['implications'],
            recommendation=data['recommendation']
        )

    def to_dict(self) -> dict:
        """Convert Error to dictionary format"""
        return {
            'errorCategory': self.errorCategory,
            'issue': self.issue,
            'implications': self.implications,
            'recommendation': self.recommendation
        }
    
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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data['title'],
            authors=data['authors'],
            published=data['published'],
            errorCount=data['errorCount'],
            logicalErrorCount=data['logicalErrorCount'],
            methodicalErrorCount=data['methodicalErrorCount'],
            calculationErrorCount=data['calculationErrorCount'],
            dataInconsistencyCount=data['dataInconsistencyCount'],
            citationErrorCount=data['citationErrorCount'],
            formattingErrorCount=data['formattingErrorCount'],
            ethicalErrorCount=data['ethicalErrorCount']
        )

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

    @classmethod
    def from_dict(cls, data: dict):
        # Filter out unexpected keywords for Error objects
        errors = []
        for error_data in data.get('errors', []):
            error_fields = {k: v for k, v in error_data.items()
                          if k in Error.__annotations__}
            errors.append(Error(**error_fields))
        return cls(errors=errors)

    def to_dict(self) -> dict:
        return {
            'errors': [error.to_dict() for error in self.errors]
        }

@dataclass
class DetailedAnalysis:
    pdf_name: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    summary: Optional[DetailedSummary] = None
    logical: Optional[CategoryAnalysis] = None
    methodical: Optional[CategoryAnalysis] = None
    calculation: Optional[CategoryAnalysis] = None
    data_inconsistencies: Optional[CategoryAnalysis] = None
    citation: Optional[CategoryAnalysis] = None
    formatting: Optional[CategoryAnalysis] = None
    ethical: Optional[CategoryAnalysis] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            pdf_name=data['pdf_name'],
            timestamp=data['timestamp'],
            summary=DetailedSummary(**data['summary']),
            **{k: CategoryAnalysis.from_dict(v) if v else None for k, v in data.get('categories', {}).items()}
        )

    def to_dict(self) -> dict:
        return {
            'pdf_name': self.pdf_name,
            'timestamp': self.timestamp,
            'summary': self.summary.to_dict() if self.summary else None,
            'logical': self.logical.to_dict() if self.logical else None,
            'methodical': self.methodical.to_dict() if self.methodical else None,
            'calculation': self.calculation.to_dict() if self.calculation else None,
            'data_inconsistencies': self.data_inconsistencies.to_dict() if self.data_inconsistencies else None,
            'citation': self.citation.to_dict() if self.citation else None,
            'formatting': self.formatting.to_dict() if self.formatting else None,
            'ethical': self.ethical.to_dict() if self.ethical else None
        }

    @classmethod
    def from_json(cls, pdf_name: str, json_str: str):
        """Convert JSON string to DetailedAnalysis object"""
        data = json.loads(json_str)
        # Create DetailedSummary from the summary data
        summary = DetailedSummary(**data['summary']) if 'summary' in data else None
        # Create CategoryAnalysis objects for each category if present
        categories = {
            'logical': data.get('logical'),
            'methodical': data.get('methodical'),
            'calculation': data.get('calculation'),
            'data_inconsistencies': data.get('data_inconsistencies'),
            'citation': data.get('citation'),
            'formatting': data.get('formatting'),
            'ethical': data.get('ethical')
        }

        return cls(
            pdf_name=pdf_name,
            timestamp= datetime.now().isoformat(),
            summary=summary,
            **{k: CategoryAnalysis.from_dict(v) if v else None 
               for k, v in categories.items()}
        )
    


