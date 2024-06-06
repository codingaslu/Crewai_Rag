from pinecone import Pinecone
from dotenv import load_dotenv
import os
from openai import OpenAI
import os


load_dotenv()

openai_api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

pc = Pinecone(api_key=os.environ["PINECONE_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX"])




#Embedding of the query
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding




json_file = index.describe_index_stats()
idg = json_file['total_vector_count']

def sort_strings_as_numbers(string_list):
  numeric_list = [int(s) for s in string_list]
  sorted_numeric_list = sorted(numeric_list)

  sorted_string_list = [str(num) for num in sorted_numeric_list]
  return sorted_string_list

# def fetch_text_from_response(id_val):
#   #index = pinecone.Index('healthexpertindexprod')
#   response = index.fetch(ids=[id_val], namespace="")
#   # return response["vectors"][id_val]["metadata"]["text"]
#   if "vectors" in response and id_val in response["vectors"]:
#     vector_data = response["vectors"][id_val]
#     if "metadata" in vector_data:
#       metadata = vector_data["metadata"]
#       if "text" in metadata:
#         return metadata["content"]
#   return None

def fetch_text_from_response(id_val):
    response = index.fetch(ids=[id_val], namespace="")
    
    if "vectors" in response and id_val in response["vectors"]:
        vector_data = response["vectors"][id_val]
        if "metadata" in vector_data:
            metadata = vector_data["metadata"]
            text = metadata.get("content", None)  # Assuming your text is stored with the key "text"
            return text, metadata
    return None, None

prev_next_count=0

json_file = index.describe_index_stats()
idg = json_file['total_vector_count']

def run_similarity_search(query):
    query_embedding = get_embedding(query)
    json_object = index.query(
        vector=query_embedding,
        top_k=3 )
    # return json_object
    # reordering = LongContextReorder()
    # json_object = reordering.transform_documents(json_object)
    ids_list = [match["id"] for match in json_object.get("matches", [])]
    # print(ids_list)
    new_list = []
    for ids in ids_list:
      new_list.append(ids)
    for idt in ids_list:
      id = int(idt)
      left = id-prev_next_count
      right = id+prev_next_count
      left = max(left, 0)
      right = min(right, idg)
      # print(left, right)
      # print(ids_list)
      for id_val in range(left, right+1):
        if str(id_val) not in new_list:
          new_list.append(str(id_val))
    # print(new_list)
    new_list = sort_strings_as_numbers(new_list)
    # return new_list
    context_list = []
    for id in new_list:
        res,metadata = fetch_text_from_response(id)
        # return res
        if res is not None:
            context_list.append(f"Document(page_content='{res}')")
    return context_list



def get_summary_chat(chat_history):
    prompt_engineering = f"""
        Chat History: {chat_history}

        Distill the above chat messages into a single summary message. Include as many specific details as you can
    """
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to summarize conversation."},
        {"role": "user", "content": prompt_engineering}
    ]
    )
    result = response.choices[0].message.content
    return result




    
import re

def remove_they_or_these_after(paragraph):
    sentences = re.split('(?<=[.!?])\\s*', paragraph)

    found = False

    new_sentences = []

    for sentence in sentences:
        if sentence.startswith("I'll need more details to provide a more tailored suggestion."):
            found = True
            new_sentences.append(sentence)
            continue

        if found and (sentence.lstrip().startswith('They ') or sentence.lstrip().startswith('These ')):
            found = False
            continue

        new_sentences.append(sentence)

    return ' '.join(new_sentences)