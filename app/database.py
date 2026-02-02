from supabase import create_client
from app.config import settings


# Validate settings before creating client
settings.validate()

# Create Supabase client
supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)