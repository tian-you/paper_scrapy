"""
终极版本，不用任何代理，逻辑完全不一样
论文搜索异步模式，速度还行
额外文件进行打包时一定要用绝对路径在源代码里
pyinstaller --onefile paper_ultra.py --icon=ccf.ico --name="DMS Paper Spider-3.0"
在PowerShell中，使用cd命令切换目录时，需要将文件夹路径放在引号中，因为路径中包含空格。请使用以下命令来切换到指定的文件夹：
Set-Location "D:\PyCharm Community Edition 2023.2.3\project\pyscript"
"""
import asyncio
import json
import logging
import aiohttp
import random

import pandas as pd
import requests
from aiohttp import TCPConnector, ClientTimeout
from colorama import init, Fore
from lxml import etree

# 颜色初始化
init(autoreset=True)
# 随机颜色(排除红色，红色警告专用)
choices = ['Fore.GREEN', 'Fore.YELLOW',
           'Fore.BLUE', 'Fore.MAGENTA', 'Fore.CYAN', 'Fore.WHITE']

proxy = None

# # 数据初始化，读取JSON文件并转换为字典(用于进行分类)
# with open('D:\\PyCharm Community Edition 2023.2.3\\project\\pyscript\\Journal_Articles.json', 'r', encoding='utf-8') as json_file:
#     Journal_Articles = json.load(json_file)
#
# # 保存Journal_Articles字典为JSON文件（压缩为一行）
# with open("Journal_data.json", "w") as json_file1:
#     json.dump(Journal_Articles, json_file1, separators=(', ', ': '))
#
# with open('D:\\PyCharm Community Edition 2023.2.3\\project\\pyscript\\Conference_and_Workshop_Papers.json', 'r', encoding='utf-8') as json_file:
#     Conference_and_Workshop_Papers = json.load(json_file)
#
# # 保存Conference_and_Workshop_Papers字典为JSON文件（压缩为一行）
# with open("Conference_data.json", "w") as json_file2:
#     json.dump(Conference_and_Workshop_Papers, json_file2, separators=(', ', ': '))

