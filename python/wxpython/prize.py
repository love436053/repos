#!/usr/bin/python
# coding:utf-8

import wx
import os
import sys
import time
import random
import wx.grid

class PrizeWindow(wx.Frame):
    def __init__(self, parent, title):
        super(PrizeWindow, self).__init__(parent = parent,
                                         title = title,
                                         size = (600, 450),
                                         name = os.path.basename(sys.argv[0]).split('.')[0])

        self.title = title
        self.total_people = {}
        self.cur_people = {}
        self.prize_people = {}
        self.last_prize_people = {}
        self.image = None
        self.file_name = None
        self.sava_flag = True
        self.repeat_prize_flag = False
        self.image_fill_flag = True

        self.window_init()
        self.event_init()

        self.SetBackgroundColour('#ADEAEA')

        self.Centre()
        self.Show()

    def window_init(self):

        self.prize_num = [str(x+1) for x in range(15)]
        self.prize_level = [unicode('特等奖', 'utf-8'),
                            unicode('一等奖', 'utf-8'),
                            unicode('二等奖', 'utf-8'),
                            unicode('三等奖', 'utf-8'),
                            unicode('四等奖', 'utf-8'),
                            unicode('五等奖', 'utf-8')]

        self.menu_bar_init()
        self.form_init()
        self.status_bar_init()

    def menu_bar_init(self):
        self.menu = [
            (unicode('&文件', 'utf-8'), (  # 一级菜单项
                (unicode('&打开\tAlt+O', 'utf-8'),
                 unicode('加载参与抽奖人员名单', 'utf-8'),
                 wx.ITEM_NORMAL,
                 self.open_event),  # 二级菜单项
                (unicode('&保存\tCtrl+S', 'utf-8'),
                 unicode('保存中奖人员名单', 'utf-8'),
                 wx.ITEM_NORMAL,
                 self.save_as_event),
                ("", "", ""),  # 分割线
                (unicode('&退出', 'utf-8'),
                 unicode('退出', 'utf-8'),
                 wx.ITEM_NORMAL,
                 self.quit_event))),
            (unicode('&设置', 'utf-8'), (
                (unicode('&重复中奖', 'utf-8'),
                 unicode('是否可以重复中奖', 'utf-8'),
                 wx.ITEM_CHECK,
                 self.draw_rule_event,
                 False),
            )),
            (unicode('&视图', 'utf-8'), (
                (unicode('&状态栏', 'utf-8'),
                 unicode('状态栏', 'utf-8'),
                 wx.ITEM_CHECK,
                 self.status_show_hide_event,
                 True),
            )),
            (unicode('&帮助', 'utf-8'), (
                (unicode('&关于', 'utf-8'),
                 unicode('关于本软件', 'utf-8'),
                 wx.ITEM_NORMAL,
                 self.about_event),
            ))
        ]

        self.menu_bar = wx.MenuBar()
        for each_menu in self.menu:
            self.menu_bar.Append(self.menu_create(each_menu[1]), each_menu[0])
        self.SetMenuBar(self.menu_bar)

    def menu_create(self, menu):
        top_menu = wx.Menu()  # 一级菜单

        for each_menu in menu:
            if len(each_menu) == 2:  # 三级菜单
                sub_menu = self.menu_create(each_menu[1])
                top_menu.AppendMenu(wx.NewId(), each_menu[0], sub_menu)
            else:  # 二级菜单
                if each_menu[0]:
                    menu = top_menu.Append(wx.NewId(), each_menu[0], each_menu[1], kind = each_menu[2])
                    self.Bind(wx.EVT_MENU, each_menu[3], menu)

                    if each_menu[2] == wx.ITEM_CHECK:
                        menu.Check(each_menu[4])
                        # top_menu.Check(menu.GetId(), each_menu[4])
                else:
                    top_menu.AppendSeparator()

        return top_menu

    def form_init(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.button_init()

        self.panel_init()

        self.vbox.Add((-1, 10))
        self.vbox.Add(self.button_vbox,
                      flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                      border = 5,
                      proportion = 0)

        self.vbox.Add((-1, 10))
        self.vbox.Add(self.panel_vbox,
                      flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                      border = 5,
                      proportion = 1)

        self.SetSizer(self.vbox)

    def button_init(self):
        self.button_vbox = wx.BoxSizer(wx.HORIZONTAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)

        text_level = wx.StaticText(self, wx.NewId(), unicode('奖等级别:', 'utf-8'))
        self.ch_level = wx.Choice(self, wx.NewId(), choices = self.prize_level)
        self.ch_level.SetSelection(len(self.prize_level) - 1)
        self.cur_prize_level = self.prize_level[-1]

        box1.Add(text_level, flag = wx.LEFT | wx.ALIGN_CENTER, border = 10)
        box1.Add(self.ch_level, flag = wx.LEFT | wx.ALIGN_CENTER, border = 5)

        text_num = wx.StaticText(self, wx.NewId(), unicode('中奖人数:', 'utf-8'))
        self.ch_num = wx.Choice(self, wx.NewId(), choices = self.prize_num)
        self.ch_num.SetSelection(len(self.prize_num) - 1)
        self.cur_prize_num = self.prize_num[-1]

        box2.Add(text_num, flag = wx.LEFT | wx.ALIGN_CENTER, border = 10)
        box2.Add(self.ch_num, flag = wx.LEFT | wx.ALIGN_CENTER, border = 5)

        self.bt_start = wx.Button(self, wx.NewId(), label = unicode('开始', 'utf-8'))
        self.bt_stop = wx.Button(self, wx.NewId(), label = unicode('停止', 'utf-8'))
        self.bt_cancel = wx.Button(self, wx.NewId(), label = unicode('撤销', 'utf-8'))

        self.bt_start.SetToolTipString(unicode('当前奖等开始抽奖', 'utf-8'))
        self.bt_start.SetToolTipString(unicode('当前奖等抽奖完成', 'utf-8'))
        self.bt_cancel.SetToolTipString(unicode('撤销上次抽奖信息', 'utf-8'))

        self.button_vbox.Add(box1,
                             flag = wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER,
                             proportion = 1,
                             border = 5)
        self.button_vbox.Add(box2,
                             flag = wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER,
                             proportion = 1,
                             border = 5)

        self.button_vbox.Add(self.bt_start,
                             flag = wx.LEFT | wx.SHAPED | wx.ALIGN_CENTER,
                             proportion = 1,
                             border = 5)
        self.button_vbox.Add(self.bt_stop,
                             flag = wx.LEFT | wx.SHAPED | wx.ALIGN_CENTER,
                             proportion = 1,
                             border = 5)
        self.button_vbox.Add(self.bt_cancel,
                             flag = wx.LEFT | wx.RIGHT | wx.SHAPED | wx.ALIGN_CENTER,
                             proportion = 1,
                             border = 5)

    def panel_init(self):
        self.panel_vbox = wx.BoxSizer(wx.HORIZONTAL)

        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(len(self.prize_num), 1)
        self.grid.SetLabelBackgroundColour('White')
        self.grid.SetCellHighlightColour('Blue')
        self.grid.SetGridLineColour('Red')
        self.grid.SetRowLabelSize(40)
        self.grid.SetColSize(0, 100)

        self.grid.SetColLabelValue(0, unicode('中奖人员', 'utf-8'))
        self.grid_clean()

        self.panel = wx.Panel(self, wx.NewId(), style = wx.FULL_REPAINT_ON_RESIZE)

        self.panel_vbox.Add(self.grid,
                            flag = wx.LEFT | wx.RIGHT | wx.TOP,
                            proportion = 0,
                            border = 10)
        self.panel_vbox.Add(self.panel,
                            flag = wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND,
                            proportion = 1,
                            border = 10)


    def grid_clean(self):
        for row in range(len(self.prize_num)):
            self.grid.SetReadOnly(row, 0)
            self.grid.SetCellValue(row, 0, '')
            self.grid.SetCellTextColour(row, 0, 'Red')
            self.grid.SetCellBackgroundColour(row, 0, 'Green')

    def status_bar_init(self):
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(3)
        self.status_bar.SetStatusWidths([-3, -2, -2])

        self.status_bar.SetStatusText(unicode('鼠标位置: 0,0', 'utf-8'), 1)
        self.status_bar.SetStatusText(unicode('窗口位置: 0,0', 'utf-8'), 2)

    def event_init(self):
        self.Bind(wx.EVT_CHOICE, self.choice_level_event, self.ch_level)
        self.Bind(wx.EVT_CHOICE, self.choice_num_event, self.ch_num)
        self.bt_start.Bind(wx.EVT_BUTTON, self.start_event)
        self.bt_stop.Bind(wx.EVT_BUTTON, self.stop_event)
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.cancel_event)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.grid_event)
        self.Bind(wx.EVT_SIZE, self.window_size_event)
        self.Bind(wx.EVT_ICONIZE, self.window_size_event) # 最小化事件
        self.Bind(wx.EVT_MAXIMIZE, self.window_size_event) # 最大化事件
        self.Bind(wx.EVT_PAINT, self.window_paint_event)
        self.Bind(wx.EVT_CLOSE, self.window_close_event) # 关闭事件

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_event, self.timer) # 定时器事件

        for child in self.GetChildren():
            for widget in child.GetChildren():
                widget.Bind(wx.EVT_MOVE, self.move_event) # 窗口移动事件
                widget.Bind(wx.EVT_MOTION, self.move_event) # 鼠标移动事件
            child.Bind(wx.EVT_MOVE, self.move_event)
            child.Bind(wx.EVT_MOTION, self.move_event)
        self.Bind(wx.EVT_MOVE, self.move_event)
        self.Bind(wx.EVT_MOTION, self.move_event)

    #     self.panel.Bind(wx.EVT_LEFT_DOWN, self.test)
    #
    # def test(self, event):
    #     print 'left down on', wx.FindWindowById(event.GetId()).GetLabel()

    def open_event(self, event):
        file_wildcard = "employee file(*.txt)|*.txt|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            unicode('打开文件', 'utf-8'),
                            os.getcwd(),
                            style = wx.OPEN,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name = dlg.GetPath()
            self.file_path = os.path.dirname(self.file_name)
            self.list_init(self.file_name)
            self.SetTitle(self.title + ' ' + self.file_name)
        dlg.Destroy()

    def save_as_event(self, event):
        file_wildcard = "prize file(*.txt)|*.txt|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            unicode('保存文件', 'utf-8'),
                            os.getcwd(),
                            style = wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            if not os.path.splitext(dlg.GetPath())[1]:  # 如果没有文件名后缀
                self.file_name = dlg.GetPath() + '.txt'
            else:
                self.file_name = dlg.GetPath()

            self.prize_file_save()
            self.SetTitle(self.title + ' ' + self.file_name)
        dlg.Destroy()

    def prize_file_save(self):
        with open(self.file_name, 'w') as fp:
            for level in self.prize_people.keys():
                fp.write(level.encode('gbk') + ':\n')
                for people in self.prize_people[level]:
                    fp.write(people + '\n')
                fp.write('\n')

        self.sava_flag = True

    def quit_event(self, event):
        self.save_as_event(event)
        self.Destroy()

    def draw_rule_event(self, event):
        if self.FindItemInMenuBar(event.GetId()).IsChecked():
            self.repeat_prize_flag = True
        else:
            self.repeat_prize_flag = False

    def status_show_hide_event(self, event):
        if self.FindItemInMenuBar(event.GetId()).IsChecked():
            self.status_bar.Show()
            #print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' show'
        else:
            self.status_bar.Hide()
            #print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' hide'

        self.Refresh()

    def about_event(self, event):
        description = '''盒子支付年会抽奖程序'''.decode('utf-8')

        licence = """File Hunter is free software; you can redistribute
                        it and/or modify it under the terms of the GNU General Public License as
                        published by the Free Software Foundation"""

        info = wx.AboutDialogInfo()
        info.SetVersion('2.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2007 - 2016 liujie@iboxpay.com')
        info.SetWebSite('http://www.iboxpay.com/')
        info.SetLicence(licence)
        info.AddDeveloper('liujie@iboxpay.com')
        info.AddDocWriter('liujie@iboxpay.com')
        info.AddArtist('liujie@iboxpay.com')
        info.AddTranslator('liujie@iboxpay.com')

        wx.AboutBox(info)

    def choice_level_event(self, event):
        self.cur_prize_level = event.GetString()

    def choice_num_event(self, event):
        self.cur_prize_num = event.GetString()

    def start_event(self, event):
        if not self.draw_check():
            return

        self.grid_clean()
        self.grid.SetColLabelValue(0, self.cur_prize_level)

        self.timer.Start(100)

    def timer_event(self, event):
        for i in range(int(self.cur_prize_num)):
            id = random.choice(self.cur_people.keys())
            self.grid.SetCellValue(i, 0, id)
            if i == 0:
                self.image_show(id)

    def stop_event(self, event):
        if not self.draw_check():
            return

        self.timer.Stop()

        self.last_prize_people = {}
        self.last_prize_people[self.cur_prize_level] = []
        self.last_prize_people['repeat_prize_flag'] = self.repeat_prize_flag

        if not self.prize_people.has_key(self.cur_prize_level):
            self.prize_people[self.cur_prize_level] = []

        for i in range(int(self.cur_prize_num)):
            people = random.choice(self.cur_people.keys())
            self.grid.SetCellValue(i, 0, people)
            self.cur_people.pop(people)
            self.prize_people[self.cur_prize_level].append(people)
            self.last_prize_people[self.cur_prize_level].append(people)

        if self.repeat_prize_flag:
            for people in self.prize_people[self.cur_prize_level]:
                self.cur_people[people] = self.total_people[people]

        self.sava_flag = False

    def draw_check(self):
        if not self.file_name:
            self.soft_warn(unicode('抽奖人员名单尚未装载', 'utf-8'))
            return False

        if len(self.cur_people) < int(self.cur_prize_num):
            self.soft_warn(unicode('当前参与抽奖人数小于奖项个数', 'utf-8'))
            return False

        return True

    def cancel_event(self, event):
        if len(self.last_prize_people) == 0:
            return

        dlg = wx.MessageDialog(self,
                               unicode('确认撤销上轮抽奖数据?', 'utf-8'),
                               unicode('提示', 'utf-8'),
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() != wx.ID_YES:
            event.Veto()

        dlg.Destroy()

        repeat_prize_flag = self.last_prize_people.pop('repeat_prize_flag')
        if len(self.last_prize_people) > 0:
            for people in self.last_prize_people.values()[0]:
                if not repeat_prize_flag:
                    self.cur_people[people] = self.total_people[people]
                self.prize_people[self.last_prize_people.keys()[0]].remove(people)

        self.last_prize_people = {}

    def soft_warn(self, message):
        dlg = wx.MessageDialog(self,
                               message,
                               unicode('提示', 'utf-8'),
                               wx.OK | wx.YES_DEFAULT | wx.ICON_QUESTION)

        dlg.ShowModal()
        dlg.Destroy()
        return

    def list_init(self, file_list):
        self.cur_people = {}

        with open(file_list, 'r') as fp:
            for line in fp.readlines():
                list = line.strip().split()

                if len(list) != 2:
                    continue

                self.cur_people[list[0]] = list[1]

        self.total_people = self.cur_people.copy()

        self.soft_warn(unicode('参与抽奖人员装载完成, 人员总数:%d', 'utf-8') % len(self.total_people))

    def grid_event(self, event):
        if not self.total_people:
            return

        if wx.grid.EVT_GRID_CELL_LEFT_CLICK.typeId == event.EventType:
            self.image_show(self.grid.GetCellValue(event.GetRow(), 0))
        elif wx.grid.EVT_GRID_LABEL_LEFT_CLICK.typeId == event.EventType:
            self.image_show(self.grid.GetCellValue(event.GetRow(), 0))

        event.Skip()

    def image_show(self, id):
        img_file = os.path.join(self.file_path, self.total_people[id])

        if 0 == len(id) or not os.path.exists(img_file):
            return

        if self.image:
            #self.image.Hide()
            self.image.Destroy()

        img = None
        prefix, suffix = img_file.split('.')
        if suffix == 'jpg' or suffix == 'jpeg':
            img = wx.Image(img_file, wx.BITMAP_TYPE_JPEG)
        elif suffix == 'png':
            img = wx.Image(img_file, wx.BITMAP_TYPE_PNG)
        elif suffix == 'pnm':
            img = wx.Image(img_file, wx.BITMAP_TYPE_PNM)

        if self.image_fill_flag:
            img.Rescale(self.panel.GetSize()[0], self.panel.GetSize()[1])
        self.image = wx.StaticBitmap(self.panel, -1, img.ConvertToBitmap())

        self.image.SetToolTipString(prefix)
        self.image.Center()
        self.Refresh()

    def move_event(self, event):
        if wx.EVT_MOTION.typeId == event.EventType:
            self.status_bar.SetStatusText(unicode('鼠标坐标: ', 'utf-8') + str(event.GetPositionTuple()), 1)
        elif wx.EVT_MOVE.typeId == event.EventType:
            self.status_bar.SetStatusText(
                unicode('窗口位置: %s, %d' % (event.GetPosition()[0], event.GetPosition()[1]), 'utf-8'), 2)
        else:
            pass

        event.Skip()

    def window_size_event(self, event):
        # print wx.EVT_SIZE.typeId, wx.EVT_ICONIZE.typeId, wx.EVT_MAXIMIZE.typeId
        # print event.EventType, self.grid.GetSize()
        self.grid.Refresh()

        event.Skip()

    def window_paint_event(self, event):
        self.Refresh()

        event.Skip()

    def window_close_event(self, event):
        if self.sava_flag:
            self.Destroy()
            return

        dlg = wx.MessageDialog(self,
                               unicode('中奖人员名单尚未保存, 确认退出?', 'utf-8'),
                               unicode('提示', 'utf-8'),
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
            self.Destroy()
        else:
            dlg.Destroy()
            event.Veto()

if __name__ == '__main__':
    app = wx.App()
    PrizeWindow(None, title = unicode('盒子支付年会抽奖', 'utf-8'))
    app.MainLoop()