# -*- coding: utf-8 -*-

import re
import json
import facebook
from access_token import TOKEN

graph = facebook.GraphAPI(TOKEN)

# URLが入っている投稿に関してはデータに入れない
url_regex = re.compile(r"[https?|ftp]://[A-Za-z0-9\-.]{0,62}?\.([A-Za-z0-9\-.]{1,255})/?[A-Za-z0-9.\-?=#%/]*")

# グループidからfeed_ids_listをロード
months = [month for month in range(4, 11)]                  # 4~10月のデータを対象にする (プロ野球のシーズン)
for i in range(len(months)):

    # load feed's ids
    with open('./crawling_data/entry_ids_' + str(months[i]) + '.list', 'r') as f_list:
        entry_ids = json.load(f_list)

    # comment内に返信しているcommentを取得
    with open('./crawling_data/conv_' + str(months[i]) + '.txt', 'w') as f:
        for entry_id in entry_ids:                                                              # グループ内のEntry ID
            response = graph.get_object(id=entry_id + '/comments', timeout=10)                  # Entry内のcommentsを取得
            for entry in response['data']:
                comment_id = str(entry['id'])
                response_comments = graph.get_object(id=comment_id + '/comments', timeout=10)   # 各commentに付随するcommentsを取得(response)
                if len(response_comments['data']) != 0:
                    print('+++ start of talk +++')
                    print(entry['message'])                                                     # responseを持っているcommentを表示
                    post = re.sub(r"(\n|\r\n)",  " ", entry['message'])
                    m_post = url_regex.search(post)
                    if m_post is None:
                        for comment in response_comments['data']:
                            print(comment['message'])                                           # commentに対するresponseを表示
                            cmnt = re.sub(r"(\n|\r\n)",  " ", comment['message'])
                            m_cmnt = url_regex.search(cmnt)
                            if m_cmnt is None:
                                f.write(post + '\t' + cmnt + '\n')
                                post = cmnt
                            else:
                                break
                    print('+++ end of talk +++')
                    print('')
            print('------------ end of entry ---------------')
