from pathlib import Path

from pypdf import PdfReader

from app.services.agents.base import BaseAgent
from app.services.agents.protocol import ProtocolMessage, ProtocolResponse
from app.utils.text_splitter import recursive_character_text_splitter


class PitchExtractionAgent(BaseAgent):
    name = "PitchExtractionAgent"

    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        file_path = Path(str(message.data["file_path"]))
        reader = PdfReader(str(file_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        chunks = recursive_character_text_splitter(text, chunk_size=900, chunk_overlap=120)
        return ProtocolResponse(
            sender=self.name,
            data={
                "extracted_text": text,
                "chunks": chunks,
                "page_count": len(reader.pages),
            },
        )
