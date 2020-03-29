import json
from simpletransformers.question_answering import QuestionAnsweringModel
import os
import logging
import re
from word2number import w2n

class GetCases:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        transformers_logger = logging.getLogger("transformers")
        transformers_logger.setLevel(logging.WARNING)   
        self.model = QuestionAnsweringModel('distilbert', 'outputs/', args={'reprocess_input_data': True, 'overwrite_output_dir': True, 'fp16': False}, use_cuda=False)

    def train_model(self):
        train_data = []
        with open('C:/Users/NathanGrant/Downloads/rona/rona/training_data.json') as f:
            train_data = json.load(f)
        self.model.train_model(train_data)
    def predict(self, news, county):
        to_predict = []
        county = re.sub(", [A-Z]+"," county", county).lower()
        temp = {'context': news,'qas': [{'question': 'Total deaths in ' + county, 'id': '0'}]}
        to_predict.append(temp)
        pre = self.model.predict(to_predict)
        cases = [prediction['answer'] for prediction in pre]
        print(cases)
        if len(cases) > 0:
            for i in range(len(cases)):
                try:
                    cases[i] = int(cases[i])
                except:
                    cases[i] = w2n.word_to_num(cases[i])
        else:
            return 0
        return cases

    def evaluate_model(self, data):
        result, text = self.model.eval_model(data)
        print(text)
        print(result)