import os
import time
from django.core.management.base import BaseCommand
from perfumes.models import Perfume

class Command(BaseCommand):
    help = 'Batch index perfumes into Pinecone Vector DB'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=50)

    def handle(self, *args, **options):
        # 1. API Keys & Configuration (Recommended to use .env)
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "olfit-perfumes")

        if not OPENAI_API_KEY or not PINECONE_API_KEY:
            self.stdout.write(self.style.WARNING("Skipping indexing: API keys not found in environment variables."))
            self.stdout.write("Please set OPENAI_API_KEY and PINECONE_API_KEY to proceed.")
            return

        try:
            from openai import OpenAI
            from pinecone import Pinecone, ServerlessSpec
        except ImportError:
            self.stdout.write(self.style.ERROR("Required libraries (openai, pinecone-client) not installed."))
            return

        # 2. Initialize Clients
        client = OpenAI(api_key=OPENAI_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # 3. Ensure Index Exists
        if PINECONE_INDEX_NAME not in pc.list_indexes().names():
            self.stdout.write(f"Creating index: {PINECONE_INDEX_NAME}...")
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1536, # text-embedding-3-small dimension
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        
        index = pc.Index(PINECONE_INDEX_NAME)

        # 4. Batch Processing
        perfumes = Perfume.objects.all()
        batch_size = options['batch_size']
        total = perfumes.count()
        
        self.stdout.write(self.style.SUCCESS(f"Starting indexing for {total} perfumes..."))

        for i in range(0, total, batch_size):
            batch = perfumes[i:i+batch_size]
            vectors = []
            
            # A. Prepare batch documents
            docs = [p.data.get("embedding_doc", "") for p in batch]
            ids = [str(p.id) for p in batch]
            
            # B. Generate Embeddings via OpenAI
            try:
                response = client.embeddings.create(input=docs, model="text-embedding-3-small")
                embeddings = [e.embedding for v, e in zip(ids, response.data)]
                
                # C. Prepare Pinecone Upsert
                for p, emb in zip(batch, embeddings):
                    vectors.append((
                        str(p.id),
                        emb,
                        {
                            "brand": p.brand.name,
                            "name": p.korean_name,
                            "family": p.family,
                            "product_type": p.product_type
                        }
                    ))
                
                # D. Upsert to Pinecone
                index.upsert(vectors=vectors)
                self.stdout.write(f"Indexed batch {i//batch_size + 1}: {len(vectors)} items.")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in batch {i}: {e}"))
                time.sleep(1) # Simple retry delay

        self.stdout.write(self.style.SUCCESS("Pinecone batch indexing complete."))
