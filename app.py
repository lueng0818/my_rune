import streamlit as st
import random
import time
import os
from PIL import Image

# --- 設定頁面 ---
st.set_page_config(
    page_title="北歐盧恩符文數位諮詢師",
    page_icon="🔮",
    layout="wide"
)

# --- 圖片路徑設定 ---
IMAGE_FOLDER = "images"

# --- 1. 完整盧恩符文資料庫 ---
runes_db = {
    "Fehu": {
        "name": "Fehu (財富)",
        "dates": "06/29-07/13",
        "file_name": "Fehu",
        "meaning_up": "豐盛、獲得、目標達成。辛苦奮鬥而得到的結果。",
        "meaning_rev": "損失、缺乏、需要保守。不適合新計畫。",
        "health": "注意飲食過量、肥胖、消化系統。",
        "career": "投資獲利、加薪機會、金融相關產業不錯。",
        "love": "感情豐富，異性緣佳。但也可能重視外在條件。",
        "element": "火土"
    },
    "Uruz": {
        "name": "Uruz (權力/野牛)",
        "dates": "07/14-07/28",
        "file_name": "Uruz",
        "meaning_up": "強大的改變力量、耐力、勇氣。自然發生的改變。",
        "meaning_rev": "意志力薄弱、錯失良機、缺乏行動力。",
        "health": "精力充沛，但需注意肌肉過勞或男性攝護腺問題。",
        "career": "適合創業或承擔重任，會有晉升機會。",
        "love": "關係中的主導權，或需要改變相處模式。",
        "element": "土"
    },
    "Thurisaz": {
        "name": "Thurisaz (雷神之槌)",
        "dates": "07/29-08/12",
        "file_name": "Thurisaz",
        "meaning_up": "突破困難、保護、好運。但容易固執己見。",
        "meaning_rev": "固執招致失敗、自我阻礙、好運用盡。",
        "health": "注意心血管、肝臟負擔、過度疲勞。",
        "career": "高科技、競爭激烈的環境。需收斂脾氣。",
        "love": "大男人/大女人主義，衝突較多，激情但不持久。",
        "element": "火"
    },
    "Ansuz": {
        "name": "Ansuz (奧丁/智慧)",
        "dates": "08/13-08/28",
        "file_name": "Ansuz",
        "meaning_up": "智慧、溝通、長輩貴人。接收訊息。",
        "meaning_rev": "溝通誤會、謊言、被誤導。長輩緣差。",
        "health": "喉嚨、口腔、牙齒、語言能力。",
        "career": "適合教學、顧問、演講。聽取長官建議。",
        "love": "心靈交流、知性伴侶。喜歡能溝通的對象。",
        "element": "空氣"
    },
    "Raidho": {
        "name": "Raidho (使徒/馬車)",
        "dates": "08/29-09/12",
        "file_name": "Raidho",
        "meaning_up": "旅行、移動、計畫順利進行。探索內心。",
        "meaning_rev": "行程延誤、計畫受阻、迷失方向。",
        "health": "腿部、關節、神經系統、交通意外。",
        "career": "適合運輸、旅遊、外派。協商的好時機。",
        "love": "共同成長、或指一段旅程中的邂逅。尋找中。",
        "element": "空氣"
    },
    "Kenaz": {
        "name": "Kenaz (烈火/火把)",
        "dates": "09/13-09/27",
        "file_name": "Kenaz",
        "meaning_up": "創造力爆發、靈感、熱情。黑暗中的光芒。",
        "meaning_rev": "靈感枯竭、分手、結束、失去熱忱。",
        "health": "發炎、發燒、視力問題、氣虛。",
        "career": "藝術、設計、創意工作大吉。新專案啟動。",
        "love": "熱戀期、或是容易因為太過熱情而灼傷對方。",
        "element": "空氣"
    },
    "Gebo": {
        "name": "Gebo (奉獻/禮物)",
        "dates": "09/28-10/12",
        "file_name": "Gebo",
        "meaning_up": "夥伴關係、施與受的平衡、合約承諾。",
        "meaning_rev": "此牌無逆位（若視為負面則指關係失衡、過度依賴）。",
        "health": "身體代謝平衡、中毒或過敏。",
        "career": "合夥順利、簽約好時機、團隊合作。",
        "love": "天作之合、互相尊重的關係、承諾。",
        "element": "空"
    },
    "Wunjo": {
        "name": "Wunjo (歡愉/喜悅)",
        "dates": "10/13-10/27",
        "file_name": "Wunjo",
        "meaning_up": "快樂、慶祝、成功、和諧。願望達成。",
        "meaning_rev": "悲傷、失望、延遲、不快樂。",
        "health": "呼吸系統、憂鬱、心理健康。",
        "career": "工作氣氛佳、獲得獎賞、娛樂產業。",
        "love": "幸福美滿、單戀者有機會成功。",
        "element": "火"
    },
    "Hagalaz": {
        "name": "Hagalaz (颶風/冰雹)",
        "dates": "10/28-11/12",
        "file_name": "Hagalaz",
        "meaning_up": "突發的變故、不可抗力、破壞後的重建。",
        "meaning_rev": "此牌無逆位（代表延遲、限制、需忍耐）。",
        "health": "意外受傷、急症、感冒病毒。",
        "career": "裁員、重組、不可控的外部風險。",
        "love": "關係破裂、外力介入、多角關係。",
        "element": "水"
    },
    "Nauthiz": {
        "name": "Nauthiz (需求/束縛)",
        "dates": "11/13-11/27",
        "file_name": "Nauthiz",
        "meaning_up": "限制、困境、需要耐心。面對內在匱乏。",
        "meaning_rev": "錯誤的決定、被慾望控制、失敗。",
        "health": "慢性病、營養不良、抵抗力差。",
        "career": "資源不足、壓力大、需等待時機。",
        "love": "單相思、苦戀、依賴性強的關係。",
        "element": "火"
    },
    "Isa": {
        "name": "Isa (冰雪/凍結)",
        "dates": "11/28-12/12",
        "file_name": "Isa",
        "meaning_up": "暫停、冷靜、孤獨、等待。不宜行動。",
        "meaning_rev": "此牌無逆位（若視為融化，則指僵局緩解）。",
        "health": "冷感冒、凍傷、血液循環不良、憂鬱。",
        "career": "專案停擺、遭到冷凍、無進展。",
        "love": "冷戰、感情降溫、單身狀態。",
        "element": "水"
    },
    "Jera": {
        "name": "Jera (豐收/收穫)",
        "dates": "12/13-12/27",
        "file_name": "Jera",
        "meaning_up": "循序漸進、耕耘收穫、因果循環。時間到了自然成。",
        "meaning_rev": "此牌無逆位（負面指時機未到、急功近利）。",
        "health": "消化系統、腸胃、長期調養見效。",
        "career": "長期投資獲利、升遷、農業或法律相關。",
        "love": "細水長流、日久生情、穩定的關係。",
        "element": "土"
    },
    "Eihwaz": {
        "name": "Eihwaz (紫杉/世界樹)",
        "dates": "12/28-01/12",
        "file_name": "Eihwaz",
        "meaning_up": "防禦、轉化、重生。經歷考驗後的成長。",
        "meaning_rev": "混亂、死亡（象徵性）、恐懼、改變。",
        "health": "脊椎、骨骼、牙齒、老化問題。",
        "career": "適合醫療、殯葬、保險、公務員。",
        "love": "糾纏不清的緣分、需要轉化的關係。",
        "element": "土風火水"
    },
    "Perthro": {
        "name": "Perthro (聖杯/秘密)",
        "dates": "01/13-01/27",
        "file_name": "Perthro",
        "meaning_up": "秘密、揭示、意外的好運、直覺。",
        "meaning_rev": "秘密洩漏、失望、不愉快的驚喜。",
        "health": "婦科、生殖系統、遺傳問題。",
        "career": "博弈、神秘學、需要運氣的行業。",
        "love": "神秘戀情、性吸引力強、意外懷孕。",
        "element": "水"
    },
    "Algiz": {
        "name": "Algiz (保護/麋鹿)",
        "dates": "01/28-02/12",
        "file_name": "Algiz",
        "meaning_up": "強力的保護、連結高層智慧、直覺敏銳。",
        "meaning_rev": "防禦漏洞、被欺騙、危險。",
        "health": "免疫系統、頭痛、神經衰弱。",
        "career": "保全、資安、環保、照顧型工作。",
        "love": "柏拉圖式戀愛、守護對方、信任。",
        "element": "風"
    },
    "Sowilo": {
        "name": "Sowilo (太陽/勝利)",
        "dates": "02/13-02/26",
        "file_name": "Sowilo",
        "meaning_up": "成功、榮耀、清晰的目標、活力。",
        "meaning_rev": "此牌無逆位（負面指過度自信、燒壞）。",
        "health": "心臟、曬傷、發炎、精力過剩。",
        "career": "領導者、公眾人物、目標達成。",
        "love": "熱情如火、公開的戀情、自我中心。",
        "element": "風"
    },
    "Tiwaz": {
        "name": "Tiwaz (戰神/正義)",
        "dates": "02/27-03/13",
        "file_name": "Tiwaz",
        "meaning_up": "正義、勝利、勇氣、犧牲小我。",
        "meaning_rev": "失敗、不公、缺乏鬥志、過度犧牲。",
        "health": "手部受傷、發炎、手術。",
        "career": "法律、軍警、競爭勝利、高階主管。",
        "love": "理性的愛、對方條件好但較強勢。",
        "element": "空氣"
    },
    "Berkano": {
        "name": "Berkano (生育/樺樹)",
        "dates": "03/14-03/30",
        "file_name": "Berkano",
        "meaning_up": "誕生、成長、滋養、新的開始。",
        "meaning_rev": "成長停滯、家庭問題、流產（象徵性）。",
        "health": "懷孕、乳房、女性特有疾病。",
        "career": "幼教、園藝、策劃新專案。",
        "love": "結婚生子、母愛、照顧型伴侶。",
        "element": "風"
    },
    "Ehwaz": {
        "name": "Ehwaz (神駒/馬)",
        "dates": "03/31-04/13",
        "file_name": "Ehwaz",
        "meaning_up": "移動、進步、合作夥伴、信任。",
        "meaning_rev": "停滯、拆夥、背叛、迷路。",
        "health": "背部、腿部、過勞。",
        "career": "交通運輸、貿易、團隊合作順利。",
        "love": "靈魂伴侶、雙向奔赴、同居或搬家。",
        "element": "土"
    },
    "Mannaz": {
        "name": "Mannaz (人類/自我)",
        "dates": "04/14-04/28",
        "file_name": "Mannaz",
        "meaning_up": "群體、合作、人際關係、自我認知。",
        "meaning_rev": "孤立、被排擠、失去自我、敵人是自己。",
        "health": "心理疾病、精神官能症。",
        "career": "人力資源、公關、社群經營。",
        "love": "像朋友般的戀人、理智的關係。",
        "element": "空氣"
    },
    "Laguz": {
        "name": "Laguz (水/直覺)",
        "dates": "04/29-05/13",
        "file_name": "Laguz",
        "meaning_up": "順流而下、直覺、潛意識、情感流動。",
        "meaning_rev": "溺水（被情緒淹沒）、恐懼、逃避現實。",
        "health": "腎臟、膀胱、水腫、血液循環。",
        "career": "藝術、心理學、身心靈產業。",
        "love": "浪漫多情、依靠直覺、易受傷。",
        "element": "水"
    },
    "Ingwaz": {
        "name": "Ingwaz (天使/豐饒)",
        "dates": "05/14-05/28",
        "file_name": "Ingwaz",
        "meaning_up": "完成、圓滿、內在成長、醞釀。",
        "meaning_rev": "此牌無逆位（負面指難產、未完成）。",
        "health": "生殖系統、基因、遺傳。",
        "career": "專案結案、儲備實力、農業。",
        "love": "成熟的愛、家庭和諧、懷孕。",
        "element": "大地/水"
    },
    "Othala": {
        "name": "Othala (家庭/繼承)",
        "dates": "05/29-06/13",
        "file_name": "Othala",
        "meaning_up": "家庭、遺產、傳統、根基、安全感。",
        "meaning_rev": "家庭紛爭、失去財產、無家可歸。",
        "health": "遺傳病、老人病。",
        "career": "家族企業、房地產、在家工作。",
        "love": "重視家庭背景、老夫老妻、傳統婚姻。",
        "element": "大地"
    },
    "Dagaz": {
        "name": "Dagaz (黎明/突破)",
        "dates": "06/14-06/28",
        "file_name": "Dagaz",
        "meaning_up": "覺醒、突破、黎明、轉折點。否極泰來。",
        "meaning_rev": "此牌無逆位（負面指看不見希望、拒絕改變）。",
        "health": "神經系統、眼睛、焦慮。",
        "career": "重大突破、轉職、創業。",
        "love": "關係的重大轉變、覺醒。",
        "element": "風火"
    },
    "Wyrd": {
        "name": "Wyrd (空牌/命運)",
        "dates": "無",
        "file_name": "Wyrd",
        "meaning_up": "未知的命運、業力、交給上天安排。",
        "meaning_rev": "同正位。問題此刻無解，需等待。",
        "health": "罕見疾病、因果病、無法診斷。",
        "career": "不可預測的變化、命運的轉折。",
        "love": "命中注定（緣起或緣滅）、無法強求。",
        "element": "虛空"
    }
}

