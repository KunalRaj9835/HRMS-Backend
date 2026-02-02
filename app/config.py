import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings"""
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # API Configuration
    API_TITLE: str = "HRMS Lite API"
    API_VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]  # Update with specific origins in production
    
    def validate(self):
        """Validate required settings"""
        if not self.SUPABASE_URL:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not self.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY environment variable is required")
        return True

# Create settings instance
settings = Settings()