import io
from app.text_extraction.base_extracter import BaseExtracter

class TextExtracter(BaseExtracter):
    """Extract text from plain .txt files, chunking by paragraph breaks."""
    
    def extract_text(self) -> list[str]:
        """
        Extract text from the TXT file, chunking by paragraph breaks (double newlines).
        """
        text_stream = self.get_file_bytes_stream()
        text=self.__get_text(text_stream)
        
        chunks = self.__create_chunks(text)
        return chunks
    
    def __get_text(self,text_stream: io.BytesIO) -> str:
        text_bytes = text_stream.read()
        try:
            return text_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return text_bytes.decode('latin-1')
        
    def __create_chunks(self,text: str) -> list[str]:
        chunks = []
        if not text.strip():
            raise ValueError("The TXT file contains no readable content.")
        
        raw_paragraphs = text.split('\n\n')
        for paragraph in raw_paragraphs:
            chunk = paragraph.strip()
            if chunk: 
                chunks.append(chunk)
        
        return chunks
        
    