rune_keys = list(runes_db.keys())

# --- 輔助函式 ---
def get_rune_image(file_base_name, is_reversed):
    """讀取圖片，若逆位則旋轉 180 度"""
    possible_extensions = [".png", ".jpg", ".jpeg"]
    image_path = None
    for ext in possible_extensions:
        temp_path = os.path.join(IMAGE_FOLDER, file_base_name + ext)
        if os.path.exists(temp_path):
            image_path = temp_path
            break
    if image_path:
        try:
            img = Image.open(image_path)
            if is_reversed:
                img = img.rotate(180)
            return img
        except:
            return None
    return None

def draw_runes(count):
    """抽牌邏輯"""
    drawn_keys = random.sample(rune_keys, count)
    results = []
    for key in drawn_keys:
        # 部分對稱牌無逆位，但為了系統統一性，仍隨機產生狀態，顯示時再處理
        is_reversed = random.choice([True, False])
        results.append({"key": key, "reversed": is_reversed})
    return results

def get_rune_meaning(rune_key, theme, is_reversed):
    """根據主題和正逆位獲取解釋"""
    rune_info = runes_db[rune_key]
    
    # 判斷對稱牌 (無逆位)
    symmetrical_runes = ["Gebo", "Isa", "Ingwaz", "Dagaz", "Sowilo", "Hagalaz", "Jera", "Eihwaz", "Wyrd"]
    is_symmetrical = rune_key in symmetrical_runes
    
    # 1. 先抓主題特有的解釋
    if theme == "事業 (Career)" and "career" in rune_info:
        base_text = rune_info["career"]
    elif theme == "愛情 (Love)" and "love" in rune_info:
        base_text = rune_info["love"]
    elif theme == "健康 (Health)" and "health" in rune_info:
        base_text = rune_info["health"]
    else:
        # 一般/綜合主題，或該主題無特定解釋，回歸正逆位核心意義
        base_text = rune_info["meaning_up"] if not is_reversed or is_symmetrical else rune_info["meaning_rev"]

    # 2. 如果是特定主題，還是要加上正逆位的狀態描述 (若是對稱牌則不需要)
    status_prefix = ""
    if not is_symmetrical and theme != "一般指引 (General)":
        if is_reversed:
            status_prefix = "【逆位阻礙】"
        else:
            status_prefix = "【正位順利】"
            
    return f"{status_prefix} {base_text}"

