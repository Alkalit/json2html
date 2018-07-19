Реализация тестового задания на конвертер из json в html

Зависимостей нет. Писалось на python 3.5.
Запускается как `python parser.py`. Результатом будет вывод в консоль который можно перенаправить стандартным юниксовым синтаксисом
`python parser.py > source.html`
Тесты запускаются через `python run_tests.py` и сами лежат в `tests/`

Пример входа: 

```
[
    {
        "span": "Title #1",
        "content": [
            {
                "p": "Example 1",
                "header": "header 1"
            }
        ]

    }
]
```

вывод

```
<ul><li><span>Title #1</span><content><ul><li><p>Example 1</p><header>header 1</header></li></ul></content></li></ul>
```
