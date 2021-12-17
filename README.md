## 基于高德行政区划的API下载中国最新的国, 省, 市, 县四级行政边界，以shp格式存储

使用之前需要先到 https://lbs.amap.com/api/webservice/guide/create-project/get-key 申请key, 建议申请5个, 一行一个放到gaode_web_keys文件中.

### 2021年12月份数据
链接:https://pan.baidu.com/s/15tu8LwOU9sygrnsOKkSLjg 提取码:sgwd


### 使用方式
```
python3 main.py shp文件存储目录
```


### 数据结构
- **china.shp**: 只有一条数据
  - code: 编码/10000
  - name: 名称/中华人民共和国
  - center: 中心点坐标

- **prov.shp**: 省
  - code: 编码
  - name: 名称
  - center: 中心点坐标

- **city.shp**: 市
  - code: 编码
  - name: 名称
  - center: 中心点坐标
  - prov_code: 所属省编码
  - prov_name: 所属省名称
  
- **city.shp**: 县
  - code: 编码
  - name: 名称
  - center: 中心点坐标
  - prov_code: 所属省编码
  - prov_name: 所属省名称
  - city_code: 所属市编码
  - city_name: 所属市名称
