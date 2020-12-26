# p1901 mysql机试题

#### 1. 找出连续的座位号

两人人准备订座火车,他们希望订座的连续的位置,seat_id是座位号,is_free为1表示座位还能被订座,0表示不能被订座了,
找出两个或以上连续的位置座位号可能性

表单:

```angular2html

| seat_id | is_free |
|---------|------|
| 32       | 1    |
| 33       | 0    |
| 34       | 1    |
| 35       | 1    |
| 36       | 1    |

```

期望输出:

```angular2html

| seat_id |
|---------|
| 34       |
| 35       |
| 36       |
```

建表语句(测试数据):

```angular2html
create table train (teat_id int,is_free int);
 
insert into train values(32,1);
insert into train values(33,1);
insert into train values(34,0);
insert into train values(35,1);
insert into train values(36,1);
insert into train values(37,1);
```


#### 2. 找出员工奖金(bonus)少于1000的员工名和奖金数额


表名

>Employee
```angular2html
+-------+--------+-----------+--------+
| empId |  name  | supervisor| salary |
+-------+--------+-----------+--------+
|   1   | John   |  3        | 1000   |
|   2   | Dan    |  3        | 2000   |
|   3   | Brad   |  null     | 4000   |
|   4   | Thomas |  3        | 4000   |
+-------+--------+-----------+--------+
```

>建表语句

```angular2html
CREATE TABLE `employee` (
  `empid` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `supervisor` int(11) DEFAULT NULL,
  `salary` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

>Bonus

```angular2html
+-------+-------+
| empId | bonus |
+-------+-------+
| 2     | 500   |
| 4     | 2000  |
+-------+-------+
```

```angular2html
CREATE TABLE `bonus` (
  `empid` int(11) DEFAULT NULL,
  `bonus` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

>期望输出

```angular2html
+-------+-------+
| name  | bonus |
+-------+-------+
| John  | null  |
| Dan   | 500   |
| Brad  | null  |
+-------+-------+
```


#### 3.找出没有销售给RED公司的订单的人

问题描述:
 
下面有三张表 salesperson, company, orders.

输出没有效果过订单给red公司的人

>员工表 salesperson

```angular2html

+----------+------+--------+-----------------+
| sales_id | name | salary | commission_rate | 
+----------+------+--------+-----------------+
|   1      | John | 100000 |     6           |
|   2      | Amy  | 120000 |     5           |
|   3      | Mark | 65000  |     12          |
|   4      | Pam  | 25000  |     25          |
|   5      | Alex | 50000  |     10          |
+----------+------+--------+-----------------+

```

>建表语句

```angular2html
CREATE TABLE `salesperson` (
  `sales_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `salary` decimal(10,0) DEFAULT NULL,
  `commission_rate` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

>公司表 company

```angular2html
+---------+--------+------------+
| com_id  |  name  |    city    |
+---------+--------+------------+
|   1     |  RED   |   Boston   |
|   2     | ORANGE |   New York |
|   3     | YELLOW |   Boston   |
|   4     | GREEN  |   Austin   |
+---------+--------+------------+
```
>建表语句
```angular2html
CREATE TABLE `company` (
  `com_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

>订单表 order
```angular2html
+----------+---------+----------+--------+
| order_id | com_id  | sales_id | amount |
+----------+---------+----------+--------+
| 1        |    3    |    4     | 100000 |
| 2        |    4    |    5     | 5000   |
| 3        |    1    |    1     | 50000  |
| 4        |    1    |    4     | 25000  |
+----------+---------+----------+--------+

```

>建表语句

```angular2html
CREATE TABLE `order` (
  `order_id` int(11) DEFAULT NULL,
  `com_id` int(11) DEFAULT NULL,
  `sales_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

期望输出

```angular2html
+------+
| name | 
+------+
| Amy  | 
| Mark | 
| Alex |
+------+
```

#### 4.找出节点的类型

问题描述 下面表的id代表数据的id号,p_id表示他的父类id是多少,比如id为2
的父类id就是 id为1的数据；


有三种类型的数据:

    1. root(根节点) 比如 id的1的数据，他是最顶级的
    2. leaf(叶子节点) 比如 id为5的数据 他有父类,但是没有子类
    3. node(节点) 比如 id为2的数据 既有父节点 1 又有 4 5两个节点指向他
 

```angular2html
+----+------+
| id | p_id |
+----+------+
| 1  | null |
| 2  | 1    |
| 3  | 1    |
| 4  | 2    |
| 5  | 2    |
+----+------+
```

>建表语句

```angular2html
CREATE TABLE `node` (
  `id` int(11) DEFAULT NULL,
  `p_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

期望输出节点类型

```angular2html
+----+------+
| id | Type |
+----+------+
| 1  | Root |
| 2  | Inner|
| 3  | Leaf |
| 4  | Leaf |
| 5  | Leaf |
+----+------+
```


#### 5.赢得投票的人

描述 选出赢得投票的人,下面有两张表,一张是含有人名和人的id的表,一个是投票表,
投票表的id是自增主键,CandidateId是哪个id的人被投了一票

>表名 Candidate

```angular2html
+-----+---------+
| id  | Name    |
+-----+---------+
| 1   | A       |
| 2   | B       |
| 3   | C       |
| 4   | D       |
| 5   | E       |
+-----+---------+  
```

```angular2html
CREATE TABLE `Candidate` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

>表名 Vote

```angular2html
+-----+--------------+
| id  | CandidateId  |
+-----+--------------+
| 1   |     2        |
| 2   |     4        |
| 3   |     3        |
| 4   |     2        |
| 5   |     5        |
+-----+--------------+

```

```angular2html
CREATE TABLE `Vote` (
  `id` int(11) DEFAULT NULL,
  `CandidateId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

期望输出B 因为b的得票最多

```angular2html
+------+
| Name |
+------+
| B    |
+------+
```









