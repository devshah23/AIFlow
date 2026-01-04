

from app.text_extraction.extracters.csv_extracter import CSVExtracter
from app.text_extraction.extracters.doc_extracter import DocExtracter
from app.text_extraction.extracters.pdf_extracter import PDFExtracter
from app.text_extraction.extracters.text_extracter import TextExtracter
from app.text_extraction.base_extracter import BaseExtracter


class ExtracterFactory:
   registry={
    "application/pdf": PDFExtracter,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocExtracter,
    "application/csv": CSVExtracter,
    "text/csv": CSVExtracter,
    "text/plain": TextExtracter,
   }
   
   @staticmethod
   def get_extracter(file_path:str,file_type:str)->BaseExtracter:
        extracter_cls=ExtracterFactory.registry.get(file_type.lower())
        if not extracter_cls:
            raise ValueError(f"Unsupported file type for extraction: {file_type}")
        
        return extracter_cls(file_name=file_path)