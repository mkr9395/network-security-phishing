from dataclasses import dataclass # dataclass acts as decorator for empty classes

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str