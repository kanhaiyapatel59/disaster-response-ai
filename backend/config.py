"""
Configuration management for the Disaster Command Center
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "AI Disaster Command Center")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "../data")
    UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "./uploads")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./disaster.db")
    MONGO_URI = os.getenv(
        "MONGO_URI", 
        os.getenv(
            "MONGODB_URI", 
            "mongodb+srv://kanhaiya:patel@foodyham.anqqbp7.mongodb.net/disaster_db?retryWrites=true&w=majority"
        )
    )
    
    # Model Settings
    DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"  # Groq
    FALLBACK_LLM_MODEL = "gemini-pro"  # Gemini
    
    # Create directories if they don't exist
    UPLOAD_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Check if required API keys are present"""
        if not cls.GROQ_API_KEY:
            print("⚠️  WARNING: GROQ_API_KEY not set. Using fallback mode.")
        if not cls.OPENWEATHER_API_KEY:
            print("⚠️  WARNING: OPENWEATHER_API_KEY not set. Weather will be simulated.")
        return True

# Create config instance
config = Config()
config.validate()