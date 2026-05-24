
"""
降级处理：
地点不明确-> 
获取IP

"""

from agents import set_tracing_disabled
set_tracing_disabled(True)
from agents import Agent, ModelSettings
from infrastructure.ai.openai_client import sub_model
from infrastructure.tools.local.service_station import (
    resolve_user_location_from_text,
    query_nearest_repair_shops_by_coords
)
from infrastructure.tools.mcp.mcp_servers import (
    baidu_mcp_client,
)
from infrastructure.ai.prompt_loader import load_prompt
comprehensive_service_agent = Agent(
    model=sub_model,
    instructions= load_prompt("comprehensive_service_agent"),
    model_settings=ModelSettings(
        temperature=0,
        max_tokens=2048,),
    tools=[],
    mcp_servers=[],
    )

async def run_single_test(case_name,input_text):
    from agents import Runner
    """运行单个测试并打印详细信息"""
    print(f"\n{'=' * 80}")
    print(f"测试用例: {case_name}")
    print(f"输入: \"{input_text}\"")
    print("-" * 80)
    await baidu_mcp_client.connect()
    result = Runner.run_streamed(
        starting_agent=comprehensive_service_agent,
        input=input_text,
    )

    # 打印关键事件
    try:
        await baidu_mcp_client.connect()
        print("思考中...")
        # result = await Runner.run(comprehensive_service_agent, input=input_text)

        # 使用流式处理
        result = Runner.run_streamed(
            starting_agent=comprehensive_service_agent,
            input=input_text,
        )

        # 打印关键事件
        async for event in result.stream_events():
            # 工具调用事件
            if event.type == "run_item_stream_event":
                if hasattr(event, "name") and event.name == "tool_called":
                    from agents import ToolCallItem
                    if isinstance(event.item, ToolCallItem):
                        raw_item = event.item.raw_item
                        print(f"\n调用工具名:{raw_item.name}--->工具参数:{raw_item.arguments}")
                elif hasattr(event, 'name') and event.name == "tool_output":
                    from agents import ToolCallOutputItem
                    if isinstance(event.item, ToolCallOutputItem):
                        print(f"调用工具结果:{event.item.output}")

        print(f"\n\nAgent的最终输出: {result.final_output}")
    except Exception as e:
        print(f"\n Error: {e}\n")
    finally:
        try:
            await baidu_mcp_client.cleanup()
        except:
            pass

async def main():
    # 服务站和地图测试案例
    test_cases = [
         # ("Case 1服务站 - 起点不明确 终点明确", "我想去小米之家修电脑"),
         # ("Case 1服务站 - 起点不明确 终点明确", "我想去最近的服务站"),
        # ("Case 2服务站 - 起点不明确 终点明确", "我想去联想thinkpad电脑售后维修服务中心"),
        # ("Case 3服务站 - 起点 终点明确", "从昌平区回龙观到联想thinkpad电脑售后维修服务中心如何走"),
        # ("Case 4服务站 - 起点不明确 终点不明确 ", "附近有官方维修点吗？"),

        # ("Case 5普通 POI - 起点不明确 终点明确", "怎么去天安门广场？"),
        # ("Case 5普通 POI - 起点不明确 终点明确", "安门广场都有哪些商场？"),
        # ("Case 6普通 POI - 起点不明确 终点明确", "昌平区温都水城怎么走？"),
        # ("Case 6普通 POI - 起点不明确 终点明确", "附近有哪些商场?"),
        # ("Case   7普通 POI - 起点 终点都明确", "从昌平区回龙观到天安门广场怎么走"),

        # ("Case 7技术问题", "电脑蓝屏了怎么办？"),  # 应拒绝
        ("Case 8闲聊", "你好啊"),  # 应拒绝
    ]

    for name, question in test_cases:
        await run_single_test(name, question)



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
