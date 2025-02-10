"""
Ollama Social Bot Wireframe

A customizable template for creating AI-powered social media bots using LlamaIndex and Bluesky.
"""

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, PromptTemplate, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from atproto import Client, models
import os
import re
import random
import datetime

# --------------------------
# Configuration
# --------------------------
class Config:
    # Social Media Configuration
    SOCIAL_MEDIA_HANDLE = os.getenv('BLUESKY_HANDLE', 'your-handle.bsky.social')
    SOCIAL_MEDIA_APP_PASSWORD = os.getenv('BLUESKY_APP_PASSWORD', 'your-app-password')
    
    # Content Generation Parameters
    MAX_POST_LENGTH = 300
    HASHTAG_POOLS = [
        "#AI #Tech #Innovation",
        "#OpenSource #Community #Dev"
    ]
    
    # Path Configuration
    DATA_DIR = "./data"
    STORAGE_DIR = "./storage"
    
    # Model Configuration
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    LLM_MODEL = "llama3.2:latest"

# --------------------------
# Prompt Engineering
# --------------------------
class ContentGenerator:
    @staticmethod
    def create_prompt_template():
        return PromptTemplate(
            template="""\
Create a social media post about {topic} with these guidelines:
- Use {tone} tone
- Include {hashtag_count} hashtags from: {hashtags}
- Maximum {max_length} characters
- Add relevant emojis

Examples:
{examples}
"""
        )

    @staticmethod
    def get_dynamic_components():
        return {
            "topics": ["AI ethics", "machine learning", "open source"],
            "tones": ["professional", "casual", "enthusiastic"],
            "examples": [
                "🤖 AI should augment human intelligence, not replace it #EthicalAI",
                "Open source fuels innovation - let's build together! 🚀 #OpenSource"
            ]
        }

# --------------------------
# Core Functionality
# --------------------------
class SocialBot:
    def __init__(self):
        self._setup_models()
        self.index = self._initialize_index()
        
    def _setup_models(self):
        Settings.embed_model = HuggingFaceEmbedding(model_name=Config.EMBEDDING_MODEL)
        Settings.llm = Ollama(model=Config.LLM_MODEL, request_timeout=360.0)
        
    def _initialize_index(self):
        if os.path.exists(Config.STORAGE_DIR):
            return load_index_from_storage(StorageContext.from_defaults(persist_dir=Config.STORAGE_DIR))
            
        documents = SimpleDirectoryReader(input_dir=Config.DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=Config.STORAGE_DIR)
        return index

    def generate_post(self, query: str) -> str:
        response = self.index.as_query_engine().query(query)
        return self._process_response(response)

    def _process_response(self, response):
        processed_text = ' '.join(str(response.response).strip().split())
        return self._sanitize_content(processed_text)

    def _sanitize_content(self, text: str) -> str:
        # Content cleaning and validation logic
        text = re.sub(r'\*\*|"', '', text)  # Remove markdown
        return self._truncate_content(text)

    def _truncate_content(self, text: str) -> str:
        if len(text) > Config.MAX_POST_LENGTH:
            return text[:Config.MAX_POST_LENGTH-3] + '...'
        return text

# --------------------------
# Social Media Integration
# --------------------------
class BlueskyClient:
    def __init__(self):
        self.client = Client()
        
    def authenticate(self):
        self.client.login(
            Config.SOCIAL_MEDIA_HANDLE,
            Config.SOCIAL_MEDIA_APP_PASSWORD
        )
        
    def create_post(self, text: str):
        facets = self._create_hashtag_facets(text)
        return self.client.send_post(text=text, facets=facets)
        
    def _create_hashtag_facets(self, text: str):
        class UnicodeString:
            def __init__(self, text: str):
                self.text = text
                self.utf8 = text.encode('utf-8')
            
            def byte_length(self, char_count: int) -> int:
                return len(self.text[:char_count].encode('utf-8'))
        
        text_obj = UnicodeString(text)
        facets = []
        
        for match in re.finditer(r'(?:^|\s)(#\w+)', text):
            hashtag = match.group(1)
            start_char = match.start(1)
            end_char = match.end(1)
            
            facets.append({
                "index": {
                    "byteStart": text_obj.byte_length(start_char),
                    "byteEnd": text_obj.byte_length(end_char)
                },
                "features": [{
                    "$type": "app.bsky.richtext.facet#tag",
                    "tag": hashtag[1:].lower()
                }]
            })
        
        return facets

# --------------------------
# Execution Flow
# --------------------------
if __name__ == "__main__":
    # Initialize components
    bot = SocialBot()
    bluesky = BlueskyClient()
    components = ContentGenerator.get_dynamic_components()
    
    # Generate query with dynamic components
    prompt_template = ContentGenerator.create_prompt_template().format(
        topic=random.choice(components["topics"]),
        tone=random.choice(components["tones"]),
        hashtags=random.choice(Config.HASHTAG_POOLS),
        hashtag_count=random.randint(1, 3),
        max_length=Config.MAX_POST_LENGTH,
        examples="\n".join(random.sample(components["examples"], 2))
    )
    
    # Generate and post content
    try:
        post_content = bot.generate_post(prompt_template)
        bluesky.authenticate()
        bluesky.create_post(post_content)
        print(f"Successfully posted: {post_content}")
    except Exception as e:
        print(f"Error posting content: {str(e)}")



