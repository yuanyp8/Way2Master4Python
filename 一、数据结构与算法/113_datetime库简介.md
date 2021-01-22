## datetime库简单使用

对日期、时间、时间戳的处理

### datetime类

#### 类方法

datetime.datetime是个类方法
类似于`int`、`str`等，都是一类方法的引用

```python
>>> type(datetime.datetime)
<class 'type'>
>>> type(int)
<class 'type'>

```

##### today()

利用类方法的时间对象  
返回本地时区当前时间的datetime对象

```python
>>> datetime.datetime.today()
datetime.datetime(2020, 1, 8, 13, 38, 46, 655917)

```

##### now(tz=None)

返回当前时区的datetime对象，时间到微秒，如果tz=None，返回和today()一样

```python
>>> import datetime     # 引入模块
>>> datetime.datetime.now()    
datetime.datetime(2020, 1, 8, 13, 34, 34, 879482)
```

##### utcnow()

没有时区的当前时间

```python
datetime.datetime(2020, 1, 8, 13, 39, 41, 756573)
>>> datetime.datetime.utcnow()
datetime.datetime(2020, 1, 8, 5, 39, 51, 640815)
```

##### fromtimestamp(timestamp,tz=None)

从一个时间戳返回一个datetime对象

先再浏览器用js得到一个时间戳


```python
new Date().getTime()
1578462570049
```

得到的结果是放大了1000倍的结果，去掉后三位，用timestamp转化

```python
>>> datetime.datetime.fromtimestamp(1578462570)
datetime.datetime(2020, 1, 8, 13, 49, 30)
```

> 类方法做的就是：没有对象，构造对象

#### datetime对象

##### timestamp()返回一个时间到微秒的时间戳

```python
>>> datetime.datetime.fromtimestamp(1578462570).timestamp()
1578462570.0
```

##### 时间差

```python
>>> d1 = datetime.datetime.now()
>>> d2 = datetime.datetime.now()
>>> d3 = d2.timestamp() -d1.timestamp()
>>> d1
datetime.datetime(2020, 1, 8, 15, 16, 4, 6129)
>>> d2
datetime.datetime(2020, 1, 8, 15, 16, 26, 835832)
>>> d3
22.829703092575073
```

##### 直接构造

直接给出`年,月,日,时,分,秒`来得到一个时间对象

```python
>>> datetime.datetime(2017,12,1,1,2,3,4)
datetime.datetime(2017, 12, 1, 1, 2, 3, 4)
```

### 时间对象的使用方法

#### 解析年月日

year、month、day、weekday()

```python
>>> d = datetime.datetime.now()
>>> d
datetime.datetime(2020, 1, 9, 9, 57, 58, 64721)
>>> d.year,d.month,d.day
(2020, 1, 9)
>>> d.weekday() #这个是老外的时间
3
>>> d.isoweekday() # ISO标准化日期
4
```


#### date()

返回日期的date对象

```python
>>> d
datetime.datetime(2020, 1, 9, 9, 57, 58, 64721)
>>> d.date()
datetime.date(2020, 1, 9)
```

#### time()

返回时间time对象

```python
>>> d.time()
datetime.time(9, 57, 58, 64721)
```

#### replace()

修改并立即返回新的时间

```python
>>> d
datetime.datetime(2020, 1, 9, 9, 57, 58, 64721)
>>> d.replace(2222,2,2)
datetime.datetime(2222, 2, 2, 9, 57, 58, 64721)
>>> d
datetime.datetime(2020, 1, 9, 9, 57, 58, 64721)
```

#### iscalendar()

返回一个三元组（年，周数，周几）

```python
>>> d.isocalendar()
(2020, 2, 4)
```



### 日期格式化

#### 类方法strptime(date_string,format)，返回datetime对象

`string-->>datetime`

```python
>>> datetime.datetime.strptime("2020, 1, 9, 9, 57, 58","%Y, %m, %d, %H, %M, %S")
datetime.datetime(2020, 1, 9, 9, 57, 58)
```


#### 对象方法strftime(format)，返回字符串

`datetime-->>string`

```python
dd = datetime.datetime(2020, 1, 9, 9, 57, 58)
>>> dd.strftime("%Y-%m-%d %H:%M:%S")
'2020-01-09 09:57:58'
```

#### 字符串format函数格式化


```python
>>> dd
datetime.datetime(2020, 1, 9, 9, 57, 58)
>>> a = "{:%Y-%M-%d :%H:%M:%S}".format(dd)
>>> a
'2020-57-09 :09:57:58'
```



#### **附录：python中时间日期格式化符号：**

| 符号 | 说明                                      |
| ---- | ----------------------------------------- |
| `%y` | 两位数的年份表示（00-99）                 |
| `%Y` | 四位数的年份表示（000-9999）              |
| `%m` | 月份（01-12）                             |
| `%d` | 月内中的一天（0-31）                      |
| `%H` | 24小时制小时数（0-23）                    |
| `%I` | 12小时制小时数（01-12）                   |
| `%M` | 分钟数（00=59）                           |
| `%S` | 秒（00-59）                               |
| `%a` | 本地简化星期名称                          |
| `%A` | 本地完整星期名称                          |
| `%b` | 本地简化的月份名称                        |
| `%B` | 本地完整的月份名称                        |
| `%c` | 本地相应的日期表示和时间表示              |
| `%j` | 年内的一天（001-366）                     |
| `%p` | 本地A.M.或P.M.的等价符                    |
| `%U` | 一年中的星期数（00-53）星期天为星期的开始 |
| `%w` | 星期（0-6），星期天为星期的开始           |
| `%W` | 一年中的星期数（00-53）星期一为星期的开始 |
| `%x` | 本地相应的日期表示                        |
| `%X` | 本地相应的时间表示                        |
| `%Z` | 当前时区的名称                            |
| `%%` | %号本身                                   |



