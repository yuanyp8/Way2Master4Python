## IO

- IO一般指两部分，包括文件IO和网络IO
- IO一般都是系统的瓶颈

### 文件IO常用操作

```python
----常用----
open 打开
read 读取
write 写入
close 关闭

----不常用----
readline 行读取
readlines 多行读取
seek 文件指针操作
tell 指针位置
```

### open用法

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

- file -- 要操作的文件的路径(包括相对路径和绝对路径),如果直接写文件名，就是当前目录，也是绝对目录
- mode -- 要操作文件的模式，是个缺省值，默认是`r`参考下面

```python
- r:   以只读方式打开，文件必须提前存在，不存在则报错(FileNotFoundError:No such file or directory)
- w:   打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件
- x:   如果文件存在则报错，如果不存在才创建一个空文件并可以写入
- t:   文本模式，打开是文本，也就是字符串
- b:   byte，操作的都是字节
- +:   为r、w、a、x提供缺失的读或写功能，但是，获取文件对象依旧按照rwxa自己的特征，+模式不能单独使用，可以认为它是为前面的模式字符做增强功能
- rb:  以二进制格式打开一个文件，用于只读模式
- r+:  打开一个文件用于读写。文件指针将会放在文件的开头。读完就追加
- w+:  打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件
- a:   打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入
- a+:  打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写
```

- *buffering* 是一个可选的整数，用于设置缓冲策略。传递0以切换缓冲关闭（仅允许在二进制模式下），1选择行缓冲（仅在文本模式下可用），并且>1的整数以指示固定大小的块缓冲区的大小（以字节为单位）。如果没有给出 *buffering* 参数，则默认缓冲策略的工作方式如下:
  - 二进制文件以固定大小的块进行缓冲；使用启发式方法选择缓冲区的大小，尝试确定底层设备的“块大小”或使用 `io.DEFAULT_BUFFER_SIZE`。在许多系统上，缓冲区的长度通常为4096或8192字节。
  - “交互式”文本文件（ `isatty()`返回 `True` 的文件）使用行缓冲。其他文本文件使用上述策略用于二进制文件。
- *encoding* 是用于解码或编码文件的编码的名称。这应该只在文本模式下使用。默认编码是依赖于平台的（不 管 `locale.getpreferredencoding()` 返回何值），但可以使用任何Python支持的 text encoding 。
- *errors* 是一个可选的字符串参数，用于指定如何处理编码和解码错误 - 这不能在二进制模式下使用。可以使用各种标准错误处理程序

#### `read`(*size=-1*)

