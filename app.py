elif menu == "🌟 五張：全方位解析":
    st.header("🌟 五張牌陣：全息觀點")
    st.markdown("適用於複雜問題的深度解析。")
    
    if st.button("🔮 誠心抽牌"):
        with st.spinner("展開神聖祭壇..."):
            time.sleep(2.5)
            results = draw_runes(5)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                display_rune_card(results[0], "1. 過去")
            with c2:
                display_rune_card(results[1], "2. 現在")
            with c3:
                display_rune_card(results[2], "3. 未來")
            
            st.markdown("---")
            
            c4, c5 = st.columns(2)
            with c4:
                display_rune_card(results[3], "4. 幫助/建議")
            with c5:
                display_rune_card(results[4], "5. 問題/挑戰")
            
            st.success("💡 **專家提示**：\n* 若「問題/挑戰」(5)出現正面盧恩：表示沒有太大困難。\n* 若「問題/挑戰」(5)出現空牌：無計可施，任由命運安排。")
