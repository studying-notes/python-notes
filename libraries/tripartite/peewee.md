---
date: 2020-12-24T10:41:03+08:00  # 创建日期
author: "Rustle Karl"  # 作者

# 文章
title: "Python ORM 数据库操作 Peewee"  # 文章标题
url:  "posts/python/libraries/tripartite/peewee"  # 设置网页永久链接
tags: [ "python", "orm", "数据库"  ]  # 自定义标签
series: [ "Python 学习笔记"]  # 文章主题/文章系列
categories: [ "学习笔记"]  # 文章分类

# 章节
weight: 20 # 排序优先级
chapter: false  # 设置为章节

index: true  # 是否可以被索引
toc: true  # 是否自动生成目录
draft: false  # 草稿
---

对象关系映射（ORM）是一种从面向对象的语言访问关系数据库的技术，它是 Python 数据库 API 的抽象。

Peewee 是一个简单而小型的 Python ORM 工具。 它支持 SQLite，MySQL 和 PostgreSQL。

```python
pip install peewee
```

## 结构映射

`Model` 映射到数据库表，`Field` 映射到表列，`instance` 映射到表行。

Peewee 对于 MySQL 使用 `MySQLDatabase`，对于 PostgreSQL 使用 `PostgresqlDatabase`，对于 SQLite 使用 `SqliteDatabase`。

## 字段类型

Peewee 模型中的字段类型定义模型的存储类型。 它们被转换为相应的数据库列类型。下表列出了 Peewee 字段类型以及相应的 SQLite，PostgreSQL 和 MySQL 列类型。

|     字段类型      |   SQLite   | PostgreSQL  |   MySQL    |
| :---------------: | :--------: | :---------: | :--------: |
|    `CharField`    | `varchar`  |  `varchar`  | `varchar`  |
|    `TextField`    |   `text`   |   `text`    | `longtext` |
|  `DateTimeField`  | `datetime` | `timestamp` | `longtext` |
|  `IntegerField`   | `integer`  |  `integer`  | `integer`  |
|  `BooleanField`   | `smallint` |   `bool`    |   `bool`   |
|   `FloatField`    |   `real`   |   `real`    |   `real`   |
|   `DoubleField`   |   `real`   |  `double`   |  `double`  |
| `BigIntegerField` | `integer`  |  `bigint`   |  `bigint`  |
|  `DecimalField`   | `decimal`  |  `numeric`  | `numeric`  |
| `PrimaryKeyField` | `integer`  |  `serial`   | `integer`  |
| `ForeignKeyField` | `integer`  |  `integer`  | `integer`  |
|    `DateField`    |   `date`   |   `date`    |   `date`   |
|    `TimeField`    |   `time`   |   `time`    |   `time`   |

## 模型定义

在第一个示例中，我们创建一个简单的数据库表。

```python
import peewee
import datetime

db = peewee.SqliteDatabase('test.db')

class Note(peewee.Model):

    text = peewee.CharField()
    created = peewee.DateField(default=datetime.date.today)

    class Meta:

        database = db
        db_table = 'notes'

Note.create_table()

note1 = Note.create(text='Went to the cinema')
note1.save()

note2 = Note.create(text='Exercised in the morning',
        created=datetime.date(2018, 10, 20))
note2.save()

note3 = Note.create(text='Worked in the garden',
        created=datetime.date(2018, 10, 22))
note3.save()

note4 = Note.create(text='Listened to music')
note4.save()
```

该示例在 SQLite 中创建 `notes` 数据库表。

```python
db = peewee.SqliteDatabase('test.db')
```

我们启动 `test.db` SQLite 数据库。这将在文件系统上创建一个 `test.db` 文件。

```python
class Note(peewee.Model):
```

我们定义了一个名为 `Note` 的数据库模型。Peewee 模型继承自 `peewee.Model`。

```python
text = peewee.CharField()
created = peewee.DateField(default=datetime.date.today)
```

我们指定模型字段。我们有一个 `CharField` 和一个 `DateField`。`CharField` 是用于存储字符串的字段类。`DateField` 是用于存储日期的字段类。如果未指定，则采用默认值。

```python
class Meta:
    database = db
    db_table = 'notes'
```

在 `Meta` 类中，我们定义对数据库的引用和数据库表名称。

```python
Note.create_table()
```

该表是使用 `create_table()` 从模型创建的。

```python
note1 = Note.create(text='Went to the cinema')
note1.save()
```

## 删除表

使用 `drop_table()` 模型方法删除该表。

```python
Note.drop_table()
```

## insert_many 批量创建

`insert_many()` 方法允许进行批量创建。

```python
data = [
    { 'text': 'Tai chi in the morning', 'created': datetime.date(2018, 10, 20) },
    { 'text': 'Visited friend', 'created': datetime.date(2018, 10, 12) },
    { 'text': 'Went to cinema', 'created': datetime.date(2018, 10, 5) },
    { 'text': 'Listened to music', 'created': datetime.date(2018, 10, 28) },
    { 'text': 'Watched TV all day', 'created': datetime.date(2018, 10, 14) },
    { 'text': 'Worked in the garden', 'created': datetime.date(2018, 10, 22) },
    { 'text': 'Walked for a hour', 'created': datetime.date(2018, 10, 28) }
]

with db.atomic():
    query = Note.insert_many(data)
    query.execute()
```

