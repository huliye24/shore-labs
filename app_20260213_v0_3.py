# 备份文件：岸 app.py（含微信登录 + 茶室 + 真身/匿名人格）
# 日期：2026-02-13
# 版本号：v0.3

import streamlit as st
from pathlib import Path
from datetime import datetime
import random


def init_state():
    """初始化会话状态：真身、匿名分身和记录列表。"""
    if "real_name" not in st.session_state:
        st.session_state.real_name = "某一个在岸上的人"
    if "anonymous_id" not in st.session_state:
        st.session_state.anonymous_id = f"浪 #{random.randint(1000, 9999)}"
    if "square_posts" not in st.session_state:
        # 匿名广场的一些初始存在
        st.session_state.square_posts = [
            {
                "text": "今天没有什么特别的事，只是想说，我还在。",
                "time": "3 分钟前",
                "from_me": False,
                "mood": "平静",
                "echoes": [],
            },
            {
                "text": "下班路上一个人走路，风有点冷，但路灯很好看。",
                "time": "47 分钟前",
                "from_me": False,
                "mood": "路上",
                "echoes": [],
            },
            {
                "text": "失眠第 27 天。打开这个页面，提醒自己还活着。",
                "time": "昨晚",
                "from_me": False,
                "mood": "失眠",
                "echoes": [],
            },
        ]
    if "my_public_posts" not in st.session_state:
        st.session_state.my_public_posts = []
    if "my_private_posts" not in st.session_state:
        st.session_state.my_private_posts = []
    if "muted_words" not in st.session_state:
        st.session_state.muted_words = []
    # 登录状态（微信登录占位实现）
    if "is_wechat_logged_in" not in st.session_state:
        st.session_state.is_wechat_logged_in = False
    if "wechat_nickname" not in st.session_state:
        st.session_state.wechat_nickname = None
    # 茶室话题 & 刮刮乐评论
    if "tea_topic" not in st.session_state:
        st.session_state.tea_topic = {
            "id": "topic_1",
            "title": "今晚，有什么想对谁都不是说的吗？",
            "created_at": "今天",
        }
    if "tea_comments" not in st.session_state:
        # 预置几条刮刮乐评论
        st.session_state.tea_comments = [
            {
                "id": "c1",
                "author": "浪 #1024",
                "time": "10 分钟前",
                "text": "其实我没有那么坚强，只是习惯了说“还行”。",
                "reports": 0,
            },
            {
                "id": "c2",
                "author": "浪 #2048",
                "time": "1 小时前",
                "text": "谢谢你把这些话写出来，我也一直这样。",
                "reports": 0,
            },
        ]
    if "tea_scratched" not in st.session_state:
        # 记录当前用户已经刮开的评论 id 集合
        st.session_state.tea_scratched = set()
    # 真身与匿名分身的人格档案和动态
    if "real_profile" not in st.session_state:
        st.session_state.real_profile = {
            "intro": "写一点关于自己的话，可以长一点，也可以只是一句。",
            "avatar_emoji": "🌊",
        }
    if "anon_profile" not in st.session_state:
        st.session_state.anon_profile = {
            "intro": "这是浪的自我介绍，在这里你可以更放松。",
            "avatar_emoji": "🌫️",
        }
    if "real_posts" not in st.session_state:
        st.session_state.real_posts = []
    if "anon_posts" not in st.session_state:
        st.session_state.anon_posts = []