Journal_Articles = {"A": ["IEEE Trans. Inf. Theory", "IEEE Trans. Vis. Comput. Graph.", "SIAM J. Comput.", "IEEE Trans. Image Process.", "Proc. IEEE", "ACM Trans. Graph.", "J. Mach. Learn. Res.", "IEEE Trans. Pattern Anal. Mach. Intell.", "ACM Trans. Comput. Hum. Interact.", "ACM Trans. Database Syst.", "ACM Trans. Softw. Eng. Methodol.", "IEEE Trans. Parallel Distributed Syst.", "VLDB J.", "IEEE/ACM Trans. Netw.", "Inf. Comput.", "IEEE Trans. Inf. Forensics Secur.", "Int. J. Comput. Vis.", "ACM Trans. Storage", "Artif. Intell.", "IEEE Trans. Comput. Aided Des. Integr. Circuits Syst.", "J. ACM", "IEEE Trans. Computers", "IEEE J. Sel. Areas Commun.", "Int. J. Hum. Comput. Stud.", "J. Cryptol.", "IEEE Trans. Software Eng.", "ACM Trans. Inf. Syst.", "Sci. China Inf. Sci.", "ACM Trans. Program. Lang. Syst.", "IEEE Trans. Serv. Comput.", "IEEE Trans. Dependable Secur. Comput.", "IEEE Trans. Knowl. Data Eng.", "ACM Trans. Comput. Syst.", "ACM Trans. Archit. Code Optim.", "IEEE Trans. Mob. Comput."], "B": ["IEEE Trans. Intell. Transp. Syst.", "Inf. Syst.", "Comput. J.", "Inf. Sci.", "Knowl. Inf. Syst.", "ACM Trans. Embed. Comput. Syst.", "Comput. Secur.", "IEE Proc. Softw.", "ACM Trans. Knowl. Discov. Data", "IEEE Trans. Affect. Comput.", "J Speech Lang Hear Res.", "Formal Aspects Comput.", "Math. Struct. Comput. Sci.", "IEEE Trans. Wirel. Commun.", "ACM Trans. Design Autom. Electr. Syst.", "Int. J. Hum. Comput. Interact.", "Sci. Comput. Program.", "Comput. Complex.", "Comput. Vis. Image Underst.", "J. Syst. Softw.", "Empir. Softw. Eng.", "J. Comput. Secur.", "Eur. J. Inf. Syst.", "IEEE Trans. Robotics", "Requir. Eng.", "Graph. Model.", "J. Web Semant.", "SIAM J. Imaging Sci.", "IEEE Trans. Syst. Man Cybern.", "Briefings Bioinform.", "IEEE Trans. Cybern.", "Comput. Support. Cooperative Work.", "Comput. Networks", "J. Comput. Syst. Sci.", "Hum. Comput. Interact.", "PLoS Comput. Biol.", "Formal Methods Syst. Des.", "INFORMS J. Comput.", "IEEE ACM Trans. Comput. Biol. Bioinform.", "Auton. Agents Multi Agent Syst.", "ACM Trans. Appl. Percept.", "J. Funct. Program.", "Autom. Softw. Eng.", "J. Glob. Optim.", "Perform. Evaluation", "IEEE ACM Trans. Audio Speech Lang. Process.", "Softw. Pract. Exp.", "IEEE Trans. Very Large Scale Integr. Syst.", "J. Am. Medical Informatics Assoc.", "IEEE Trans. Evol. Comput.", "Comput. Linguistics", "ACM Trans. Multim. Comput. Commun. Appl.", "World Wide Web (WWW)", "Bioinform.", "ACM Trans. Reconfigurable Technol. Syst.", "Data Knowl. Eng.", "J. Symb. Comput.", "J. Comput. Sci. Technol.", "IEEE Trans. Commun.", "Comput. Aided Geom. Des.", "IEEE Trans. Geosci. Remote. Sens.", "Data Min. Knowl. Discov.", "Des. Codes Cryptogr.", "Softw. Syst. Model.", "IEEE Trans. Fuzzy Syst.", "Neural Comput.", "ACM Trans. Algorithms", "Frontiers Comput. Sci.", "IEEE Trans Autom. Sci. Eng.", "J. Syst. Archit.", "Evol. Comput.", "J. Artif. Intell. Res.", "IEEE Trans. Hum. Mach. Syst.", "Interact. Comput.", "ACM Trans. Comput. Log.", "J. Assoc. Inf. Sci. Technol.", "Inf. Process. Manag.", "IEEE Trans. Circuits Syst. Video Technol.", "J. Parallel Distributed Comput.", "ACM Trans. Priv. Secur.", "Comput. Aided Des.", "Inf. Softw. Technol.", "Neural Networks", "User Model. User Adapt. Interact.", "Comput. Graph. Forum", "Theor. Comput. Sci.", "Parallel Comput.", "J. Autom. Reason.", "ACM Trans. Web", "ACM Trans. Math. Softw.", "Trans. Assoc. Comput. Linguistics", "ACM Trans. Sens. Networks", "IEEE Trans. Medical Imaging", "Adv. Eng. Informatics", "Int. J. Approx. Reason.", "Softw. Test. Verification Reliab.", "IEEE Trans. Multim.", "ACM Trans. Auton. Adapt. Syst.", "IEEE Trans. Neural Networks Learn. Syst.", "Mach. Learn.", "J. Softw. Evol. Process.", "GeoInformatica, Algorithmica", "Speech Commun.", "ACM Trans. Internet Techn."], "C": ["Distributed Parallel Databases", "IEEE Trans. Reliab.", "Wirel. Commun. Mob. Comput.", "Int. J. Document Anal. Recognit.", "J. Database Manag.", "Serv. Oriented Comput. Appl.", "Int. J. Intell. Syst.", "Artif. Intell. Medicine", "Expert Syst. J. Knowl. Eng.", "Log. Methods Comput. Sci.", "Comput. Vis. Media", "J. Comput. Inf. Syst.", "J. Log. Comput.", "IEEE Trans. Games", "Integr.", "Ann. Pure Appl. Log.", "ACM Trans. Comput. Educ.", "J. Symb. Log.", "Concurr. Comput. Pract. Exp.", "Int. J. Softw. Eng. Knowl. Eng.", "IEEE Signal Process. Lett.", "Acta Informatica", "Distributed Comput.", "Decis. Support Syst.", "Mach. Vis. Appl.", "ACM Trans. Cyber Phys. Syst.", "J. Strateg. Inf. Syst.", "Nat. Comput.", "IET Commun.", "Signal Process. Image Commun.", "Neural Comput. Appl.", "Discret. Appl. Math.", "BMC Bioinform.", "Theory Pract. Log. Program.", "Signal Process.", "IEEE Trans. Big Data", "Appl. Intell.", "Multim. Syst.", "IET Signal Process.", "J. Exp. Theor. Artif. Intell.", "Frontiers Inf. Technol. Electron. Eng.", "Secur. Commun. Networks", "Comput. Graph.", "Comput. Animat. Virtual Worlds", "Comput. Commun.", "EURASIP J. Inf. Secur.", "Inf. Retr. J.", "IEEE Geosci. Remote. Sens. Lett.", "Image Vis. Comput.", "Fuzzy Sets Syst.", "J. Complex.", "Future Gener. Comput. Syst.", "Int. J. Uncertain. Fuzziness Knowl. Based Syst.", "Int. J. Comput. Intell. Appl.", "Behav. Inf. Technol.", "IEEE Trans. Netw. Serv. Manag.", "Proc. ACM Hum. Comput. Interact.", "Medical Image Anal.", "ACM Trans. Interact. Intell. Syst.", "J. Supercomput.", "Discret. Comput. Geom.", "J. Intell. Inf. Syst.", "IET Inf. Secur.", "Comput. Speech Lang.", "Real Time Syst.", "Intell. Data Anal.", "Pattern Recognit. Lett.", "Int. J. Inf. Secur. Priv.", "Connect. Sci.", "Softw. Qual. J.", "Pers. Ubiquitous Comput.", "IEEE Trans. Circuits Syst. I Regul. Pap.", "Cybern. Syst.", "Int. J. Softw. Tools Technol. Transf.", "Fundam. Informaticae", "Comput. Intell.", "Cybersecur.", "Int. J. Neural Syst.", "IEEE Trans. Sustain. Comput.", "Inf. Comput. Secur.", "Inf. Process. Lett.", "Eng. Appl. Artif. Intell.", "Peer Peer Netw. Appl.", "Data Sci. Eng.", "Nat. Lang. Eng.", "SIAM J. Discret. Math.", "IEEE Trans. Ind. Informatics", "J. Netw. Comput. Appl.", "J. Glob. Inf. Manag.", "J. Electron. Test.", "Int. J. Semantic Web Inf. Syst.", "ACM Trans. Asian Low Resour. Lang. Inf. Process.", "Inf. Manag.", "IEEE J. Biomed. Health Informatics", "IEEE Trans. Comput. Soc. Syst.", "Ad Hoc Networks", "Mob. Networks Appl.", "Vis. Comput.", "Internet Things", "Wirel. Networks", "Networks", "Neurocomputing", "J. Log. Algebraic Methods Program.", "IET Image Process.", "ACM J. Emerg. Technol. Comput. Syst.", "Soft Comput.", "Proc. ACM Program. Lang.", "Theory Comput. Syst.", "IEEE Trans. Cloud Comput.", "Mach. Transl.", "Web Intell.", "Multim. Tools Appl.", "Artif. Life", "J. Inf. Secur. Appl.", "Int. J. Geogr. Inf. Sci.", "J. Vis. Commun. Image Represent.", "IET Comput. Vis.", "Knowl. Based Syst.", "J. Grid Comput.", "J. Web Eng.", "Comput. Law Secur. Rev.", "Comput. Lang. Syst. Struct.", "Pattern Anal. Appl.", "Expert Syst. Appl.", "Int. J. Pattern Recognit. Artif. Intell.", "Comput. Geom.", "Neural Process. Lett.", "CCF Trans. High Perform. Comput.", "Int. J. Inf. Comput. Secur.", "Int. J. Knowl. Manag.", "Int. J. Cooperative Inf. Syst.", "Pervasive Mob. Comput.", "J. Biomed. Informatics"]}

