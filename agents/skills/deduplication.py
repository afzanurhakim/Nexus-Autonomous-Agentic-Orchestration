import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger

# Note: In a production environment, you would use an Embedding Model 
# (like OpenAI's text-embedding-3-small) to get these vectors.
# For the demo, we use a vectorized representation of the task strings.

def get_embedding(text):
    """
    Placeholder for an Embedding API call.
    In production, this would call OpenAI or Gemini Embeddings.
    """
    # Simulate a 1536-dimension vector (standard for OpenAI)
    # This keeps the logic ready for the real API integration.
    return np.random.rand(1, 1536) 

def check_duplicate_task(new_task, existing_tasks, threshold=0.85):
    """
    The 'Semantic Filter' Skill.
    Calculates the Cosine Similarity between a new task and a list of existing tasks.
    """
    
    if not existing_tasks:
        logger.info("🕵️ Deduplication: No existing tasks found. Proceeding with creation.")
        return False

    logger.info(f"🕵️ Deduplication: Comparing '{new_task['title']}' against {len(existing_tasks)} board items...")

    # 1. Vectorize the new task
    new_vec = get_embedding(new_task['title'])
    
    # 2. Compare against the "Board History"
    for task in existing_tasks:
        existing_vec = get_embedding(task['title'])
        
        # 3. Calculate Cosine Similarity: (A . B) / (||A|| ||B||)
        similarity = cosine_similarity(new_vec, existing_vec)[0][0]
        
        if similarity > threshold:
            logger.warning(f"⚠️ Duplicate Detected! Similarity: {similarity:.2f}")
            logger.info(f"Match: '{new_task['title']}' ≈ '{task['title']}'")
            return True # Found a match, stop and report duplicate

    logger.success("✅ Deduplication: No significant overlap found. Task is unique.")
    return False

if __name__ == "__main__":
    # Test Logic
    new_item = {"title": "Update the Gree Brand Deck"}
    history = [{"title": "Revise Gree Campaign Slides"}]
    
    is_duplicate = check_duplicate_task(new_item, history)
    print(f"Is Duplicate: {is_duplicate}")