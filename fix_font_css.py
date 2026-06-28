with open('question_bank_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('st.markdown(f"""')
end = content.find('""", unsafe_allow_html=True)', start) + len('""", unsafe_allow_html=True)')

replacement = '''font_css = f"<style>@font-face {{ font-family: '方正小标宋简'; src: url('data:font/truetype;base64,{font_base64}') format('truetype'); font-weight: normal; font-style: normal; }} .fzxbs {{ font-family: '方正小标宋简', 'FZ XiaoBiaoSongJ', sans-serif !important; }}</style>"
        st.markdown(font_css, unsafe_allow_html=True)
        st.markdown("""
        <style>
        [data-testid="stSidebar"] div[data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            margin: 0 auto 4px auto !important;
        }
        [data-testid="stSidebar"] div[data-testid="stImage"] img {
            width: 72px !important;
            max-width: 72px !important;
            height: auto !important;
        }
        .sol-logo-link,
        .sol-logo-link:visited,
        .sol-logo-link:hover,
        .sol-logo-link:active {
            display: block !important;
            text-decoration: none !important;
            color: #58a6ff !important;
            cursor: pointer !important;
        }
        .sol-logo-link span,
        .sol-logo-link:visited span,
        .sol-logo-link:hover span,
        .sol-logo-link:active span {
            color: #58a6ff !important;
        }
        /* 隐藏侧边栏的规范说明菜单项 */
        [data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(9) {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)'''

new_content = content[:start] + replacement + content[end:]

with open('question_bank_app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Fixed successfully')