该代码示例通过一次批量创建操作来重新创建 `notes` 表。在词典列表中定义数据，执行批量操作。`atomic()` 方法将批量操作置于事务中。

## 选择所有实例

`select()` 方法用于检索定义的模型的实例。

```python
notes = Note.select()

for note in notes:
    print('{} on {}'.format(note.text, note.created))
```

该示例获取并显示所有 `Note` 实例。

`select()` 方法创建一个 SELECT 查询。如果未明确提供任何字段，则查询将默认选择模型上定义的所有字段。

## where 过滤器

`where()` 方法可以根据给定条件过滤数据。

```python
notes = Note.select().where(Note.id > 3)

for note in notes:
    print('{} {} on {}'.format(note.id, note.text, note.created))
```

检索 ID 大于三的所有行。

## 多个 where 表达式

我们可以组合多个 where 表达式。

```python
notes = Note.select().where((Note.id > 2) & (Note.id < 6))

for note in notes:
    print('{} {} on {}'.format(note.id, note.text, note.created))
```

该示例检索 id 大于 2 且小于 6 的所有行。

## 检索单个实例

选择单个实例有两种方法： 它们每个都使用 `get()` 方法。

```python
note1 = Note.select().where(Note.text == 'Went to cinema').get()

print(note1.id)
print(note1.text)
print(note1.created)
```

```python
note2 = Note.get(Note.text == 'Listened to music')

print(note2.id)
print(note2.text)
print(note2.created)
```

## 选择特定的列

在 `select()` 方法内部，我们可以指定要包含在查询中的列的名称。

```python
notes = Note.select(Note.text, Note.created).limit(2)

output = [e for e in notes.tuples()]
print(output)
```

该示例包括两列：text 和 created。 该 ID 被跳过。 我们将查询限制为两个实例。

## 计数 count()

要计算表中的模型实例数，我们可以使用 `count()` 方法。

```python
n = Note.select().count()
print(n)

n2 = Note.select().where(Note.created >= datetime.date(2018, 10, 20)).count()
print(n2)
```

该示例计算所有实例的数量以及日期等于或晚于 2018/10/20 的实例的数量。

## 显示 SQL 语句

可以使用 `sql()` 方法显示生成的 SQL 语句。

```python
note3 = Note.select().where(Note.id == 3)
print(note3.sql())
```

## offset 和 limit

通过 `offset` 和 `limit` 属性，我们可以定义实例的初始跳过和要包含在 `select()` 中的实例数。

```python
notes = Note.select().offset(2).limit(3)

for note in notes:
    print(note.id, note.text, note.created)
```

该示例从第二个实例开始返回三个实例。

## 排序

可以使用 `order_by()` 对检索到的实例进行排序。

```python
print('Ascending order')
print('*****************************')

notes = Note.select(Note.text, Note.created).order_by(Note.created)

for note in notes:
    print(note.text, note.created)

print()
print('Descending order')
print('*****************************')

notes = Note.select(Note.text, Note.created).order_by(Note.created.desc())

for note in notes:
    print(note.text, note.created)
```

该代码示例按创建日期对实例进行排序。

## 删除实例

`delete_by_id()` 方法删除由其 ID 标识的实例。 它返回已删除实例的数量。

```python
n2 = Note.delete_by_id(1)
print(n2)
```

该示例删除一个 ID 为 1 的 `Note` 实例。

## 删除多个实例

要删除更多实例，我们调用 `delete()` 方法。它返回成功删除的实例数。

```python
query = Note.delete().where(Note.id > 3)
n = query.execute()

print('{} instances deleted'.format(n))
```

## 更新实例

`update()` 方法更新一个实例。 它返回成功更新的实例数。

```python
query = Note.update(created=datetime.date(2018, 10, 27)).where(Note.id == 1)
n = query.execute()

print('# of rows updated: {}'.format(n))
```

## 一对多关系

在以下示例中，我们将模型映射到现有表。使用 `ForeignKeyField` 创建模型之间的关系。

`customers` 和 `reservations`。两个表之间存在一对多的关系：一个客户可以进行很多预订。

```python
import peewee
import datetime

db = peewee.SqliteDatabase('test.db')

class Customer(peewee.Model):

    name = peewee.TextField()

    class Meta:

        database = db
        db_table = 'customers'

class Reservation(peewee.Model):

    customer = peewee.ForeignKeyField(Customer, backref='reservations')
    created = peewee.DateField(default=datetime.date.today)

    class Meta:

        database = db
        db_table = 'reservations'

customer = Customer.select().where(Customer.name == 'Paul Novak').get()

for reservation in customer.reservations:

    print(reservation.id)
    print(reservation.created)
```

在示例中，我们定义了两个映射到表的模型。 然后，我们选择一个客户并显示其预订。

```python
customer = peewee.ForeignKeyField(Customer, backref='reservations')
```

