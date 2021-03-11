## csv

csv是最通用的一种文件格式，它可以非常容易地被导入各种PC表格及数据库中。此文件，一行即为数据表的一行。生成数据表字段用半角逗号隔开。csv文件用记事本和excel都能打开，用记事本打开显示逗号，用excel打开，没有逗号了，逗号都用来分列了,还可有Editplus打开。

- 逗号分隔值Comma-Separated Values
- csv是一个被行分隔符、列分隔符划分成行和列的文本文件
- csv不指定字符编码
- 行分隔符为\r\n
- 列分隔符为逗号或者制表符
- 每一行称为一条记录record
- 字段可以使用双括号括起来，也可也不使用
- 如果字段出现了双引号、逗号、换行符必须使用双引号括起来
- 如果字段的值是双引号，可以使用两个双引号表示转义
- 表头可选，和字段列对齐就行

### 写一个简单的例子

```python
from pathlib import Path


path = Path('D:/test/test.csv')

csv_body = """\
Name, Age, Sex, Birth, Scool
Gavin, 28, 男, 2021/03/03, 华北电力大学
Xiaoming, 22, 男, 2020/02/02, “清华大学”
"""

with path.open(mode='w+') as f:
    f.write(csv_body)
```

### csv模块

#### csv.reader()

```python
from pathlib import Path
import csv

path = Path('D:/test/test.csv')

csv_body = """\
Name, Age, Sex, Birth, Scool
Gavin, 28, 男, 2021/03/03, 华北电力大学
Xiaoming, 22, 男, 2020/02/02, “清华大学”
"""

with path.open(mode='w+') as f:
    f.write(csv_body)


with path.open() as f:
    body = csv.reader(f)
    for line in body:
        print(line, type(line))
```

#### csv.writer()

- 单行写入

```python
from pathlib import Path
import csv

p = Path().cwd()/'demo.csv'
body = ['3', 'ben', '28', '这是\n一  段\n中文']

with p.open('w+') as f:
    write = csv.writer(f)
    write.writerow(body)

    f.seek(0)
    [print(i) for i in csv.reader(f)]

# 结果如下
['3', 'ben', '28', '这是\n一  段\n中文']
[]
```

- 多行写入

```python
from pathlib import Path
import csv

p = Path().cwd() / 'demo.csv'
body = [
    ['3', 'ben', '28', '这是\n一  段\n中文'],
    ['4', 'Bben', '284', '这是\n一  段\n中文']
        ]

with p.open('a+') as f:
    write = csv.writer(f)
    write.writerows(body)

    f.seek(0)
    [print(i) for i in csv.reader(f)]

# 结果如下
['3', 'ben', '28', '这是\n一  段\n中文']
[]
['3', 'ben', '28', '这是\n一  段\n中文']
[]
['4', 'Bben', '284', '这是\n一  段\n中文']
[]
```

- 取消空行


```python
from pathlib import Path
import csv

p = Path().cwd() / 'demo.csv'
body = [
    ['3', 'ben', '28', '这是\n一  段\n中文'],
    ['4', 'Bben', '284', '这是\n一  段\n中文']
        ]

with p.open('w+', newline='') as f:
    write = csv.writer(f)
    write.writerows(body)

    f.seek(0)
    [print(i) for i in csv.reader(f)]

# 结果如下
['3', 'ben', '28', '这是\n一  段\n中文']
['4', 'Bben', '284', '这是\n一  段\n中文']
```

>csv最大的问题是无法描述数据类型

## ini文件处理

- 作为配置文件，ini文件格式很流行
- 与csv一样，纯文本文件

### section

- 用`[]`括起来的区域就是一个section
- section里面的赋值语句其实就是k=v
- k(name) 叫做option，

```python
[DEFAULT]
name = test
```

>注意：这里的DEFAULT是缺省section的名字，必须大写

### configparser

configparser模块的configpaeser类就是用来操作

```python
import configparser

cfg = configparser.ConfigParser()
cfg.read()
```

#### 看下read源码

有个技巧点

```python
    def read(self, filenames, encoding=None):
        """Read and parse a filename or an iterable of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify an iterable of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the iterable will be read.  A single
        filename may also be given.

        Return list of successfully read files.
        """
        if isinstance(filenames, (str, bytes, os.PathLike)):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            try:
                with open(filename, encoding=encoding) as fp:
                    self._read(fp, filename)
            except OSError:
                continue
            if isinstance(filename, os.PathLike):
                filename = os.fspath(filename)
            read_ok.append(filename)
        return read_ok
```

可以由上面的思想整理出来

```python
def read(filenames):
    if isinstance(filenames, str):
        filenames = [filenames]
    for filename in filenames:
        pass
# 传参方式一
read('/etc/grafana.ini')

# 传参方式二
read(['/etc/grafana.ini', '/etc/my.cfg', '/etc/passwd'])
```

#### 查看ini的sections


