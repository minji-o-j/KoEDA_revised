from koeda import AEDA
import random

SPACE_TOKEN = "\u241F"


def replace_space(text: str) -> str:
    return text.replace(" ", SPACE_TOKEN)


def revert_space(text: list) -> str:
    clean = " ".join("".join(text).replace(SPACE_TOKEN, " ").split()).strip()
    return clean

class Fixed_AEDA(AEDA):
    def _aeda(self, data: str, p: float) -> str:
        if p is None:
            p = self.ratio

        split_words = self.morpheme_analyzer.morphs(replace_space(data)) # '\u241F'를 포함하여 토크나이징
        words = self.morpheme_analyzer.morphs(data)

        # 몇번째 토큰이 '\u241F'인지 찾기
        space_indices = [] # space token index 저장 
        token_indices = [] # space를 제외한 token의 index 저장

        for i, word in enumerate(split_words):  # split_words 내에서
            if word == SPACE_TOKEN:             # i번째 원소가 SPACE_TOKEN이면 append
                space_indices.append(i)
            else:                               # space 아닌 token append
                token_indices.append(i)


        new_words = []
        q = random.randint(1, int(p * len(words) + 1))  # 1~ ((원본 문장 토큰 개수) * p + 1) 중 랜덤으로 정수 선택
        qs = random.sample(token_indices, q)            # 0 ~ len(split_words) -1 까지의 숫자 중 q개의 숫자를 중복 없이 랜덤으로 선택
        
        for j, word in enumerate(split_words):
            if j in qs:                                 # j가 랜덤 선택된 숫자 목록에 있으면
                new_words.append(SPACE_TOKEN)           # SPACE TOKEN이 new_words에 들어감
                new_words.append(                       # random punctuation이 new_words에 들어감
                    self.punctuations[random.randint(0, len(self.punctuations) - 1)])
                new_words.append(SPACE_TOKEN)           # SPACE TOKEN이 new_words에 한번 더 들어감
                new_words.append(word)                  # 기존 word가 new_words에 들어감
            else:
                new_words.append(word)                  # j가 랜덤 선택된 숫자 목록에 없으면 기존 word만 new_words에 들어감


        augmented_sentences = revert_space(new_words)

        return augmented_sentences

        