Conference_and_Workshop_Papers = {"A": ["SODA", "ISCA", "INFOCOM", "WINE", "ACL", "ACM MM", "USENIX ATC", "RTSS", "CCS", "UbiComp", "VR", "S&P", "ICML", "NeurIPS", "SIGKDD", "WWW", "DAC", "LICS", "EUROCRYPT", "FM", "EuroSys", "UIST", "ICSE", "SIGMOD", "FSE/ESEC", "OSDI", "IJCAI", "PPoPP", "MobiCom", "ICDE", "CAV", "HPCA", "FAST", "SIGCOMM", "SOSP", "SIGIR", "ISSTA", "AAAI", "NDSS", "NSDI", "POPL", "SIGGRAPH", "CVPR", "ICCV", "MICRO", "FOCS", "ASE", "STOC", "OOPSLA", "VLDB", "IEEE VIS", "CSCW", "PLDI", "ASPLOS", "CHI", "SC", "USENIX Security", "CRYPTO"], "B": ["CLUSTER", "SGP", "DASFAA", "MSST", "SCA", "EDBT", "PODS", "IMC", "DATE", "ICALP", "FPGA", "ICDT", "HOT CHIPS", "LCTES", "MobiHoc", "ICME", "IUI", "Euro-Par", "CODES+ISSS", "SANER", "RAID", "NAACL", "ISWC", "EuroVis", "PPSN", "FSE", "Middleware", "SECON", "MobiSys", "Eurographics", "RecSys", "PERCOM", "SPM", "DSN", "COLING", "SOCC", "ICNP", "ACSAC", "ICS", "ESORICS", "ICCD", "CAiSE", "ITC", "CogSci", "MICCAI", "ICASSP", "ISMB", "ICPC", "HotOS", "ICWSM", "COLT", "CONCUR", "PG", "EMSOFT", "RE", "DCC", "CGO", "ECML-PKDD", "ECCV", "CIKM", "IWQoS", "CCC", "MobileHCI", "RECOMB", "WSDM", "PACT", "PKC", "ICRA", "UAI", "IPSN", "ICSOC", "PODC", "HSCC", "CoNEXT", "VEE", "TCC", "SIGMETRICS", "SAS", "SenSys", "SoCG", "SAT", "AAMAS", "COCOON", "BIBM", "HPDC", "ICCAD", "Performance", "ICAPS", "EGSR", "ICSME", "ICPP", "GROUP", "ECAI", "MoDELS", "CHES", "ICCBR", "SPAA", "ECSCW", "ICDCS", "LISA", "EMNLP", "ISSRE", "ISMAR", "SRDS", "ECOOP", "ICDM", "ASIACRYPT", "CP", "ESEM", "CADE", "ICMR", "ESA", "ICWS", "ICFP", "I3D", "ETAPS", "NOSSDAV", "VMCAI", "KR", "RTAS", "IPDPS", "ITS", "CSFW", "HiPEAC", "CIDR", "SDM"], "C": ["ICIP", "ICTAI", "ISPA", "VRST", "ACCV", "COSIT", "ISLPED", "SEC", "LOPSTR", "APLAS", "TASE", "IPCO", "SMC", "ACISP", "ICFEM", "HiPC", "SSTD", "CASES", "WAIM", "ICMI", "BMVC", "COMPSAC", "MobiQuitous", "ICICS", "IDC", "SYSTOR", "ICCCN", "AISTATS", "WISE", "MMAsia", "CF", "FC", "ICPADS", "APNet", "ICST", "ICSSP", "WHC", "ICANN", "P2P", "ICDF2C", "PASTE", "IH&MMSec", "CT-RSA", "ATVA", "ICC", "RTA", "SACMAT", "CoNLL", "SAC", "ICECCS", "ECIR", "CSCWD", "ATS", "DEXA", "INTERSPEECH", "ASP-DAC", "AMIA", "PRCV", "SecureComm", "SCC", "UIC", "REFSQ", "GI", "APNOMS", "PEPM", "SIGSPATIAL", "WASA", "ER", "MMM", "ANCS", "EuroS&P", "ASSETS", "FCCM", "RV", "ICIC", "Inscrypt", "AsiaCCS", "FPL", "APBC", "SCAM", "CollaborateCom", "KSEM", "WICSA", "GMP", "CAD/Graphics", "GLOBECOM", "IM", "MSN", "CSL", "CoopIS", "ADMA", "NOCS", "GLSVLSI", "ICTAC", "PETS", "NSPW", "DIS", "MDM", "WoWMoM", "FORTE", "ISPD", "INTERACT", "IEEE CLOUD", "SPIN", "Networking", "WebDB", "ICSR", "3DV", "GECCO", "MSWiM", "SOUPS", "FG", "SAGT", "WiSec", "PRICAI", "ITC-Asia", "ICVRV", "ASAP", "PAKDD", "IJCB", "FSTTCS", "ISBRA", "PAM", "ACML", "MASS", "IPCCC", "ETS", "CCGRID", "CGI", "AVI", "ISAAC", "ISCAS", "FMCAD", "IEEE BigData", "SEKE", "HOTI", "MSR", "ISC", "DSAA", "MFCS", "NLPCC", "ESWC", "HotSec", "ICONIP", "ICPR", "IROS", "ISCC", "EASE", "SETTA", "SMI", "MASCOTS", "APSEC", "DIMVA", "Internetware", "HPCC", "NPC", "HotNets", "CASA", "WCNC", "DFRWS", "APWeb", "ISPASS", "IJCNN", "SSDBM", "PacificVis", "ICWE", "VTS", "FPT", "DRM", "ACNS", "ALT", "ILP", "QRS", "ICDAR", "CVM", "LCN", "ICA3PP", "IFIP WG 11.9", "STACS", "TrustCom"]}

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='test.log',  # 日志输出到文件
    filemode='a'  # 追加模式
)


