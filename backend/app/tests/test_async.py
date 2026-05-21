# def sync_make():
#     print("xxxxx")
#     yield "123"
#
# for  chunk in sync_make():
#     print(chunk)
import asyncio


async def sync_make():
    print("xxxxx")
    yield "123"


async def main():
    async for chunk in sync_make():
        yield chunk


if __name__ == '__main__':
    pass
    # 1. 异步生成器的遍历一定要加 async for
    # 2. 加了async for 所在的方法一定要是async
