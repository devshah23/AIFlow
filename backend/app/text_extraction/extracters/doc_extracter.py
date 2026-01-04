from docx import Document
from app.text_extraction.base_extracter import BaseExtracter

class DocExtracter(BaseExtracter):
    
    def extract_text(self) -> list[str]:
        """Extract text from the docx file, chunking by paragraph."""
        try:
            doc_stream = self.get_file_from_storage()
            
            
            doc_reader = Document(doc_stream)
            
            chunks = []
            
            for paragraph in doc_reader.paragraphs:
                text = paragraph.text.strip()
                if text:
                    chunks.append(text)
            
            if not chunks:
                raise ValueError("The DOCX file contains no extractable content.")
                
            return chunks
        except Exception as e:
            raise e