def display_credits_and_notes():
    """
    Display the creator's name and some notes to the user.
    """
    print("==========================================")
    print(Fore.RED + "DMS Paper Spider - Version 1.0")
    print(Fore.RED + "Created by: [", eval(random.choice(choices)) + "tian_you", Fore.RED + "]")
    print("==========================================")
    print(Fore.YELLOW + "\n注意事项:")
    print(Fore.RED + "1. 本脚本功能自动根据关键词汇总CCF-A B C类期刊或会议。")
    print(Fore.RED + "2. 启动和搜索过程", Fore.YELLOW + "可能比较缓慢，因为云服务器上部署的代理IP池有限，请耐心等待，感谢理解！！！")
    print(Fore.RED + "3. 如有任何问题，请联系[制作人的邮箱:2389765824@qq.com]。")
    print(Fore.RED + "4. 请不要在未经授权的情况下分发或修改此脚本。")
    print("==========================================\n")


async def get_proxy(session):
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    # async with aiohttp.ClientSession() as session:
    async with session.get("http://123.57.226.67:6666/get/") as res:
        return await res.json()


async def delete_proxy(prox, session):
    # async with aiohttp.ClientSession() as session:
    await session.get(f"http://123.57.226.67:6666/delete/?proxy={prox}")


# 2. 验证代理IP可用性
async def verify_proxy(prox, session):
    # 构造请求头，模拟浏览器请求
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
    ]
    header = {'User-Agent': random.choice(user_agent_list)}

    # 请求目标网页并判断响应码
    u = "http://www.baidu.com"
    try:
        # 注意这里使用了 await 来等待异步操作的结果
        async with session.get(u, headers=header, proxy=f"http://{prox}", timeout=10) as res:
            # 这里也需要使用 await 来等待 raise_for_status 的结果
            res.raise_for_status()
            return True
    except aiohttp.ClientError as e:
        logging.error(f"代理 {proxy} 验证失败: {e}")
        return False


