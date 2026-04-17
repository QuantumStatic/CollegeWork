import concurrent.futures
import numpy
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from typing import Generator



def calculate_dissimilarity(sentence1:str, sentence2:str) -> float:
    """Calculate the dissimilarity between two sentences using the cosine distance"""

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    sentence_embeddings = model.encode([sentence1, sentence2])
    return distance.cosine(sentence_embeddings[0], sentence_embeddings[1])


def _parallel_calculate_dissimilarity(target_sentence_encoding:numpy.ndarray, sentence2:str, idx:int) -> tuple[int, float]:
    
    """Unit function for multi_sentence_disimilarity"""

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    sentence2_encoding = model.encode([sentence2])
    return (idx, distance.cosine(target_sentence_encoding, sentence2_encoding))


def multi_sentence_disimilarity(target_sentence:str, sentences:list[str]) -> Generator[tuple[int, float], None, None]:

    """Calculate the dissimilarity between a target sentence and a list of sentences"""
    
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Encode the target sentence once only
    target_sentence_embedding = model.encode([target_sentence])

    # Initialise the executor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = [executor.submit(_parallel_calculate_dissimilarity, target_sentence_embedding, sentence, idx) for idx, sentence in enumerate(sentences)]

        for process in concurrent.futures.as_completed(processes):
            yield process.result()


def get_enocoded_sentences(sentences:list[str]) -> list[numpy.ndarray]:
    """Encode a list of sentences using the sentence transformer model"""

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return model.encode(sentences)


def _get_cosine_score(args:tuple[numpy.ndarray, numpy.ndarray]):
    """Return the cosine distance between two vectors"""
    return distance.cosine(args[0], args[1])


def get_multi_sentence_cosine(target_sentence:numpy.ndarray, sentences:numpy.ndarray) -> Generator[float, None, None]:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = executor.map(_get_cosine_score, [(target_sentence, x) for x in sentences])

        # In this case we are not using as_completed because we want to return the results in the order they were submitted
        for process in processes:
            yield process


def _parallel_multi_match_cosine(args:tuple[numpy.ndarray, list[numpy.ndarray]]):
    return tuple(distance.cosine(args[0], x) for x in args[1])


def multi_match_cosine_thresh(target_sentences:list[numpy.ndarray], sentences:list[numpy.ndarray], threshold:float=0.5):
    """Return a generator of booleans indicating whether the cosine distance between the target sentence and the sentences is above the threshold"""

    if sentences is None:
        yield from (None for _ in target_sentences)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = executor.map(_parallel_multi_match_cosine, [(x, sentences) for x in target_sentences])

        for process in processes:
            yield all(map(lambda x: x > threshold, process))


def non_similar_filtering(sentences:list[numpy.ndarray], threshold:float=0.5):
    """Return a generator of booleans indicating whether the cosine distance within sentences themselves is above the threshold or not"""

    if sentences is None:
        yield from (None for _ in sentences)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = executor.map(_parallel_multi_match_cosine, [(x, sentences) for x in sentences])

        for process in processes:
            yield all(map(lambda x: x > threshold or x < 0.08, process))