从流中读取至多 *size* 个字符并以单个 [`str`](stdtypes.html#str) 的形式返回。 如果 *size* 为负值或 `None`，则读取至 EOF。

#### `readline`(*size=-1*)

读取至换行符或 EOF 并返回单个 `str`。 如果流已经到达 EOF，则将返回一个空字符串。

如果指定了 *size* ，最多将读取 *size* 个字符。

#### `tell`()

以不透明数字形式返回当前流的位置。 该数字通常并不代表下层二进制存储中对应的字节数。

#### `write`(*s*)

将字符串 *s* 写入到流并返回写入的字符数。



#### 演示

- 针对一个已存在文件，利用只读查看文件

```python
(blog) (base) [root@10-255-20-221 test]# echo "Hello Python" > test
(blog) (base) [root@10-255-20-221 test]# cat test
Hello Python
(blog) (base) [root@10-255-20-221 test]# python
Python 3.7.4 (default, Aug 13 2019, 20:35:49)
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> f = open('test',mode='r',encoding='utf-8')
>>> f.read()
'Hello Python\n'
>>> f.close()
```

- 以二进制方式读取一个文件，打开内容由字符串转为byte

```python
>>> f = open('test',mode='rb')
>>> f.read()
b'Hello Python\n'
>>> f.close()
```

- 以w方式打开文件，源文件没有创建，有则覆盖

```python
(blog) (base) [root@10-255-20-221 test]# cat test
Hello Python
(blog) (base) [root@10-255-20-221 test]# python
Python 3.7.4 (default, Aug 13 2019, 20:35:49)
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> f = open('test',mode='w')    
>>> f.write('Again print after Hello Python')
30
>>> f
<_io.TextIOWrapper name='test' mode='w' encoding='UTF-8'>
>>> f.read()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
io.UnsupportedOperation: not readable
>>> exit()
(blog) (base) [root@10-255-20-221 test]# cat test
Again print after Hello Python(blog) (base) [root@10-255-20-221 test]#
# 可以看到这个文件被覆盖了，这个方式慎用
```

- x模式，判断文件是否存在并写入数据

```python
>>> f = open('test',mode='x')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileExistsError: [Errno 17] File exists: 'test'
>>> f = open('testq',mode='x')
>>> f.write("My mode is x")
12
>>> f.close()
```


- 追加的模式写入文件，不可读，如果文件不存在也可也创建

```python
>>> f = open('test',mode='a')
>>> f.close()
>>> f = open('test')
>>> f.read()
'Again print after Hello Python'
>>> f1 = open('test',mode='a')
>>> f1.write('\nMy mode is a\n')
14
>>> f1.close()
(blog) (base) [root@10-255-20-221 test]# cat test
Again print after Hello Python
My mode is a
# a 与 w 的区别是w是覆盖，a为追加
```

- 字节模式'b'

```python
>>> f = open('test','wb')
>>> f.write('123'.encode('utf-8'))
3
>>> f.write('教育'.encode())
6
# 由于utf编码，汉字一般是三个字节

>>> f = open('test')
>>> f.read()
'123教育'
>>> f = open('test',encoding='GBK')
>>> f.read()
'123鏁欒偛'
# 这就是乱码的根源
```

> 操作字节的方式不需要考虑编码方式，但是针对文本操作，尤其是中文编码，一定要注意编码方式，utf-8和GBK


- `r+`的模式，就是读增强,注意文件指针

```python
(blog) (base) [root@10-255-20-221 test]# cat test
abcd
(blog) (base) [root@10-255-20-221 test]# python
Python 3.7.4 (default, Aug 13 2019, 20:35:49)
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> f = open('test','r+')
>>> f.read()
'abcd\n'
>>> f.read()
''
>>> f.write('efg')
3
>>> f.close()
>>> exit()
(blog) (base) [root@10-255-20-221 test]# cat test
abcd
```

> r+打开一个文件，如果不加任何操作，就是指针在最开始位置，如果读一遍后，指针就在最后







### 文件指针

`seek`(*offset*, *whence=SEEK_SET*)

将流位置改为给定的偏移位置 *offset*。 具体行为取决于 *whence* 形参。 *whence* 的默认值为 `SEEK_SET`。

- `SEEK_SET` 或 `0`: 从流的开始位置起查找（默认值）；*offset* 必须为 TextIOBase.tell() 所返回的数值或为零。 任何其他 *offset* 值都将导致未定义的行为。
- `SEEK_CUR` 或 `1`: "查找" 到当前位置；*offset* 必须为零，表示无操作（所有其他值均不受支持）。
- `SEEK_END` 或 `2`: 查找到流的末尾；*offset* 必须为零（所有其他值均不受支持）。

以不透明数字形式返回新的绝对位置。

> mode=r，指针起始位置在0
> mode=w，指针起始位置在EOF

#### 字符模式

```python
>>> f = open('tt',mode='r')
>>> f.tell()
0
>>> f.read(0)
''
>>> f.read(1)
'一'
>>> f.read(2)
'二三'
>>> f.tell()
9
>>> f.read(1)
'四'
>>> f.tell()
12
>>> f.read()
'五六七八九\n'
>>> f.tell()
28
>>> f.seek(0,2)
28
>>> f.tell()
28
>>> f.seek(1000)
1000
>>> f.tell()
1000
>>> f.read()
''
>>> f.seek(-10000,0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: negative seek position -10000

>>> f.seek(50)
50
>>> f.write('123')
3
>>> f.close()
>>> f = open('tt','r+')
>>> f.read()
'一二三四五六七八九\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00123'
```

##### 对于字符操作来说

- read() -- 是指从当前位置读到EOF
- read(n) -- 指从当前位置往后读n个**字符**
- tell() -- 告诉当前指针
- seek(0,0)=seek(0) -- 回到0位置,偏移0**字节**
- seek(3,0)=seek(3) -- 从0开始偏移3位，这个3可以超过字节长度
- seek(0,1) -- 从当前位置，移动0位(前面必须为0)**字节**
- seek(0,2) -- 从EOF开始，偏移0位(前面必须为0)**字节**

#### 字节模式

```python
>>> f = open('tt','rb+')
>>> f.read()
b'123456789\n'
>>> f.seek(0)
0
>>> f.seek(1)
1
>>> f.read()
b'23456789\n'
>>> f.seek(-2,0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 22] Invalid argument
>>> f.seek(2,1)
12
>>> f.tell()
12
>>> f.seek(-1,1)
11
11
>>> f.tell()
11
>>> f.seek(2,2)
12
>>> f.read()
b''
>>> f.seek(2,2)
12
>>> f.seek(-1,2)
9
>>> f.read()
b'\n'

```

##### 对于字节模式来说

- seek(n,0) -- n 必须为大于0的整数，但是移动位数的时候要确定跳过的字节数和字符能否正确的decode
- seek(n,1) -- n 可以是正数负数和0，左边界不能超过字节长度
- seek(n,2) -- n 可以是正数负数和0，左边界不能超过字节长度

> seek不管是字节还是字符模式下，都能超过右边界，不能超过左边界！！！



