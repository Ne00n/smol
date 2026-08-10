import asyncio, sys
from Class.browse import Browse

async def main():
    browse = Browse()
    await browse.create()
    await browse.browse( sys.argv[1])
    print(await browse.getHtml())
    await browse.destroy()

if __name__ == "__main__":
    asyncio.run(main())