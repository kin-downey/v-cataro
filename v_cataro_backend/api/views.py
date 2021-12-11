from os import stat_result
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import requests
import urllib
import re
from kotodama import kotodama
from janome.tokenizer import Tokenizer
from pymagnitude import Magnitude
import time

import sys

from rest_framework.utils import json
sys.path.append('lib.bs4')
from bs4 import BeautifulSoup

import random

'''========================================================
日本語->EUC-JPにエンコードし，格フレーム取得用のURLを生成する
========================================================'''
def generate_url_case(search_word: str) -> str:
    quote = urllib.parse.quote(search_word, encoding="euc-jp")
    url = 'https://lotus.kuee.kyoto-u.ac.jp/cf-search/?text={}&noun=on&ex_print_uniqth_user=20&ex_print_freqth_user=2&.cgifields=csv&.cgifields=noun'.format(quote)

    return url


'''============================================
格フレームを取得する
============================================'''
def get_case_frame(key_word: str):
    t = Tokenizer()
    # 取得した共起後の先頭のものの格フレームを検索（BeautifulSoupによる）
    url = generate_url_case(key_word)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    # 結果がtrタグ内に存在する（多数）
    tr_s = soup.find_all('tr')
    case_frame = {}

    try:
        # 検索結果の上位1つを取得
        for i in range(1,2):
            # 取得した結果を成形
            tr_split = re.split('[/:\d+]', tr_s[i].text)
            # 動詞を取得
            verb = tr_split[0]
            token = str(t.tokenize(verb).__next__()).split(',')[0]
            flag = token.split('\t')[1]

            # 取得したものが名詞だった場合，名詞＋したを格納する（卒業＋した）
            if flag == "名詞":
                case_frame["noun"] = verb + "した"

            # 格を取得(ヲ格など...)
            case = tr_split[3]
            print("case: ", case)

            # ansに動詞が登録されていなかったら
            if verb not in case_frame.keys():
                # ansに格を格納
                case_frame["verb"] = verb
                case_frame["case"] = case
        # ["noun": "名詞", "verb": "動詞", "case": "格"]という形を返す
        return case_frame
    except:
        case_frame["verb"] = "なし"
        case_frame["case"] = "なし"
        return case_frame


# 値を文字列型で受け取っているのは，JSONがそういう形式だから
@csrf_exempt
def check_emotion(request) -> JsonResponse:
    if request.method == 'POST':
        emotions = JSONParser().parse(request)
    
    key_word = emotions.pop('key_word')
    
    # 辞書の値を浮動小数に変換
    for key in emotions.keys():
        emotions[key] = float(emotions[key])

    # 感情のリストの中で，最大の値をもつ感情を取得する
    max_emotion = max(emotions, key=emotions.get)

    # 以下，条件分岐によって相槌を変化させる
    if max_emotion == "neutral":
        # 相槌を複数定義
        aiduti_list = ["なるほど。", "そうなんですね。", "うん。うん。", "ああー！"]
        # ランダムに相槌を選択
        aiduti = random.choice(aiduti_list)
        response ={
            "sentence": aiduti + key_word + "ですね？",
            'emotion': "neutral"
        }
        return JsonResponse(response, status=201)

    elif max_emotion == "happy":
        aiduti_list = ["それは良いですね！", "いいなー!", "素敵ですね！"]
        aiduti = random.choice(aiduti_list)
        response = {
            "sentence": aiduti + key_word + 'ですか！',
            "emotion": "happy"
        }
        return JsonResponse(response, status=201)
    
    elif max_emotion == "sad":
        subjects = ['どのようなスポーツは好きですか？', '思い出に残っている旅行について教えてください', 'あなたの人生で最大の失敗はなんですか？', 'あなたの人生で最大の成功はなんですか？', '世界中の人に声が届くなら，なにを言いたいですか？']
        new_subject = random.choice(subjects)
        aiduti = "そうだったのですね。話題を変えましょう"

        response = {
            "sentence": aiduti,
            "emotion": "sad",
            "subject": new_subject
        }
        return JsonResponse(response, status=201)

    elif max_emotion == "angry":
        subjects = ['どのようなスポーツは好きですか？', '思い出に残っている旅行について教えてください', 'あなたの人生で最大の失敗はなんですか？', 'あなたの人生で最大の成功はなんですか？', '世界中の人に声が届くなら，なにを言いたいですか？']
        new_subject = random.choice(subjects)
        aiduti = "それは，ひどいですね！話題を変えましょう"
        response = {
            "sentence": aiduti,
            "emotion": "angry",
            "subject": new_subject
        }
        return JsonResponse(response, status=201)

    elif max_emotion == "fearful":
        # 相槌を複数定義
        aiduti_list = ["なるほど", "そうなんですね", "うん．うん", "ああー！"]
        # ランダムに相槌を選択
        aiduti = random.choice(aiduti_list)
        response ={
            "sentence": aiduti + key_word + "ですね？",
            "emotion": "fearful"
        }
        return JsonResponse(response, status=201)
    
    elif max_emotion == "disgusted":
        # 相槌を複数定義
        aiduti_list = ["なるほど", "そうなんですね", "うん．うん", "ああー！"]
        # ランダムに相槌を選択
        aiduti = random.choice(aiduti_list)
        response ={
            "sentence": aiduti + key_word + "ですね？",
            "emotion": "disgusted"
        }
        return JsonResponse(response, status=201)
    
    elif max_emotion == "surprised":
        aiduti_list = ["それは驚きです!", "わあ！", "びっくりです！"]
        aiduti = random.choice(aiduti_list)
        response = {
            "sentence": aiduti + key_word + "ですか！",
            "emotion": "surprised"
        }
    
        
        return JsonResponse(response, status=201)
 
    return JsonResponse(emotions, status=201)


