import numpy as np
import json

# 1. Chunking text
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# 2. Cosine similarity / top-k retrieval
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Test 3: top_k_docs
def top_k_docs(query_embedding, docs, k=3):
    scored = []

    for doc in docs:
        score = cosine_similarity(query_embedding, doc["embedding"])
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:k]]


# Test 4. Validate LLM JSON output
def parse_llm_response(response_text, required_fields):

    # required_fields = ["event_type", "severity", "summary"]

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
    # except Exception as e:
        return {"valid": False, "error": f"{e}"}


    for field in required_fields:
        if field not in data:
            return {"valid": False, "error": f"Missing field: {field}"}

    return {"valid": True, "data": data}



if __name__ == "__main__":

    testing = 4

    if testing ==1:
        # Test 1: chunk_text
        text = "abcdefghijklmnopqrstuvwxyz" * 5
        chunks = chunk_text(text, chunk_size=20, overlap=5)

        print("Chunks:")
        for c in chunks:
            print(c)

        assert len(chunks) > 1
        assert chunks[0][-5:] == chunks[1][:5]
        print("chunk_text test passed")

    if testing ==2:
        # Test 2: cosine_similarity
        a = [1, 0, 0]
        b = [1, 0, 0]
        c = [0, 1, 0]

        assert cosine_similarity(a, b) == 1.0
        assert cosine_similarity(a, c) == 0.0
        print("cosine_similarity test passed")

    if testing ==3:
        # Test 3: top_k_docs
        query_embedding = [1, 0, 0]

        docs = [
            {"id": 1, "text": "AI document", "embedding": [1, 0, 0]},
            {"id": 2, "text": "Finance document", "embedding": [0.8, 0.2, 0]},
            {"id": 3, "text": "Cooking document", "embedding": [0, 1, 0]},
        ]

        top_docs = top_k_docs(query_embedding, docs, k=2)

        assert len(top_docs) == 2
        assert top_docs[0]["id"] == 1
        print("top_k_docs test passed")


    if testing ==4:

        # Test 4: valid LLM JSON
    
        required_fields = ["event_type", "severity", "summary"]


        valid_response = """
        {
            "event_type": "market_notice",
            "severity": "high",
            "summary": "ERCOT issued an operating condition notice."
        }
        """

        result = parse_llm_response(valid_response, required_fields)

        assert result["valid"] is True
        assert result["data"]["event_type"] == "market_notice"
        assert result["data"]["severity"] == "high"
        assert result["data"]["summary"] == "ERCOT issued an operating condition notice."

        print("valid JSON test passed")

        # Test 2: invalid JSON
        invalid_response = """
        {
            "event_type": "market_notice",
            "severity": "high",
            "summary": "Missing closing brace"
        """

        result = parse_llm_response(invalid_response, required_fields)

        assert result["valid"] is False
        assert "Expecting" in result["error"] or "delimiter" in result["error"]

        print("invalid JSON test passed")

        # Test 3: missing required field
        missing_field_response = """
        {
            "event_type": "market_notice",
            "severity": "high"
        }
        """

        result = parse_llm_response(missing_field_response, required_fields)

        assert result["valid"] is False
        assert result["error"] == "Missing field: summary"

        print("missing field test passed")

        # Test 4: different schema
        required_fields_2 = ["answer", "confidence", "sources"]

        response_2 = """
        {
            "answer": "Kinesis is used for real-time streaming.",
            "confidence": 0.92,
            "sources": ["doc1", "doc2"]
        }
        """

        result = parse_llm_response(response_2, required_fields_2)

        assert result["valid"] is True
        assert result["data"]["answer"] == "Kinesis is used for real-time streaming."
        assert result["data"]["confidence"] == 0.92
        assert result["data"]["sources"] == ["doc1", "doc2"]

        print("different schema test passed")

        # Test 5: empty required fields
        result = parse_llm_response(valid_response, [])

        assert result["valid"] is True

        print("empty required fields test passed")

        print("\nAll tests passed successfully.")