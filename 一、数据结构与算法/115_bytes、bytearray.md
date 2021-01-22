
  * [bytes、bytearray](#bytesbytearray)
     * [ASCII码](#ascii码)
        * [ASCII扩展表](#ascii扩展表)
        * [多种编码表](#多种编码表)
        * [双字节编码表](#双字节编码表)
        * [统一的多字节编码表](#统一的多字节编码表)
        * [utf-8](#utf-8)
           * [GBk](#gbk)
        * [编码表](#编码表)
     * [bytes](#bytes)
        * [字符串与bytes互相转换](#字符串与bytes互相转换)
           * [encode()](#encode)
           * [decode()](#decode)
        * [bytes定义](#bytes定义)
           * [<strong>可迭代对象</strong>](#可迭代对象)
        * [bytes的类方法](#bytes的类方法)
        * [hex()](#hex)
        * [索引](#索引)
     * [bytearray](#bytearray)
        * [一些定义概念](#一些定义概念)
        * [和bytes类型相同的一些方法](#和bytes类型相同的一些方法)
           * [类方法](#类方法)
           * [hex()](#hex-1)
           * [索引](#索引-1)
        * [extend()](#extend)
        * [append()](#append)
        * [pop()](#pop)
        * [remove()](#remove)
     * [字节序](#字节序)
        * [通识](#通识)
        * [int和字节序列的转化](#int和字节序列的转化)
           * [字节序转int](#字节序转int)
           * [int转字节序](#int转字节序)
     * [切片](#切片)
        * [用法](#用法)
        * [切片赋值](#切片赋值)
     * [学过的线性结构](#学过的线性结构)
        * [线性结构特性](#线性结构特性)

## bytes、bytearray

python3引入的两个新概念
其中：

- bytes是不可变字节序列
- bytearray是可变的字节数组



### ASCII码

ASCII（American Standard Code For Information Interchange)(美国信息交换标准代码)
是基于拉丁字母的一套**单**字节编码系统  

内存中只能存放数字，而ASCII表将字符用数字代表，这样想要记录字符序列就记录ASCII表对应的数字就可以  

而计算机又是二进制，将ASCII表的hex()进制转换为二进制。  

这样一来，计算机的二进制数字0和1就能代表了字符。  

#### ASCII扩展表

ASCII码表有0-127的选项，一共128个表格  

而在内存中一个字节有8位，一共就有2**8个选择，也就是256个选择  

所以又有人将ASCII的128-255的表格了，也叫做ASCII码扩展表  

#### 多种编码表

各个国家看到了美国的ASCII表，所以纷纷推出了自己的编码表  

但是各个国家的0-127位基本都兼容了ASCII的编码表    

 等到中国引入了编码表的时候，已经太晚太晚了

#### 双字节编码表

前面的单字节编码表已经泛滥了

中国引入编码表的时候，准备用**多**字节编码表，因为中国的字节太多。。。这种表结构也影响力日韩等国家

这就是中国的GBK2312编码表，但是中国日本韩国的国家的编码表也是不统一的。。。

>GB2312-80 是 1980 年制定的中国汉字编码国家标准。共收录 7445 个字符，其中汉字 6763 个。GB2312 兼容标准 ASCII码，采用扩展 ASCII 码的编码空间进行编码，一个汉字占用两个字节，每个字节的最高位为 1。具体办法是：收集了 7445 个字符组成 94*94 的方阵，每一行称为一个“区”，每一列称为一个“位”，区号位号的范围均为 01-94，区号和位号组成的代码称为“区位码”。



#### 统一的多字节编码表

随着国际化的信息化建设，一张统一的编码表迫切需要  

全球编码的发展，逐渐形成了两套编码体系，最后合并成了统一的一张编码体系  

这就是全球统一的编码表`Unicode`，双字节最多有2**16种变化，也就是65536

#### utf-8

utf-8可以将unicode转化为1-6个字节，是一种变长的转化方式，中文大多数都转换成了3字节的长度

##### GBk

```python
b'\xe5\x95\x8a'
>>> '啊'.encode("GBk")
b'\xb0\xa1'
>>> '啊'.encode('utf-8')
b'\xe5\x95\x8a'
```

可以看到，GBK的编码'啊'用了两个字节，而Utf-8用了三个字节。所以windows一直在用GBK,但是如今硬盘白菜价。。，所以还是用utf-8吧

#### 编码表

如果某个页面的字符采用的是Utf-8的编码规范，用gbk或者其他的编码表去解析，那么就会产生乱码

```python
>>> '和我一起学Python3'.encode('utf-8')
b'\xe5\x92\x8c\xe6\x88\x91\xe4\xb8\x80\xe8\xb5\xb7\xe5\xad\xa6Python3'
>>> b'\xe5\x92\x8c\xe6\x88\x91\xe4\xb8\x80\xe8\xb5\xb7\xe5\xad\xa6Python3'.decode('utf-8')
'和我一起学Python3'
>>> b'\xe5\x92\x8c\xe6\x88\x91\xe4\xb8\x80\xe8\xb5\xb7\xe5\xad\xa6Python3'.decode('GBK')
Traceback (most recent call last):
  File "<pyshell#100>", line 1, in <module>
    b'\xe5\x92\x8c\xe6\x88\x91\xe4\xb8\x80\xe8\xb5\xb7\xe5\xad\xa6Python3'.decode('GBK')
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 8: illegal multibyte sequence
```

所以网络传输的字节序列，要用正确的编码表去decode()


对于ASCII表，我们要熟记以下内容

- \\t \\r \\n
- A-Z
- a-z
- 0-9


### bytes

在内存中连续排放的字节序列，每个字节有8位

>字符串是字符序列，而中文是多字节序列，但是人类看的是不同于计算机的。例如十进制数字`60000`这个数字存在计算机中就是多字节存储，在内存中如果不加以区分，我们是无法分辨字节和字符序列，所以高级语言一定要有数据类型！

#### 字符串与bytes互相转换

##### encode()

编码，默认使用utf-8编码表，得到字节序列

```python
>>> 'abc'.encode()
b'abc'
>>> "中国".encode()
b'\xe4\xb8\xad\xe5\x9b\xbd'
>>> type(b'\xe4\xb8\xad\xe5\x9b\xbd')
<class 'bytes'>
```

##### decode()

解码，默认使用utf-8编码表，得到字符序列

```python
>>> b'abc'.decode()
'abc'
>>> b'\xe4\xb8\xad\xe5\x9b\xbd'.decode()
'中国'
```

#### bytes定义

定义一个bytes

```python
>>> 'abc'.encode()
b'abc'
>>> bytes('abc','utf-8')
b'abc'
>>> b'abc'
b'abc'
```

注意！bytes(5)指的是x00,是ascii码的0，八位全是0，不是字符串'0'

```python
>>> bytes(5)
b'\x00\x00\x00\x00\x00'
```

##### **可迭代对象**

对多个ints的可迭代对象

```python
>>> bytes([61])
b'='

>>> hex(61)  #z
'0x3d'

>>> bytes([0x3d])
b'='

>>> bytes(b'=')
b'='
```

注意

```python
>>> b1 = bytes([61])
>>> b1
b'='
>>> b2 = bytes(b1)
>>> b2
b'='
>>> id(b1)
2448563030272
>>> id(b2)
2448563030272
>>> id(b1)==id(b2)
True
```

>[python的坑]
>python对某些常量进行了优化，bytes和str一样属于字面常量



#### bytes的类方法

`bytes.fromhex(str)` , 其中string必须是2个字符的16进制的形式;类似'6162 6a 6b',空格将被忽略


```python
>>> bytes.fromhex('3d')
b'='
>>> bytes.fromhex('61')
b'a'
>>> bytes.fromhex('61626364')
b'abcd'
>>> bytes.fromhex('61 62 63 64')
b'abcd'
```

#### hex()

将bytes转化为16进制，形成字符串

```python
>>> b'abcd'.hex()
'61626364'
```

#### 索引

- 一个一个字节的索引
- 返回的是十进制的int类型的数字！

```python
>>> b'abcd'[0]
97                  # 十进制
>>> b'abcd'[1]
98
>>> hex(97)
'0x61'             # 十六进制
>>> hex(98)
'0x62'
```

### bytearray

可变类型！可以理解为bytes的数组


#### 一些定义概念

- bytearray(b'') 可以增加，然而bytes()不可以增加


- bytearray(int)指定字节的bytearray,被0填充

```python
>>> bytearray(2)
bytearray(b'\x00\x00')
```

- bytearray(iterable_of_ints) -> bytearray[0,255]的int组成的可迭代对象


```python
>>> bytearray(range(1,6))
bytearray(b'\x01\x02\x03\x04\x05')
```

- bytearray(string,encoding[,errors]) -> bytearray 近似于string.encode(),不过返回可变对象



- bytearray(bytes_or_buffer)从一个字节序列或者buffer复制出一个新的可变的bytearray

```python
>>> b = b''
>>> c = bytearray(b)
>>> c
bytearray(b'')
>>> c.append(41)
>>> c
bytearray(b')')
```

#### 和bytes类型相同的一些方法

##### 类方法

```python
>>> bytes.fromhex('2d')
b'-'
>>> bytearray.fromhex('2d')
bytearray(b'-')
```

##### hex()

```python
>>> b'='.hex()
'3d'
>>> bytearray(b'=').hex()
'3d'
```

##### 索引

```python
>>> b'abcd'[0]
97
>>> bytearray(b'abcd')[0]
97
>>>
```


#### extend()

和列表一样，需要放入可迭代对象

```python
>>> b1 = b'a'
>>> b2 = b'b'
>>> b3 = bytearray(b1)
>>> b3
bytearray(b'a')
>>> b3.extend(90)
Traceback (most recent call last):
  File "<pyshell#54>", line 1, in <module>
    b3.extend(90)
TypeError: 'int' object is not iterable
>>> b3.extend([90])             # 和bytes一样，需要放入可迭代对象
>>> b3
bytearray(b'aZ')

>>> b3.extend(range(100,104))
>>> b3
bytearray(b'aZdefg')
```

#### append()

插入整行数，十进制十六进制都可以

```python
>>> b3
bytearray(b'aZdefg')
>>> b3.append(0x90)
>>> b3
bytearray(b'aZdefg\x90')
>>> b3.append(0x41)
>>> b3
bytearray(b'aZdefg\x90A')
```

#### pop()

与列表pop()用法一样

```python
>>> b3.append(42)
>>> b3
bytearray(b'aZdefg\x90A)*')
>>> b3.pop()
42
>>> b3
bytearray(b'aZdefg\x90A)')
>>> b3.pop(0x41)
Traceback (most recent call last):
  File "<pyshell#70>", line 1, in <module>
    b3.pop(0x41)
IndexError: pop index out of range
>>> b3.pop(0)
97
>>> b3
bytearray(b'Zdefg\x90A)')
>>>
```

#### remove()

与列表remove()用法一样

```python
>>> b3
bytearray(b'ZdefgA')
>>> b'A'.hex()
'41'
>>> b3.remove(0x41)
>>> b3
bytearray(b'Zdefg')
```




### 字节序

计算机硬件有两种储存数据的方式：大端字节序（big endian）和小端字节序（little endian）。
举例来说，数值0x2211使用两个字节储存：高位字节是0x22，低位字节是0x11。

- 大端字节序：高位字节在前，低位字节在后，这是人类读写数值的方法。
- 小端字节序：低位字节在前，高位字节在后，即以`0x1122`形式储存。





>计算机处理字节序的时候，不知道什么是高位字节，什么是低位字节。它只知道按顺序读取字节，先读第一个字节，再读第二个字节。
>如果是大端字节序，先读到的就是高位字节，后读到的就是低位字节。小端字节序正好相反。
>理解这一点，才能理解计算机如何处理字节序


**"只有读取的时候，才必须区分字节序，其他情况都不用考虑。"**






#### 通识

- Inter X86 CPU 使用小端模式
- 网络传输，基本都是大端模式
- Windows、Linux使用小端模式
- Mac OS 使用大端模式
- Java虚拟机使用大端模式

> 记不住没关系，单独记住网络传输是大端序




#### int和字节序列的转化







##### 字节序转int

int.from_bytes(bytes, 'big/little')

```python
>>> int.from_bytes(b'abcd')
Traceback (most recent call last):
  File "<pyshell#117>", line 1, in <module>
    int.from_bytes(b'abcd')
TypeError: from_bytes() missing required argument 'byteorder' (pos 2)
```

呕吼，少了byteorder,应该指定字节序

指定大端模式

```python
>>> int.from_bytes(b'abcd','big')
1633837924

>>> hex(1633837924)
'0x61626364'
```

##### int转字节序

`int.to_bytes(length, byteorder, * ,  signed=Flase) -> bytes `

```python
>>> i = 1633837924
>>> i.to_bytes(4,'big')
b'abcd'
```


### 切片

通过索引区间访问线性结构的一段数据

#### 用法

- `sequence[start:end]`表示返回[start,stop)q区间的子序列
- 支持负索引
- start为0可省略
- stop为末尾，可省略
- 超过上界（右边界），就取到末尾，超过下界（左边界），取到开头
- start一定要在stop的左边

> 基本规则与range()函数一致



**[:]表示从头至尾，全部元素被取出，等于copy(),注意深浅拷贝**


```python
>>> b = b'abcd'
>>> b[0:1]
b'a'
>>> b[:]
b'abcd'
>>> b[:3]
b'abc'
>>> b[1:]
b'bcd'
#步长
>>> b[0:3:2]
b'ac'

list('abcdef')[0::3]
['a', 'd']

list('abcdef')[::-1]
['f', 'e', 'd', 'c', 'b', 'a']
```

#### 切片赋值


```python
>>> l = list(b'abcdef')
>>> l
[97, 98, 99, 100, 101, 102]
>>> l[0:2]=(10,)
>>> l
[10, 99, 100, 101, 102]
>>> l
[10, 99, 100, 101, 102]
>>> l[:2]=(1,2,3,4,5,6)
>>> l
[1, 2, 3, 4, 5, 6, 100, 101, 102]
```



### 学过的线性结构

- 列表、元组、字符串、bytes、bytearray、链表
- 不是所有的线性结构访问列表都能提高效率
- 链表通过访问索引效率不高



#### 线性结构特性

- 可迭代的特性 `for ... in `; 可迭代不一定是线性，也可能无序
- len()可以获取长度
- 可以通过索引访问查询
- 可以切片

