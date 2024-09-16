import random
import webbrowser
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from pytkUI.widgets import *


class WinGUI(Window):
    def __init__(self):
        super().__init__(themename="cosmo", hdpi=False)
        self.__win()
        self.ext_tabs_lvafo83d = self.__ext_tabs_lvafo83d(self)
        self.tk_input_search_input = self.__tk_input_search_input(self.ext_tabs_lvafo83d_0)
        self.tk_button_search_button = self.__tk_button_search_button(self.ext_tabs_lvafo83d_0)
        self.tk_text_status = self.__tk_text_status(self.ext_tabs_lvafo83d_0)
        self.tk_input_filepath_show_01 = self.__tk_input_filepath_show_01(self.ext_tabs_lvafo83d_1)
        self.tk_button_file_choose_01 = self.__tk_button_file_choose_01(self.ext_tabs_lvafo83d_1)
        self.tk_select_box_shop_select = self.__tk_select_box_shop_select(self.ext_tabs_lvafo83d_0)
        self.tk_table_data_table = self.__tk_table_data_table(self.ext_tabs_lvafo83d_1)
        self.tk_input_filepath_show_02 = self.__tk_input_filepath_show_02(self.ext_tabs_lvafo83d_2)
        self.tk_button_file_choose_02 = self.__tk_button_file_choose_02(self.ext_tabs_lvafo83d_2)
        self.tk_select_box_page_select = self.__tk_select_box_page_select(self.ext_tabs_lvafo83d_0)
        self.tk_label_pages = self.__tk_label_pages(self.ext_tabs_lvafo83d_0)
        self.tk_button_cookie_reset = self.__tk_button_cookie_reset(self.ext_tabs_lvafo83d_0)
        self.tk_canvas_cnavas = self.__tk_canvas_cnavas(self.ext_tabs_lvafo83d_2)
        self.tk_button_hot_item = self.__tk_button_hot_item(self.ext_tabs_lvafo83d_2)
        self.tk_button_range_sale = self.__tk_button_range_sale(self.ext_tabs_lvafo83d_2)
        self.tk_button_range_quantity = self.__tk_button_range_quantity(self.ext_tabs_lvafo83d_2)
        self.tk_button_hot_shop = self.__tk_button_hot_shop(self.ext_tabs_lvafo83d_2)
        self.tk_input_filepath_show_03 = self.__tk_input_filepath_show_03(self.ext_tabs_lvafo83d_3)
        self.tk_button_file_choose_03 = self.__tk_button_file_choose_03(self.ext_tabs_lvafo83d_3)
        self.tk_table_rating_table = self.__tk_table_rating_table(self.ext_tabs_lvafo83d_3)
        self.tk_scale_scale = self.__tk_scale_scale(self.ext_tabs_lvafo83d_3)
        self.tk_label_label_price = self.__tk_label_label_price(self.ext_tabs_lvafo83d_3)
        self.tk_label_label_sale = self.__tk_label_label_sale(self.ext_tabs_lvafo83d_3)
        self.tk_label_label_set = self.__tk_label_label_set(self.ext_tabs_lvafo83d_3)
        self.tk_button_check_button = self.__tk_button_check_button(self.ext_tabs_lvafo83d_3)
        self.tk_label_lw568fv5 = self.__tk_label_lw568fv5(self.ext_tabs_lvafo83d_3)
        self.tk_label_lw56bq01 = self.__tk_label_lw56bq01(self.ext_tabs_lvafo83d_3)
        self.tk_select_box_percent_set_box = self.__tk_select_box_percent_set_box(self.ext_tabs_lvafo83d_3)
        self.tk_check_button_check_button_01 = self.__tk_check_button_check_button_01(self.ext_tabs_lvafo83d_3)
        self.tk_check_button_check_button_02 = self.__tk_check_button_check_button_02(self.ext_tabs_lvafo83d_3)

    def __win(self):
        self.title("商城比价")
        # 设置窗口大小、居中
        width = 1100
        height = 455
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def open_link_01(self, event):
        link = event.widget.item(event.widget.focus())['values'][3]  # 获取单击行的链接数据
        webbrowser.open(link)

    def open_link_02(self, event):
        item = self.tk_table_rating_table.identify('item', event.x, event.y)
        if item:
            cell_text = self.tk_table_rating_table.item(item)['values'][2]
            if cell_text.startswith('http'):
                webbrowser.open(cell_text)

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def new_style(self, widget):
        ctl = widget.cget('style')
        ctl = "".join(random.sample('0123456789', 5)) + "." + ctl
        widget.configure(style=ctl)
        return ctl

    def __tk_frame_lvafo83d_0(self, parent):
        frame = Frame(parent)
        return frame

    def __tk_frame_lvafo83d_1(self, parent):
        frame = Frame(parent)
        return frame

    def __tk_frame_lvafo83d_2(self, parent):
        frame = Frame(parent)
        return frame

    def __tk_frame_lvafo83d_3(self, parent):
        frame = Frame(parent)
        return frame

    def __ext_tabs_lvafo83d(self, parent):
        frame = ExtTabs(parent)
        self.ext_tabs_lvafo83d_0 = self.__tk_frame_lvafo83d_0(frame)
        self.ext_tabs_lvafo83d_1 = self.__tk_frame_lvafo83d_1(frame)
        self.ext_tabs_lvafo83d_2 = self.__tk_frame_lvafo83d_2(frame)
        self.ext_tabs_lvafo83d_3 = self.__tk_frame_lvafo83d_3(frame)
        tabs = [
            TabItem("1-circle", "爬虫", self.ext_tabs_lvafo83d_0),
            TabItem("2-circle", "数据概览", self.ext_tabs_lvafo83d_1),
            TabItem("3-circle", "数据分析", self.ext_tabs_lvafo83d_2),
            TabItem("4-circle", "商品比较", self.ext_tabs_lvafo83d_3),
        ]
        frame.init(tabs=tabs)
        frame.place(relx=0.0000, rely=0.0000, relwidth=1.0000, relheight=1.0000)
        return frame

    def __tk_input_search_input(self, parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(relx=0.0000, rely=0.0330, relwidth=0.6818, relheight=0.0659)
        return ipt

    def __tk_button_search_button(self, parent):
        btn = Button(parent, text="搜索", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.7027, rely=0.0330, relwidth=0.1036, relheight=0.0659)
        return btn

    def __tk_text_status(self, parent):
        text = Text(parent)
        text.place(relx=0.0000, rely=0.1429, relwidth=0.6800, relheight=0.3297)
        self.create_bar(parent, text, True, False, 0, 65, 748, 150, 1100, 455)
        return text

    def __tk_input_filepath_show_01(self, parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(relx=0.0000, rely=0.0330, relwidth=0.6818, relheight=0.0659)
        return ipt

    def __tk_button_file_choose_01(self, parent):
        btn = Button(parent, text="选择文件", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.7091, rely=0.0330, relwidth=0.0955, relheight=0.0659)
        return btn

    def __tk_select_box_shop_select(self, parent):
        cb = Combobox(parent, state="readonly", bootstyle="secondary")
        cb['values'] = ("京东", "淘宝")
        cb.place(relx=0.7027, rely=0.1516, relwidth=0.1045, relheight=0.0659)
        return cb

    def __tk_table_data_table(self, parent):
        # 表头字段 表头宽度
        columns = {"商品名": 269, "价格": 44, "店铺名称": 89, "商品链接": 224, "销量": 44, "活动": 89}
        tk_table = Treeview(parent, show="headings", columns=list(columns), bootstyle="default")
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        tk_table.place(relx=0.0000, rely=0.1538, relwidth=0.8182, relheight=0.8132)
        self.create_bar(parent, tk_table, True, True, 0, 70, 900, 370, 1100, 455)
        tk_table.tag_bind("Link", "<Button-1>", self.open_link_01)
        return tk_table

    def __tk_input_filepath_show_02(self, parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(relx=0.0000, rely=0.0330, relwidth=0.6818, relheight=0.0659)
        return ipt

    def __tk_button_file_choose_02(self, parent):
        btn = Button(parent, text="选择文件", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.7091, rely=0.0330, relwidth=0.0955, relheight=0.0659)
        return btn

    def __tk_select_box_page_select(self, parent):
        cb = Combobox(parent, state="readonly", bootstyle="secondary")
        cb['values'] = (
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20")
        cb.place(relx=0.1091, rely=0.5165, relwidth=0.2027, relheight=0.0659)
        return cb

    def __tk_label_pages(self, parent):
        label = Label(parent, text="爬取页数", anchor="center", bootstyle="default")
        label.place(relx=0.0209, rely=0.5165, relwidth=0.0718, relheight=0.0659)
        return label

    def __tk_button_cookie_reset(self, parent):
        btn = Button(parent, text="cookie重置", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.7027, rely=0.3297, relwidth=0.1027, relheight=0.0659)
        return btn

    def __tk_canvas_cnavas(self, parent):
        canvas = Canvas(parent, bg="#aaa")
        canvas.place(relx=0.0000, rely=0.2308, relwidth=0.8182, relheight=0.7582)
        return canvas

    def __tk_button_hot_item(self, parent):
        btn = Button(parent, text="热门商品", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.0091, rely=0.1319, relwidth=0.1136, relheight=0.0659)
        return btn

    def __tk_button_range_sale(self, parent):
        btn = Button(parent, text="销量区间", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.2636, rely=0.1319, relwidth=0.1136, relheight=0.0659)
        return btn

    def __tk_button_range_quantity(self, parent):
        btn = Button(parent, text="商品数量区间", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.3909, rely=0.1319, relwidth=0.1136, relheight=0.0659)
        return btn

    def __tk_button_hot_shop(self, parent):
        btn = Button(parent, text="热门店铺", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.1364, rely=0.1319, relwidth=0.1136, relheight=0.0659)
        return btn

    def __tk_input_filepath_show_03(self, parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(relx=0.0000, rely=0.0330, relwidth=0.6818, relheight=0.0659)
        return ipt

    def __tk_button_file_choose_03(self, parent):
        btn = Button(parent, text="选择文件", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.7273, rely=0.0330, relwidth=0.0955, relheight=0.0659)
        return btn

    def __tk_table_rating_table(self, parent):
        # 表头字段 表头宽度
        columns = {"商品名": 187, "价格": 74, "商品链接": 187, "销量": 74, "评分": 74}
        tk_table = Treeview(parent, show="headings", columns=list(columns), bootstyle="default")
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        tk_table.place(relx=0.0000, rely=0.2857, relwidth=0.6818, relheight=0.6593)
        self.create_bar(parent, tk_table, True, False, 0, 130, 750, 300, 1100, 455)
        tk_table.tag_bind("Link", "<Button-1>", self.open_link_02)
        return tk_table

    def __tk_scale_scale(self, parent):
        scale = Scale(parent, orient=HORIZONTAL, bootstyle="dark", from_=0.1, to=0.9)
        scale.place(relx=0.0909, rely=0.1758, relwidth=0.2727, relheight=0.0659)
        return scale

    def __tk_label_label_price(self, parent):
        label = Label(parent, text="价格", anchor="center", bootstyle="default")
        label.place(relx=0.0273, rely=0.1758, relwidth=0.0455, relheight=0.0659)
        return label

    def __tk_label_label_sale(self, parent):
        label = Label(parent, text="销量", anchor="center", bootstyle="default")
        label.place(relx=0.3818, rely=0.1758, relwidth=0.0455, relheight=0.0659)
        return label

    def __tk_label_label_set(self, parent):
        label = Label(parent, text="评分比重设定", anchor="center", bootstyle="default")
        label.place(relx=0.4545, rely=0.1758, relwidth=0.0909, relheight=0.0659)
        return label

    def __tk_button_check_button(self, parent):
        btn = Button(parent, text="查看", takefocus=False, bootstyle="secondary")
        btn.place(relx=0.5682, rely=0.1758, relwidth=0.0818, relheight=0.0659)
        return btn

    def __tk_label_lw568fv5(self, parent):
        label = Label(parent, text="商品活动评分依据", anchor="center", bootstyle="default")
        label.place(relx=0.7182, rely=0.1758, relwidth=0.1091, relheight=0.0659)
        return label

    def __tk_label_lw56bq01(self, parent):
        label = Label(parent, text="商品活动提升比重", anchor="center", bootstyle="default")
        label.place(relx=0.7182, rely=0.5055, relwidth=0.1091, relheight=0.0659)
        return label

    def __tk_select_box_percent_set_box(self, parent):
        cb = Combobox(parent, state="readonly", bootstyle="secondary")
        cb['values'] = ("低", "中", "高")
        cb.place(relx=0.7364, rely=0.6374, relwidth=0.0818, relheight=0.0659)
        return cb

    def __tk_check_button_check_button_01(self, parent):
        cb = Checkbutton(parent, text="免邮", bootstyle="secondary")
        cb.place(relx=0.7364, rely=0.2857, relwidth=0.0818, relheight=0.0659)
        return cb

    def __tk_check_button_check_button_02(self, parent):
        cb = Checkbutton(parent, text="自营", bootstyle="secondary")
        cb.place(relx=0.7364, rely=0.3956, relwidth=0.0818, relheight=0.0659)
        return cb


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_search_button.bind('<Button-1>', self.ctl.start_crawler)
        self.tk_button_file_choose_01.bind('<Button-1>', self.ctl.choose_file_01)
        self.tk_button_file_choose_02.bind('<Button-1>', self.ctl.choose_file_02)
        self.tk_button_cookie_reset.bind('<Button-1>', self.ctl.get_cookie)
        self.tk_button_hot_item.bind('<Button-1>', self.ctl.show_top_10_by_price_group)
        self.tk_button_range_sale.bind('<Button-1>', self.ctl.show_sales_by_price_range)
        self.tk_button_range_quantity.bind('<Button-1>', self.ctl.count_products_by_price_range)
        self.tk_button_hot_shop.bind('<Button-1>', self.ctl.analyze_store_data)
        self.tk_button_file_choose_03.bind('<Button-1>', self.ctl.choose_file_03)
        self.tk_button_check_button.bind('<Button-1>', self.ctl.data_show)
        pass

    def __style_config(self):
        sty = Style()
        sty.configure(self.new_style(self.tk_button_search_button), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_file_choose_01), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_file_choose_02), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_pages), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_cookie_reset), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_hot_item), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_range_sale), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_range_quantity), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_hot_shop), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_file_choose_03), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_label_price), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_label_sale), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_label_set), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_button_check_button), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_lw568fv5), font=("微软雅黑", -12))
        sty.configure(self.new_style(self.tk_label_lw56bq01), font=("微软雅黑", -12))
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