`Customer` 和 `Reservation` 模型之间的关系是通过 `ForeignKeyField` 创建的。`backref` 属性设置了我们如何参考客户的预订。

# 增删改查

## 读取数据

基本的语法是 `Model.select(fields).where(**coditions).get()`. 或者直接简写成 `Model.get()`。

```python
# peewee 只会查询一次数据库，不管迭代多少次。
query = Pet.select().where(Pet.animal_type == "cat")
for pet in query:
    print(pet.name, pet.owner.name)  # 注意这里有 N+1 问题，N 指的是获取 owner.name

# 直接获取一条数据，select, where 全省略了
grandma = Person.get(Person.name == "Grandma L.")

# 或者全写出来
grandma = Person.select().where(Person.name == "Gramdma L.").get()

# in 查询使用 in_ 方法
Pet.select().where(Pet.id.in_([1,2]))

# 对于 id 可以直接使用 get_by_id

Person.get_by_id(100)

# 使用 get_or_none 阻止抛出异常

Person.get_or_none()

# 可以使用 join 解决 N+1 问题
query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == "cat"))
         .order_by(Pet.name)  # 或者 Pet.name.desc() 逆序排列

for pet in query:
    print(pet.name, pet.owner.name)
```

可以直接使用 | 来作为查询条件，这个相比 django 需要使用 Q 来说，设计地非常优雅。

```python
d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Grandma L. 1935-03-01

query.count()  #  返回记录的大小
```

### get*or*create

peewee 模仿 django 实现了 get*or*create 的方法。注意他的参数是 Django 风格的，而不是 peewee 的 model.attr == xxx 的风格。

```python
person, created = Person.get_or_create(
    first_name=first_name,
    last_name=last_name,
    defaults={"dob": dob, "favorite_color": "green"})
```

### iterator

对于返回结果过多的查询，可以使用 iterator 方法。

### 返回简单对象

## 插入数据

跟 django 的 ORM 貌似是一样的。使用 Model.create() 或者 Model.save() 或者 Model.insert()

```python
from datetime import date

# 使用 save
uncle_bob = Person(name="Bob", birthday=date(1960, 1, 15))
uncle_bob.save() # bob is now stored in the database

# 使用 create
grandma = Person.create(name="Grandma", birthday=date(1935, 3, 1))
bob_kitty = Pet.create(owner=uncle_bob, name="Kitty", animal_type="cat")  # 带有外键的宠物

# 使用 bulk_create
users = [User(username="u%s" % i) for i in range(10)]
User.bulk_create(users, batch_size=100)

# 使用 insert
User.insert(username="mickey").execute()

# 使用 insert many。或者使用 tuple 也可以
data_source = [
    {"field1": "val1-1", "field2": "val1-2"},
    {"field1": "val2-1", "field2": "val2-2"},
    # ...
]

# Fastest way to INSERT multiple rows.
MyModel.insert_many(data_source).execute()

# We can INSERT tuples as well...
data = [("val1-1", "val1-2"),
        ("val2-1", "val2-2"),
        ("val3-1", "val3-2")]

# But we need to indicate which fields the values correspond to.
MyModel.insert_many(data, fields=[MyModel.field1, MyModel.field2]).execute()
```

## 更新数据

可以使用 Model.update 或者 model.save 更新数据。

```python
# 使用 save 更新
herb_fido.owner = uncle_bob
herb_fido.save()

# 使用 update 更新
query = Tweet.update(is_published=True).where(Tweet.creation_date < today)

# 批量更新数据
# First, create 3 users with usernames u1, u2, u3.
u1, u2, u3 = [User.create(username="u%s" % i) for i in (1, 2, 3)]

# Now we"ll modify the user instances.
u1.username = "u1-x"
u2.username = "u2-y"
u3.username = "u3-z"

# Update all three users with a single UPDATE query.
User.bulk_update([u1, u2, u3], fields=[User.username])
```

需要注意的是，在使用 update 的时候千万不要在 Python 中使用计算再更新，要使用 SQL 语句来更新，这样才能具有原子性。

错误做法

```python
>>> for stat in Stat.select().where(Stat.url == request.url):
...     stat.counter += 1
...     stat.save()
```

正确做法

```python
>>> query = Stat.update(counter=Stat.counter + 1).where(Stat.url == request.url)
>>> query.execute()
```

## 删除数据

可以使用 model.delete_instance 或者 Model.delete。

```python
# 使用 object.delete_instance
herb_mittens.delete_instance()

# 使用 Model.delete
Tweet.delete().where(Tweet.creation_date < one_year_ago).execute()
```

# 一些有用的拓展

## 模型转换成字典

除了在查询的时候使用 model.dicts 以外，还可以使用 model*to*dict(model) 这个函数。

```
>>> user = User.create(username="charlie")
>>> model_to_dict(user)
{"id": 1, "username": "charlie"}
```

## 从数据库生成模型

最后也是最牛逼的一点，可以使用 pwiz 工具从已有的数据库产生 peewee 的模型文件：

```shell
python -m pwiz -e postgresql charles_blog > blog_models.py
```
