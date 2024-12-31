import random
from bs4 import BeautifulSoup
import requests

class Crawler:
    def __init__(self):
        self.classes = []
        self.commit_data = {}

        ### 提交信息
        self.commit_data['standard_id'] = '5acc257f51c9565988d01357'
        self.commit_data['standard_name'] = '研究生评教指标体系'
        self.commit_data['5acc764d51c9565ea001cd6c'] = '任课教师为人师表，教书育人，在授课过程中，结合课程内容，体现课程伦理、学术规范、人文及科学素养等方面内容；遵章守纪，恪守教师职业道德；弘扬正气，坚持社会主义核心价值观，无不当言论；在教学活动中体现出良好的师德师风和严谨的学术态度。'
        self.commit_data['5acc76db51c9565ea001cd93'] = '我没有建议'
        self.commit_data['5acc773651c9565ea001cd97'] = '我没有建议'
        self.commit_data['5e85aa25ff3f8d0d458d4a84'] = '1'
        self.commit_data['5b2a1d3dff3f8d0757da4a98-51'] = '任课教师在教学时融入了启发性、引导式的教学方法，能够鼓励学生参与课堂讨论、提出问题、发表不同的观点或提出质疑，师生互动良好。'
        self.commit_data['5da65e76ff3f8d070307318b'] = '我没有建议'


    def get_unevaluated_classes(self, j_session_id):
        headers = {'Cookie': 'JSESSIONID=' + j_session_id}
        get_list_url = 'http://gste.xjtu.edu.cn/app/sshd4Stu/list.do?key=value'

        get_list_result = requests.get(get_list_url, headers=headers)

        self.classes = get_list_result.json()

        content = 'graph LR;'
        for item in self.classes:
            content += '\n'
            content += '\t课程 --> ' + item['kcmc'].replace('（', '**').replace('）', '**') + '_' + item['jsxm'].replace(' ', '-') + ';'

        return content

    def commit(self, metrics_mode, cookie_1, cookie_2):
        commit_url = 'http://gste.xjtu.edu.cn/app/student/saveForm.do'
        commit_headers = {'Cookie': 'JSESSIONID=' + cookie_1}
        info_headers = {'Cookie': 'JSESSIONID=' + cookie_2}
        metrics = ['5acc734751c9565ea001cd1b',
                    '5acc746151c9565ea001cd32',
                    '5acc74a051c9565ea001cd3b',
                    '5acc74d351c9565ea001cd3e']
        for item in self.classes:
            self.commit_data['bjid'] = item['bjid']
            self.commit_data['jsbh'] = item['jsbh']
            self.commit_data['termcode'] = item['termcode']
            self.commit_data['5aebd5d90c9e00458c6f5bb1'] = item['kcmc']
            self.commit_data['5aebd5cc0c9e00458c6f5bb0'] = item['jsxm']

            if metrics_mode == 1:
                random.shuffle(metrics)
                self.commit_data[metrics[0]] = '100'
                self.commit_data[metrics[1]] = '100'
                self.commit_data[metrics[2]] = '100'
                self.commit_data[metrics[3]] = '80'

            elif metrics_mode == 2:
                self.commit_data[metrics[0]] = '80'
                self.commit_data[metrics[1]] = '80'
                self.commit_data[metrics[2]] = '80'
                self.commit_data[metrics[3]] = '80'
            info_url = 'http://gmis.xjtu.edu.cn/pyxx/pygl/kckk/view/new/' + item['kcbh'] + '/2024'
            result = requests.get(info_url, headers=info_headers)

            bs = BeautifulSoup(result.content, 'html.parser')

            self.commit_data['5b1a5b06ff3f8d4680fc2bc5'] = bs.find_all('tbody')[0].find_all('td')[1].get_text()

            lang = bs.find_all('tr')[9].find_all('td')[3].get_text().strip()

            if lang == '全英文授课':
                self.commit_data['5aebcfeb0c9e00458c6f5aac'] = 'qyw'
            elif lang == '中英文授课':
                self.commit_data['5aebcfeb0c9e00458c6f5aac'] = 'zyw'
            elif lang == '全中文授课':
                self.commit_data['5aebcfeb0c9e00458c6f5aac'] = 'zw'
            else:
                self.commit_data['5aebcfeb0c9e00458c6f5aac'] = 'qt'

            self.commit_data['5acc724651c9565ea001cd09'] = '3'
            self.commit_data['5b1a5b21ff3f8d4680fc2bc6'] = '中文'

            # TODO
            self.commit_data['5aebcfd10c9e00458c6f5aa0']= 'xwk'

            assess_result = requests.post(commit_url, data=self.commit_data, headers=commit_headers)

            print(assess_result.text)
