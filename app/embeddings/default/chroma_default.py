import chromadb.utils.embedding_functions as embedding_functions

from loguru import logger

class ChromaDefaultEmbedding:
    def __init__(self):
        logger.info("Initialising embedding providers")
        self.ef = embedding_functions.DefaultEmbeddingFunction()

    def load_emb(self):
        return self.ef
    

