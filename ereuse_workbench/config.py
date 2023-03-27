from decouple import AutoConfig


class WorkbenchConfig:
    # Path where find settings.ini file
    config = AutoConfig(search_path='/mnt/settings/')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='')
    DH_HOST = config('DH_HOST', default='')
    DH_DATABASE = config('DH_DATABASE', default='')
    DEVICEHUB_URL = 'https://{host}/{db}/'.format(
        host=DH_HOST,
        db=DH_DATABASE
    )  # type: str

    ## Env variables for WB parameters
    WB_BENCHMARK = config('WB_BENCHMARK', default=False, cast=bool)
    WB_STRESS_TEST = config('WB_STRESS_TEST', default=0, cast=int)
    WB_SMART_TEST = config('WB_SMART_TEST', default='')

    ## Erase parameters
    WB_ERASE = config('WB_ERASE', default='EraseBasic', cast=str)
    WB_ERASE_STEPS = config('WB_ERASE_STEPS', default=1, cast=int)
    WB_ERASE_LEADING_ZEROS = config('WB_ERASE_LEADING_ZEROS', default=False,
                                    cast=bool)
    WB_ERASE_CONFIRMATION = config('WB_ERASE_CONFIRMATION', default=True, cast=bool)
                  
    # Todo: Improve the method to get dynamic step values.
    WB_ERASE_1_METHOD = config('WB_ERASE_1_METHOD', default='')
    WB_ERASE_1_STEP_TYPE = config('WB_ERASE_1_STEP_TYPE', default=1)

    WB_ERASE_2_METHOD = config('WB_ERASE_2_METHOD', default='')
    WB_ERASE_2_STEP_TYPE = config('WB_ERASE_2_STEP_TYPE', default='')

    WB_ERASE_3_METHOD = config('WB_ERASE_3_METHOD', default='')
    WB_ERASE_3_STEP_TYPE = config('WB_ERASE_3_STEP_TYPE', default='')

    WB_ERASE_4_METHOD = config('WB_ERASE_4_METHOD', default='')
    WB_ERASE_4_STEP_TYPE = config('WB_ERASE_4_STEP_TYPE', default='')

    VERSION = config('VERSION', default='Default Basic Erasure (DBE)',
                     cast=str)

    @classmethod
    def load_steps(cls):
        steps = []
        for step in range(1, 99):
            try:
                method = getattr(cls, f'WB_ERASE_{step}_METHOD')
                erasure_type = getattr(cls, f'WB_ERASE_{step}_STEP_TYPE')
                if (method is '') and (erasure_type is not ''):
                    method = getattr(cls, f'WB_ERASE')
                if method and erasure_type is not '':
                    steps.append({'method': method, 'type': erasure_type})
            except AttributeError:
                break
        return steps
