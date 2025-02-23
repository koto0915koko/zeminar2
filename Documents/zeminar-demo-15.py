import flet as ft
import csv

# ファイル埋め込み
opponents_plofile=[
    ["wakana","女性",21],
    ["rio","男性",45],
    ["eri","男性",24],
    ["takai","男性",33],
    ["mao","女性",40],
]

opponents_answers_personalities = [
    ["はい", "いいえ", "どちらでもない", "はい", "アウトドア"],
    ["いいえ", "はい", "はい", "はい", "インドア"],
    ["いいえ", "はい", "いいえ", "いいえ", "どちらでもない"],
    ["いいえ", "いいえ", "はい", "いいえ", "アウトドア"],
    ["どちらでもない", "はい", "いいえ", "いいえ", "インドア"]
]

    
opponents_answers_personalities_friend = [
    ["はい", "いいえ", "はい", "大人数", "インドア派"],
    ["はい", "いいえ", "いいえ", "少人数", "アウトドア派"],
    ["はい", "はい", "どちらでもない", "大人数", "インドア派"],
    ["いいえ", "はい", "はい", "どちらでもいい", "インドア派"],
    ["どちらでもない", "はい", "はい", "少人数", "どちらでもない"]
]


opponents_answers_hobbies = [
    ["映画鑑賞", "料理"],
    ["旅行", "ゲーム"],
    ["アニメ", "ゲーム"],
    ["読書", "旅行"],
    ["映画鑑賞", "アニメ"]
]


# プレイヤーの入力情報を管理
player_data={
    "player_profile":{},
    "player_requirements":{},
    "player_personalities_lover":[],
    "player_personalities_friend":[],
    "player_hobbies":[],
}
player_requirements=[] #答えた条件を格納
player_personalities_lover=[] 
player_personalities_friend=[] #答えた性格診断結果を格納
player_hobbies=[] #答えた趣味に関する回答を格納


#マッチング
def matching(player_requirements,player_personalities_lover,player_personalities_friend,player_hobbies):
    each_count_requirements=[] #条件
    each_count_personalities_lover=[] #性格診断
    each_count_personalities_friend=[]
    each_count_hobbies=[] #趣味

#ポイントの合計を格納する
    each_count_all=[]
    
    for i in range(len(opponents_plofile)):
        count_a=0
        count_b=0
        count_c=0
        
        #求める条件
        if player_requirements["player_opp_gender"]==opponents_plofile[i][1]:
            count_a+=1
        if int(player_requirements["player_opp_age"]) <= int(opponents_plofile[i][2]) <= int(player_requirements["player_opp_age"])+10:
            count_a+=1
        each_count_requirements.append(count_a)
        
        #性格の一致(恋人)
        if len(player_data["player_personalities_lover"]) > 1 :
            if player_personalities_lover[0] == opponents_answers_personalities[i][0]:
                count_b+=1
            if player_personalities_lover[1] == opponents_answers_personalities[i][1]:
                count_b+=1
            each_count_personalities_lover.append(count_b)
        
        #性格の一致（友人）
        if len(player_data["player_personalities_friend"]) > 1:
            if player_personalities_friend[0] == opponents_answers_personalities_friend[i][0]:
                count_b+=1
            if player_personalities_friend[1] == opponents_answers_personalities_friend[i][1]:
                count_b+=1
            each_count_personalities_friend.append(count_b)   
            
        #趣味の一致
        for player_hobby in player_hobbies:
            if player_hobby in opponents_answers_hobbies[i]:
                count_c+=1
            each_count_hobbies.append(count_c)
        
        #ポイントの合計
        each_count_all.append(count_a+count_b+count_c)
    #点数が高い順にインデックスをソート
    sorted_indices=sorted(range(len(each_count_all)),key=lambda i:each_count_all[i],reverse=True)
    
    #上位結果
    results=[]
    if len(player_personalities_lover) > 1:
        for i in range(min(5,len(sorted_indices))): #上位五人まで
            index=sorted_indices[i]
            results.append({
                "name":opponents_plofile[index][0],
                "requirement_score":int((each_count_requirements[index]/2)*100),
                "personality_lover_score":int((each_count_personalities_lover[index]/2)*100),
                "hobby_score":int((each_count_hobbies[index]/2)*100),
                "total_score": int((each_count_all[index]/6)*100),
            })
    if len(player_personalities_friend) > 1:
        for i in range(min(5,len(sorted_indices))): #上位五人まで
            index=sorted_indices[i]
            results.append({
                "name":opponents_plofile[index][0],
                "requirement_score":int((each_count_requirements[index]/2)*100),
                "personality_friend_score":int((each_count_personalities_friend[index]/2)*100),
                "hobby_score":int((each_count_hobbies[index]/2)*100),
                "total_score": int((each_count_all[index]/6)*100),
            })
    return results


