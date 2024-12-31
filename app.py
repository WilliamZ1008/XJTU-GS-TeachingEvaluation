from nicegui import (ui)
from crawler import Crawler


def commit():
    if metrics.value == '自动评价三个优秀和一个随机良好':
        crawler.commit(1, cookie_1.value, cookie_2.value)
    elif metrics.value == '自动评价四个良好':
        crawler.commit(2, cookie_1.value, cookie_2.value)
    ui.notify('已自动填写评教', position='center')

crawler = Crawler()

with ui.card():
    ui.markdown('研究生课程评教')

with ui.row():
    with ui.column():
        with ui.card():
            ui.icon('home')
            ui.markdown('自动评教')

            ui.separator()
            ### Cookie区域
            ui.icon('cookie')
            ui.markdown('**Cookie区域**')
            with ui.grid(columns=2):
                ui.markdown('请输入Cookie1')
                cookie_1 = ui.input()

                ui.markdown('请输入Cookie2')
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
                ui.button('获取信息', on_click=lambda: classes_visual.set_content(crawler.get_unevaluated_classes(cookie_1.value)))
                ui.button('开始评价', on_click= commit)

    with ui.card():
        classes_visual = ui.mermaid('''
        graph LR;
            课程 --> A;
            课程 --> B;
        ''')



ui.run()


