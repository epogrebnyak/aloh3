# Моделирование выбора заказов и объемов производства

Пакет `aloh` позволяет оптимизировать дискретное производство и выбрать наиболее выгодные заказы. 
 
#### Что за алгоритм?

Мы решаем задачу смешанного линейного целочисленного программирования (MILP). Заказам присваивается бинарная переменная (взяли-не взяли), объемам производства - непрерывные переменные от нуля до максимального выпуска. Мы также учитываем ограничения на срок хранения продукта на складе. Оптимизация ведется с целью максимизации прибыли и уменьшения запасов продукции на складе.

#### Чем решаем?

Для формулировки задачи используется пакет [PuLP][pulp], решение ищется с помощью открытых солверов, таких как [CBC][cbc].

[pulp]: https://coin-or.github.io/pulp/
[cbc]: https://github.com/coin-or/Cbc

#### Что такое `aloh`?

`aloh` - сокращение от химической формулы гидроксида алюминия, нашего первого демонстрационного примера оптимизации производства.


## Примеры

### 1. Простой пример - формулировка задачи
 
Один продукт ("A"), планирование на три дня, пять заказов. Необходимо выбрать выгодные заказы и объем производства по дням.

В портфеле есть заказы, которые невозможно выполнить (недостаточно производственных мощностей), невыгодные заказы (цены ниже себестоимости) и заказы с разной 
маржинальностью. Мы выбираем из них заказы, которые, во-первых, возможно и, во-вторых, выгодно выполнить.

```python
from aloh import OptModel, Product

pa = Product(name="A", capacity=10, unit_cost=0.1, storage_days=1)
pa.add_order(day=0, volume=7, price=0.2)     # менее выгодный заказ
pa.add_order(day=0, volume=7, price=0.3)     # более выгодный заказ, берем
pa.add_order(day=1, volume=10, price=0.09)   # убыточный заказ, не берем
pa.add_order(day=2, volume=6, price=0.25)    # } если есть возможность хранения, 
pa.add_order(day=2, volume=6, price=0.25)    # } берем оба заказа

m = OptModel(products=[pa], model_name="model_0", inventory_weight=0)
ac, xs = m.evaluate()
```

    Solved in 0.099 sec
    

#### План производства, отгрузка, запасы

Производство (*x*), поставки (*ship*), запасы (_inv_) - в натуральном выражении,
продажи (*sales*) and затраты (*costs*) - в денежном выражении.


```python
m.product_dataframe("A")
```

| day |   x |  ship |  inv |  sales |  costs |
|:---:|:---:|:-----:|:----:|:------:|:------:|
|   0 |   7 |     7 |    0 |    2.1 |    0.7 |
|   1 |   2 |     0 |    2 |    0   |    0.2 |
|   2 |  10 |    12 |    0 |    3   |    1   |



#### Выбор заказов

*accept=1* показывает принятый заказ.


```python
 m.orders_dataframe("A")
```

|  n |   day |   volume |   price |   accept |
|:--:|:-----:|:--------:|:-------:|:--------:|
|  0 |     0 |        7 |    0.2  |        0 |
|  1 |     0 |        7 |    0.3  |        1 |
|  2 |     1 |       10 |    0.09 |        0 |
|  3 |     2 |        6 |    0.25 |        1 |
|  4 |     2 |        6 |    0.25 |        1 |

## Документация

https://epogrebnyak.github.io/aloh/

## Запуск  

```console
set PYTHONIOENCODING=utf8  
git clone https://github.com/epogrebnyak/aloh
cd aloh
pip install _requirements.txt  
pip install -e .
```
