import streamlit as st

st.set_page_config(
    page_title='To-Do-List',
    page_icon='✅',
    layout='centered'
)

st.title('📝나의 할 일 목록'
         , anchor='title-section'
         , help='anchor 존재'
)
st.write('간단하고 효율적인 할 일 관리를 시작해 보세요!')

st.header('📖사용법')

use_app = '''
    1. **할 일 추가**: 텍스트 입력 후 '추가하기' 버튼 클릭
    2. **완료 표시** : 체크박스를 클릭하여 완료 표시
    3. **할 일 삭제**: 🗑️버튼으로 개별 삭제
    4. **일괄 관리** : 완료된 할 일만 삭제하거나 전체 삭제
'''
st.write(use_app)

def custom_warning(message):
    st.markdown(f"""
    <div style="
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-left: 4px solid #ff6b35;
        background-color: var(--warning-bg, #fff3cd);
        border-radius: 0.25rem;
        color: var(--warning-text, #856404);
        font-size: 14px;
        line-height: 1.5;
    ">
         {message}
    </div>
    <style>
        @media (prefers-color-scheme: dark) {{
            :root {{
                --warning-bg: #3d2914;
                --warning-text: #ffcc02;
            }}
        }}
        [data-theme="dark"] {{
            --warning-bg: #3d2914;
            --warning-text: #ffcc02;
        }}
    </style>
    """, unsafe_allow_html=True)

def custom_success(message):
    st.markdown(f"""
    <div style="
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        background-color: var(--success-bg, #d4edda);
        border-radius: 0.25rem;
        color: var(--success-text, #155724);
        font-size: 14px;
        line-height: 1.5;
    ">
         {message}
    </div>
    <style>
        @media (prefers-color-scheme: dark) {{
            :root {{
                --success-bg: #1e3a24;
                --success-text: #4caf50;
            }}
        }}
        [data-theme="dark"] {{
            --success-bg: #1e3a24;
            --success-text: #4caf50;
        }}
    </style>
    """, unsafe_allow_html=True)

def custom_info(message):
    st.markdown(f"""
    <div style="
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
        background-color: var(--info-bg, #d1ecf1);
        border-radius: 0.25rem;
        color: var(--info-text, #0c5460);
        font-size: 14px;
        line-height: 1.5;
    ">
         {message}
    </div>
    <style>
        @media (prefers-color-scheme: dark) {{
            :root {{
                --info-bg: #0d2a3a;
                --info-text: #5bc0de;
            }}
        }}
        [data-theme="dark"] {{
            --info-bg: #0d2a3a;
            --info-text: #5bc0de;
        }}
    </style>
    """, unsafe_allow_html=True)

def custom_error(message):
    st.markdown(f"""
    <div style="
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        background-color: var(--error-bg, #f8d7da);
        border-radius: 0.25rem;
        color: var(--error-text, #721c24);
        font-size: 14px;
        line-height: 1.5;
    ">
         {message}
    </div>
    <style>
        @media (prefers-color-scheme: dark) {{
            :root {{
                --error-bg: #3a1a1d;
                --error-text: #f44336;
            }}
        }}
        [data-theme="dark"] {{
            --error-bg: #3a1a1d;
            --error-text: #f44336;
        }}
    </style>
    """, unsafe_allow_html=True)

st.subheader('➕새로운 할 일 추가')

new_todo = st.text_input('할 일을 입력하세요 : ',
                        placeholder='예 : 퇴근하기, 집가기, 드러눕기')

submitted = st.button('추가하기')

if 'todos' not in st.session_state:
    st.session_state.todos = [] #st.session_state에 todos가 없으면 저장

if submitted:
    if new_todo.strip(): #빈 문자열이 아닌지 판단하는 함수
        st.session_state.todos.append({
            'task':new_todo.strip(),
            'completed':False
        })
        custom_success(f"☑️: '{new_todo}'가 추가되었습니다.")
    else:
        custom_warning('⚠️할 일을 입력해주세요.')

st.divider()

st.subheader('📚할 일 목록')

# st.write(st.session_state.todos)

