# 智能问数 API

## 权限和数据范围

- 使用问数能力需要 `qa.use`。
- 普通用户仅可访问属于自己的会话、消息和引用。
- 问数仅使用状态为 `available` 的数据内容。

## 会话

### `GET /api/v1/qa/sessions`

权限：`qa.use`。支持 `page`、`page_size` 与 `q`。

返回当前用户会话列表：

```json
{
  "data":[{
    "id":"uuid",
    "title":"最近农业新闻",
    "status":"active",
    "updated_at":"2026-05-27T00:00:00Z"
  }]
}
```

### `POST /api/v1/qa/sessions`

权限：`qa.use`。

请求：`{"title":"最近农业新闻"}`，标题可为空。

响应 `201`：返回新建会话对象。

### `GET /api/v1/qa/sessions/{session_id}`

权限：`qa.use` 且会话属于当前用户。

返回单个会话详情：

```json
{
  "data": {
    "id": "uuid",
    "title": "最近农业新闻",
    "status": "active",
    "updated_at": "2026-05-27T00:00:00Z",
    "created_at": "2026-05-27T00:00:00Z"
  }
}
```

### `PATCH /api/v1/qa/sessions/{session_id}`

权限：`qa.use` 且会话属于当前用户。

可修改字段：`title`、`status` (`active/archived`)。

### `GET /api/v1/qa/sessions/{session_id}/messages`

权限：`qa.use` 且会话属于当前用户。

返回完成或失败的消息记录。回答消息可包含引用摘要：

```json
{
  "id":"answer-id",
  "role":"assistant",
  "content":"根据已采集信息...",
  "status":"completed",
  "citations":[
    {
      "knowledge_item_id":"item-id",
      "rank":1,
      "title":"来源标题",
      "source_name":"公开新闻来源",
      "excerpt":"引用摘要"
    }
  ]
}
```

## 提问与流式回答

### `POST /api/v1/qa/sessions/{session_id}/questions/stream`

权限：`qa.use` 且会话属于当前用户。该请求需要 CSRF 防护。

请求：

```json
{"question":"最近采集到的农业相关信息有哪些重点？"}
```

行为：

1. 校验会话、问题内容和可用默认模型。
2. 保存用户问题。
3. 检索与问题相关的可用知识内容。
4. 创建回答记录与模型调用记录。
5. 以 SSE 输出回答片段。
6. 完成后保存回答正文和实际引用关系。

SSE 完成事件：

```text
event: completed
data: {"message_id":"answer-id","citations":[{"knowledge_item_id":"item-id","rank":1,"title":"来源标题","source_name":"公开新闻来源","excerpt":"引用摘要"}]}
```

失败规则：

- 没有启用默认模型：在流开始前返回 `422 MODEL_UNAVAILABLE`。
- 无匹配依据：系统可返回说明未找到依据的回答，但不得伪造引用；该策略在实现时必须保持一致。
- 上游在流开始后失败：发送 `error` 事件，并将回答和调用记录标为失败。

## 引用查看

### `GET /api/v1/qa/messages/{answer_id}/citations`

权限：`qa.use` 且回答属于当前用户会话。

返回回答生成时固定保存的引用列表和摘录。若对应知识内容后来归档或排除，历史引用仍可供用户理解旧回答，但应标注当前内容状态。

## 数据与安全边界

- 前端不能提交任意 `knowledge_item_id` 强行加入依据；依据由服务端检索确定。
- 模型输入中的采集内容按不可信资料处理，不执行其中包含的指令。
- 回答接口不得返回内部提示词、模型凭据、采集认证配置或其他用户的内容。

