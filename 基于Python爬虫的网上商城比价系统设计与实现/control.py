import csv
import json
import os
import time
import webbrowser
from tkinter import filedialog, ttk, END
import pandas as pd
import chardet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.service import Service
from sklearn.cluster import KMeans

from ui import Win
import tkinter as tk

plt.rcParams['font.sans-serif'] = 'SimSun'


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        pass

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.ui.tk_select_box_shop_select.set("京东")
        self.ui.tk_select_box_page_select.set("1")
        self.ui.tk_text_status.insert("1.0", chars=f'若爬虫时要求登录验证\n请关闭网页并重置cookie\n')
        self.ui.tk_text_status.insert("1.0", chars=f'完成网页登录后请耐心等待网页自动关闭\n')
        self.ui.tk_scale_scale.set(0.5)
        self.ui.tk_select_box_percent_set_box.set("低")
        # TODO 组件初始化 赋值操作

    def get_cookie(self, evt):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service('./chromedriver.exe')
        driver = webdriver.Chrome(options=options, service=service)
        if self.ui.tk_select_box_shop_select.get() == "京东":
            url = 'https://www.jd.com/'
            filename = "jd"
        elif self.ui.tk_select_box_shop_select.get() == "淘宝":
            url = 'https://www.taobao.com/'
            filename = "taobao"
        driver.get(url)

        for delaytime in range(0, 61):
            time_left = 60 - delaytime
            time.sleep(1)

        with open(f'{filename}.cookie', 'w') as file:
            file.write(json.dumps(driver.get_cookies()))
        driver.close()
        driver.quit()

    def start_crawler(self, evt):
        keyword = self.ui.tk_input_search_input.get()
        if keyword == "":
            self.ui.tk_text_status.insert("1.0", chars=f'请输入搜索关键词\n')
        else:
            start_page = 1
            end_page = int(self.ui.tk_select_box_page_select.get())
            if self.ui.tk_select_box_shop_select.get() == "京东":
                self.jd_start_crawler(keyword, start_page, end_page)
                self.ui.tk_text_status.insert("1.0", chars=f'开始京东爬虫\n目标商品:{keyword}\n获取页数:{end_page}\n')
            elif self.ui.tk_select_box_shop_select.get() == "淘宝":
                self.tb_start_crawler(keyword, start_page, end_page)
                self.ui.tk_text_status.insert("1.0", chars=f'开始淘宝爬虫\n目标商品:{keyword}\n获取页数:{end_page}\n')

    def jd_start_crawler(self, keyword, start_page, end_page):
        try:
            os.makedirs("data")  # 尝试创建"data"文件夹
        except FileExistsError:
            pass

        filepath = f"data/{keyword}_jd_{time.strftime('%Y-%m-%d_%H-%M', time.localtime())}.csv"
        try:
            csvfile = open(filepath, 'a', encoding='utf-8', newline='')
        except FileNotFoundError:
            os.makedirs("data")  # 创建"data"文件夹
            csvfile = open(filepath, 'a', encoding='utf-8', newline='')
        csvWriter = csv.DictWriter(csvfile,
                                   fieldnames=['item_name', 'item_price', 'item_shop', 'item_link',
                                               'item_comment_amount', 'item_discount'])
        csvWriter.writerow(
            {'item_name': '商品名',
             'item_price': '商品价格',
             'item_shop': '店铺名称',
             'item_link': '商品链接',
             'item_comment_amount': '销量',
             'item_discount': '活动'
             })

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('./chromedriver.exe')
        browser = webdriver.Chrome(options=options, service=service)
        browser.get('https://www.jd.com')
        browser.implicitly_wait(10)
        try:
            with open('jd.cookie', 'r') as f:
                cookie_list = json.load(f)
                for cookie in cookie_list:
                    browser.add_cookie(cookie)
        except:
            pass
        browser.refresh()

        browser.find_element(By.ID, 'key').send_keys(keyword)
        browser.find_element(By.CLASS_NAME, 'button').click()
        browser.implicitly_wait(10)
        jdPage = browser.find_element(By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b').text
        for page in range(start_page, end_page + 1):
            browser.execute_script(f"SEARCH.page({2 * page - 1}, true)")
            browser.refresh()
            for i in range(0, 30):
                try:
                    item_name = browser.find_element(By.CSS_SELECTOR,
                                                     f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-name.p-name-type-2 > a > em').text
                    item_price = browser.find_element(By.CSS_SELECTOR,
                                                      f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-price > strong > i').text
                    item_shop = browser.find_element(By.CSS_SELECTOR,
                                                     f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-shop > span > a').text
                    item_link = browser.find_element(By.CSS_SELECTOR,
                                                     f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-img > a').get_attribute(
                        'href')
                    item_comment_amount = browser.find_element(By.CSS_SELECTOR,
                                                               f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-commit > strong').text
                    try:
                        item_discounts = browser.find_elements(By.CSS_SELECTOR,
                                                               f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-icons > i')
                    except NoSuchElementException:
                        item_discounts = []
                    item_discounts_text = [element.text for element in item_discounts]
                    item_discount = ','.join(item_discounts_text)
                    csvWriter.writerow(
                        {'item_name': item_name,
                         'item_price': item_price,
                         'item_shop': item_shop,
                         'item_link': item_link,
                         'item_comment_amount': item_comment_amount,
                         'item_discount': item_discount
                         })
                    csvfile.flush()
                except:
                    pass

        csvfile.close()
        browser.close()
        self.ui.tk_text_status.insert("1.0", chars=f'爬虫结束\n文件已保存\n')

    def tb_start_crawler(self, keyword, start_page, end_page):
        try:
            os.makedirs("data")  # 尝试创建"data"文件夹
        except FileExistsError:
            pass

        filepath = f"data/{keyword}_taobao_{time.strftime('%Y-%m-%d_%H-%M', time.localtime())}.csv"
        try:
            csvfile = open(filepath, 'a', encoding='utf-8', newline='')
        except FileNotFoundError:
            os.makedirs("data")  # 创建"data"文件夹
            csvfile = open(filepath, 'a', encoding='utf-8', newline='')
        csvWriter = csv.DictWriter(csvfile,
                                   fieldnames=['item_name', 'item_price', 'item_shop', 'item_link', 'item_sale',
                                               'item_discount'])
        csvWriter.writerow(
            {'item_name': '商品名',
             'item_price': '商品价格',
             'item_shop': '店铺名称',
             'item_link': '商品链接',
             'item_sale': '销量',
             'item_discount': '活动'
             })

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('./chromedriver.exe')
        browser = webdriver.Chrome(options=options, service=service)
        browser.get('https://www.taobao.com')
        browser.implicitly_wait(5)
        try:
            with open('taobao.cookie', 'r') as f:
                cookie_list = json.load(f)
                for cookie in cookie_list:
                    browser.add_cookie(cookie)
        except:
            pass
        browser.get(f'https://s.taobao.com/search?q={keyword}')
        browser.implicitly_wait(10)

        for page in range(start_page, end_page + 1):
            browser.get(f'https://s.taobao.com/search?q={keyword}&page={page}')
            for i in range(1, 45):
                item_name = browser.find_element(By.CSS_SELECTOR,
                                                 f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Title--descWrapper--HqxzYq0.Title--normalMod--HpNGsui > div > span').text
                item_price_int = browser.find_element(By.CSS_SELECTOR,
                                                      f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > div:nth-child(2) > span.Price--priceInt--ZlsSi_M').text
                item_price_float = browser.find_element(By.CSS_SELECTOR,
                                                        f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > div:nth-child(2) > span.Price--priceFloat--h2RR0RK').text
                item_price = item_price_int + item_price_float
                item_shop = browser.find_element(By.CSS_SELECTOR,
                                                 f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.ShopInfo--shopInfo--ORFs6rK > div.ShopInfo--TextAndPic--yH0AZfx > a').text
                item_sale = browser.find_element(By.CSS_SELECTOR,
                                                 f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > span.Price--realSales--FhTZc7U').text
                item_link = browser.find_element(By.CSS_SELECTOR,
                                                 f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a').get_attribute(
                    'href')
                try:
                    item_discounts = browser.find_elements(By.CSS_SELECTOR,
                                                           f'#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child({i}) > a > div > div.SalesPoint--subIconWrapper--s6vanNY > div > span')
                except NoSuchElementException:
                    item_discounts = []
                item_discounts_text = [element.text for element in item_discounts]
                item_discount = ','.join(item_discounts_text)
                csvWriter.writerow(
                    {'item_name': item_name,
                     'item_price': item_price,
                     'item_shop': item_shop,
                     'item_link': item_link,
                     'item_sale': item_sale,
                     'item_discount': item_discount
                     })
                csvfile.flush()
            time.sleep(1)

        csvfile.close()
        browser.close()
        self.ui.tk_text_status.insert("1.0", chars=f'爬虫结束\n文件已保存\n')

    def choose_file_01(self, evt):
        self.ui.tk_input_filepath_show_01.delete(0, END)
        path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        self.csv_process(path)
        self.ui.tk_input_filepath_show_01.insert(0, path)
        self.ui.tk_table_data_table.delete(*self.ui.tk_table_data_table.get_children())
        with open(path, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            # 逐行读取CSV文件中的数据，并添加到表格中
            next(reader)
            for i, row in enumerate(reader):
                self.ui.tk_table_data_table.insert("", "end", values=row)
                self.ui.tk_table_data_table.item(self.ui.tk_table_data_table.get_children()[i], tags=("Link",))

    def choose_file_02(self, evt):
        self.ui.tk_input_filepath_show_02.delete(0, END)
        path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        self.csv_process(path)
        self.ui.tk_input_filepath_show_02.insert(0, path)
        return path

    def csv_process(self, csv_name):
        with open(csv_name, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        df = pd.read_csv(f'{csv_name}', encoding=encoding)

        # 使用str.replace方法在指定列中删除关键字
        df['商品价格'] = df['商品价格'].astype(str)
        df['销量'] = df['销量'].astype(str)
        df['商品价格'] = df['商品价格'].str.replace('¥', '', regex=False)
        df['商品价格'] = df['商品价格'].str.replace('到手价', '', regex=False)
        df['销量'] = df['销量'].str.replace('+评价', '', regex=False)
        df['销量'] = df['销量'].str.replace('+条评价', '', regex=False)
        df['销量'] = df['销量'].str.replace('+', '', regex=False)
        df['销量'] = df['销量'].str.replace('万', '0000', regex=False)
        df['销量'] = df['销量'].str.replace('人付款', '', regex=False)
        df['销量'] = pd.to_numeric(df['销量'], errors='coerce')
        df['活动'] = df['活动'].str.replace('京东物流,', '', regex=False)
        df['活动'] = df['活动'].str.replace('新品,', '', regex=False)

        df.to_csv(f'{csv_name}', index=False, encoding='utf-8')

    def show_top_10_by_price_group(self, evt):
        file_path = self.ui.tk_input_filepath_show_02.get()

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 清空Canvas
        canvas = self.ui.tk_canvas_cnavas
        canvas.delete("all")

        # 清空canvas上的所有组件
        for child in canvas.winfo_children():
            child.destroy()

        # 将价格分为六组
        price_groups = pd.cut(df['商品价格'], bins=[0, 100, 500, 1000, 3000, 5000, float('inf')], labels=False,
                              right=False)

        # 创建滑动条
        scrollbar = tk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 配置Canvas和滑动条的关联
        canvas.configure(yscrollcommand=scrollbar.set)

        # 创建一个Frame用于放置Treeview表格
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # 创建Treeview表格
        tree = ttk.Treeview(frame, height=12)

        # 添加表格列名
        columns = df.columns.tolist()
        tree["columns"] = columns
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column,width=100)

        # 循环处理每个价位段
        for group in range(6):
            # 获取当前分组的数据
            group_df = df[price_groups == group]

            # 输出每组销量最高的前三并按价格排序
            top_3_df = group_df.nlargest(3, '销量').sort_values('商品价格')
            for index, row in top_3_df.iterrows():
                tree.insert("", "end", values=row.tolist())

        # 显示表格
        tree.pack(side=tk.LEFT,padx=10,pady=10)

        # 更新Canvas的可滚动区域
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_sales_by_price_range(self, evt):
        file_path = self.ui.tk_input_filepath_show_02.get()

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 将商品价格转换为数值类型
        df['商品价格'] = pd.to_numeric(df['商品价格'], errors='coerce')

        # 创建价格区间
        price_ranges = ['0-100', '100-500', '500-1000', '1000-3000', '3000以上']

        # 计算每个价格区间的销量
        sales_by_price_range = []
        for i in range(len(price_ranges)):
            if i < len(price_ranges) - 1:
                price_range_sales = df[(df['商品价格'] >= i * 100) & (df['商品价格'] < (i + 1) * 100)]['销量'].sum()
            else:
                price_range_sales = df[df['商品价格'] >= (i + 1) * 100]['销量'].sum()
            sales_by_price_range.append(price_range_sales)

        # 创建销量条形图
        fig, ax = plt.subplots()
        ax.bar(price_ranges, sales_by_price_range)

        # 设置图形属性
        ax.set_xlabel('价格区间', fontname='SimHei', fontsize=12)  # 设置横坐标标签为中文
        ax.set_ylabel('销量', fontname='SimHei', fontsize=12)  # 设置纵坐标标签为中文
        ax.set_title('销量按价格区间统计', fontname='SimHei', fontsize=14)  # 设置图的标题为中文

        self.ui.tk_canvas_cnavas.delete("all")
        # 清空canvas上的所有组件
        for child in self.ui.tk_canvas_cnavas.winfo_children():
            child.destroy()

        # 创建图形画布
        canvas_fig = FigureCanvasTkAgg(fig, master=self.ui.tk_canvas_cnavas)
        canvas_fig.draw()

        # 将图形画布放置在Canvas上
        canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def count_products_by_price_range(self, evt):
        file_path = self.ui.tk_input_filepath_show_02.get()

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 将商品价格转换为数值类型
        df['商品价格'] = pd.to_numeric(df['商品价格'], errors='coerce')

        # 创建价格区间
        price_ranges = ['0-100', '100-500', '500-1000', '1000-3000', '3000以上']

        # 统计每个价格区间的商品数量
        products_by_price_range = []
        for i in range(len(price_ranges)):
            if i < len(price_ranges) - 1:
                price_range_products = len(df[(df['商品价格'] >= i * 100) & (df['商品价格'] < (i + 1) * 100)])
            else:
                price_range_products = len(df[df['商品价格'] >= (i + 1) * 100])
            products_by_price_range.append(price_range_products)

        # 创建商品数量条形图
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(price_ranges, products_by_price_range)

        # 设置图形属性
        ax.set_xlabel('价格区间', fontname='SimHei', fontsize=12)
        ax.set_ylabel('商品数量', fontname='SimHei', fontsize=12)
        ax.set_title('商品数量按价格区间统计', fontname='SimHei', fontsize=14)

        # 清空Canvas
        self.ui.tk_canvas_cnavas.delete("all")
        # 清空canvas上的所有组件
        for child in self.ui.tk_canvas_cnavas.winfo_children():
            child.destroy()

        # 创建图形画布
        canvas_fig = FigureCanvasTkAgg(fig, master=self.ui.tk_canvas_cnavas)
        canvas_fig.draw()

        # 将图形画布放置在Canvas上
        canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def analyze_store_data(self, evt):
        file_path = self.ui.tk_input_filepath_show_02.get()
        canvas = self.ui.tk_canvas_cnavas

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 清空Canvas
        self.ui.tk_canvas_cnavas.delete("all")

        # 清空canvas上的所有组件
        for child in self.ui.tk_canvas_cnavas.winfo_children():
            child.destroy()

        # 唯一值计数：统计不同的店铺名称有多少个唯一值
        unique_stores = df['店铺名称'].nunique()

        # 热门店铺：查找最受欢迎的店铺名称或出现频率最高的店铺名称
        top_stores = df['店铺名称'].value_counts().head(10)

        # 创建表格
        tree = ttk.Treeview(canvas)
        tree["columns"] = ("唯一值计数", "热门店铺")
        tree.heading("#0", text="指标")
        tree.heading("唯一值计数", text="唯一值计数")
        tree.heading("热门店铺", text="热门店铺")

        # 插入唯一值计数数据
        tree.insert("", "end", text="不同的店铺名称数量", values=(unique_stores, ""))

        # 插入热门店铺数据
        for store, count in top_stores.items():
            tree.insert("", "end", text="热门店铺名称", values=("", f"{store}: {count}"))

        # 创建窗口并将表格嵌入到窗口中
        canvas.create_window(0, 0, anchor=tk.NW, window=tree)

        # 更新Canvas的滚动区域
        canvas.update()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    def choose_file_03(self, evt):
        self.ui.tk_input_filepath_show_03.delete(0, END)
        path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        self.csv_process(path)
        self.ui.tk_input_filepath_show_03.insert(0, path)
        return path

    def data_show(self, evt):
        filepath = self.ui.tk_input_filepath_show_03.get()
        df = pd.read_csv(filepath)

        # 提取需要显示的列
        selected_columns = ['商品名', '商品价格', '商品链接', '销量']

        # 提取价格列作为特征向量
        X = df['商品价格'].values.reshape(-1, 1)

        # 使用K均值聚类算法进行聚类
        kmeans = KMeans()
        kmeans.fit(X)

        price_weight = float(1 - self.ui.tk_scale_scale.get())
        sales_weight = float(self.ui.tk_scale_scale.get())

        # 获取每个商品所属的聚类标签
        labels = kmeans.labels_

        # 计算每个商品在价格聚类中的排名
        df['价格排名'] = df.groupby(labels)['商品价格'].rank(ascending=False)

        # 计算每个商品在销量聚类中的排名
        df['销量排名'] = df.groupby(labels)['销量'].rank(ascending=True)

        # 计算评分并添加到数据中
        df['评分'] = price_weight * df['价格排名'] + sales_weight * df['销量排名']

        # 根据评分对数据进行排序
        data = df.sort_values(by='评分', ascending=False)

        # 清空表格内容
        self.ui.tk_table_rating_table.delete(*self.ui.tk_table_rating_table.get_children())

        # 添加评分结果到表格中
        for index, row in data.iterrows():
            values = [row[column] for column in selected_columns] + [row['评分']]
            # 创建超链接单元格
            link = row['商品链接']
            cell_widget = tk.Label(self.ui.tk_table_rating_table, text=link, foreground="blue", cursor="hand2")
            cell_widget.bind("<Button-1>", lambda event, link=link: webbrowser.open(link))

            # 插入单元格到表格
            if self.ui.tk_check_button_check_button_01 and self.ui.tk_check_button_check_button_02:
                if any(char != '自营' for char in row['活动']):
                    self.value_check(values[-1])
            elif self.ui.tk_check_button_check_button_01 and self.ui.tk_check_button_check_button_02:
                if any(char != '免邮' and char != '包邮' for char in row['活动']):
                    self.value_check(values[-1])
            elif self.ui.tk_check_button_check_button_01 and self.ui.tk_check_button_check_button_02:
                if any(char != '' for char in row['活动']):
                    self.value_check(values[-1])
            elif self.ui.tk_check_button_check_button_01 and self.ui.tk_check_button_check_button_02:
                if any(char != '免邮' and char != '包邮' and char != '自营' for char in row['活动']):
                    self.value_check(values[-1])
            self.ui.tk_table_rating_table.insert('', 'end', values=values)
            self.ui.tk_table_rating_table.item(self.ui.tk_table_rating_table.get_children()[:index], tags=("Link",))

    def value_check(self, i):
        if self.ui.tk_select_box_percent_set_box.get() == "低":
            i *= 1.1
        elif self.ui.tk_select_box_percent_set_box.get() == "中":
            i *= 1.2
        elif self.ui.tk_select_box_percent_set_box.get() == "高":
            i *= 1.3
        return i
