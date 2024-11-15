"""
Generate answer based on user query
"""

import os
import spacy_universal_sentence_encoder

from openai import OpenAI
from scrape import read_faq_json

JSON_FILE_PATH = "../data/faq.json"
LOG_FILE_PATH = "../data/logs.txt"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

faq_content = read_faq_json()
nlp = spacy_universal_sentence_encoder.load_model('en_use_lg')

def find_best_matching(query):
    """
    Given a query, return a list of similarity scores between the query and FAQ titles
    :return: List of tuples containing FAQ and similarity score, sorted by score in descending order
    """
    query = query.strip()
    if len(query) == 0:
        return []
    query_doc = nlp(query)
    top_matches = []
    for faq in faq_content:
        title_doc = nlp(faq['Title'])
        if len(faq['Title']) == 0:
            continue
        score = query_doc.similarity(title_doc)
        top_matches.append((faq, score))
    top_matches.sort(key=lambda x: x[1], reverse=True)
    return top_matches

def generate_answer(query):
    top_matches = find_best_matching(query)
    no_match_reply = "Sorry, I couldn't find any relevant FAQ to your query. Please visit our FAQ page https://support.highrise.game/en/ for more information."
    if len(top_matches) == 0:
        write_logs(query, no_match_reply)
        return no_match_reply
    prompt = f"""
        You are a helpful assistant that answers questions based on several provided FAQ examples. Find the example that are most relevant to user's question and respond by summarizing the content.
        Please reply in the following format:
        \"\"\"
        <Your summarized response here>
        Find out more, please visit the link: <Link to the FAQ>
        \"\"\"
        If none of the given examples are related, say {no_match_reply}
    """
    for (faq, _) in top_matches[:3]:
        prompt += f"""
        **Example Question:** {faq['Title']}
        **Example Answer:** {faq['Content']}
        **Example Link:** {faq['Link']}
        """
    prompt += f"\nUser Question: {query}"
    # print(prompt)
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=True
    )
    return response

def write_logs(query, response):
    """
    Write the query and response to a log file
    :param query: User query
    :param response: Chatbot response
    """
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"Query: {query} Response: {response}")
