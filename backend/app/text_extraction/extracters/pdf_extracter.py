from pypdf import PdfReader
from app.text_extraction.base_extracter import BaseExtracter

class PDFExtracter(BaseExtracter):
    """Extract text from PDF files, returning a list of chunks."""
    
    def extract_text(self) -> list[str]:
        """Extract text from the PDF file, chunking by page."""
        try:
            pdf_stream = self.get_file_from_storage()
            reader = PdfReader(pdf_stream)
            
            chunks = []
            
            
            for i, page in enumerate(reader.pages):
                extracted_text = page.extract_text()
                
                contextual_chunk = f"Page {i+1} of Document:\n" + (extracted_text or "")
                
                if extracted_text and extracted_text.strip():
                    chunks.append(contextual_chunk)
            
            if not chunks:
                raise ValueError("The PDF file contains no readable text or pages.")
                
            return chunks
        except Exception as e:
            raise e