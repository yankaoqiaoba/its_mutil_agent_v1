# ITS 多智能体系统 —— LangGraph 编排设计方案

> **基于项目**: ITS 智能客服与知识库平台
> **当前方案**: OpenAI Agents SDK (Swarm 模式)
> **迁移目标**: LangGraph (图状态机编排)
> **版本**: v1.0

---

## 一、项目现状分析

### 1.1 当前架构（OpenAI Agents SDK）

```
前端 (Agent Web UI / Knowledge Platform UI)
  |
  v
FastAPI /api/query (SSE 流式端点)
  |
  v
MultiAgentService.process_task()
  |
  ├── SessionService (会话历史管理)
  |
  └── Orchestrator Agent (主调度智能体) 
       |
       ├── handoff → consult_technical_expert()
       |    └── Technical Agent [阿里百炼]
       |         ├── query_knowledge → ChromaDB 知识库
       |         └── search_mcp → 百度搜索 MCP
       |
       └── handoff → query_service_station_and_navigate()
            └── Service Agent [阿里百炼]
                 ├── resolve_user_location → 百度地图Geocode / IP定位
                 ├── query_nearest_shops → MySQL 服务站表
                 └── baidu_mcp → 百度地图 MCP (导航/POI)
```

### 1.2 当前智能体角色

| 角色 | 类名 | 模型 | 核心工具 | 职责 |
|------|------|------|----------|------|
| 主调度智能体 | `orchestrator_agent` | 硅基流动(主) | `consult_technical_expert` / `query_service_station_and_navigate` | 意图识别、任务分发、结果聚合 |
| 技术专家 | `technical_agent` | 阿里百炼(子) | `query_knowledge` / `search_mcp_client` | 技术问答、实时资讯 |
| 业务专家 | `comprehensive_service_agent` | 阿里百炼(子) | `resolve_user_location_from_text` / `query_nearest_repair_shops_by_coords` / `baidu_mcp_client` | 服务站查询、地图导航 |

### 1.3 当前编排模式：Swarm (Agent as tool)

```
用户输入 → Orchestrator(意图识别) → 调用 function_tool(子Agent) → 子Agent执行工具 → 返回结果 → Orchestrator聚合 → 用户
```

**痛点**：
- 黑盒 handoff，流程不可视
- 条件分支依赖 prompt 驱动，不够精确
- 无法做复杂的多步条件路由
- 难以加入人工审核节点
- 中间状态不可持久化

---

## 二、LangGraph 方案设计

### 2.1 为什么选 LangGraph

| 维度 | OpenAI Agents SDK | LangGraph |
|------|------------------|-----------|
| 编排模式 | Swarm Handoff（隐式） | StateGraph（显式） |
| 流程可视化 | 黑盒 | DAG 有向无环图 |
| 条件路由 | Prompt 驱动 | 显式条件边 + 函数 |
| 状态管理 | 框架内部 | `State` TypedDict，可持久化 |
| 中间节点 | 不支持 | 原生支持（如人工审核） |
| 流式支持 | `run_streamed()` | `astream_events()` |
| 检查点/恢复 | 不支持 | `Checkpointer` 原生支持 |
| 并行执行 | 有限 | `Send` API 原生支持 |
| LLM 无关 | 绑定 OpenAI | 支持任意 LLM |