def render_global_style_and_header():
    """统一的样式、logo 和主标题。"""
    # 自定义样式：极简、浅灰背景
    st.markdown(
        """
        <style>
        body {
            background-color: #f3f3f3;
        }
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 720px;
        }
        .exist-card {
            background-color: #ffffff;
            border-radius: 18px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        }
        .exist-text {
            font-size: 0.95rem;
            color: #222222;
        }
        .exist-meta {
            font-size: 0.8rem;
            color: #999999;
            margin-top: 0.25rem;
        }
        .main-title {
            font-size: 1.4rem;
            font-weight: 500;
            letter-spacing: 0.06em;
        }
        .logo-img {
            display: block;
            margin: 0 auto 1.5rem auto;
            border-radius: 26px;
        }
        .scratch-card {
            position: relative;
            overflow: hidden;
            border-radius: 14px;
            background: #e0e0e0;
        }
        .scratch-cover {
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(
                45deg,
                #d0d0d0,
                #d0d0d0 4px,
                #e4e4e4 4px,
                #e4e4e4 8px
            );
            mix-blend-mode: multiply;
        }
        .scratch-blur {
            filter: blur(8px);
            opacity: 0.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 顶部 logo（使用相对 app.py 的稳定路径）
    logo_path = (
        Path(__file__)
        .parent
        / "assets"
        / "c__Users_Administrator_AppData_Roaming_Cursor_User_workspaceStorage_fad021f518cdfd0b5cd8028ecd4ddfc0_images_3bcc7230bb8c2597cd62ae7a65f622bb_720-f94de829-fe86-4ad9-86db-003f8cc70c6c.png"
    )
    if logo_path.exists():
        st.image(
            str(logo_path),
            use_column_width=False,
            width=180,
        )

    # 页面顶部标题
    st.markdown(
        "<div class='main-title'>🌊 岸 - 不需要变好，只需要坐下。</div>",
        unsafe_allow_html=True,
    )
    st.markdown(" ")


def render_auth_bar():
    """顶部登录区域：微信登录占位版，实现登录/退出和昵称。"""
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.session_state.is_wechat_logged_in:
            nick = st.session_state.wechat_nickname or "微信用户"
            st.markdown(f"**已登录：** 使用微信身份 `{nick}`")
        else:
            st.caption("当前为游客模式，可以随时用微信登录切换为自己的岸。")

    with col2:
        if not st.session_state.is_wechat_logged_in:
            if st.button("用微信登录", use_container_width=True):
                # 这里是原型：实际项目中应替换为微信 OAuth 跳转与回调
                st.session_state.is_wechat_logged_in = True
                # 简单生成一个占位昵称
                if not st.session_state.wechat_nickname:
                    st.session_state.wechat_nickname = f"微信用户{random.randint(1000,9999)}"
                st.session_state.real_name = st.session_state.wechat_nickname
                st.success("已以微信身份登录（原型模式）。")
        else:
            if st.button("退出登录", use_container_width=True):
                st.session_state.is_wechat_logged_in = False
                st.info("你已退出登录，现在是游客模式。")


def page_now():
    """「现在」页：写给自己 / 写给广场。"""
    st.subheader("现在", divider="gray")
    st.caption("这一刻，你想和谁说话？是和所有人，还是只和自己。")

    content = st.text_area(
        " ",
        placeholder="我在想什么？",
        label_visibility="collapsed",
        height=120,
    )
    mood = st.selectbox(
        "给这句话贴一个小情绪（可选）",
        ["", "平静", "开心", "难过", "焦虑", "失眠", "路上", "想家"],
        index=0,
    )

    col1, col2 = st.columns(2)
    with col1:
        send_square = st.button("以浪的身份说", use_container_width=True)
    with col2:
        send_private = st.button("只发给自己", use_container_width=True)

    now_str = datetime.now().strftime("%H:%M")

    if send_square and content.strip():
        mood_val = mood or "未贴标签"
        st.session_state.square_posts.insert(
            0,
            {
                "text": content.strip(),
                "time": f"今天 {now_str}",
                "from_me": True,
                "mood": mood_val,
                "echoes": [],
            },
        )
        st.session_state.my_public_posts.insert(
            0,
            {
                "text": content.strip(),
                "time": f"今天 {now_str}",
                "mood": mood_val,
            },
        )
        st.success("已经以「浪」的身份，把这句话放进广场了。")

    if send_private and content.strip():
        st.session_state.my_private_posts.insert(
            0,
            {
                "text": content.strip(),
                "time": f"今天 %H:%M",
            },
        )
        st.success("这句话只会留在这里，只属于你自己。")

    if (send_square or send_private) and not content.strip():
        st.info("什么都不说也没关系。如果想说点什么，也可以随时回来。")

    st.markdown("---")
    st.caption("最近你说过的几句话（只展示本地会话中的记录）：")

    recent = (st.session_state.my_public_posts + st.session_state.my_private_posts)[
        :5
    ]
    for idx, record in enumerate(recent):
        st.markdown(
            f"""
            <div class="exist-card">
                <div class="exist-text">{record['text']}</div>
                <div class="exist-meta">{record['time']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_square():
    """「匿名广场」页：所有浪的存在。"""
    st.subheader("匿名广场", divider="gray")
    st.caption(f"这里只有浪和浪之间的碰撞。你现在的身份是：**{st.session_state.anonymous_id}**。")

    # 根据屏蔽词过滤
    muted = [w for w in st.session_state.muted_words if w.strip()]

    for i, record in enumerate(st.session_state.square_posts):
        # 如果包含屏蔽词，则跳过显示
        if any(word in record["text"] for word in muted):
            continue

        from_me = record.get("from_me", False)
        meta = record["time"]
        who = st.session_state.anonymous_id if from_me else "某个浪"
        mood = record.get("mood")
        mood_str = f" · {mood}" if mood else ""

        st.markdown(
            f"""
            <div class="exist-card">
                <div class="exist-text">{record['text']}</div>
                <div class="exist-meta">{meta} · {who}{mood_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("收到了", key=f"received_{i}", use_container_width=True):
                st.toast("这句存在被你悄悄收下了。")
        with c2:
            if st.button("回声", key=f"echo_{i}", use_container_width=True):
                with st.expander("给这句话留一个回声", expanded=True):
                    echo_text = st.text_area(
                        f"echo_input_{i}",
                        placeholder="你想怎么回应？",
                        label_visibility="collapsed",
                        height=80,
                    )
                    if st.button("发送回声", key=f"send_echo_{i}", use_container_width=True):
                        if echo_text.strip():
                            record.setdefault("echoes", []).append(
                                {
                                    "text": echo_text.strip(),
                                    "time": datetime.now().strftime("%H:%M"),
                                    "from": st.session_state.anonymous_id,
                                }
                            )
                            st.success("你的回声已经悄悄飘过去了。")
                        else:
                            st.info("可以什么都不说，也可以说一点点。")

        # 展示已有回声（不显示数量，只以列表形式）
        echoes = record.get("echoes") or []
        if echoes:
            with st.expander("看到过的回声"):
                for e in echoes:
                    st.markdown(
                        f"""
                        <div class="exist-card">
                            <div class="exist-text">{e['text']}</div>
                            <div class="exist-meta">{e['time']} · 来自某个浪</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def page_mine():
    """「我的岸」页：真身 & 匿名分身的人格空间。"""
    st.subheader("我的岸", divider="gray")
    st.caption("这里是只有你和自己知道的岸，你可以同时照看真身和浪。")

    persona_tabs = st.tabs(["真身 · 我", "匿名分身 · 浪"])

    # 真身人格
    with persona_tabs[0]:
        st.markdown(f"**真身昵称：** `{st.session_state.real_name}`")
        real_intro = st.text_area(
            "自我介绍（真身）",
            value=st.session_state.real_profile.get("intro", ""),
            height=100,
        )
        st.session_state.real_profile["intro"] = real_intro

        st.markdown("**发一条真身动态**")
        real_content = st.text_area(
            " ",
            placeholder="最近发生了什么？这一条是以真身的身份写的。",
            label_visibility="collapsed",
            key="real_post_input",
            height=100,
        )
        real_image = st.file_uploader(
            "可选：加一张图片",
            type=["png", "jpg", "jpeg"],
            key="real_post_image",
        )
        if st.button("发布真身动态", use_container_width=True):
            if real_content.strip() or real_image is not None:
                image_path = None
                if real_image is not None:
                    upload_dir = Path(__file__).parent / "uploads"
                    upload_dir.mkdir(exist_ok=True)
                    file_path = upload_dir / real_image.name
                    with open(file_path, "wb") as f:
                        f.write(real_image.getbuffer())
                    image_path = str(file_path)
                st.session_state.real_posts.insert(
                    0,
                    {
                        "text": real_content.strip(),
                        "time": datetime.now().strftime("今天 %H:%M"),
                        "image": image_path,
                    },
                )
                st.success("真身的这一条，被安静地放在了这里。")
            else:
                st.info("可以只发一句话，也可以只发一张图片。")

        st.markdown("**真身的动态**")
        if not st.session_state.real_posts:
            st.write("还没有写过真身动态。")
        else:
            for post in st.session_state.real_posts:
                st.markdown(
                    f"""
                    <div class="exist-card">
                        <div class="exist-text">{post['text'] or '（只有图片，没有文字）'}</div>
                        <div class="exist-meta">{post['time']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if post.get("image"):
                    st.image(post["image"], use_container_width=True)

    # 匿名分身人格
    with persona_tabs[1]:
        st.markdown(f"**匿名分身代号：** `{st.session_state.anonymous_id}`")
        anon_intro = st.text_area(
            "自我介绍（浪）",
            value=st.session_state.anon_profile.get("intro", ""),
            height=100,
        )
        st.session_state.anon_profile["intro"] = anon_intro

        st.markdown("**发一条浪的动态**")
        anon_content = st.text_area(
            " ",
            placeholder="这一条，是只以浪的身份留下的。",
            label_visibility="collapsed",
            key="anon_post_input",
            height=100,
        )
        anon_image = st.file_uploader(
            "可选：加一张图片",
            type=["png", "jpg", "jpeg"],
            key="anon_post_image",
        )
        if st.button("发布浪的动态", use_container_width=True):
            if anon_content.strip() or anon_image is not None:
                image_path = None
                if anon_image is not None:
                    upload_dir = Path(__file__).parent / "uploads"
                    upload_dir.mkdir(exist_ok=True)
                    file_path = upload_dir / anon_image.name
                    with open(file_path, "wb") as f:
                        f.write(anon_image.getbuffer())
                    image_path = str(file_path)
                st.session_state.anon_posts.insert(
                    0,
                    {
                        "text": anon_content.strip(),
                        "time": datetime.now().strftime("今天 %H:%M"),
                        "image": image_path,
                    },
                )
                st.success("浪留下了一条只有在这里才能看见的动态。")
            else:
                st.info("浪也可以只留下一张图片，不必解释什么。")

        st.markdown("**浪的动态**")
        if not st.session_state.anon_posts:
            st.write("浪还没有留下任何东西。")
        else:
            for post in st.session_state.anon_posts:
                st.markdown(
                    f"""
                    <div class="exist-card">
                        <div class="exist-text">{post['text'] or '（只有图片，没有文字）'}</div>
                        <div class="exist-meta">{post['time']} · 以浪的身份</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if post.get("image"):
                    st.image(post["image"], use_container_width=True)


def page_settings():
    """「设置 / 安全感」页：真身昵称与匿名代号管理。"""
    st.subheader("设置与安全感", divider="gray")

    st.markdown("**真身昵称**")
    new_name = st.text_input(
        "真身昵称",
        value=st.session_state.real_name,
        label_visibility="collapsed",
    )
    if new_name != st.session_state.real_name:
        st.session_state.real_name = new_name or "某一个在岸上的人"

    st.markdown("---")

    st.markdown("**匿名分身**")
    st.write(f"当前匿名代号：`{st.session_state.anonymous_id}`")
    if st.button("换一个新的浪的代号", use_container_width=True):
        st.session_state.anonymous_id = f"浪 #{random.randint(1000, 9999)}"
        st.success(f"新的匿名代号是：{st.session_state.anonymous_id}")

    st.caption("说明：在匿名广场里，别人只能看到你的匿名代号，看不到你的真身昵称。")

    st.markdown("---")

    st.markdown("**屏蔽词**")
    st.caption("包含以下词语的内容会在匿名广场中被自动折叠，不主动出现在你面前。")
    muted_str = ", ".join(st.session_state.muted_words) if st.session_state.muted_words else ""
    new_muted = st.text_input(
        "屏蔽词（用英文逗号分隔，例如：加班, 分手）",
        value=muted_str,
    )
    # 轻量更新：用户只要输入框内容变化，就更新列表
    parsed = [w.strip() for w in new_muted.split(",") if w.strip()]
    st.session_state.muted_words = parsed


def page_tea_room():
    """茶室：实验性的「刮开可见」评论功能原型。"""
    topic = st.session_state.tea_topic

    st.subheader("茶室 · 刮开可见", divider="gray")
    st.caption("这里是可以被讨论的话题区，但评论内容需要你亲手刮开才会出现。")

    # 话题卡片
    st.markdown(
        f"""
        <div class="exist-card">
            <div class="exist-text"><strong>{topic['title']}</strong></div>
            <div class="exist-meta">{topic['created_at']} · 由你发起</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**写一条给话题发起者的悄悄话（发布后会被涂层遮住）**")
    comment_text = st.text_area(
        " ",
        placeholder="想说什么都可以，对方只有在准备好的时候，才会刮开看到。",
        label_visibility="collapsed",
        height=100,
    )
    if st.button("投递一张刮刮乐", use_container_width=True):
        if comment_text.strip():
            new_id = f"c{len(st.session_state.tea_comments) + 1}"
            st.session_state.tea_comments.insert(
                0,
                {
                    "id": new_id,
                    "author": st.session_state.anonymous_id,
                    "time": "刚刚",
                    "text": comment_text.strip(),
                    "reports": 0,
                },
            )
            st.success("已经投递出去啦。对方什么时候刮开，看缘分。")
        else:
            st.info("你也可以什么都不说，等下一次想开口的时候。")

    st.markdown("---")
    st.markdown("**待刮开的纸条**（只有你能决定要不要看）")

    for c in st.session_state.tea_comments:
        scratched = c["id"] in st.session_state.tea_scratched

        with st.container():
            st.markdown(
                f"""
                <div class="exist-card scratch-card">
                    <div class="exist-text {'scratch-blur' if not scratched else ''}">
                        {c['text'] if scratched else '内容被银灰色的涂层遮住，刮开才可见。'}
                    </div>
                    <div class="exist-meta">{c['time']} · 来自 {c['author']} · 刮开可见</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if not scratched and st.button("刮一刮", key=f"scratch_{c['id']}", use_container_width=True):
                    st.session_state.tea_scratched.add(c["id"])
                    st.success("你选择看见这一句了。")
            with col2:
                if scratched:
                    if st.button("收到了", key=f"tea_received_{c['id']}", use_container_width=True):
                        st.toast("这句话被你轻轻放进心里。")
            with col3:
                if st.button("举报", key=f"tea_report_{c['id']}", use_container_width=True):
                    c["reports"] += 1
                    if c["reports"] >= 3:
                        # 简化版：达到阈值后不再展示内容，只保留一行提示
                        c["text"] = "这条内容因为多次被举报，已经被封存。"
                    st.info("已收到举报，我们会在之后的版本里补充更完整的后台处理。")


def main():
    # 基础页面配置
    st.set_page_config(
        page_title="岸 - 匿名社交原型",
        page_icon="🌊",
        layout="centered",
    )

    init_state()
    render_global_style_and_header()
    render_auth_bar()

    tabs = st.tabs(["现在", "匿名广场", "茶室 · 刮开可见", "我的岸", "设置"])

    with tabs[0]:
        page_now()
    with tabs[1]:
        page_square()
    with tabs[2]:
        page_tea_room()
    with tabs[3]:
        page_mine()
    with tabs[4]:
        page_settings()


if __name__ == "__main__":
    main()