def main(page: ft.Page):
    def route_change(route):
        if page.route == "/":
            page.views.clear()
            page.views.append(main_view(page))
        elif page.route == "/second":
            page.views.clear()
            page.views.append(second(page))
        elif page.route == "/lover_questions":
            page.views.clear()
            page.views.append(lover_questions(page))
        elif page.route == "/friend_questions":
            page.views.clear()
            page.views.append(friend_questions(page))
        elif page.route == "/hobbies":
            page.views.clear()
            page.views.append(hobbies(page))
        elif page.route == "/third":
            page.views.clear()
            page.views.append(third(page))
            
            
        page.update()

    page.on_route_change = route_change
    page.go("/")

def main_view(page: ft.Page):
    name = ft.TextField(label="お名前")
    sex = ft.Dropdown(
        label="性別",
        options=[
            ft.dropdown.Option("男性"),
            ft.dropdown.Option("女性"),
        ],
    )
    age = ft.TextField(label="年齢")

    def on_enter(e):
        if name.value and sex.value and age.value:
            player_data["player_profile"] = {"name": name.value, "sex": sex.value, "age": age.value}
            page.go("/second")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("すべての項目を入力してください。"))
            page.snack_bar.open = True
            page.update()

    enter_button = ft.ElevatedButton("決定", on_click=on_enter)

    return ft.View(
        "/",
        [
            ft.Text("マッチングアプリだよ！"),
            name,
            sex,
            age,
            enter_button,
        ],
    )

def second(page: ft.Page):
    player_purpose = ft.Dropdown(
        label="友人か恋人、どちらが欲しいですか？",
        options=[
            ft.dropdown.Option("友人"),
            ft.dropdown.Option("恋人"),
        ],
    )
    player_opp_gender = ft.Dropdown(
        label="相手の希望する性別を教えてね！",
        options=[
            ft.dropdown.Option("男性"),
            ft.dropdown.Option("女性"),
        ],
    )
    player_opp_age = ft.Dropdown(
        label="相手の希望する年齢を教えてね！",
        options=[
            ft.dropdown.Option("20"),
            ft.dropdown.Option("30"),
            ft.dropdown.Option("40"),
        ],
    )

    def on_purpose_select(e):
        if player_purpose.value == "恋人":
            player_data["player_requirements"]={"player_purpose": player_purpose.value, "player_opp_gender": player_opp_gender.value, "player_opp_age": player_opp_age.value}
            print(player_requirements)
            page.go("/lover_questions")
        elif player_purpose.value == "友人":
            player_data["player_requirements"]={"player_purpose": player_purpose.value, "player_opp_gender": player_opp_gender.value, "player_opp_age": player_opp_age.value}
            print(player_requirements)
            page.go("/friend_questions")

    next_button = ft.ElevatedButton("次へ", on_click=on_purpose_select)

    return ft.View(
        "/second",
        [
            ft.Text("相手に求める条件を入力しよう！"),
            player_purpose,
            player_opp_gender,
            player_opp_age,
            next_button,
        ],
    )