def generate_overall_interpretation(results, spread_type, theme):
    """生成綜合解讀報告"""
    synthesis = ""
    
    # 判斷結果牌是否為空牌
    last_rune = results[-1]
    is_last_wyrd = last_rune['key'] == "Wyrd"
    
    if spread_type == "單張指引 (1 Rune)":
        synthesis = f"這是針對您目前關於**{theme}**問題最直接的指引。請以此符文的核心能量作為當下的冥想主題。"
    
    elif spread_type == "三張牌：時間流 (Time Flow)":
        synthesis = f"從過去的 **{runes_db[results[0]['key']]['name']}** 影響至今，"
        synthesis += f"您目前正處於 **{runes_db[results[1]['key']]['name']}** 的能量狀態。"
        synthesis += f"若依照此趨勢，未來將走向 **{runes_db[results[2]['key']]['name']}**。"
        if is_last_wyrd:
            synthesis += "\n\n⚠️ **特別提示**：結果位置出現了空牌，代表未來變數極大，目前尚未定論，請聽從直覺行事。"

    elif spread_type == "三張牌：行動建議 (Action)":
        synthesis = f"您的核心問題在於 **{runes_db[results[0]['key']]['name']}**。"
        synthesis += f"盧恩建議您採取 **{runes_db[results[1]['key']]['name']}** 的行動或態度。"
        synthesis += f"如此一來，預期結果將會是 **{runes_db[results[2]['key']]['name']}**。"

    elif spread_type == "五張牌：全方位解析 (Holistic)":
        synthesis = f"針對**{theme}**的深度解析：\n"
        synthesis += f"過去的成因是 **{runes_db[results[0]['key']]['name']}**，導致了現在 **{runes_db[results[1]['key']]['name']}** 的局面。\n"
        synthesis += f"面對 **{runes_db[results[4]['key']]['name']}** 這個挑戰，"
        synthesis += f"奧丁的忠告是運用 **{runes_db[results[3]['key']]['name']}** 的智慧來應對。\n"
        synthesis += f"最終將導向 **{runes_db[results[2]['key']]['name']}** 的未來。"
    
    return synthesis

