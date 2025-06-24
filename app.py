import nicegui
from nicegui import (ui)
from crawler import Crawler

classes_visual = ui.mermaid('''
            graph LR;
            ''')

def commit():
    if metrics.value == '自动评价三个优秀和一个随机良好':
        crawler.commit(1, cookie_1.value, cookie_2.value)
    elif metrics.value == '自动评价四个良好':
        crawler.commit(2, cookie_1.value, cookie_2.value)
    ui.notify('已自动填写评教', position='center', close_button='OK')

def set_mermaid():
    global classes_visual
    nicegui.ui.notify('正在获取课程信息中，请过十秒点击刷新按钮', position='center', close_button='OK'),
    classes_visual.set_content(crawler.get_unevaluated_classes(cookie_1.value)),
    ui.notify('已获取课程信息！', position='center', close_button='OK')

def refresh():
    ui.run_javascript('location.reload();')

if __name__ in {"__main__", "__mp_main__"}:
    crawler = Crawler()

    with ui.card():
        ui.markdown('研究生课程评教')

    with ui.row():
        with ui.column(align_items='end'):
            with ui.card():
                ui.icon('home')
                ui.markdown('自动评教')

                ui.separator()
                ### Cookie区域
                ui.icon('cookie')
                ui.markdown('**Cookie区域**')
                with ui.grid(columns=2):
                    ui.markdown('请输入Cookie1 (http://gste.xjtu.edu.cn/)')
                    cookie_1 = ui.input()

                    ui.markdown('请输入Cookie2 (http://gmis.xjtu.edu.cn/pyxx/)')
                    cookie_2 = ui.input()

                ui.separator()
                ### 教材区域
                ui.icon('book')
                ui.markdown('**教材区域**')
                ui.radio(['自动获取教材'], value='自动获取教材').props('inline')
                ui.separator()
                ### 评价指标区域
                ui.icon('thumbs_up_down')
                ui.markdown('**评价指标区域**')
                metrics = ui.radio(['自动评价三个优秀和一个随机良好', '自动评价四个良好'], value='自动评价三个优秀和一个随机良好').props('inline')

                ui.separator()
                ### 评价区域
                ui.icon('gavel')
                ui.markdown('**评价区域**')
                ui.radio(['使用默认评价'], value='使用默认评价').props('inline')

            with ui.card():
                with ui.grid(columns=2):
                    ui.button('获取信息(点击后请点击刷新)', on_click= set_mermaid)
                    ui.button('开始评价', on_click= commit)
                    ui.button('刷新', on_click=refresh)

        with ui.card():
            classes_visual = ui.mermaid('''
            graph LR;
                课程 --> A;
                课程 --> B;
            ''')

    ui.run(reload=False,native=True)


