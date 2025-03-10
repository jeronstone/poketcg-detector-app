#import torch
import open_clip
import cv2
from sentence_transformers import util
from PIL import Image
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import easyocr

class Similarity():
    
    def __init__(self, imgproc=False):
        # if imgproc:
        #     self.device = "cuda" if torch.cuda.is_available() else "cpu"
        #     m, _, pp = open_clip.create_model_and_transforms('ViT-B-16-plus-240', pretrained="laion400m_e32")
        #     self.model = m
        #     self.preprocess = pp
        #     self.model.to(self.device)
        self.reader = easyocr.Reader(['en'])

    '''
    def imageEncoder(self, img):
        img1 = Image.fromarray(img).convert('RGB')
        img1 = self.preprocess(img1).unsqueeze(0).to(self.device)
        img1 = self.model.encode_image(img1)
        return img1

    def generateScore(self, image1, image2):
        test_img = cv2.imread(image1, cv2.IMREAD_UNCHANGED)
        data_img = cv2.imread(image2, cv2.IMREAD_UNCHANGED)
        #st = time.time()
        img1 = self.imageEncoder(test_img)
        #print(f'Image 1 Encode Time: {time.time() - st}')
        st = time.time()
        img2 = self.imageEncoder(data_img)
        #print(f'Image 2 Encode Time: {time.time() - st}')
        #st = time.time()
        cos_scores = util.pytorch_cos_sim(img1, img2)
        score = round(float(cos_scores[0][0])*100, 2)
        #print(f'Similarity Time: {time.time() - st}')
        return score

    def tensor_similarity(self, t1, t2):
        #st = time.time()
        cos_scores = util.pytorch_cos_sim(t1, t2)
        score = round(float(cos_scores[0][0])*100, 2)
        #print(f'Similarity Time: {time.time() - st}')
        return score
    '''
    def get_text(self, img):
        result = self.reader.readtext(img, detail=0)
        result = " ".join([word for line in result for word in line.split()])
        return result

    def vectorize_text(self, texts):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)
        return vectorizer, tfidf_matrix

    def vector_transform(self, v, text):
        return v.transform([text])

    def vector_cosine_similarity(self, v1, v2):
        similarity_score = cosine_similarity(v1, v2)
        return similarity_score


if __name__ == '__main__':
    #image1 = '/home/jestone/tcgdetector/card_imgs_desc/Abra_43_Common_base1-43.jpg'
    image2 = '/home/jestone/tcgdetector/card_imgs_desc/Zweilous_61_Uncommon_sm4-61.jpg'
    image1 = '/home/jestone/tcgdetector/card_imgs_desc/Zweilous_73_Uncommon_xy4-73.jpg'

    sim = Similarity()
    st = time.time()
    print(f"similarity Score: ", round(sim.generateScore(image1, image2), 2))
    print(f'Total Time: {time.time()-st}')