# 网址访问函数
async def get_response(u, i, session, qe):
    global proxy
    param = {
        'q': qe,
        's': 'ydvspc',
        'h': '30',
        'b': f'{i}'
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
    ]
    header = {'User-Agent': random.choice(user_agent_list)}

    while True:
        # if proxy is None:
        #     proxy_info = await get_proxy(session)  # 使用 await 调用异步函数
        #     if not proxy_info:
        #         logging.error("无法获取代理")
        #         return None
        #     proxy = proxy_info.get("proxy")
        #     logging.info(f"使用新代理: {proxy}")
        #
        # if not await verify_proxy(proxy, session):  # 使用 await 调用异步函数
        #     await delete_proxy(proxy, session)  # 使用 await 调用异步函数
        #     proxy = None
        #     continue
        try:
            async with session.get(u, params=param, headers=header) as res:
                res.raise_for_status()
                return await res.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"请求异常: {e}")
            # await delete_proxy(proxy, session)
            # proxy = None
        except Exception as e:
            logging.error(f"未预料的错误: {e}")
            # proxy = None


async def fetch(u, i, session, q):
    retries = 0
    max_retries = 100
    while retries < max_retries:
        try:
            res = await get_response(u, i, session, q)  # 确保传递正确的参数以获取不同页的结果
            return res
        except Exception as e:
            # 如果发生异常，记录或处理它，并进行重试
            logging.error(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            # print(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            retries += 1
            await asyncio.sleep(1)  # 增加延迟避免立即重试可能导致的问题


journal_data_lock = asyncio.Lock()
global_journal_data = []


async def parse(html_content, cho):
    tree = etree.HTML(html_content)

    if cho == 'Journal_Articles':
        li_tags = tree.xpath('//li[@class="entry article toc"]')
    else:
        li_tags = tree.xpath('//li[@class="entry inproceedings toc"]')

    j_data = []

    for li in li_tags:
        title_list = li.xpath('.//span[@class="title" and @itemprop="name"]//text()')
        title = ''.join(title_list).strip()
        # title = title_list[0].strip() if title_list else "Title not found"

        publisher_list = li.xpath('.//a/span/span[@itemprop="name"]/text()')
        publisher = publisher_list[0].strip() if publisher_list else "Publisher not found"

        years_list = li.xpath('.//span[@itemprop="datePublished"]/text()')
        year = years_list[0].strip() if years_list else "Year not found"

        j_data.append({
            'title': title,
            'publisher': publisher,
            'year': year
        })

    async with journal_data_lock:
        global_journal_data.extend(j_data)


async def main(total, qury, cho):
    u = 'https://dblp.uni-trier.de/search/publ/inc'
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10),
                                         connector=TCPConnector(ssl=False)) as session:  # 创建一次会话用于所有的请求

            tasks = []
            for i in range(0, int(total) // 30 + 1):
                ts = asyncio.create_task(fetch(u, i, session, qury))
                tasks.append(ts)  # 创建异步获取任务
            print(eval(random.choice(choices)) + '\n并发异步执行所有获取任务......\n')
            pages_content = await asyncio.gather(*tasks, return_exceptions=True)

        tasks = []
        for html_content in pages_content:
            ts = asyncio.create_task(parse(html_content, cho))
            tasks.append(ts)  # 创建解析任务

        print(eval(random.choice(choices)) + '\n并发异步执行所有的解析任务......\n')
        await asyncio.gather(*tasks, return_exceptions=True)  # 并发执行所有的解析任务

    except Exception as e:
        print(f"An error occurred: {e}")


def create_journal_entry(title, typ, years):
    # 将年份列表转换成字符串，并用'|'符号连接
    years_str = '|'.join(map(str, years))
    # 根据输入拼接字符串
    entry = f"title:{title} type:{typ}:year:{years_str}"
    return entry


def save_titles_to_excel(titles_A, titles_B, titles_C, sum_article, keyword, star, en, file_name):
    # 根据提供的titles数据结构，指定列名
    column_names = ['Title', 'Journal', 'Year']
    file_name = f"{keyword}_{str(star)}_{str(en)}_{'共'+str(sum_article)+'篇'}_{file_name}"

    # 创建ExcelWriter对象，用于写入Excel文件
    excel_writer = pd.ExcelWriter(file_name, engine='openpyxl', mode='w')

    # 将titles_A写入到Sheet1
    df_a = pd.DataFrame(titles_A, columns=column_names)
    df_a.to_excel(excel_writer, sheet_name='A类', index=False)

    # 将titles_B写入到Sheet2
    df_b = pd.DataFrame(titles_B, columns=column_names)
    df_b.to_excel(excel_writer, sheet_name='B类', index=False)

    # 将titles_C写入到Sheet3
    df_c = pd.DataFrame(titles_C, columns=column_names)
    df_c.to_excel(excel_writer, sheet_name='C类', index=False)

    # 保存并关闭ExcelWriter对象
    # excel_writer.save()
    excel_writer.close()
    # 生成文件名
    # file_name = f"{keyword}_{str(star)}_{str(en)}_{str(sum_article)}_{file_name}"


if __name__ == '__main__':

    display_credits_and_notes()

    title_input = None

    # journal_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    while True:
        input_valid = False
        while not input_valid:
            title_input = input(eval(random.choice(choices)) + "请输入关键词：").strip()

            print(eval(random.choice(choices)) + "您输入的关键词是：", title_input)
            confirm = input(Fore.RED + "确认输入正确吗？(按回车确认，或输入任意字符重新输入): ")

            if confirm == '':
                input_valid = True
            else:
                print(Fore.RED + "返回重新输入标题。")

        input_valid = False
        type_input = None
        while not input_valid:
            choice = input(eval(random.choice(choices)) + "请输入数字选择内容：1. Journal_Articles(期刊）  2. Conference_and_Workshop_Papers(会议): ")
            if choice == '1':
                type_input = 'Journal_Articles'
                input_valid = True
            elif choice == '2':
                type_input = 'Conference_and_Workshop_Papers'
                input_valid = True
            else:
                print(Fore.RED + "错误：请输入1或2进行选择。")
        # 假设用户可以输入多个年份，以逗号分隔
        while True:
            try:
                start_year = int(input(eval(random.choice(choices)) + "请输入开始年份："))
                end_year = int(input(eval(random.choice(choices)) + "请输入结束年份："))

                if start_year > end_year:
                    print(Fore.RED + "错误：开始年份不能大于结束年份，请重新输入。")
                    continue

                # 确认选项
                print(eval(random.choice(choices)) + f"您输入的开始年份为 {start_year}，结束年份为 {end_year}")
                confirm = input(Fore.RED + "确认输入正确吗？(按回车确认，或输入任意字符重新输入): ")
                if confirm != '':
                    continue

                break
            except ValueError:
                print(Fore.RED + "错误：请输入有效的整数年份。\n")

        print(eval(random.choice(choices)) + '\n任务创建成功，正在全力检索dblp数据库中......\n')

        year_list = [str(year) for year in range(start_year, end_year + 1)]
        # 调用函数并打印结果
        journal_entry = create_journal_entry(title_input, type_input, year_list)

        url = ('https://dblp.uni-trier.de/search/publ/api?callback=jQuery31109242945945981864_1699447770265&q=' +
               journal_entry.replace("type:", "%20type:") +
               '&compl=year&p=2&h=0&c=10&rw=3d&format=jsonp&_=1699447770266')
        # print(url)
        # 获取搜素的文章总数
        response = requests.get(url=url, headers=headers)
        response_text = response.text  # 假设这是从请求中获取的文本
        # 找到 JSON 数据的开始和结束位置
        start = response_text.find('(') + 1
        end = response_text.rfind(')')
        # 提取 JSON 字符串
        json_str = response_text[start:end]
        # 解析 JSON 数据
        data = json.loads(json_str)
        total_hits = data['result']['hits']['@total']

        print(f"\n总共检索到文章{Fore.RED + total_hits}", "篇！\n")

        asyncio.get_event_loop().run_until_complete(main(total_hits, journal_entry, type_input))  # 运行异步主函数

        # print(global_journal_data)  # 打印结果
        # 用于存储分类结果
        Journal_A = []
        Journal_B = []
        Journal_C = []

        Conference_A = []
        Conference_B = []
        Conference_C = []

        # 输出配对结果
        for journal in global_journal_data:
            if type_input == 'Journal_Articles':
                if journal['publisher'] in Journal_Articles['A']:
                    Journal_A.append(journal)
                elif journal['publisher'] in Journal_Articles['B']:
                    Journal_B.append(journal)
                elif journal['publisher'] in Journal_Articles['C']:
                    Journal_C.append(journal)

            else:
                if journal['publisher'] in Conference_and_Workshop_Papers['A']:
                    Conference_A.append(journal)
                elif journal['publisher'] in Conference_and_Workshop_Papers['B']:
                    Conference_B.append(journal)
                elif journal['publisher'] in Conference_and_Workshop_Papers['C']:
                    Conference_C.append(journal)

        if type_input == 'Journal_Articles':
            ja = []
            jb = []
            jc = []
            # 检查是否搜索成功
            # print('总共', len(global_journal_data), '篇文章！\n')
            if int(total_hits) == len(global_journal_data):
                print(eval(random.choice(choices)) + '搜索成功！！！\n')
            else:
                print(Fore.RED + '搜索失败！！！\n')

            # 输出类别A的文章
            print("Category A articles:")
            print(eval(random.choice(choices)) + f'总共{len(Journal_A)}篇。')
            for j in Journal_A:
                print(Fore.CYAN + j['title'])
                ja.append((j['title'], j['publisher'], j['year']))

            # # 输出类别B的文章
            print("\nCategory B articles:")
            print(eval(random.choice(choices)) + f'总共{len(Journal_B)}篇。')
            for j in Journal_B:
                print(Fore.CYAN + j['title'])
                jb.append((j['title'], j['publisher'], j['year']))

            # 输出类别C的文章
            print("\nCategory C articles:")
            print(eval(random.choice(choices)) + f'总共{len(Journal_C)}篇。')
            for j in Journal_C:
                print(Fore.CYAN + j['title'])
                jc.append((j['title'], j['publisher'], j['year']))

            save_titles_to_excel(ja, jb, jc, len(global_journal_data), title_input, start_year,
                                 end_year, 'journal_titles.xlsx')
            print(Fore.RED + '\n所有文章已经成功保存为Excel文件到本地！！！\n')
        else:
            ca = []
            cb = []
            cc = []
            # 检查是否搜索成功
            # print(eval(random.choice(choices)) + '总共', len(global_journal_data), '篇会议！\n')
            if int(total_hits) == len(global_journal_data):
                print(eval(random.choice(choices)) + '搜索成功！！！')
            else:
                print(Fore.RED + '搜索失败！！！')

            # 输出类别A的文章
            print("Category A conferences:")
            print(eval(random.choice(choices)) + f'总共{len(Conference_A)}篇。')
            for c in Conference_A:
                print(Fore.CYAN + c['title'])
                ca.append((c['title'], c['publisher'], c['year']))

            # # 输出类别B的文章
            print("\nCategory B conferences:")
            print(eval(random.choice(choices)) + f'总共{len(Conference_B)}篇。')
            for c in Conference_B:
                print(Fore.CYAN + c['title'])
                cb.append((c['title'], c['publisher'], c['year']))

            # 输出类别C的文章
            print("\nCategory C conferences:")
            print(eval(random.choice(choices)) + f'总共{len(Conference_C)}篇。')
            for c in Conference_C:
                print(Fore.CYAN + c['title'])
                cc.append((c['title'], c['publisher'], c['year']))

            save_titles_to_excel(ca, cb, cc, len(global_journal_data), title_input, start_year,
                                 end_year, 'conference_titles.xlsx')
            print(Fore.RED + '\n所有会议已经成功保存为Excel文件到本地！！！\n')

        # 询问用户是否继续
        user_choice = input(eval(random.choice(choices)) + "是否继续（输入 'q' 退出，其他键继续）: \n")
        if user_choice.lower() == 'q':
            print(eval(random.choice(choices)) + '已成功退出！！！\n')
            break  # 如果用户输入 'q'，则退出循环
