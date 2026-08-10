import asyncio, json, time, sys, os
from pyvirtualdisplay import Display
from fake_useragent import UserAgent
from pyppeteer import launch


class Browse():

    async def create(self):
        self.headless = True
        if self.headless:
            print("Starting virtual display")
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()

        args = ['--no-sandbox', '--disable-setuid-sandbox']
        
        launch_kwargs = {
            'headless': True,
            'autoClose': True,
            'args': args
        }

        args.append('--start-maximized')
        launch_kwargs['defaultViewport'] = None
        launch_kwargs['executablePath'] = "/usr/bin/chromium"

        self.browser = await launch(**launch_kwargs)
        self.page = await self.browser.newPage()
        ua = UserAgent()
        userAgent = ua.chrome
        print(f"Using {userAgent}")
        await self.page.setUserAgent(userAgent)

    async def browse(self,url):
        print(f"Browsing {url}")
        await self.page.goto(url)
        await asyncio.sleep(3)

    async def getHtml(self):
        return await self.page.content()

    async def destroy(self):
        await self.page.close()
        await self.browser.close()
        if self.headless: self.display.stop()

async def main():
    browse = Browse()
    await browse.create()
    await browse.browse( sys.argv[1])
    print(await browse.getHtml())
    await browse.destroy()

if __name__ == "__main__":
    asyncio.run(main())