from enum import StrEnum

class VoltageTier(StrEnum):
    ULV = 'ULV'
    LV = 'LV'
    MV = 'MV'
    HV = 'HV'
    EV = 'EV'
    IV = 'IV'
    LuV = 'LuV'
    ZPM = 'ZPM'
    UV = 'UV'

class Machine(StrEnum):
    LCR = 'LCR'
    CR = 'Chemical reactor'
    EBF = 'EBF'
    Sieve = 'Sieve'
    MBSieve = 'MB Sieve'
    Ele = 'Electrolyzer'
    MBEle = 'MB Electrolyzer'
    Distill = 'Distill'
