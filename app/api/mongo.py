from pymongo import MongoClient
from typing import Optional
from ..data.comprehensive_analysis_errors import AnalysisResult, ComprehensiveAnalysis
from ..data.detailed_analysis_errors import DetailedAnalysis

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

    def get_comprehensive_analysis(self, pdf_name: str) -> Optional[ComprehensiveAnalysis]:
        """Retrieve a specific analysis by PDF name from MongoDB."""
        result = self.collection.find_one({"pdf_name": pdf_name})
        if result:
            return ComprehensiveAnalysis.from_dict(result)
        return None
    
    def save_detailed_analysis(self, analysis: DetailedAnalysis) -> str:
        """Save a detailed analysis to MongoDB."""
        analysis_dict = analysis.to_dict()
        result = self.collection.insert_one(analysis_dict)
        return str(result.inserted_id)
    
    def get_detailed_analysis(self, pdf_name: str) -> Optional[DetailedAnalysis]:
        """Retrieve a specific analysis by PDF name from MongoDB."""
        result = self.collection.find_one({"pdf_name": pdf_name})
        if result:
            return DetailedAnalysis.from_dict(result)
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
