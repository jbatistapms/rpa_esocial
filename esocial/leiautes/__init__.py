import core

if core.VERSAO_LEIAUTE == 'S_1_1':
    from .S_1_1 import tipos
    from .S_1_1 import evt_info_empregador as S1000
    from .S_1_1 import evt_remun as S1200
elif core.VERSAO_LEIAUTE == 'S_1_0':
    from .S_1_0 import tipos
    from .S_1_0 import evt_info_empregador as S1000
    from .S_1_0 import evt_pgtos as S1210
    from .S_1_0 import evt_remun as S1200