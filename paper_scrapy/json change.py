import json

# # JSON文件的路径
# json_file_path = 'Conference_and_Workshop_Papers.json'
# # 读取JSON数据并转换为字典
# with open(json_file_path, 'r') as file:
#     Conference_and_Workshop_Papers = json.load(file)
# print(Conference_and_Workshop_Papers['C'])
from pathlib import Path
Journal_Articles = {
    "A": [
        " ACM Trans. Comput. Syst.",
        " ACM Trans. Storage",
        " IEEE Trans. Comput. Aided Des. Integr. Circuits Syst.",
        " IEEE Trans. Computers",
        " IEEE Trans. Parallel Distributed Syst.",
        " ACM Trans. Archit. Code Optim.",
        " IEEE J. Sel. Areas Commun.",
        " IEEE Trans. Mob. Comput.",
        " IEEE/ACM Trans. Netw.",
        " IEEE Trans. Dependable Secur. Comput.",
        " IEEE Trans. Inf. Forensics Secur.",
        " J. Cryptol.",
        " ACM Trans. Program. Lang. Syst.",
        " ACM Trans. Softw. Eng. Methodol.",
        " IEEE Trans. Software Eng.",
        " IEEE Trans. Serv. Comput.",
        " ACM Trans. Database Syst.",
        " ACM Trans. Inf. Syst.",
        " IEEE Trans. Knowl. Data Eng.",
        " VLDB J.",
        " IEEE Trans. Inf. Theory",
        " Inf. Comput.",
        " SIAM J. Comput.",
        " ACM Trans. Graph.",
        " IEEE Trans. Image Process.",
        " IEEE Trans. Vis. Comput. Graph.",
        " Artif. Intell.",
        " IEEE Trans. Pattern Anal. Mach. Intell.",
        " Int. J. Comput. Vis.",
        " J. Mach. Learn. Res.",
        " ACM Trans. Comput. Hum. Interact.",
        " Int. J. Hum. Comput. Stud.",
        " J. ACM",
        " Proc. IEEE",
        " Sci. China Inf. Sci."
    ],
    "B": [
        "J Speech Lang Hear Res. ",
        "GeoInformatica, Algorithmica",
        "Neural Networks",
        "IEEE Trans. Syst. Man Cybern.",
        "World Wide Web (WWW)",
        " ACM Trans. Auton. Adapt. Syst.",
        " ACM Trans. Design Autom. Electr. Syst.",
        " ACM Trans. Embed. Comput. Syst.",
        " ACM Trans. Reconfigurable Technol. Syst.",
        " IEEE Trans. Very Large Scale Integr. Syst.",
        " J. Parallel Distributed Comput.",
        " J. Syst. Archit.",
        " Parallel Comput.",
        " Perform. Evaluation",
        " ACM Trans. Internet Techn.",
        " ACM Trans. Multim. Comput. Commun. Appl.",
        " ACM Trans. Sens. Networks",
        " Comput. Networks",
        " IEEE Trans. Commun.",
        " IEEE Trans. Wirel. Commun.",
        " ACM Trans. Priv. Secur.",
        " Comput. Secur.",
        " Des. Codes Cryptogr.",
        " J. Comput. Secur.",
        " Autom. Softw. Eng.",
        " Empir. Softw. Eng.",
        " IEE Proc. Softw.",
        " Inf. Softw. Technol.",
        " J. Funct. Program.",
        " J. Softw. Evol. Process.",
        " J. Syst. Softw.",
        " Requir. Eng.",
        " Sci. Comput. Program.",
        " Softw. Syst. Model.",
        " Softw. Test. Verification Reliab.",
        " Softw. Pract. Exp.",
        " ACM Trans. Knowl. Discov. Data",
        " ACM Trans. Web",
        " Adv. Eng. Informatics",
        " Data Knowl. Eng.",
        " Data Min. Knowl. Discov.",
        " Eur. J. Inf. Syst.",
        " Inf. Process. Manag.",
        " Inf. Sci.",
        " Inf. Syst.",
        " J. Assoc. Inf. Sci. Technol.",
        " J. Web Semant.",
        " Knowl. Inf. Syst.",
        " ACM Trans. Algorithms",
        " ACM Trans. Comput. Log.",
        " ACM Trans. Math. Softw.",
        " Comput. Complex.",
        " Formal Aspects Comput.",
        " Formal Methods Syst. Des.",
        " INFORMS J. Comput.",
        " J. Comput. Syst. Sci.",
        " J. Glob. Optim.",
        " J. Symb. Comput.",
        " Math. Struct. Comput. Sci.",
        " Theor. Comput. Sci.",
        " ACM Trans. Multim. Comput. Commun. Appl.",
        " Comput. Aided Geom. Des.",
        " Comput. Graph. Forum",
        " Comput. Aided Des.",
        " Graph. Model.",
        " IEEE Trans. Circuits Syst. Video Technol.",
        " IEEE Trans. Multim.",
        " SIAM J. Imaging Sci.",
        " Speech Commun.",
        " ACM Trans. Appl. Percept.",
        " Auton. Agents Multi Agent Syst.",
        " Comput. Linguistics",
        " Comput. Vis. Image Underst.",
        " Data Knowl. Eng.",
        " Evol. Comput.",
        " IEEE Trans. Affect. Comput.",
        " IEEE ACM Trans. Audio Speech Lang. Process.",
        " IEEE Trans. Cybern.",
        " IEEE Trans. Evol. Comput.",
        " IEEE Trans. Fuzzy Syst.",
        " IEEE Trans. Neural Networks Learn. Syst.",
        " Int. J. Approx. Reason.",
        " J. Artif. Intell. Res.",
        " J. Autom. Reason.",
        " Mach. Learn.",
        " Neural Comput.",
        " Trans. Assoc. Comput. Linguistics",
        " Comput. Support. Cooperative Work.",
        " Hum. Comput. Interact.",
        " IEEE Trans. Hum. Mach. Syst.",
        " Interact. Comput.",
        " Int. J. Hum. Comput. Interact.",
        " User Model. User Adapt. Interact.",
        " Bioinform.",
        " Briefings Bioinform.",
        " IEEE Trans Autom. Sci. Eng.",
        " IEEE Trans. Geosci. Remote. Sens.",
        " IEEE Trans. Intell. Transp. Syst.",
        " IEEE Trans. Medical Imaging",
        " IEEE Trans. Robotics",
        " IEEE ACM Trans. Comput. Biol. Bioinform.",
        " J. Comput. Sci. Technol.",
        " J. Am. Medical Informatics Assoc.",
        " PLoS Comput. Biol.",
        " Comput. J.",
        " Frontiers Comput. Sci."
    ],
    "C": [
        " Neurocomputing",
        "Proc. ACM Hum. Comput. Interact.",
        "J. Log. Comput.",
        "J. Symb. Log.",
        "Log. Methods Comput. Sci.",
        "SIAM J. Discret. Math.",
        "Theory Comput. Syst.",
        "Acta Informatica",
        "Networks",
        "Ad Hoc Networks",
        "J. Grid Comput.",
        "ACM J. Emerg. Technol. Comput. Syst.",
        "Concurr. Comput. Pract. Exp.",
        "Distributed Comput.",
        "Future Gener. Comput. Syst.",
        "IEEE Trans. Cloud Comput.",
        "Integr.",
        "J. Electron. Test.",
        "Real Time Syst.",
        "J. Supercomput.",
        "IEEE Trans. Circuits Syst. I Regul. Pap.",
        "CCF Trans. High Perform. Comput.",
        "IEEE Trans. Sustain. Comput.",
        "Comput. Commun.",
        "IEEE Trans. Netw. Serv. Manag.",
        "IET Commun.",
        "J. Netw. Comput. Appl.",
        "Mob. Networks Appl.",
        "Peer Peer Netw. Appl.",
        "Wirel. Commun. Mob. Comput.",
        "Wirel. Networks",
        "Internet Things",
        "Comput. Law Secur. Rev.",
        "EURASIP J. Inf. Secur.",
        "IET Inf. Secur.",
        "Inf. Comput. Secur.",
        "Int. J. Inf. Comput. Secur.",
        "Int. J. Inf. Secur. Priv.",
        "J. Inf. Secur. Appl.",
        "Secur. Commun. Networks",
        "Cybersecur.",
        "Comput. Lang. Syst. Struct.",
        "Int. J. Softw. Eng. Knowl. Eng.",
        "Int. J. Softw. Tools Technol. Transf.",
        "J. Log. Algebraic Methods Program.",
        "J. Web Eng.",
        "Serv. Oriented Comput. Appl.",
        "Softw. Qual. J.",
        "Theory Pract. Log. Program.",
        "Proc. ACM Program. Lang.",
        "Distributed Parallel Databases",
        "Inf. Manag.",
        "Inf. Process. Lett.",
        "Inf. Retr. J.",
        "Int. J. Cooperative Inf. Syst.",
        "Int. J. Geogr. Inf. Sci.",
        "Int. J. Intell. Syst.",
        "Int. J. Knowl. Manag.",
        "Int. J. Semantic Web Inf. Syst.",
        "J. Comput. Inf. Syst.",
        "J. Database Manag.",
        "J. Glob. Inf. Manag.",
        "J. Intell. Inf. Syst.",
        "J. Strateg. Inf. Syst.",
        "Data Sci. Eng.",
        "Ann. Pure Appl. Log.",
        "Discret. Appl. Math.",
        "Fundam. Informaticae",
        "Inf. Process. Lett.",
        "J. Complex.",
        "Comput. Geom.",
        "Comput. Animat. Virtual Worlds",
        "Comput. Graph.",
        "Discret. Comput. Geom.",
        "IEEE Signal Process. Lett.",
        "IET Image Process.",
        "J. Vis. Commun. Image Represent.",
        "Multim. Syst.",
        "Multim. Tools Appl.",
        "Signal Process.",
        "Signal Process. Image Commun.",
        "Vis. Comput.",
        "Comput. Vis. Media",
        "ACM Trans. Asian Low Resour. Lang. Inf. Process.",
        "Appl. Intell.",
        "Artif. Intell. Medicine",
        "Artif. Life",
        "Comput. Intell.",
        "Comput. Speech Lang.",
        "Connect. Sci.",
        "Decis. Support Syst.",
        "Eng. Appl. Artif. Intell.",
        "Expert Syst. J. Knowl. Eng.",
        "Expert Syst. Appl.",
        "Fuzzy Sets Syst.",
        "IEEE Trans. Games",
        "IET Comput. Vis.",
        "IET Signal Process.",
        "Image Vis. Comput.",
        "Intell. Data Anal.",
        "Int. J. Comput. Intell. Appl.",
        "Int. J. Intell. Syst.",
        "Int. J. Neural Syst.",
        "Int. J. Pattern Recognit. Artif. Intell.",
        "Int. J. Uncertain. Fuzziness Knowl. Based Syst.",
        "Int. J. Document Anal. Recognit.",
        "J. Exp. Theor. Artif. Intell.",
        "Knowl. Based Syst.",
        "Mach. Transl.",
        "Mach. Vis. Appl.",
        "Nat. Comput.",
        "Nat. Lang. Eng.",
        "Neural Comput. Appl.",
        "Neural Process. Lett.",
        "Pattern Anal. Appl.",
        "Pattern Recognit. Lett.",
        "Soft Comput.",
        "Web Intell.",
        "ACM Trans. Interact. Intell. Syst.",
        "Behav. Inf. Technol.",
        "Pers. Ubiquitous Comput.",
        "Pervasive Mob. Comput.",
        "BMC Bioinform.",
        "Cybern. Syst.",
        "IEEE Geosci. Remote. Sens. Lett.",
        "IEEE J. Biomed. Health Informatics",
        "IEEE Trans. Big Data",
        "J. Biomed. Informatics",
        "Medical Image Anal.",
        "IEEE Trans. Ind. Informatics",
        "ACM Trans. Cyber Phys. Syst.",
        "ACM Trans. Comput. Educ.",
        "Frontiers Inf. Technol. Electron. Eng.",
        "IEEE Trans. Comput. Soc. Syst.",
        "IEEE Trans. Reliab."
    ]
}
Conference_and_Workshop_Papers = {"A": ["PPoPP", "FAST", "DAC", "HPCA", "MICRO", "SC", "ASPLOS", "ISCA", "USENIX ATC", "EuroSys", "SIGCOMM", "MobiCom", "INFOCOM", "NSDI", "CCS", "EUROCRYPT", "S&P", "CRYPTO", "USENIX Security", "NDSS", "PLDI", "POPL", "FSE/ESEC", "SOSP", "OOPSLA", "ASE", "ICSE", "ISSTA", "OSDI", "FM", "SIGMOD", "SIGKDD", "ICDE", "SIGIR", "VLDB", "STOC", "SODA", "CAV", "FOCS", "LICS", "ACM MM", "SIGGRAPH", "VR", "IEEE VIS", "AAAI", "NeurIPS", "ACL", "CVPR", "ICCV", "ICML", "IJCAI", "CSCW", "CHI", "UbiComp", "UIST", "WWW", "RTSS", "WINE"], "B": ["SOCC", "SPAA", "PODC", "FPGA", "CGO", "DATE", "HOT CHIPS", "CLUSTER", "ICCD", "ICCAD", "ICDCS", "CODES+ISSS", "HiPEAC", "SIGMETRICS", "PACT", "ICPP", "ICS", "VEE", "IPDPS", "Performance", "HPDC", "ITC", "LISA", "MSST", "RTAS", "Euro-Par", "SenSys", "CoNEXT", "SECON", "IPSN", "MobiSys", "ICNP", "MobiHoc", "NOSSDAV", "IWQoS", "IMC", "ACSAC", "ASIACRYPT", "ESORICS", "FSE", "CSFW", "SRDS", "CHES", "DSN", "RAID", "PKC", "TCC", "ECOOP", "ETAPS", "ICPC", "RE", "CAiSE", "ICFP", "LCTES", "MoDELS", "CP", "ICSOC", "SANER", "ICSME", "VMCAI", "ICWS", "Middleware", "SAS", "ESEM", "ISSRE", "HotOS", "CIKM", "WSDM", "PODS", "DASFAA", "ECML-PKDD", "ISWC", "ICDM", "ICDT", "EDBT", "CIDR", "SDM", "RecSys", "SoCG", "ESA", "CCC", "ICALP", "CONCUR", "HSCC", "SAT", "COCOON", "ICMR", "I3D", "SCA", "DCC", "Eurographics", "EuroVis", "SGP", "EGSR", "ICASSP", "ICME", "ISMAR", "PG", "SPM", "COLT", "EMNLP", "ECAI", "ECCV", "ICRA", "ICAPS", "ICCBR", "COLING", "KR", "UAI", "AAMAS", "PPSN", "NAACL", "GROUP", "IUI", "ITS", "ECSCW", "PERCOM", "MobileHCI", "ICWSM", "CogSci", "BIBM", "EMSOFT", "ISMB", "RECOMB", "MICCAI", "CADE"], "C": ["CF", "SYSTOR", "NOCS", "ASAP", "ASP-DAC", "ETS", "FPL", "FCCM", "GLSVLSI", "ATS", "HPCC", "HiPC", "MASCOTS", "ISPA", "CCGRID", "NPC", "ICA3PP", "CASES", "FPT", "ICPADS", "ISCAS", "ISLPED", "ISPD", "HOTI", "VTS", "ITC-Asia", "ANCS", "APNOMS", "FORTE", "LCN", "GLOBECOM", "ICC", "ICCCN", "MASS", "P2P", "IPCCC", "WoWMoM", "ISCC", "WCNC", "Networking", "IM", "MSN", "MSWiM", "WASA", "HotNets", "APNet", "WiSec", "SACMAT", "DRM", "IH&MMSec", "ACNS", "AsiaCCS", "ACISP", "CT-RSA", "DIMVA", "DFRWS", "FC", "TrustCom", "SEC", "IFIP WG 11.9", "ISC", "ICDF2C", "ICICS", "SecureComm", "NSPW", "PAM", "PETS", "SAC", "SOUPS", "HotSec", "EuroS&P", "Inscrypt", "PEPM", "PASTE", "APLAS", "APSEC", "EASE", "ICECCS", "ICST", "ISPASS", "SCAM", "COMPSAC", "ICFEM", "SCC", "ICSSP", "SEKE", "QRS", "ICSR", "ICWE", "SPIN", "ATVA", "LOPSTR", "TASE", "MSR", "REFSQ", "WICSA", "Internetware", "RV", "APWeb", "DEXA", "ECIR", "ESWC", "WebDB", "ER", "MDM", "SSDBM", "WAIM", "SSTD", "PAKDD", "WISE", "ADMA", "CSL", "FMCAD", "FSTTCS", "DSAA", "ICTAC", "IPCO", "RTA", "ISAAC", "MFCS", "STACS", "SETTA", "VRST", "CASA", "CGI", "INTERSPEECH", "GMP", "PacificVis", "3DV", "CAD/Graphics", "ICIP", "MMM", "MMAsia", "SMI", "ICVRV", "CVM", "PRCV", "AISTATS", "ACCV", "ACML", "BMVC", "NLPCC", "CoNLL", "GECCO", "ICTAI", "IROS", "ALT", "ICANN", "FG", "ICDAR", "ILP", "KSEM", "ICONIP", "ICPR", "IJCB", "IJCNN", "PRICAI", "DIS", "ICMI", "ASSETS", "GI", "UIC", "INTERACT", "IDC", "CollaborateCom", "CSCWD", "CoopIS", "MobiQuitous", "AVI", "AMIA", "APBC", "IEEE BigData", "IEEE CLOUD", "SMC", "COSIT", "ISBRA", "SAGT", "SIGSPATIAL", "ICIC", "WHC"]}

