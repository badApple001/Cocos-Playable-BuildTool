
#pyinstaller -F main.py

import base64
import json
import time
import IUtils
from consoleColorFont import printGreen,printYellowRed
from progressBar import ProgressBar
import os
from IPlatform import Debug
import re

root = os.getcwd()


def build():
    try:
        path_setting = IUtils.fromJsonAsDict(f'{root}/bin/base_path_setting.json')
        project_root = f'{root}/{path_setting["project_root"]}'
        index_html_path = f'{root}/{path_setting["index_html_path"]}'
        style_css_path = f'{root}/{path_setting["style_css"]}'
        out_file_url = f'{root}/{path_setting["out_file"]}'
        splash_path = f'{root}/{path_setting["splash_path"]}'
        setting_js_path = f'{root}/{path_setting["setting_js_path"]}'
        main_js_path = f'{root}/{path_setting["main_js_path"]}'
        ccjs_path = f'{root}/{path_setting["ccjs_path"]}'
        physicsJs_path = f'{root}/{path_setting["physicsJs_path"]}'


        printGreen("Conversion Progress:")
        bar = ProgressBar(total = 12,width=10)
        stime = time.time()
        
        #Clean Html
        html_content = IUtils.fromFile(index_html_path)
        html_content = re.sub(
            r'<link rel="stylesheet".*/>', "", html_content)
        html_content = re.sub(
            r'<script.[\s\S]*</script>', "", html_content)
        html_content = re.sub(
            r'<link rel="icon".*/>', '<link rel="icon"/>', html_content)
        bar.step()

        # toreal title
        titleContent = re.findall(r'<title.*title>', html_content)[0]
        realTitle = "<title>" + titleContent[23:-8] + "</title>"
        html_content = re.sub(
            r'<title.*title>', realTitle, html_content, 1)
        bar.step()

        # html style
        style_css_content = IUtils.fromFile(style_css_path)
        style_css_content = IUtils.StyleScript(style_css_content,False)
        bar.step()
        
        # splash icon
        splash_content = IUtils.fromFile2Base64(splash_path)
        style_css_content = re.sub(
                r'background.*no-repeat center;', f'background: #171717 url(data:image/jpeg;base64,{splash_content}) no-repeat center;', style_css_content, 1)
        html_content = html_content.replace(
                '</head>', "\t" + style_css_content+'\n</head>', 1)
        bar.step()

        #window._CCSettings
        BODY_CONTENT = ""
        settingJs_content = IUtils.fromFile(setting_js_path)
        settingJs_content = IUtils.JavaScript(settingJs_content,False)
        BODY_CONTENT += settingJs_content
        bar.step()

        #cocos2d-js-min.js
        ccjs_path_content = IUtils.fromFile(ccjs_path)
        ccjs_path_content = IUtils.JavaScript(ccjs_path_content,False)
        BODY_CONTENT += ccjs_path_content
        bar.step()

        #physics-min.js
        if os.path.exists(physicsJs_path):
            physicsJs_path_content = IUtils.fromFile(physicsJs_path)
            physicsJs_path_content = IUtils.JavaScript(physicsJs_path_content,False)
            BODY_CONTENT += physicsJs_path_content
        bar.step()

        #window.resMap
        def HashAssets(dir, filter='', resMap={}):
            def convert2base64(url, str1):
                binBuffer = IUtils.fromFile(url,'rb',None)
                return str1 +  str(base64.b64encode(binBuffer), encoding='utf-8')
            def convert2text(url):
                return IUtils.fromFile(url)

            pConvertFunctor = {
                '.json': lambda x: convert2text(x),
                '.js': lambda x: convert2text(x),
                '.wasm': lambda x: convert2base64(x, ''),
                '.png': lambda x: convert2base64(x, ''),
                '.jpg': lambda x: convert2base64(x, ''),
                '.gif': lambda x: convert2base64(x, ''),
                '.wav': lambda x: convert2base64(x, ''),
                '.bin': lambda x: convert2base64(x, ''),
                '.plist':lambda x: convert2text(x),
                '.mp3': lambda x: convert2base64(x, ''),
                '.ttf': lambda x: convert2base64(x,''),
                '.pem':lambda x: convert2text(x),
                '.dbbin':lambda x: convert2base64(x,''),
                '.mp4':lambda x: convert2base64(x,''),
                '.atlas':lambda x: convert2text(x)
            }
          
            for root, dirs, files in os.walk(dir):
                path = root.replace(filter, '', 1).replace('\\', '/')
                for f in files:
                    url = '%s/%s' % (path, f)
                    ext = os.path.splitext(f)[1]
                    resMap[url] = pConvertFunctor[ext](root + '/' + f)
            return resMap
        bar.step()

        resMap = HashAssets(project_root+"/assets",project_root+"/")
        resMapContent = json.dumps(resMap, ensure_ascii=False)
        resMapContent = IUtils.JavaScript('window.resMap = ' + resMapContent)
        BODY_CONTENT += resMapContent
        bar.step()

        #cc.assetManager.downloader.register
        downloader_content = IUtils.fromFile(root+'/bin/downloader-min.js')
        downloader_content = IUtils.JavaScript(downloader_content)
        BODY_CONTENT += downloader_content
        bar.step()

        #main.js
        mainJs_content = IUtils.fromFile(main_js_path)
        mainJs_content = IUtils.JavaScript(mainJs_content)
        BODY_CONTENT += mainJs_content
        bar.step()

        #window.boot()
        jsContent = '<script type="text/javascript">\nwindow.boot();\n</script>\n'
        BODY_CONTENT += jsContent

        html_content =  html_content.replace(
                '</body>',BODY_CONTENT+'\n</body>', 1)
        IUtils.writeInFile(out_file_url,html_content)
        bar.step()
        printGreen("Conversion completed！")
        printYellowRed(f'\nuse time: {round(time.time()-stime,2)} seconds')
    except:
        Debug.LogExcept()




if __name__ == '__main__':
    build()
    Debug.Export()