if st.session_state.todos:
    for i in reversed(range(len(st.session_state.todos))):
        todo=st.session_state.todos[i]

        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

        with col1:
            completed=st.checkbox('',
                value=todo['completed'],
                key=f'check_{i}',
                help='완료 시 체크')
            
            if completed!=todo['completed']:
                st.session_state.todos[i]['completed']=completed
                st.rerun() #rerun 이후에는 출력 안됨

        with col2:
            if completed:
                st.markdown(f"~~_{todo['task']}_~~",help='완료된 할 일')
            else:
                st.write(todo['task'])

        with col3:
            if st.button('🗑️', key=f'delete_{i}', help='삭제'):
                st.session_state.todos.pop(i)
                custom_success('삭제되었습니다.')
                st.rerun()

        if i>=0:
            st.markdown('---')
else:
    custom_info('🥹아직 할 일이 없습니다. 새로운 할 일을 추가해 보세요!')

if st.session_state.todos:
    total_todos = len(st.session_state.todos)
    completed_todos = 0
    for i in st.session_state.todos:
        if i['completed']:
            completed_todos += 1
    remaining_todos=total_todos-completed_todos
    if total_todos>0:
        completion_rate = (completed_todos/total_todos*100)
    else:
        completion_rate=0
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button('🗑️전체 삭제', type='secondary'):
            st.session_state.todos=[]
            custom_success('모든 할 일이 삭제되었습니다.')
            st.rerun()

    with col2:
        if completed_todos>0:
            if st.button(f'✅완료된 할 일 {completed_todos}개 삭제'
                         , type='secondary'):
                todo_list=[]
                for i in st.session_state.todos:
                    if not i['completed']:
                        todo_list.append(i)
                st.session_state.todos=todo_list
                custom_success(f'완료된 할 일이 {completed_todos}개 삭제되었습니다.')
                st.rerun()
        
    st.subheader('📊통계')

    def display_state(title, value, delta=None, value_color=None):
        delta_str=''
        if delta is not None:
            if delta > 0:
                delta_str=f'(+{delta})'
            elif delta<0:
                delta_str=f'({delta})'
            else:
                delta_str=''
        
        if value_color is None:
            value_color='var(--text-color, #262730)'

        st.markdown(f"""
            <div style="
                padding: 1rem; 
                background-color: var(--stat-bg, #f0f2f6); 
                border: 1px solid var(--stat-border, transparent);
                border-radius: 10px; 
                text-align: center;
                box-shadow: var(--stat-shadow, 0 1px 3px rgba(0,0,0,0.1));
            ">
                <div style="
                    font-size: 18px; 
                    font-weight: bold; 
                    color: var(--title-color, #262730);
                    margin-bottom: 0.5rem;
                ">{title}</div>
                <div style="
                    font-size: 32px; 
                    font-weight: bold; 
                    color: {value_color};
                ">{value}{delta_str}</div>
            </div>
            <style>
                /* 라이트모드 기본값 */
                :root {{
                    --stat-bg: #f0f2f6;
                    --stat-border: transparent;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    --title-color: #262730;
                    --text-color: #262730;
                }}
                
                /* 다크모드 스타일 */
                @media (prefers-color-scheme: dark) {{
                    :root {{
                        --stat-bg: #2b2b35;
                        --stat-border: #404040;
                        --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                        --title-color: #fafafa;
                        --text-color: #fafafa;
                    }}
                }}
                
                /* Streamlit 다크모드 */
                [data-theme="dark"] {{
                    --stat-bg: #2b2b35;
                    --stat-border: #404040;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    --title-color: #fafafa;
                    --text-color: #fafafa;
                }}
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_state('전체 할 일', total_todos)
    with col2:
        display_state('완료된 할 일', completed_todos
                      ,delta=completed_todos
                      ,value_color='#4CAF50')
    with col3:
        display_state('남은 할 일', remaining_todos
                      ,delta=-completed_todos
                      ,value_color='#f44336')

    if completion_rate == 100:
        custom_success('모든 할 일을 완료했습니다.')
    elif completion_rate >= 80:
        custom_info('할 일을 거의 다 완료했습니다.')
    elif completion_rate >= 50:
        custom_warning('할 일을 절반 이상 완료했습니다.')
    elif completion_rate == 0:
        custom_error('완료된 할 일이 없습니다.')
    else:
        custom_warning(f'진행률 : {completion_rate:.1f}% ({completed_todos}/{total_todos})')
# else:
#     custom_info('할 일을 추가해보세요!')

st.divider()

st.markdown('''
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    💡 팁: 통계를 통해 완료된 할 일과 남은 할 일 개수 확인 가능
</div>
''', unsafe_allow_html=True)