```python
from pathlib import Path
import configparser

grafana_body = """
    [auth.github]
    enabled = false
    allow_sign_up = false
    client_id = some_id
    client_secret = some_secret
    scopes = user:email


    [auth.google]
    enabled = false
    allow_sign_up = false
    client_id = some_client_id
    client_secret = some_client_secret
    scopes = https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
    auth_url = https://accounts.google.com/o/oauth2/auth
    token_url = https://accounts.google.com/o/oauth2/token
    api_url = https://www.googleapis.com/oauth2/v1/userinfo
            """

p = Path().cwd()/'grafana.ini'
with p.open('w+') as f:
    f.write(grafana_body)

cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))
print(read_ok_ini)
print(cfg.sections(), cfg.default_section)

# 结果如下
['D:\\Gitee\\python\\test\\grafana.ini']
['auth.github', 'auth.google'] DEFAULT
```

#### 查看sections的源码

```python
 def sections(self):
        """Return a list of section names, excluding [DEFAULT]"""
        # self._sections will never have [DEFAULT] in it
        return list(self._sections.keys())
```

我们直接看看_sections


```python
from pathlib import Path
import configparser

grafana_body = """
    [DEFAULT]
    name = grafana


    [auth.github]
    enabled = false
    allow_sign_up = false
    client_id = some_id
    client_secret = some_secret
    scopes = user:email


    [auth.google]
    enabled = false
    allow_sign_up = false
    client_id = some_client_id
    client_secret = some_client_secret
    scopes = https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
    auth_url = https://accounts.google.com/o/oauth2/auth
    token_url = https://accounts.google.com/o/oauth2/token
    api_url = https://www.googleapis.com/oauth2/v1/userinfo
            """

p = Path().cwd()/'grafana.ini'
with p.open('w+') as f:
    f.write(grafana_body)

cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))
print(cfg._sections)

# 结果如下
OrderedDict([('auth.github', OrderedDict([('enabled', 'false'), ('allow_sign_up', 'false'), ('client_id', 'some_id'), ('client_secret', 'some_secret'), ('scopes', 'user:email')])), ('auth.google', OrderedDict([('enabled', 'false'), ('allow_sign_up', 'false'), ('client_id', 'some_client_id'), ('client_secret', 'some_client_secret'), ('scopes', 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'), ('auth_url', 'https://accounts.google.com/o/oauth2/auth'), ('token_url', 'https://accounts.google.com/o/oauth2/token'), ('api_url', 'https://www.googleapis.com/oauth2/v1/userinfo')]))])
```

####  cfg.items()

先看源码

```python
    def items(self, section=_UNSET, raw=False, vars=None):
        """Return a list of (name, value) tuples for each option in a section.

        All % interpolations are expanded in the return values, based on the
        defaults passed into the constructor, unless the optional argument
        `raw' is true.  Additional substitutions may be provided using the
        `vars' argument, which must be a dictionary whose contents overrides
        any pre-existing defaults.

        The section DEFAULT is special.
        """
        if section is _UNSET:  # 如果没有设定section
            return super().items()  # 返回一个超集
        d = self._defaults.copy()  # d是一个self._defaults = self._dict()，最终的就是OrderedDict的浅拷贝
        try:  
            d.update(self._sections[section])  # 如果设置了section
        except KeyError:   # 如果上面的d字典update了一个你输入的不存在的session
            if section != self.default_section:  # 如上面的_section里面没有default缺省值，这里再判断的是如果你输入的section不等于default这个节点里面的option
                raise NoSectionError(section)  
        # Update with the entry specific variables
        if vars:                                # 缺省参数vars默认值是None，如果给定则就是一个字典格式，用来更新default这个section里面预设的值
            for key, value in vars.items():    # 这里也验证了vars是一个字典
                d[self.optionxform(key)] = value  # 这里的optionform就是把key的大小写格式统一为小写
        value_getter = lambda option: self._interpolation.before_get(self,  # 实际是通过key把value取出来
            section, option, d[option], d)
        if raw:
            value_getter = lambda option: d[option]
        return [(option, value_getter(option)) for option in d.keys()]  # 通过k 和 dict[k]构成一个二元组 当k在d中
```

#### 验证下items用法

```python
from pathlib import Path
import configparser

grafana_body = """
    [DEFAULT]
    name = grafana


    [auth.github]
    enabled = false
    allow_sign_up = false
    client_id = some_id
    client_secret = some_secret
    scopes = user:email


    [auth.google]
    enabled = false
    allow_sign_up = false
    client_id = some_client_id
    client_secret = some_client_secret
    scopes = https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
    auth_url = https://accounts.google.com/o/oauth2/auth
    token_url = https://accounts.google.com/o/oauth2/token
    api_url = https://www.googleapis.com/oauth2/v1/userinfo
            """

p = Path().cwd()/'grafana.ini'
with p.open('w+') as f:
    f.write(grafana_body)

cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))
x = cfg.items('auth.google')
print(x, type(x))
print('~'*10)
for i in x:
    print(type(i), i)

# 结果如下
[('name', 'grafana'), ('enabled', 'false'), ('allow_sign_up', 'false'), ('client_id', 'some_client_id'), ('client_secret', 'some_client_secret'), ('scopes', 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'), ('auth_url', 'https://accounts.google.com/o/oauth2/auth'), ('token_url', 'https://accounts.google.com/o/oauth2/token'), ('api_url', 'https://www.googleapis.com/oauth2/v1/userinfo')] <class 'list'>
~~~~~~~~~~
<class 'tuple'> ('name', 'grafana')
<class 'tuple'> ('enabled', 'false')
<class 'tuple'> ('allow_sign_up', 'false')
<class 'tuple'> ('client_id', 'some_client_id')
<class 'tuple'> ('client_secret', 'some_client_secret')
<class 'tuple'> ('scopes', 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email')
<class 'tuple'> ('auth_url', 'https://accounts.google.com/o/oauth2/auth')
<class 'tuple'> ('token_url', 'https://accounts.google.com/o/oauth2/token')
<class 'tuple'> ('api_url', 'https://www.googleapis.com/oauth2/v1/userinfo')
```