'''============================================
メインとなる関数(最終的にここで応答を返す)
============================================'''
@csrf_exempt
def generate_response(request) -> JsonResponse:
    # フロントからの単語のリストを受け取る
    start = time.time()
    if request.method == 'POST':
        response = JSONParser().parse(request)
    # 単語の抽出を行う
    temp = []

    # print("emotions: ", response['neutral'] + '\n' + response['happy'] + '\n'  + response['sad'] + '\n' + response['angry'] + '\n' + response['surprised'] + '\n' + response['fearful'] + '\n' + response['disgusted'])
    for index, word in enumerate(response['word']):
        temp.append(word)
        print(f"word_{index} :", word)
    
    # chiVeデータのPATH
    model_path = "/run/backend/chive-1.2-mc5.magnitude"
    
    # モデルの読み込み
    wv = Magnitude(model_path)
    
    # 類似度上位1件を取得
    match = wv.most_similar(positive=temp, topn=1)
    
    # 単語を抜き出す（元の形式がタプルであるため）
    key_word = match[0][0]
    print("key_word :", key_word)
    
    # 得た共起後に対して格フレームを取得
    case_frame = get_case_frame(key_word)
    print("case_frame: ", case_frame)
    # 格フレームから疑問文を生成
    # 格フレームが名詞だった場合，名詞＋したを過去形に格納
    if "noun" in case_frame.keys():
        past_verb = case_frame["noun"]
    # 格フレームの動詞を過去形に変換
    # 格と結びつける
    if case_frame["verb"] == "なし" and case_frame["case"] == "なし":
        return JsonResponse({"sentence": "それは，どんなものですか？よろしければ，教えていただけますか？"})
    else:
        change = {"ヲ格": "を", "ニ格": "に", "ヘ格": "へ", "ガ格": "が", "ト格": "と", "デ格": "で", "ノ格": "の", "カラ格": "から"}
        if "noun" in case_frame.keys():
            ans = key_word + change[case_frame["case"]] + case_frame["noun"] + "のですか？"
            response = {"sentence": ans}
            print("response: ", response)
            return JsonResponse(response, status=201)
        else:
            try:
                ans = key_word + change[case_frame["case"]] + kotodama.transformVerb(case_frame["verb"], {"過去"}) + "のですか？"
                # 応答を返す
                print(ans)
                response = {"sentence": ans}
                print("response: ", response)
                end = time.time()
                print("total_time: ", end - start)
                return JsonResponse(response, status=201)
            except:
                return JsonResponse({"sentence": "それは，どんなものですか？よろしければ，教えていただけますか？"})