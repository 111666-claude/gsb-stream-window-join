# stream-window-join

把两条事件流按事件键与时间窗口做 join：窗口含端点、水位之下的迟到事件丢弃、同一事件只参与一次。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m windowjoin --sample=boundary
python3 -m windowjoin --sample=key
python3 -m windowjoin --sample=late
python3 -m windowjoin --sample=idem
python3 -m windowjoin --sample=work
```

## 口径

- **键**：只有事件键相同的两条记录才能配对。
- **窗口**：两条记录的时间差小于等于窗口就能配对（含端点）。
- **水位**：时间戳低于"已见最大时间戳减窗口"的记录算迟到，直接丢弃。
- **幂等**：同一个事件 id 只参与一次，重复投递不产生新配对。
- **查找**：按事件键分桶，配对只在与键相关的桶里找。

## 不变量

- 每条配对都满足键相同、时间差不超过窗口。
- 迟到事件不产生配对；同一事件 id 只参与一次。
- `scanned` 不随事件数平方级放大：一千六百条事件的 `scanned` 不超过 6000。

## 输出契约

`feed` 返回本次产生的配对列表（每项是两条事件 id）。场景打印一行 JSON。
`--sample=work` 打印 `{"events": N, "scanned": N}`。