#性格診断（恋人）
def lover_questions(page: ft.Page):
    l_q1 = ft.Dropdown(
        label="結婚について真剣に考えていますか？",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    l_q2 = ft.Dropdown(
        label="恋人が異性の友人と二人きりで遊ぶのはアリですか？",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    l_q3=ft.Dropdown(
        label="記念日を大事にしたいですか？",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    l_q4=ft.Dropdown(
        label="恋人の夢を応援するのが大切だと思いますか？",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    l_q5=ft.Dropdown(
        label="インドア派ですか？アウトドア派ですか？",
        options=[
            ft.dropdown.Option("インドア"),
            ft.dropdown.Option("アウトドア"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    def on_submit(e):
        player_data["player_personalities_lover"]=[l_q1.value,l_q2.value,l_q3.value,l_q4.value,l_q5.value]
        page.go("/hobbies")
    submit_button = ft.ElevatedButton("送信", on_click=on_submit)

    return ft.View(
        "/lover_questions",
        [
            ft.Text("性格診断（恋人編）"),
            l_q1,
            l_q2,
            l_q3,
            l_q4,
            l_q5,
            submit_button,
        ],
    )


#性格診断（友人編）

def friend_questions(page: ft.Page):
    f_q1 = ft.Dropdown(
        label="時間にルーズなタイプだ",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    f_q2 = ft.Dropdown(
        label="つい長電話してしまう",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    f_q3=ft.Dropdown(
        label="恋人よりも友達を優先しますか？",
        options=[
            ft.dropdown.Option("はい"),
            ft.dropdown.Option("いいえ"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    f_q4=ft.Dropdown(
        label="少人数で遊ぶのが好きですか？大人数で遊ぶのが好きですか？",
        options=[
            ft.dropdown.Option("大人数"),
            ft.dropdown.Option("少人数"),
            ft.dropdown.Option("どちらでもいい"),
        ],
    )    
    
    f_q5=ft.Dropdown(
        label="インドア派ですか？アウトドア派ですか？",
        options=[
            ft.dropdown.Option("インドア派"),
            ft.dropdown.Option("アウトドア派"),
            ft.dropdown.Option("どちらでもない"),
        ],
    )
    
    def on_submit(e):
        player_data["player_personalities_friend"]=[f_q1.value, f_q2.value,f_q3.value,f_q4.value,f_q5.value]
        page.go("/hobbies")
    submit2_button = ft.ElevatedButton("送信", on_click=on_submit)

    return ft.View(
        "/friend_questions",
        [
            ft.Text("性格診断（友人編）"),
            f_q1,
            f_q2,
            f_q3,
            f_q4,
            f_q5,
            submit2_button,
        ],
    )



#趣味診断（友人編）
def hobbies(page:ft.Page):
    label="以下からあなたの趣味を２つ選択してください",
    hobbies=[
        {"name":"読書","selected":False},
        {"name":"ゲーム","selected":False},
        {"name":"料理","selected":False},
        {"name":"旅行","selected":False},
        {"name":"映画鑑賞","selected":False},
        {"name":"アニメ","selected":False},
    ]
    
    result=ft.Text("何も選ばれていません")
    
    def update_selected(e):
        #クリックされたチェックボックスの選択状態を更新
        for hobby in hobbies:
            if hobby["name"]==e.control.label:
                hobby["selected"] =e.control.value
        #更新された選択状態を表示
        selected_hobbies=[hobby["name"] for hobby in hobbies if hobby["selected"]]
        result.value=f"選択された趣味:{','.join(selected_hobbies)}" if selected_hobbies else "何も選ばれていません"
        page.update()
        
    def on_submit(e):
        #選択された趣味を収集
        selected_hobbies=[hobby["name"] for hobby in hobbies if hobby ["selected"]]
        player_data["player_hobbies"]=selected_hobbies
        page.go("/third")
    submit4_button = ft.ElevatedButton("送信", on_click=on_submit)
    
    #チェックボックスを作成
    checkboxes =[
        ft.Checkbox(label=hobby["name"],value=hobby["selected"],on_change=update_selected)
        for hobby in hobbies
    ]
    
    return ft.View(
        "/hobbies",
        [
            ft.Text("趣味診断"),
            *checkboxes,
            result,
            submit4_button,
        ],
    )

def third(page: ft.Page):
    results = matching(
        player_data["player_requirements"],
        player_data["player_personalities_lover"],
        player_data["player_personalities_friend"],
        player_data["player_hobbies"],
    )
    views = [ft.Text("マッチング結果:")]
    if len(player_data["player_personalities_lover"]) > 1:
        for i, result in enumerate(results):
            views.append(ft.Text(f"{i+1}位: {result['name']}"))
            views.append(ft.Text(f"条件一致: {result['requirement_score']}%"))
            views.append(ft.Text(f"性格一致: {result['personality_lover_score']}%"))
            views.append(ft.Text(f"趣味一致: {result['hobby_score']}%"))
            views.append(ft.Text(f"総合一致度: {result['total_score']}%"))
            views.append(ft.Text(""))
            
    if len(player_data["player_personalities_friend"]) > 1:
        for i, result in enumerate(results):
            views.append(ft.Text(f"{i+1}位: {result['name']}"))
            views.append(ft.Text(f"条件一致: {result['requirement_score']}%"))
            views.append(ft.Text(f"性格一致: {result['personality_friend_score']}%"))
            views.append(ft.Text(f"趣味一致: {result['hobby_score']}%"))
            views.append(ft.Text(f"総合一致度: {result['total_score']}%"))
            views.append(ft.Text(""))

    return ft.View(
        "/third",
        views,
    )

ft.app(target=main, view=ft.WEB_BROWSER)

