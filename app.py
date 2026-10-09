import streamlit as st

from rag_engine import RAGEngine

from scaffold import (
    SCAFFOLDING,
    clamp_level
)

from config import (
    APP_TITLE,
    SOURCE_NAME,
    SOURCE_URL
)


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide"
)


st.title(
    "🎓 AI Tutor lập trình"
)

st.caption(
    "RAG + Progressive Scaffolding"
)


# -------------------------
# API KEY
# -------------------------

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)

if not api_key:

    st.error(
        "Chưa cấu hình GEMINI_API_KEY."
    )

    st.stop()


# -------------------------
# ENGINE
# -------------------------

@st.cache_resource
def load_engine():

    return RAGEngine(
        api_key
    )


engine = load_engine()


# -------------------------
# SESSION STATE
# -------------------------

if "level" not in st.session_state:
    st.session_state.level = 1

if "messages" not in st.session_state:
    st.session_state.messages = []

if "solved" not in st.session_state:
    st.session_state.solved = 0


# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.header(
        "Progressive Scaffolding"
    )

    st.metric(
        "Mức hỗ trợ",
        f"{st.session_state.level}/5"
    )

    if st.button(
        "🆘 Em vẫn chưa hiểu",
        use_container_width=True
    ):

        st.session_state.level = (
            clamp_level(
                st.session_state.level + 1
            )
        )

        st.rerun()


    if st.button(
        "💡 Cho thêm gợi ý",
        use_container_width=True
    ):

        st.session_state.level = (
            clamp_level(
                st.session_state.level + 1
            )
        )

        st.rerun()


    if st.button(
        "✅ Em làm được rồi",
        use_container_width=True
    ):

        st.session_state.solved += 1

        st.session_state.level = (
            clamp_level(
                st.session_state.level - 2
            )
        )

        st.rerun()


    st.divider()

    st.write(
        f"Đã hoàn thành: "
        f"{st.session_state.solved}"
    )

    st.markdown(
        f"""
### Học liệu

[{SOURCE_NAME}]({SOURCE_URL})
"""
    )


# -------------------------
# SHOW CHAT
# -------------------------

for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# -------------------------
# CHAT INPUT
# -------------------------

question = st.chat_input(
    "Nhập câu hỏi hoặc dán code..."
)


if question:

    st.session_state.messages.append({
        "role":
        "user",

        "content":
        question
    })


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # ---------------------
    # RETRIEVAL
    # ---------------------

    retrieved = engine.retrieve(
        question
    )


    context = ""

    for i, item in enumerate(
        retrieved,
        start=1
    ):

        context += f"""

[NGUỒN {i}]

{item["text"]}

"""


    # ---------------------
    # PROMPT
    # ---------------------

    level = (
        st.session_state.level
    )


    prompt = f"""
Bạn là AI Tutor hỗ trợ
sinh viên giáo dục nghề nghiệp
học lập trình.

MỤC TIÊU:

- Không làm bài thay sinh viên.
- Giúp sinh viên tự suy nghĩ.
- Ưu tiên học liệu giảng viên.
- Trả lời bằng tiếng Việt.
- Giữ thuật ngữ lập trình bằng English.
- Trả lời ngắn, rõ và thực hành được.

QUY TẮC RAG:

Chỉ khẳng định kiến thức môn học
dựa trên các đoạn học liệu dưới đây.

Nếu học liệu chưa đủ,
hãy nói:

"Học liệu hiện tại chưa đủ
để kết luận phần này."

Khi sử dụng thông tin,
hãy ghi:

[Nguồn 1]
[Nguồn 2]
...

=====================

HỌC LIỆU

{context}

=====================

PROGRESSIVE SCAFFOLDING

Mức hiện tại:

{level}/5

{SCAFFOLDING[level]}

=====================

CÂU HỎI SINH VIÊN

{question}

=====================

Trả lời theo cấu trúc:

### Nhận định

### Gợi ý

### Việc em làm tiếp theo

### Tự kiểm tra
"""


    # ---------------------
    # GENERATION
    # ---------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Đang tìm học liệu..."
        ):

            answer = engine.generate(
                prompt
            )


        st.markdown(
            answer
        )


        with st.expander(
            "🔎 Xem học liệu RAG"
        ):

            for i, item in enumerate(
                retrieved,
                start=1
            ):

                st.markdown(
                    f"""
**Nguồn {i}**

Similarity:
`{item["score"]:.3f}`

{item["text"][:800]}
"""
                )


    st.session_state.messages.append({
        "role":
        "assistant",

        "content":
        answer
    })
