import requests,pytest,jsonpath,allure,os
from xToolkit import xfile
from string import Template
from gobal_value import g_var

# 1. 读取excel,并且把读出来的数据转换成列表
case_list = xfile.read("接口测试用例.xls").excel_to_dict(sheet=1)
print(case_list)

"""
最简单的框架封装思想
问题：我还要写个购物车接口怎么办？ token 全局变量
订单接口 -- 商品接口信息？
结算接口 -- 订单信息？
xxx --  另外的接口信息呢？1500个接口
用一个对象去做全局变量
"""

# eval 这个函数，会自动按你的数据格式，格式化掉对应的数据 () []
# pytest有一个对应的方式 参数化机制
# 自动循环 DDT
@pytest.mark.parametrize("case_info", case_list)
def test_case_exec(case_info):  # 把这个列表传进来

    url = case_info["接口URL"]
    dic = g_var().show_dict()
    if "$" in url:
        url = Template(url).substitute(dic)

    rep = requests.request(
        url=url,
        method=case_info["请求方式"],
        params=eval(case_info["URL参数"]),
        data =eval(case_info["JSON参数"])
    )

    # 数据写入到对象中去
    if case_info['提取参数'] != None or case_info['提取参数'] !='':
        lst = jsonpath.jsonpath(rep.json(),'$..'+case_info['提取参数'])
        g_var().set_dict(case_info['提取参数'],lst[0])

    assert rep.status_code == case_info["预期状态码"]

    # 数据库断言 目的是校验 开发写的SQL是不是正确
    # 是否存在 逻辑关系  huace_xm sql  huace_xm
    # 返回结果做对比  --找(核心数据) 主键 id 唯一值 特写的数据
    # locust  jmeter loadrunner -- 找问题，调优 不是曲线图能调的


"""if __name__ == '__main__':
    # pytest的启动命令
    pytest.main(['test_framework.py','-vs','--alluredir=allure_results'])
    os.system('allure generate allure_results -o 测试报告 --clean')
"""