def display_card_html(rune_data, position, theme):
    """顯示卡片的 HTML 組件"""
    rune_key = rune_data['key']
    is_reversed = rune_data['reversed']
    rune_info = runes_db[rune_key]
    
    # 處理圖片
    symmetrical_runes = ["Gebo", "Isa", "Ingwaz", "Dagaz", "Sowilo", "Hagalaz", "Jera", "Eihwaz", "Wyrd"]
    is_symmetrical = rune_key in symmetrical_runes
    
    img = get_rune_image(rune_info['file_name'], False if is_symmetrical else is_reversed)
    
    # 獲取解釋文字
    meaning_text = get_rune_meaning(rune_key, theme, is_reversed)
    
    # 狀態文字
    status_text = "正位"
    if is_symmetrical:
        status_text = "正位 (無逆位)"
    elif is_reversed:
        status_text = "逆位"

    # Streamlit 顯示
    with st.container():
        st.markdown(f"#### {position}")
        if img:
            st.image(img, width=120, caption=f"{rune_info['name']} ({status_text})")
        else:
            st.markdown(f"## {rune_info['name']}")
            st.caption(status_text)
        
        st.info(meaning_text)

# --- 側邊欄：諮詢設定 ---
st.sidebar.title("🌿 諮詢設定")

# 1. 選擇主題
selected_theme = st.sidebar.selectbox(
    "1. 請問您想諮詢的主題是？",
    ["一般指引 (General)", "事業 (Career)", "愛情 (Love)", "健康 (Health)"]
)

