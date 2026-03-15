from typing import List

def recursive_character_text_splitter(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Splits text into chunks of roughly chunk_size with chunk_overlap.
    Simple implementation mimicking LangChain's RecursiveCharacterTextSplitter.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If we're not at the end, try to find a nice breaking point (newline or space)
        if end < len(text):
            # Look for last newline in the window
            last_newline = text.rfind('\n', start, end)
            if last_newline != -1 and last_newline > start + (chunk_size // 2):
                end = last_newline + 1
            else:
                # Look for last space
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and last_space > start + (chunk_size // 2):
                    end = last_space + 1
                    
        chunks.append(text[start:end].strip())
        
        # Move start forward, but account for overlap
        start = end - chunk_overlap
        if start < 0 or start >= len(text) or end >= len(text):
            break
            
    # Filter out empty or whitespace-only chunks
    return [c for c in chunks if c]
