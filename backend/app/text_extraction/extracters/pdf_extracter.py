import re
from pypdf import PdfReader
from app.text_extraction.base_extracter import BaseExtracter

class PDFExtracter(BaseExtracter):
    """Extract text from PDF files, returning a list of chunks."""
    
    def extract_text(self) -> list[str]:
        """Extract text from the PDF file, chunking by page."""
        pdf_stream = self.get_file_bytes_stream()
        reader = PdfReader(pdf_stream)
        
        chunks = self.__get_chunks_by_page(reader)
        if not chunks:
            raise ValueError("The PDF file contains no readable text or pages.")
        
        return chunks
    
    def __get_chunks_by_page(self, reader: PdfReader) -> list[str]:
        """Helper method to extract text from each page and return as chunks."""
        chunks = []
        
        for i, page in enumerate(reader.pages):
            extracted_text = page.extract_text()
            text = re.sub(r"-\n", "", extracted_text or "")   
            text = re.sub(r"\n+", " ", text)  
            text=text.strip()
            if text:
                chunks.append(text)
                
        return chunks