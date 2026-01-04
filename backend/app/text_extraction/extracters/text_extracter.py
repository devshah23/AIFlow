import io
from app.text_extraction.base_extracter import BaseExtracter

class TextExtracter(BaseExtracter):
    """Extract text from plain .txt files, chunking by paragraph breaks."""
    
    def extract_text(self) -> list[str]:
        """
        Reads the .txt file and returns a list of chunks, 
        where each chunk is typically a paragraph.
        """
        try:
            text_stream = self.get_file_from_storage()
            text_bytes = text_stream.read()
            
            try:
                full_text = text_bytes.decode('utf-8')
            except UnicodeDecodeError:
                
                full_text = text_bytes.decode('latin-1') 

            chunks = []
            raw_paragraphs = full_text.split('\n\n')
            
            for paragraph in raw_paragraphs:
                chunk = paragraph.strip()
                if chunk: 
                    chunks.append(chunk)

            if not chunks:   
                 if full_text.strip():
                     chunks.append(full_text.strip())
                 else:
                     raise ValueError("The TXT file contains no readable content.")
                
            return chunks
            
        except Exception as e:
            raise e