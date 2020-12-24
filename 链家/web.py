import json
from flask import Flask
from flask import render_template, send_file
from pyecharts.charts import Radar, Line, Bar, Map, Pie, Funnel, WordCloud, Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType, SymbolType

app = Flask(__name__)


@app.route("/", methods=['GET'])
def echarts():
    """
    echarts图表界面
    """
    return send_file("echarts.html")


@app.route("/api/charts", methods=['GET'])
def _get_charts():
    """
    获取图表json字符串
    """
    return get_charts()


DATA_PATH = 'data.json'  # 房源json数据路径


def get_charts() -> str:
    data = {}

    with open(DATA_PATH, 'r') as f:  # 读取房源json数据
        data = json.load(f)  # 转为字典

    # 数字-月份 映射
    num_to_word = {'01': '一月', '02': '二月', '03': '三月', '04': '四月', '05': '五月', '06': '六月',
                   '07': '七月', '08': '八月', '09': '九月', '10': '十月', '11': '十一月', '12': '十二月'}
    month_lis = []
    month_num_lis = []
    date = data['date']
    for m in date:
        month_lis.append(num_to_word[m])
        month_num_lis.append(date[m])

    dis_lis = []
    district = data['district']
    for d in district:
        t = ()
        t = t+(d+"区",)
        t = t+(district[d],)
        dis_lis.append(t)

    price = data['price']
    price_lis = []
    price_num_lis = []
    for p in price:
        price_lis.append((p+'万'))
        price_num_lis.append(price[p])

    # 各区成交量地图
    map_ = Map()
    map_.add("成交数", dis_lis, "南京")
    map_.set_global_opts(title_opts=opts.TitleOpts(title="南京市各区二手房成交数", subtitle="包含10个主城区，数据从2012年开始，高淳区暂无数据"), visualmap_opts=opts.VisualMapOpts(max_=13000, is_piecewise=True),
                        toolbox_opts=opts.ToolboxOpts(),)

    # 各月成交量柱状图+折线图
    bar = Bar()
    bar.add_xaxis(month_lis)
    bar.add_yaxis('成交数', month_num_lis)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="南京市各月二手房成交数", subtitle="包含10个主城区，数据从2012年开始"),
                        toolbox_opts=opts.ToolboxOpts(), xaxis_opts=opts.AxisOpts(name="月份"))
    line = Line()
    line.add_xaxis(month_lis)
    line.add_yaxis("成交数", month_num_lis)
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar.overlap(line)
    # c.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    #     data=[opts.MarkPointItem(type_="max",name="最大值")]
    #     ))

    dis_lis = []
    for d in district:
        t = ()
        t = t+(d,)
        t = t+(district[d],)
        dis_lis.append(t)

    # 各区成交量饼状图
    pie = Pie()
    pie.add("", dis_lis)
    pie.set_global_opts(title_opts=opts.TitleOpts(
        title="南京市各区二手房成交数", subtitle="包含10个主城区，数据从2012年开始"), toolbox_opts=opts.ToolboxOpts())
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    # 成交价格区间柱状图
    bar2 = Bar()
    bar2.add_xaxis(price_lis)
    bar2.add_yaxis('成交数', price_num_lis, color="blue")
    bar2.set_global_opts(title_opts=opts.TitleOpts(title="南京市二手房成交价格区间", subtitle="包含10个主城区，数据从2012年开始"),
                         toolbox_opts=opts.ToolboxOpts())

    price_per_square_dis = data['price_per_square_dis']

    # 各年份各区成交量
    dis_lis = []
    lis_2019 = []
    lis_2018 = []
    lis_2017 = []
    for dis in price_per_square_dis:
        dis_lis.append(dis)
        lis_2019.append(price_per_square_dis[dis]['2019'])
        lis_2018.append(price_per_square_dis[dis]['2018'])
        try:
            lis_2017.append(price_per_square_dis[dis]['2017'])
        except:
            lis_2017.append(0)

    # 各区今年成交量折线图
    line = Line()
    line.add_xaxis(dis_lis)
    line.add_yaxis('2019', lis_2019)
    line.add_yaxis('2018', lis_2018)
    line.add_yaxis('2017', lis_2017)
    line.set_global_opts(title_opts=opts.TitleOpts(title="南京市各区二手房每平米单价平均值（元）", subtitle="包含2017、2018、2019三个年份"),
                         toolbox_opts=opts.ToolboxOpts(), xaxis_opts=opts.AxisOpts(name="区"))

    # 建筑面积区间漏斗图
    area_lis = []
    area = data['area']
    for a in area:
        t = ()
        t = t+(a+"m²",)
        t = t+(area[a],)
        area_lis.append(t)

    funnel = Funnel()
    funnel.add("面积（平米）", area_lis)
    funnel.set_global_opts(title_opts=opts.TitleOpts(title="南京市二手房面积区间"))

    resblock = data['resblock']

    # 各区成交量词云图
    wordcloud = WordCloud()
    wordcloud.add("成交数", resblock, shape=SymbolType.DIAMOND,
                  word_size_range=[20, 100])
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(
        title="南京市二手房最受欢迎小区", subtitle="选取成交量最高的30个小区"), toolbox_opts=opts.ToolboxOpts())

    # pie2 = Pie()
    # pie2.add("", resblock)
    # pie2.set_global_opts(title_opts=opts.TitleOpts(
    #     title="南京市二手房受欢迎小区", subtitle=""), toolbox_opts=opts.ToolboxOpts())
    # pie2.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    # page=Page(layout=Page.SimplePageLayout)
    # page.add(bar)
    # page.add(pie)
    # page.add(wordcloud)
    # page.add(line)
    # page.add(bar2)
    # page.add(funnel)
    # page.add(map)
    # page.render()

    dic = {}
    dic['date'] = json.loads(bar.dump_options_with_quotes())  # json先转字典
    dic['district'] = json.loads(pie.dump_options_with_quotes())  # json先转字典
    dic['price'] = json.loads(bar2.dump_options_with_quotes())  # json先转字典
    dic['price_per_square_dis'] = json.loads(
        line.dump_options_with_quotes())  # json先转字典
    dic['area'] = json.loads(funnel.dump_options_with_quotes())  # json先转字典
    dic['map'] = json.loads(map_.dump_options_with_quotes())  # json先转字典
    dic['resblock'] = json.loads(
        wordcloud.dump_options_with_quotes())  # json先转字典

    ret = json.dumps(dic)
    return ret


app.run(host='127.0.0.1', debug=True, port=80)
