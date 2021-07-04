from aiogram.dispatcher.filters.state import StatesGroup, State

class Employer_Steps(StatesGroup):

    #Targets
    get_name_company_targ = State()
    get_profile_targ      = State()
    get_adress_targ       = State()
    get_phone_targ        = State()
    get_email_targ        = State()
    get_url_targ          = State()
    get_fio_targ          = State()

    #Variables
    get_name_company_var = State()
    get_profile_var      = State()
    get_adress_var       = State()
    get_phone_var        = State()
    get_email_var        = State()
    get_url_var          = State()
    get_fio_var          = State()

class Candidat_Steps(StatesGroup):

    #Targets
    get_fio_targ       = State()
    get_date_born_targ = State()
    get_adress_targ    = State()
    get_email_targ     = State()
    get_phone_targ     = State()
    get_url_targ       = State()

    #Variables
    get_fio_var       = State()
    get_date_born_var = State()
    get_adress_var    = State()
    get_email_var     = State()
    get_phone_var     = State()
    get_url_var       = State()

class Application_Steps(StatesGroup):

    #Targets 
    get_position_targ   = State()
    get_experience_targ = State()
    get_tasks_targ      = State()

    #Variables
    get_position_var   = State()
    get_experience_var = State()
    get_age_var        = State()
    get_wage_var       = State()
    get_tasks_var      = State()

class Resume_Steps(StatesGroup):

    #Targets
    get_company_targ   = State()
    get_position_targ  = State()
    get_results_targ   = State()
    get_dismissal_targ = State()

    #Variables
    get_company_var    = State()
    get_position_var   = State()
    get_experience_var = State()
    get_results_var    = State()
    get_dismissal_var  = State()