> 可以发现auth.google并没有name=grafana这option，但是显示出来了，说明DEFAULT这个公共模板的值被找出来了

继续看var这个参数


```python
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))
x = cfg.items('auth.google', vars={'name': 'Python'})
print(x, type(x))
print('~'*10)
for i in x:
    print(type(i), i)

# 结果如下
[('name', 'Python'), ('enabled', 'false'), ('allow_sign_up', 'false'), ('client_id', 'some_client_id'), ('client_secret', 'some_client_secret'), ('scopes', 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'), ('auth_url', 'https://accounts.google.com/o/oauth2/auth'), ('token_url', 'https://accounts.google.com/o/oauth2/token'), ('api_url', 'https://www.googleapis.com/oauth2/v1/userinfo')] <class 'list'>
~~~~~~~~~~
<class 'tuple'> ('name', 'Python')
<class 'tuple'> ('enabled', 'false')
<class 'tuple'> ('allow_sign_up', 'false')
<class 'tuple'> ('client_id', 'some_client_id')
<class 'tuple'> ('client_secret', 'some_client_secret')
<class 'tuple'> ('scopes', 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email')
<class 'tuple'> ('auth_url', 'https://accounts.google.com/o/oauth2/auth')
<class 'tuple'> ('token_url', 'https://accounts.google.com/o/oauth2/token')
<class 'tuple'> ('api_url', 'https://www.googleapis.com/oauth2/v1/userinfo')
```

> 看到var传入的dict已经将公共模板的值替换掉了

#### get()

```python
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))
x = cfg.items('auth.google', vars={'name': 'Python'})

print(cfg.get('auth.google', 'enabled'))

# 结果如下
false
```

- 这有个问题，如果option不存在直接报错
- 以前我们处理过这种问题，就是加一个default_func
- 这里也有这个参数

```python
p = Path().cwd()/'grafana.ini'

cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

print(cfg.get('auth.google', 'unfound', fallback='None'))

# 结果如下
None
```


#### set

```python
p = Path().cwd()/'grafana.ini'

cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

print(cfg.get('auth.google', 'api_url'))
cfg.set('auth.google', 'api_url', value='Do not ask me')
print(cfg.get('auth.google', 'api_url'))

# 结果如下
https://www.googleapis.com/oauth2/v1/userinfo
Do not ask me
```

default 这个sections也可以修改

```python
print(cfg.get('DEFAULT', 'name'))
cfg.set('DEFAULT', 'name', value='Do not ask me')
print(cfg.get('DEFAULT', 'name'))
```

#### 文件保存

cfg.write()
前面的种种操作并没有真正的修改文件，只是对内存中的数据结构修改，需要落地一下

```python
from pathlib import Path
import configparser

p = Path().cwd()/'grafana.ini'
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

cfg.set('DEFAULT', 'name', value='Do not ask me')
with p.open('w+') as f:
    cfg.write(f)
```

#### 当作字典直接访问

```python
from pathlib import Path
import configparser

p = Path().cwd()/'grafana.ini'
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

print(cfg, type(cfg))
print(cfg['auth.google']['enabled'])

# 结果如下
<configparser.ConfigParser object at 0x000001DB42E3CE88> <class 'configparser.ConfigParser'>
false
```

#### add_section

```python
from pathlib import Path
import configparser

p = Path().cwd()/'grafana.ini'
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

cfg.add_section('[Gitee]')
print(cfg.sections())

# 结果如下
['auth.github', 'auth.google', '[Gitee]']
```

#### remove_section

```python
from pathlib import Path
import configparser

p = Path().cwd()/'grafana.ini'
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

cfg.add_section('Gitee')
print(cfg.sections())

if cfg.has_section('Gitee'):
    cfg.remove_section("Gitee")
print(cfg.sections())

# 结果如下
['auth.github', 'auth.google', 'Gitee']
['auth.github', 'auth.google']
```

#### 增加section和option

```python
from pathlib import Path
import configparser

p = Path().cwd()/'grafana.ini'
cfg = configparser.ConfigParser()
read_ok_ini = cfg.read(str(p))

cfg['Abcc'] = {'other_option': 'new_option'}
print(cfg.sections())
print(cfg['Abcc']['other_option'])

# 结果如下
['auth.github', 'auth.google', 'Abcc']
new_option
```