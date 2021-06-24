from selenium import webdriver

profile = webdriver.FirefoxProfile()

# 指定下载路径，默认只会自动创建一级目录，如果是不存在的多级目录，将会下载到默认路径
profile.set_preference('browser.download.dir', 'F:\White Turing\Downloads')

# 2 表示将文件下载到指定路径
# 0 表示将文件下载到桌面
# 1 表示将文件下载到默认路径
profile.set_preference('browser.download.folderList', 2)

# 对于未知的MIME类型文件会弹出窗口让用户处理，默认值为True，设定为False表示不会记录打开未知MIME类型文件的方式
profile.set_preference('browser.helperApps.alwaysAsk.force', False)

# 在开始下载时是否显示下载管理器
profile.set_preference('browser.download.manager.showWhenStarting', False)

# 设定为False会把下载框进行隐藏
profile.set_preference('browser.download.manager.useWindow', False)

# 默认值为True，设定为False表示不获取焦点
profile.set_preference('browser.download.manager.focusWhenStarting', False)

# 下载.exe文件弹出警告，默认值是True，设定为False则不会弹出警告框
profile.set_preference('browser.download.manager.alertOnEXEOpen', False)


# browser.helperApps.neverAsk.openFile表示直接打开下载文件，不显示确认框
# 默认值为空字符串，下行代码行设定了多种文件的MIME类型，
# 例如application/exe，表示.exe类型的文件，
# application/excel表示Excel类型的文件
profile.set_preference(
    'browser.helperApps.neverAsk.openFile', 'application/pdf')

# 对所给出文件类型不再弹出提示框进行询问，直接保存到本地磁盘
profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                       'application/zip, application/octet-stream')

# browser.download.manager.showAlertOnComplete设定下载文件结束后是否显示下载完成提示框
# 默认为True，设定为False表示下载完成后不显示下载完成提示框
profile.set_preference('browser.download.manager.showAlertOnComplete', False)

# browser.download.manager.closeWhenDone设定下载结束后是否自动关闭下载框，
# 默认值为True，设定为False表示不关闭下载管理器
profile.set_preference('browser.download.manager.closeWhenDone', False)

driver = webdriver.Firefox(firefox_profile=profile)

driver.get('http://github.com/mozilla/geckodriver/releases')
driver.find_element_by_xpath(
    '//strong[.="geckodriver-v0.20.0-win64.zip"]').click()

driver.get('https://www.python.org/downloads/windows/')
driver.find_element_by_link_text('Windows x86-64 executable installer').click()
