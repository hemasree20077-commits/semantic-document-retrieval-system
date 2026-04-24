from nltk.tokenize import sent_tokenize
import re


# -----------------------------
# 🔥 Clean text properly (robust)
# -----------------------------
def clean_text(text):

    if not text:
        return ""

    # remove newlines & tabs
    text = text.replace("\n", " ").replace("\t", " ")

    # remove extra spaces
    text = " ".join(text.split())

    # 🔥 fix broken words (e.g., "c are" → "care")
    text = re.sub(r"\b([a-zA-Z])\s+([a-zA-Z]{2,})\b", r"\1\2", text)

    return text.strip()


# -----------------------------
# 🔥 Chunking function
# -----------------------------
def chunk_documents(documents, max_words=150):

    chunks = []

    for doc in documents:

        text = doc.get("text", "")

        # 🚫 skip empty pages
        if not text or not text.strip():
            continue

        sentences = sent_tokenize(text)

        # 🚫 skip if no sentences
        if not sentences:
            continue

        current_chunk = []
        current_word_count = 0

        for sentence in sentences:

            sentence = clean_text(sentence)

            if not sentence:
                continue

            word_count = len(sentence.split())

            # ✅ add to current chunk
            if current_word_count + word_count <= max_words:
                current_chunk.append(sentence)
                current_word_count += word_count

            else:
                chunk_text = clean_text(" ".join(current_chunk))

                if chunk_text:
                    chunks.append({
                        "book_hash": doc["book_hash"],
                        "book_name": doc["book_name"],
                        "page_number": doc["page_number"],
                        "chunk_text": chunk_text
                    })

                # start new chunk
                current_chunk = [sentence]
                current_word_count = word_count

        # ✅ add last chunk
        if current_chunk:
            chunk_text = clean_text(" ".join(current_chunk))

            if chunk_text:
                chunks.append({
                    "book_hash": doc["book_hash"],
                    "book_name": doc["book_name"],
                    "page_number": doc["page_number"],
                    "chunk_text": chunk_text
                })

    return chunks