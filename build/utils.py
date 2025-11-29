"""Utility functions for logging and file management."""

import os
import logging
from pathlib import Path
from typing import Optional


class Logger:
    """Simple logger for the alignment system."""
    
    def __init__(self, name: str = "ontology_aligner", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)


class FileManager:
    """Manages file paths and directory operations."""
    
    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            # Auto-detect project root from this file's location
            current_file = Path(__file__).resolve()
            self.project_root = current_file.parent.parent
        else:
            self.project_root = Path(project_root)
    
    def get_build_dir(self) -> Path:
        """Get build directory path."""
        return self.project_root / "build"
    
    def get_data_dir(self) -> Path:
        """Get data directory path."""
        return self.get_build_dir() / "data"
    
    def get_alignment_dir(self, framework: str) -> Path:
        """Get alignment directory for a specific framework."""
        return self.get_build_dir() / "alignment" / framework
    
    def get_composite_graph_path(self) -> Path:
        """Get path to composite knowledge graph."""
        return self.get_data_dir() / "composite_knowledge_graph.ttl"
    
    def get_alignment_output_path(self, framework: str, filename: str = "llm_generated_alignment.ttl") -> Path:
        """Get output path for alignment file."""
        return self.get_alignment_dir(framework) / filename
    
    def ensure_dir_exists(self, directory: Path) -> None:
        """Create directory if it doesn't exist."""
        directory.mkdir(parents=True, exist_ok=True)
    
    def file_exists(self, filepath: Path) -> bool:
        """Check if file exists."""
        return filepath.exists() and filepath.is_file()
    
    def validate_file(self, filepath: Path, file_description: str = "File") -> None:
        """Validate that a file exists, raise error if not."""
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"{file_description} not found: {filepath}")


class ConfigManager:
    """Manages configuration and environment variables."""
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get API key from environment variables."""
        return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    @staticmethod
    def validate_api_key() -> str:
        """Validate and return API key, raise error if not found."""
        api_key = ConfigManager.get_api_key()
        if not api_key:
            raise ValueError(
                "No API key found! Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.\n"
                "Example: export GEMINI_API_KEY='your-key-here'"
            )
        return api_key
    
    @staticmethod
    def validate_framework(framework: str) -> None:
        """Validate framework name."""
        valid_frameworks = ["fibo", "gufo", "saref"]
        if framework not in valid_frameworks:
            raise ValueError(
                f"Invalid framework '{framework}'. Must be one of: {', '.join(valid_frameworks)}"
            )


def setup_logging(level: int = logging.INFO) -> Logger:
    """Set up and return a logger instance."""
    return Logger(level=level)
