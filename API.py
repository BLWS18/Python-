import pandas as pd
data = pd.read_excel('test_baidu.xlsx')
data
import json
from urllib.request import urlopen, quote
import requests
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '你的百度地图ak' # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    address = quote(address) # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat,lng   # 纬度 latitude   ，   经度 longitude  ，
for indexs in data.index:
    get_location = getlnglat(data.loc[indexs,'圈定区域'])
    get_lat = get_location[0]
    get_lng = get_location[1]
    data.loc[indexs,'纬度'] = get_lat
    data.loc[indexs,'经度'] = get_lng

data
data_html = pd.DataFrame(columns=['content'])

for indexs in data.index:
    data_html.loc[indexs,'content'] = '{' + \
                                      '"lat":' + str(data.loc[indexs,'纬度']) + ',' +  \
                                      '"lng":' + str(data.loc[indexs,'经度']) + ',' +  \
                                      '"quyu":' + '"' + str(data.loc[indexs,'圈定区域']) +'"' +   \
                                      '}' + ','

data_html.to_csv ("data_html.csv",encoding="gbk")
data_html

#百度官网HTML示例
'''
<!DOCTYPE HTML>
<html>
<head>
  <title>加载海量点</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
  <style type="text/css">
    html,body{
        margin:0;
        width:100%;
        height:100%;
        background:#ffffff;
    }
    #map{
        width:100%;
        height:100%;
    }
    #panel {
        position: absolute;
        top:30px;
        left:10px;
        z-index: 999;
        color: #fff;
    }
    #login{
        position:absolute;
        width:300px;
        height:40px;
        left:50%;
        top:50%;
        margin:-40px 0 0 -150px;
    }
    #login input[type=password]{
        width:200px;
        height:30px;
        padding:3px;
        line-height:30px;
        border:1px solid #000;
    }
    #login input[type=submit]{
        width:80px;
        height:38px;
        display:inline-block;
        line-height:38px;
    }
  </style>
  <script type="text/javascript" src="//api.map.baidu.com/api?v=2.0&ak=您的密钥"></script>
  <script type="text/javascript" src="/jsdemo/data/points-sample-data.js"></script>
</head>
<body>
    <div id="map"></div>
    <script type="text/javascript">
    var map = new BMap.Map("map", {});                        // 创建Map实例
    map.centerAndZoom(new BMap.Point(105.000, 38.000), 5);     // 初始化地图,设置中心点坐标和地图级别
    map.enableScrollWheelZoom();                        //启用滚轮放大缩小
    if (document.createElement('canvas').getContext) {  // 判断当前浏览器是否支持绘制海量点
        var points = [];  // 添加海量点数据
        for (var i = 0; i < data.data.length; i++) {
          points.push(new BMap.Point(data.data[i][0], data.data[i][1]));
        }
        var options = {
            size: BMAP_POINT_SIZE_SMALL,
            shape: BMAP_POINT_SHAPE_STAR,
            color: '#d340c3'
        }
        var pointCollection = new BMap.PointCollection(points, options);  // 初始化PointCollection
        pointCollection.addEventListener('click', function (e) {
          alert('单击点的坐标为：' + e.point.lng + ',' + e.point.lat);  // 监听点击事件
        });
        map.addOverlay(pointCollection);  // 添加Overlay
    } else {
        alert('请在chrome、safari、IE8+以上浏览器查看本示例');
    }
  </script>
</body>
</html>
'''