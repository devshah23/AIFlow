import io
import pandas as pd
from app.text_extraction.base_extracter import BaseExtracter

class CSVExtracter(BaseExtracter):
    
    def extract_text(self) -> list[str]:
        """Extract text from the CSV file, chunking by row."""
        try:
            csv_stream = self.get_file_from_storage()
            csv_bytes = csv_stream.read()
            
            csv_text = csv_bytes.decode('utf-8')
            csv_io = io.StringIO(csv_text)
            
            df = pd.read_csv(csv_io)
            chunks = []
            
            column_names = ', '.join(df.columns)
            
            
            for index, row in df.iterrows():
                row_data_string = ", ".join([f"{col}: {val}" for col, val in row.items()])
                
                chunk = f"(Columns: {column_names}): {row_data_string}"
                chunks.append(chunk)
                
            return chunks
        except Exception as e:
            raise e