# 预处理步骤：移除每个元素的前后空格，并转换列表为集合
Journal_Articles = {k: list(set(item.strip() for item in v)) for k, v in Journal_Articles.items()}
Conference_and_Workshop_Papers = {k: list(set(item.strip()for item in v)) for k, v in Conference_and_Workshop_Papers.items()}


# # 假设您有几个JSON文件的路径列表
# json_file_paths = [
#     'Journal_Articles_A.json',
#     'Journal_Articles_B.json',
#     'Journal_Articles_C.json'
#     # ... 可以添加更多的JSON文件路径
# ]
#
# # 初始化一个空字典来存储合并后的数据
# merged_dict = {}
#
# # 遍历文件路径列表
# for file_path in json_file_paths:
#     # 确保文件存在
#     if Path(file_path).is_file():
#         with open(file_path, 'r') as file:
#             # 读取当前JSON文件并将其转换成字典
#             data = json.load(file)
#             # 更新到我们的合并字典中（注意这会覆盖重复的键）
#             merged_dict.update(data)
#
# # 合并后的JSON文件名称，您可以选择一个合适的文件名和路径
# merged_json_file_path = 'Journal_Articles.json'
#
# # 将合并后的字典写入新的JSON文件
# with open(merged_json_file_path, 'w') as file:
#     json.dump(merged_dict, file, indent=4)

# # 文本文件的路径
# text_file_path = 'Journal_Articles_A.txt'
#
# # 读取文本文件中的期刊名称
# with open(text_file_path, 'r') as file:
#     # 假设整个文件只有一行，且所有名称都是逗号加空格隔开
#     journal_names = file.readline().split(', ')
#
# # 创建JSON格式的字典
# journal_dict = {"A": journal_names}
#
# JSON文件的名称
json_file_path1 = 'Journal_Articles.json'
json_file_path2 = 'Conference_and_Workshop_Papers.json'

# 将字典写入JSON文件
with open(json_file_path1, 'w') as file:
    json.dump(Journal_Articles, file, indent=4)

with open(json_file_path2, 'w') as file:
    json.dump(Conference_and_Workshop_Papers, file, indent=4)
