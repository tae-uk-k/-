import urllib3
import json
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import ElectraTokenizer, ElectraModel


class TextSimilarityChecker:
    def check_paraphrase(self,sentence1, sentence2):
        open_api_url = "http://aiopen.etri.re.kr:8000/ParaphraseQA"
        access_key = "d7da6e7b-90c7-4ca4-ace2-e7cc1e082506"  
        request_json = {
            "argument": {
                "sentence1": sentence1,
                "sentence2": sentence2
        }
    }

   
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            open_api_url,
            headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": access_key},
            body=json.dumps(request_json)
        )

        #print("[responseCode] " + str(response.status))
        #print("[responBody]")
        #print(str(response.data, "utf-8"))

    
        result_json = json.loads(response.data.decode('utf-8'))
        print(result_json)
        return result_json["return_object"]["result"] != "not paraphrase"
    
    def calculate_similarity(self,sentence1, sentence2):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        embedding1 = model.encode(sentence1, convert_to_tensor=True)
        embedding2 = model.encode(sentence2, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(embedding1, embedding2)[0].item()

        return similarity*100
    def calculate_similarity_tfidf(self,sentence1, sentence2):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([sentence1, sentence2])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity * 100
    def get_koelectra_embedding(selff,sentence):
        model_name = "monologg/koelectra-base-v3-discriminator"
        tokenizer = ElectraTokenizer.from_pretrained(model_name)
        model = ElectraModel.from_pretrained(model_name)

        input_ids = tokenizer(sentence, return_tensors="pt")["input_ids"]
        with torch.no_grad():
            output = model(input_ids)
    
        embedding = output.last_hidden_state[:, 0, :]

        return embedding * 100
    def get_embedding(self,model_name, sentence):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        input_ids = tokenizer(sentence, return_tensors="pt")["input_ids"]
        with torch.no_grad():
            output = model(input_ids)
        
        embedding = output.last_hidden_state[:, 0, :]

        return embedding

    def calculate_cosine_similarity(self,embedding1, embedding2):
        # PyTorch의 코사인 유사도 계산
        similarity = cosine_similarity(embedding1, embedding2)
        return similarity[0][0]

similarity_checker = TextSimilarityChecker()
# 예제 문장
sentence1 = "안녕하세요, 한국어 언어 모델 테스트입니다."
sentence2 = "안녕하세요, 모델 테스트 중입니다."


# 코사인 유사도 계산
is_paraphrase = similarity_checker.check_paraphrase(sentence1, sentence2)
print(f"두 문장이 패러프레이즈인가요? {is_paraphrase}")
if is_paraphrase:
    
    koelectra_embedding1 = similarity_checker.get_koelectra_embedding(sentence1)
    koelectra_embedding2 = similarity_checker.get_koelectra_embedding(sentence2)

    similarity_sentence_transformers = similarity_checker.calculate_similarity(sentence1, sentence2)
    similarity_tfidf = similarity_checker.calculate_similarity_tfidf(sentence1, sentence2)
    similarity_koelectra = similarity_checker.calculate_cosine_similarity(koelectra_embedding1, koelectra_embedding2)*100

# # 결과 출력
    print(f"Sentence Transformers 유사도: {similarity_sentence_transformers:.4f}")
    print(f"TF-IDF 유사도: {similarity_tfidf:.4f}")
    print(f"KoELECTRA 유사도: {similarity_koelectra:.4f}")
    print(f"최종 유사도: {(similarity_sentence_transformers+similarity_tfidf+similarity_koelectra)/3:.4f}")