# 2. 選擇牌陣 (張數)
selected_spread = st.sidebar.selectbox(
    "2. 請選擇使用的牌陣：",
    [
        "單張指引 (1 Rune)",
        "三張牌：時間流 (Time Flow)",
        "三張牌：行動建議 (Action)",
        "五張牌：全方位解析 (Holistic)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **操作提示**：\n先在心中默念問題，並誦讀右側的奧丁禱詞，準備好後點擊「誠心抽牌」。")

# --- 主畫面 ---

st.title("🌲 北歐盧恩符文數位諮詢")
st.markdown(f"### 當前主題：{selected_theme}")

# 顯示禱詞 (儀式感)
with st.expander("📜 點擊查看奧丁禱詞 (請在抽牌前默念)", expanded=True):
    st.markdown("> **「全能且有智慧的奧丁神，盧恩的主人，**")
    st.markdown("> **請指引我的手及意念，讓我得到真理。」**")

# 抽牌按鈕
if st.button("🔮 誠心抽牌", type="primary"):
    
    # 決定抽牌張數
    num_draw = 1
    labels = []
    
    if "單張" in selected_spread:
        num_draw = 1
        labels = ["指引盧恩"]
    elif "時間流" in selected_spread:
        num_draw = 3
        labels = ["1. 過去 (Past)", "2. 現在 (Present)", "3. 未來 (Future)"]
    elif "行動建議" in selected_spread:
        num_draw = 3
        labels = ["1. 問題核心 (Issue)", "2. 採取作法 (Action)", "3. 預期結果 (Result)"]
    elif "五張牌" in selected_spread:
        num_draw = 5
        labels = ["1. 過去 (Past)", "2. 現在 (Present)", "3. 未來 (Future)", "4. 幫助/建議 (Advice)", "5. 問題/挑戰 (Challenge)"]

    # 動畫效果
    with st.spinner("連結奧丁的智慧中..."):
        time.sleep(1.5)
        results = draw_runes(num_draw)
        
        st.divider()
        
        # --- 顯示牌卡 ---
        if num_draw == 1:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                display_card_html(results[0], labels[0], selected_theme)
                
        elif num_draw == 3:
            cols = st.columns(3)
            for i in range(3):
                with cols[i]:
                    display_card_html(results[i], labels[i], selected_theme)
                    
        elif num_draw == 5:
            # 上排 3 張
            cols_top = st.columns(3)
            for i in range(3):
                with cols_top[i]:
                    display_card_html(results[i], labels[i], selected_theme)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 下排 2 張 (建議與挑戰)
            cols_bottom = st.columns(2)
            with cols_bottom[0]:
                display_card_html(results[3], labels[3], selected_theme)
            with cols_bottom[1]:
                display_card_html(results[4], labels[4], selected_theme)

        # --- 整體解讀報告 ---
        st.divider()
        st.subheader("📝 整體解讀報告")
        
        overall_text = generate_overall_interpretation(results, selected_spread, selected_theme)
        
        st.success(overall_text)
        
        # 根據講義的額外提示
        if selected_theme == "健康 (Health)":
            st.warning("⚠️ 免責聲明：盧恩諮詢僅供參考，身體不適請務必尋求專業醫療協助。")
        
        if num_draw == 5:
            st.info("💡 **進階解讀技巧**：請觀察第4張「建議牌」如何能夠解決第5張「挑戰牌」的困難，這通常是改變未來的關鍵鑰匙。")

st.markdown("---")
st.markdown("<center>資料來源：北歐盧恩符文諮詢師整合班講義 & 初階證書課程講義</center>", unsafe_allow_html=True)
